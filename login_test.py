from run import create_app

app = create_app()

with app.test_client() as client:
    # GET login page
    r = client.get('/auth/login')
    print('GET /auth/login ->', r.status_code)

    # POST credentials
    r2 = client.post('/auth/login', data={'username':'admin','password':'1234'}, follow_redirects=True)
    print('POST /auth/login ->', r2.status_code)
    print('Location (final):', r2.request.path)
    # show small snippet or exceptions in body
    body = r2.data.decode('utf-8', errors='replace')
    print('\n--- body snippet ---\n', body[:800])
