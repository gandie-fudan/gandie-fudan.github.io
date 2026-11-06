"""Let the repository's existing branch publisher finish before publishing new output.

This also works when Pages is later switched to GitHub Actions in Settings.
Only workflow metadata is read; credentials are never printed or persisted.
"""
import json,os,time,urllib.request
repo=os.environ['GITHUB_REPOSITORY']
sha=os.environ['GITHUB_SHA']
request=urllib.request.Request(
 f'https://api.github.com/repos/{repo}/actions/runs?head_sha={sha}&per_page=100',
 headers={'Authorization':'Bearer '+os.environ['GH_TOKEN'],
          'Accept':'application/vnd.github+json','User-Agent':'academic-site-deploy'})
started=time.monotonic()
while time.monotonic()-started<600:
 with urllib.request.urlopen(request,timeout=30) as response:
  runs=json.load(response)['workflow_runs']
 legacy=[r for r in runs if r.get('path','').startswith('dynamic/pages/')]
 if legacy and all(r['status']=='completed' for r in legacy):
  print('Legacy publisher finished; the current build will publish last.')
  break
 if not legacy and time.monotonic()-started>=30:
  print('No legacy publisher detected; proceeding with the current build.')
  break
 time.sleep(10)
else:
 raise SystemExit('Legacy Pages run did not finish in 10 minutes; retry this workflow after it completes.')
