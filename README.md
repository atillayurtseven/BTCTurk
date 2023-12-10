# BTCTurk API Python Wrapper

Bu proje, BTCTurk kripto para borsası için Python ile geliştirilmiş bir API wrapper'ıdır. BTCTurk API'sini kullanarak çeşitli kripto para işlemleri ve sorgulamaları yapmanızı sağlar.

## Özellikler

* BTCTurk API'sini kullanarak piyasa verilerini sorgulama.
* Kullanıcı hesabı bilgilerine erişim.
* Alım-satım işlemlerini gerçekleştirme.

## Kurulum

Bu kütüphaneyi kullanmadan önce, BTCTurk'ten bir API anahtarı ve gizli anahtarınızın olması gerekmektedir. Bu anahtarlar, BTCTurk hesabınızın API yönetimi bölümünden elde edilebilir.

1. Projeyi klonlayın veya indirin.
```bash
git clone https://github.com/atillayurtseven/BTCTurk
```

2. Gerekli kütüphaneleri yükleyin.
```bash
pip install -r requirements.txt
```

## Kullanım

Bu wrapper'ı kullanmak için, öncelikle BTCTurk sınıfından bir nesne oluşturmalısınız. Bu nesne, API anahtarınızı ve gizli anahtarınızı argüman olarak alır.
```python
from btcturk import BTCTurk

api_key = "API_ANAHTARINIZ"
api_secret = "API_GIZLI_ANAHTARINIZ"

btcturk = BTCTurk(api_key, api_secret)
```

Daha sonra, BTCTurk API'sinin sunduğu çeşitli fonksiyonları bu nesne üzerinden kullanabilirsiniz.

## Lisans

Bu proje [MIT Lisansı]([LICENSE_dosyasının_linki](https://github.com/atillayurtseven/BTCTurk/blob/master/LICENSE)https://github.com/atillayurtseven/BTCTurk/blob/master/LICENSE) altında lisanslanmıştır.
