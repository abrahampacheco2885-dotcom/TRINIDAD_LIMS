from run import create_app

routes = [
    '/',
    '/auth/login',
    '/patients',
    '/patients/nuevo',
    '/patients/list',
    '/samples',
    '/analysis',
]

app = create_app()

with app.test_client() as client:
    results = {}
    for r in routes:
        try:
            res = client.get(r)
            results[r] = (res.status_code, res.data[:500].decode('utf-8', errors='replace'))
        except Exception as e:
            results[r] = ('EXCEPTION', str(e))

for k,v in results.items():
    print(k, '=>', v[0])
    if isinstance(v[0], int) and v[0] == 200:
        print('--- body snippet ---')
        print(v[1][:300])
        print('--------------------')

print('SMOKE_DONE')
