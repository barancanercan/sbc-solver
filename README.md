# SBC Çözücü (Squad Building Challenge Solver)

Bu proje, EA FC 26 oyununda Squad Building Challenges (SBC) görevlerini çözmek için optimize edilmiş bir araçtır. En düşük toplam fiyata sahip kartları seçerek SBC görevlerinizi hızlı ve verimli bir şekilde tamamlamanızı sağlar.

## 🌟 Özellikler

### FC 26 Uyumlu
- ✅ EA FC 26 oyuncu verileriyle uyumlu
- ✅ Güncellenmiş oyuncu özellikleri ve değerlemeleri
- ✅ Gerçek zamanlı piyasa fiyatları

### Ücretsiz Veri Kaynakları
- ✅ FUTBIN web kazıma (tamamen ücretsiz, API anahtarı gerekmez)
- ✅ FutDB API entegrasyonu (ücretsiz katman mevcut)
- ✅ Otomatik önbellekleme sistemi
- ✅ Çoklu platform desteği

## 🚀 Hızlı Başlangıç

### Gereksinimler
- Python 3.7 veya üzeri
- pip (Python paket yöneticisi)

### Kurulum

1. Depoyu klonlayın:
```bash
git clone https://github.com/barancanercan/sbc-solver.git
cd sbc-solver
```

2. Sanal ortam oluşturun:
```bash
python -m venv fc26_env
```

3. Sanal ortamı etkinleştirin:

Windows:
```bash
fc26_env\Scripts\activate
```

macOS/Linux:
```bash
source fc26_env/bin/activate
```

4. Bağımlılıkları yükleyin:
```bash
pip install -r requirements_fc26.txt
```

### Kullanım

Botu çalıştırın:
```bash
python main_fc26.py
```

İlk çalıştırmada veriler otomatik olarak çekilir. Bu işlem yaklaşık 5-10 dakika sürebilir.

## 🛠️ Detaylı Kullanım

### Temel Örnek
```python
from src.data.fc26_data_provider import FC26DataProvider
from src.sbc_solver.ea_fc_sbc_solver import EaFcSbcSolver
from src.utils.formations import Formations

# Veri sağlayıcıyı başlat
provider = FC26DataProvider()

# Oyuncu verilerini al (otomatik olarak en iyi kaynağı seçer)
dataset = provider.get_players_data(source="auto")

# Formasyonu belirle
formation = Formations.F4_4_2.value  # 4-4-2 formasyonu

# Çözücüyü oluştur
solver = EaFcSbcSolver(dataset, formation)

# Kısıtlamaları ekle
solver.set_min_overall_of_squad(80)  # Takımın minimum genel puanı
solver.set_min_cards_with_overall(3, 64)  # En az 3 adet 64 puana sahip oyuncu
solver.set_min_unique_nations(4)  # Minimum 4 farklı ülke
solver.set_min_cards_with_nation("Spain", 1)  # En az 1 İspanyol oyuncu

# SBC'yi çöz
result = solver.solve()
```

### Mevcut Kısıtlamalar

- `set_min_overall_of_squad(min_overall)` - Takımın minimum genel puanı
- `set_min_cards_with_overall(count, rating)` - Belirli puanda minimum oyuncu sayısı
- `set_min_team_chemistry(min_chemistry)` - Minimum takım kimyası
- `set_exact_unique_nations(count)` - Tam olarak bu kadar farklı ülke
- `set_max_unique_nations(count)` - Maksimum farklı ülke sayısı
- `set_min_unique_nations(count)` - Minimum farklı ülke sayısı
- `set_exact_unique_leagues(count)` - Tam olarak bu kadar farklı lig
- `set_max_unique_leagues(count)` - Maksimum farklı lig sayısı
- `set_min_unique_leagues(count)` - Minimum farklı lig sayısı
- `set_max_nations_for_solution(count)` - Çözümde kullanılacak maksimum ülke sayısı
- `set_max_leagues_for_solution(count)` - Çözümde kullanılacak maksimum lig sayısı
- `set_min_rare_cards(count)` - Minimum nadir kart sayısı
- `set_min_cards_with_version(version, count)` - Belirli sürümde minimum kart sayısı
- `set_min_cards_with_league(league, count)` - Belirli ligde minimum kart sayısı
- `set_min_cards_with_nation(nation, count)` - Belirli ülkede minimum kart sayısı
- `set_min_cards_with_club(club, count)` - Belirli kulüpte minimum kart sayısı

## 📋 Desteklenen Formasyonlar

- `F4_4_2` - 4-4-2
- `F4_1_3_2` - 4-1-3-2
- `F4_1_2_1_2` - 4-1-2-1-2
- `F4_2_3_1` - 4-2-3-1
- `F4_3_3` - 4-3-3
- `F3_5_2` - 3-5-2
- `F5_3_2` - 5-3-2
- `F5_4_1` - 5-4-1
- `F4_2_2_2` - 4-2-2-2 (FC 26 özel)
- `F4_1_4_1` - 4-1-4-1 (FC 26 özel)
- `F3_4_3` - 3-4-3 (FC 26 özel)

## ⚙️ Veri Kaynakları

### FUTBIN (Önerilen)
- Tamamen ücretsiz
- API anahtarı gerekmez
- Güncel piyasa fiyatları
- İlk çalışma: ~5-10 dakika (20.000+ oyuncu)
- Sonraki çalışmalar: <1 saniye (önbellekten)

### FutDB API
- Hızlı ve güvenilir
- Ücretsiz API anahtarı gerekli ([futdb.app](https://futdb.app/))
- Günlük 1000 ücretsiz istek hakkı

## ⚠️ Önemli Notlar

1. **İlk Kullanım**: FUTBIN veri çekimi ilk seferde 5-10 dakika sürebilir
2. **Oran Sınırlama**: FUTBIN'e çok sık sorgu göndermeyin (yerleşik 1 saniye gecikme)
3. **Önbellek**: Daha hızlı sonraki çalıştırmalar için önbelleği kullanın
4. **Yasal**: Veri kaynaklarının kullanım koşullarına uyun

## 📁 Proje Yapısı

```
fc26-bot/
├── src/
│   ├── data/
│   │   └── fc26_data_provider.py  # Veri çekme modülü
│   ├── sbc_solver/
│   │   └── ea_fc_sbc_solver.py    # Ana çözücü
│   ├── solution_display/
│   │   └── console_display.py     # Çözüm göstergesi
│   └── utils/
│       └── formations.py          # Formasyon tanımları
├── main_fc26.py                   # Ana yürütme dosyası
├── requirements_fc26.txt          # Bağımlılıklar
└── README.md                      # Bu dosya
```

## 🤝 Katkıda Bulunma

Katkıda bulunmak isterseniz:
1. Sorunları bildirin
2. İyileştirme önerilerinde bulunun
3. Yeni özellikler ekleyin
4. Belgeleri geliştirin

## 📄 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır.