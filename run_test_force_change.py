from run import create_app

app = create_app()
app.config['WTF_CSRF_ENABLED'] = False

# Use the last password printed in previous operation. Update if changed.
ADMIN_PW = 'T8xu*A$a(a%DuGll'

with app.test_client() as client:
    res = client.post('/auth/login', data={'username':'admin','password':ADMIN_PW}, follow_redirects=False)
    print('POST /auth/login ->', res.status_code)
    loc = res.headers.get('Location')
    print('Redirect location:', loc)
    if loc and '/auth/change_password' in loc:
        print('OK: user redirected to change password page')
    else:
        # Try following
        res2 = client.post('/auth/login', data={'username':'admin','password':ADMIN_PW}, follow_redirects=True)
        print('Follow redirects status:', res2.status_code)
        data = res2.data.decode('utf-8', errors='replace')
        if 'Cambiar Contraseña' in data:
            print('OK: change password form present in response body')
        else:
            print('WARN: change password not enforced (check flag)')

print('TEST_FORCE_CHANGE_DONE')
