# URL Kısaltıcı

![Python](https://img.shields.io/badge/python-3.9%2B-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1-000000?logo=flask)
[![Lisans: MIT](https://img.shields.io/badge/lisans-MIT-blue.svg)](LICENSE)

Uzun URL'leri kısa ve yönetilebilir bağlantılara dönüştüren, QR kod üreten ve tıklanma istatistiği tutan küçük bir Flask web uygulaması.

## Özellikler

- 🔗 URL'leri kısa kodlara dönüştürme
- 📊 Tıklanma istatistikleri takibi
- 📱 QR kod oluşturma ve indirme
- 💾 JSON dosyasında veri saklama
- 🎨 Modern ve kullanıcı dostu arayüz
- 🗑️ URL silme özelliği
- 🛡️ Yalnızca `http`/`https` bağlantıları kabul edilir

## Ekran Görüntüleri

![Ana Sayfa](screenshots/main.png)
![Kısaltılmış URL](screenshots/main_with_url.png)
![İstatistikler](screenshots/stats.png)

## Kurulum

1. Projeyi klonlayın:
```bash
git clone https://github.com/EfeKesgin/url-kisaltici.git
cd url-kisaltici
```

2. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

3. Uygulamayı başlatın:
```bash
python app.py
```

4. Tarayıcınızda `http://localhost:5000` adresine gidin.

> Veriler proje klasöründeki `urls.json` dosyasında tutulur (ilk kısaltmada otomatik oluşur, depoya eklenmez).
> Geliştirme sırasında hata ayıklama modu için: `FLASK_DEBUG=1 python app.py`

## Kullanım

1. Ana sayfada URL'yi girin
2. İsteğe bağlı olarak özel bir kısa kod belirleyin
3. "URL'yi Kısalt" butonuna tıklayın
4. Kısaltılmış URL'yi ve QR kodunu görüntüleyin
5. İstatistikleri takip edin

## Teknolojiler

- Python 3.9+
- Flask
- QRCode
- JSON
- HTML/CSS
- JavaScript

## Katkıda Bulunma

1. Bu depoyu fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/yeniOzellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik: Açıklama'`)
4. Branch'inizi push edin (`git push origin feature/yeniOzellik`)
5. Pull Request oluşturun

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına bakın.

## İletişim

Efe Kesgin - [@EfeKesgin](https://github.com/EfeKesgin)

Proje Linki: [https://github.com/EfeKesgin/url-kisaltici](https://github.com/EfeKesgin/url-kisaltici)
