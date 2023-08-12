# telegram-notify

You can use this to notify about deploy from gitlab
- git log --format="%ad %ae SEPARATOR %s" $(consul kv get app/ms/ntv/release)..${CI_COMMIT_SHA} | python notify.py
