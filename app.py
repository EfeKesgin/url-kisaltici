from flask import Flask, request, redirect, render_template_string, send_file
import string
import random
from datetime import datetime
import json
import os
import qrcode
from io import BytesIO
from urllib.parse import urlparse

app = Flask(__name__)

# URL'leri JSON'dan yükleme fonksiyonu
def url_yukle():
    if os.path.exists('urls.json'):
        with open('urls.json', 'r', encoding='utf-8') as f:
            veri = json.load(f)
            # JSON'dan tarih bilgilerini geri yükle
            for kod, url_bilgisi in veri.items():
                url_bilgisi['olusturma_tarihi'] = datetime.fromisoformat(url_bilgisi['olusturma_tarihi'])
                url_bilgisi['son_kullanim'] = datetime.fromisoformat(url_bilgisi['son_kullanim'])
            return veri
    return {}

# URL'leri JSON'a kaydetme fonksiyonu
def url_kaydet():
    # tarih bilgilerini string'e çevir
    veri = {}
    for kod, url_bilgisi in urls.items():
        veri[kod] = {
            'url': url_bilgisi['url'],
            'olusturma_tarihi': url_bilgisi['olusturma_tarihi'].isoformat(),
            'son_kullanim': url_bilgisi['son_kullanim'].isoformat(),
            'tiklanma': url_bilgisi['tiklanma']
        }
    
    with open('urls.json', 'w', encoding='utf-8') as f:
        json.dump(veri, f, ensure_ascii=False, indent=2)

# URL'leri yükle
urls = url_yukle()

# Uygulamanın kendi yollarıyla çakışan özel kodlar
AYRILMIS_YOLLAR = {'shorten', 'stats', 'qr', 'delete'}

def gecerli_url_mi(url):
    # Yalnızca http/https bağlantılarına izin ver (javascript: vb. engellenir)
    parca = urlparse(url)
    return parca.scheme in ('http', 'https') and bool(parca.netloc)

def kisa_kod_olustur():
    karakterler = string.ascii_letters + string.digits
    while True:
        kod = ''.join(random.choices(karakterler, k=6))
        if kod not in urls:
            return kod

def qr_kod_olustur(url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    return img

# Ana sayfa HTML template'i
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>URL Kısaltıcı</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f0f2f5;
        }
        .container {
            background-color: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        h1 {
            color: #1a73e8;
            text-align: center;
            margin-bottom: 30px;
        }
        form {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        input[type="url"], input[type="text"] {
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input[type="url"]:focus, input[type="text"]:focus {
            border-color: #1a73e8;
            outline: none;
        }
        button {
            padding: 12px 24px;
            background-color: #1a73e8;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 500;
            transition: background-color 0.3s;
        }
        button:hover {
            background-color: #1557b0;
        }
        .result {
            margin-top: 25px;
            padding: 20px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            background-color: #f8f9fa;
        }
        .error {
            color: #d32f2f;
            margin-top: 15px;
            padding: 10px;
            background-color: #ffebee;
            border-radius: 8px;
        }
        .url-list {
            margin-top: 30px;
        }
        .url-item {
            padding: 15px;
            border-bottom: 1px solid #e0e0e0;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: background-color 0.3s;
        }
        .url-item:hover {
            background-color: #f5f5f5;
        }
        .url-item:last-child {
            border-bottom: none;
        }
        .url-info {
            flex-grow: 1;
        }
        .url-actions {
            display: flex;
            gap: 10px;
        }
        .delete-btn {
            background-color: #d32f2f;
        }
        .delete-btn:hover {
            background-color: #b71c1c;
        }
        .qr-code {
            margin-top: 20px;
            text-align: center;
            padding: 15px;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .qr-code img {
            max-width: 200px;
            height: auto;
            border-radius: 4px;
        }
        .button {
            text-decoration: none;
            padding: 8px 16px;
            background-color: #1a73e8;
            color: white;
            border-radius: 6px;
            font-size: 14px;
            transition: background-color 0.3s;
        }
        .button:hover {
            background-color: #1557b0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>URL Kısaltıcı</h1>
        <form method="POST" action="/shorten">
            <input type="url" name="url" placeholder="Kısaltmak istediğiniz URL'yi girin" required>
            <input type="text" name="custom_code" placeholder="İsteğe bağlı: Özel kısa kod (6 karakter)" maxlength="6" pattern="[a-zA-Z0-9]+" title="Sadece harf ve rakam kullanabilirsiniz">
            <button type="submit">URL'yi Kısalt</button>
        </form>
        {% if short_url %}
        <div class="result">
            <p>Kısaltılmış URL: <a href="{{ short_url }}" target="_blank">{{ short_url }}</a></p>
            <p>İstatistikler için: <a href="/stats/{{ short_code }}" target="_blank">İstatistikleri Görüntüle</a></p>
            <div class="qr-code">
                <p>QR Kod:</p>
                <img src="/qr/{{ short_code }}" alt="QR Code">
                <p><a href="/qr/{{ short_code }}/download" download>QR Kodu İndir</a></p>
            </div>
        </div>
        {% endif %}
        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
        
        {% if urls %}
        <div class="url-list">
            <h2>Kısaltılmış URL'ler</h2>
            {% for code, data in urls.items() %}
            <div class="url-item">
                <div class="url-info">
                    <p><strong>Kısa Kod:</strong> {{ code }}</p>
                    <p><strong>Orijinal URL:</strong> <a href="{{ data.url }}">{{ data.url }}</a></p>
                    <p><strong>Oluşturulma:</strong> {{ data.olusturma_tarihi.strftime('%d/%m/%Y %H:%M:%S') }}</p>
                    <p><strong>Son Kullanım:</strong> {{ data.son_kullanim.strftime('%d/%m/%Y %H:%M:%S') }}</p>
                    <p><strong>Tıklanma:</strong> {{ data.tiklanma }}</p>
                </div>
                <div class="url-actions">
                    <a href="/stats/{{ code }}" class="button">İstatistikler</a>
                    <form method="POST" action="/delete/{{ code }}" style="display: inline;">
                        <button type="submit" class="delete-btn">Sil</button>
                    </form>
                </div>
            </div>
            {% endfor %}
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/')
def ana_sayfa():
    return render_template_string(HTML_TEMPLATE, urls=urls)

@app.route('/shorten', methods=['GET', 'POST'])
def url_kisalt():
    if request.method == 'POST':
        url = request.form.get('url')
        custom_code = request.form.get('custom_code', '').strip()
        
        if not url:
            return render_template_string(HTML_TEMPLATE, error='URL gerekli', urls=urls)
        if not gecerli_url_mi(url):
            return render_template_string(HTML_TEMPLATE, error='Geçerli bir http(s) adresi girin', urls=urls)
        
        # Özel kod kontrolü
        if custom_code:
            if not custom_code.isalnum():
                return render_template_string(HTML_TEMPLATE, error='Özel kod sadece harf ve rakam içerebilir', urls=urls)
            if len(custom_code) > 6:
                return render_template_string(HTML_TEMPLATE, error='Özel kod en fazla 6 karakter olabilir', urls=urls)
            if custom_code in urls or custom_code in AYRILMIS_YOLLAR:
                return render_template_string(HTML_TEMPLATE, error='Bu özel kod zaten kullanımda', urls=urls)
            short_code = custom_code
        else:
            short_code = kisa_kod_olustur()
        
        # URL'yi kaydet
        urls[short_code] = {
            'url': url,
            'olusturma_tarihi': datetime.now(),
            'son_kullanim': datetime.now(),
            'tiklanma': 0
        }
        
        # JSON dosyasına kaydet
        url_kaydet()
        
        short_url = request.host_url + short_code
        return render_template_string(HTML_TEMPLATE, short_url=short_url, short_code=short_code, urls=urls)
    
    return render_template_string(HTML_TEMPLATE, urls=urls)

@app.route('/<short_code>')
def yonlendir(short_code):
    if short_code in urls:
        urls[short_code]['tiklanma'] += 1
        urls[short_code]['son_kullanim'] = datetime.now()
        url_kaydet()  # Değişiklikleri kaydet
        return redirect(urls[short_code]['url'])
    
    return render_template_string(HTML_TEMPLATE, error='URL bulunamadı', urls=urls)

@app.route('/stats/<short_code>')
def istatistikler(short_code):
    if short_code in urls:
        url_data = urls[short_code]
        return render_template_string('''
            <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px;">
                <h1 style="color: #1a73e8; text-align: center;">URL İstatistikleri</h1>
                <div style="background-color: white; padding: 25px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                    <p><strong>Orijinal URL:</strong> <a href="{{ url_data.url }}">{{ url_data.url }}</a></p>
                    <p><strong>Kısa Kod:</strong> {{ short_code }}</p>
                    <p><strong>Oluşturulma Tarihi:</strong> {{ url_data.olusturma_tarihi.strftime('%d/%m/%Y %H:%M:%S') }}</p>
                    <p><strong>Son Kullanım:</strong> {{ url_data.son_kullanim.strftime('%d/%m/%Y %H:%M:%S') }}</p>
                    <p><strong>Tıklanma Sayısı:</strong> {{ url_data.tiklanma }}</p>
                    <div style="text-align: center; margin-top: 20px; padding: 15px; background-color: #f8f9fa; border-radius: 8px;">
                        <h3 style="color: #1a73e8;">QR Kod</h3>
                        <img src="/qr/{{ short_code }}" alt="QR Code" style="max-width: 200px; border-radius: 4px;">
                        <p><a href="/qr/{{ short_code }}/download" download style="color: #1a73e8; text-decoration: none;">QR Kodu İndir</a></p>
                    </div>
                    <p style="text-align: center; margin-top: 20px;"><a href="/" style="color: #1a73e8; text-decoration: none;">← Ana Sayfaya Dön</a></p>
                </div>
            </div>
        ''', url_data=url_data, short_code=short_code)
    
    return render_template_string(HTML_TEMPLATE, error='URL bulunamadı', urls=urls)

@app.route('/qr/<short_code>')
def qr_kod_goster(short_code):
    if short_code in urls:
        url = request.host_url + short_code
        img = qr_kod_olustur(url)
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')
    return 'URL bulunamadı', 404

@app.route('/qr/<short_code>/download')
def qr_kod_indir(short_code):
    if short_code in urls:
        url = request.host_url + short_code
        img = qr_kod_olustur(url)
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(
            img_io,
            mimetype='image/png',
            as_attachment=True,
            download_name=f'qr-{short_code}.png'
        )
    return 'URL bulunamadı', 404

@app.route('/delete/<short_code>', methods=['POST'])
def url_sil(short_code):
    if short_code in urls:
        del urls[short_code]
        url_kaydet()  # Değişiklikleri kaydet
    return redirect('/')

if __name__ == '__main__':
    # Hata ayıklama modu yalnızca FLASK_DEBUG=1 ile açılır
    app.run(debug=os.environ.get('FLASK_DEBUG') == '1') 