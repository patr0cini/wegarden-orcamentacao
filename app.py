import base64, io, os, json
from flask import Flask, request, send_file, session, redirect, send_from_directory
import openpyxl

BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
# index.html may be in static/ or directly in BASE_DIR
STATIC_DIR   = os.path.join(BASE_DIR, 'static') if os.path.exists(os.path.join(BASE_DIR, 'static', 'index.html')) else BASE_DIR

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'wegarden-secret-2026')
APP_PASSWORD  = os.environ.get('APP_PASSWORD', 'wegarden2026')

def authed():
    return session.get('auth') is True

def login_page(error=''):
    err_html = f'<div class="err">{error}</div>' if error else ''
    return f'''<!DOCTYPE html>
<html lang="pt"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>We Garden</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600&display=swap');
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Instrument Sans',sans-serif;background:#f0ede6;display:flex;align-items:center;justify-content:center;min-height:100vh}}
.card{{background:#fff;border-radius:16px;padding:2.5rem 2rem;width:100%;max-width:360px;box-shadow:0 4px 24px rgba(0,0,0,.08)}}
.logo{{display:flex;align-items:center;gap:10px;margin-bottom:2rem}}
.dot{{width:32px;height:32px;background:#3d7a52;border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:17px}}
.lt{{font-size:17px;font-weight:600;color:#1e3a28}}
h1{{font-size:15px;font-weight:500;color:#4a5249;margin-bottom:1.25rem}}
input{{width:100%;padding:10px 12px;border:1px solid #d0ccc4;border-radius:8px;font-family:inherit;font-size:14px;background:#faf9f6;outline:none;margin-bottom:1rem}}
input:focus{{border-color:#3d7a52;box-shadow:0 0 0 3px #eaf2ec}}
button{{width:100%;padding:10px;background:#1e3a28;color:#fff;border:none;border-radius:8px;font-family:inherit;font-size:14px;font-weight:600;cursor:pointer}}
button:hover{{background:#2d5a3d}}
.err{{color:#8b2020;font-size:13px;margin-bottom:.75rem;background:#fef0ee;padding:8px 12px;border-radius:6px}}
</style></head><body>
<div class="card">
  <div class="logo"><div class="dot">&#127807;</div><div class="lt">We Garden</div></div>
  <h1>Introduz a password para aceder</h1>
  {err_html}
  <form method="post">
    <input type="password" name="password" placeholder="Password" autofocus autocomplete="current-password">
    <button type="submit">Entrar &rarr;</button>
  </form>
</div></body></html>'''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == APP_PASSWORD:
            session['auth'] = True
            return redirect('/')
        return login_page('Password incorrecta.')
    return login_page()

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/')
def index():
    if not authed():
        return redirect('/login')
    return send_from_directory(STATIC_DIR, 'index.html')

@app.route('/debug')
def debug():
    return json.dumps({
        'BASE_DIR': BASE_DIR,
        'STATIC_DIR': STATIC_DIR,
        'base_files': os.listdir(BASE_DIR),
        'static_exists': os.path.exists(os.path.join(BASE_DIR, 'static')),
        'index_in_base': os.path.exists(os.path.join(BASE_DIR, 'index.html')),
        'index_in_static': os.path.exists(os.path.join(BASE_DIR, 'static', 'index.html')),
    }, indent=2), 200, {'Content-Type': 'application/json'}

@app.route('/api/fill-excel', methods=['POST'])
def fill_excel():
    if not authed():
        return 'Nao autorizado', 401
    try:
        data     = request.get_json(force=True)
        filename = data.get('filename', 'orcamento.xlsx')
        wb       = openpyxl.load_workbook(io.BytesIO(base64.b64decode(data['file_base64'])))
        for it in data['prices']:
            if it['sheet'] not in wb.sheetnames:
                continue
            ws = wb[it['sheet']]
            r  = it['row']
            if it['priceCol'] >= 0:
                ws.cell(row=r, column=it['priceCol'] + 1).value = it['price']
            if it.get('total') is not None and it['totalCol'] >= 0:
                ws.cell(row=r, column=it['totalCol'] + 1).value = it['total']
        out = io.BytesIO()
        wb.save(out)
        out.seek(0)
        return send_file(out,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename.rsplit('.', 1)[0] + '_preenchido.xlsx')
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
