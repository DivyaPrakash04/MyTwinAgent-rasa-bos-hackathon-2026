import urllib.request
print('Root:')
print(urllib.request.urlopen('http://localhost:5005/').read().decode())
print('\nTracker:')
import urllib.error
try:
    print(urllib.request.urlopen('http://localhost:5005/conversations/demo_user/tracker').read().decode())
except urllib.error.HTTPError as e:
    print('HTTPError', e.code)
    print(e.read().decode())
