import urllib.request, json, time
URL='http://localhost:5005/webhooks/rest/webhook'
headers={'Content-Type':'application/json'}

def send(msg):
    data=json.dumps({'sender':'demo_user','message':msg}).encode('utf-8')
    req=urllib.request.Request(URL, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as r:
        resp=r.read().decode('utf-8')
    print('\n--- SENT:', msg)
    print('RESPONSE:', resp)

send('I need to open a support ticket')
time.sleep(0.8)
send('Fridge B temperature dropped to -1C')
time.sleep(0.8)
send('temperature')
time.sleep(0.8)
send('urgent')
time.sleep(0.8)
send('divya@example.com')
