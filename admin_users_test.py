from run import create_app

app = create_app()
with app.test_client() as client:
    # login as admin
    res = client.post('/auth/login', data={'username':'admin','password':'1234'}, follow_redirects=True)
    print('POST /auth/login ->', res.status_code, 'final path', res.request.path)

    r = client.get('/auth/users')
    print('/auth/users ->', r.status_code)
    if r.status_code == 200:
        print('users page OK, snippet:')
        print(r.data.decode('utf-8')[:400])

    r2 = client.get('/auth/users/nuevo')
    print('/auth/users/nuevo ->', r2.status_code)
    if r2.status_code == 200:
        print('user create page OK')
