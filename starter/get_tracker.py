import urllib.request
import urllib.error
try:
	resp=urllib.request.urlopen('http://localhost:5005/conversations/demo_user/tracker')
	print(resp.read().decode())
except urllib.error.HTTPError as e:
	body=e.read().decode(errors='replace')
	print('HTTPError', e.code)
	print(body)
