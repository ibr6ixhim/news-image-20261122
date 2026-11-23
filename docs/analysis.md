# Analisis Leaderboard — news-image-20261122
# "Sum up 22 November's world news in one image"

Tanggal analisis: **Minggu 23 Nov 2026, ~10.35 WIB** (03.35 UTC).
Fase: **dev** (scores live). Tenggat: **Selasa 24 Nov 2026, 00.00 UTC (07.00 WIB)**.
Total submission: **16.098**. Pot: **USD 100 untuk 50 besar**
(1st $20, 2nd $12, 3rd $6, 4–10 $2, 11–50 $1,20).
Aturan: Force_Last (hanya submission terakhir per akun yang diperingkat),
tie-break = ukuran file (lebih kecil lebih baik), gambar ≤1 MiB dan ≤1024×1024.

Sumber data: `GET /api/competitions/news-image-20261122/leaderboard?view=performance&limit=50`
(ditarik 23 Nov 03.35 UTC) + inspeksi visual langsung 10 gambar teratas
(diunduh dari endpoint artifact resmi ke /tmp untuk analisis saja — TIDAK disalin
ke repo ini, TIDAK dipakai sebagai aset, TIDAK dijiplak isinya).

## 1. Tabel Top 10

Semua top 10 punya rekor **12-0-0** (sempurna). Peringkat ditentukan oleh
win-rate estimate (Bayesian), bukan jumlah kemenangan — selisih #1 ke #10
hanya **0,17 poin**, dan #1 ke #50 hanya **0,54 poin**. Artinya: di level ini
yang membedakan bukan "menang vs kalah" melainkan nuansa kecil yang membuat
juri memilih satu gambar atas yang lain dalam duel pairwise.

| Rank | Handle | Judge rate | Interval 90% | Cerita | Wilayah | Bytes | Judul entry |
|------|--------|------------|--------------|--------|---------|-------|-------------|
| 1 | jolly-stork-27 | 99,2370% | 99,03–99,44% | 36 | 7 | 245.676 | atlas22b |
| 2 | evolution0795 | 99,2026% | 98,99–99,41% | 24 | 7 | 765.579 | Sunday 22 November 2026 — the world on one page |
| 3 | gime22 | 99,1843% | 98,97–99,40% | 35 | 7 | 300.136 | Sunday 22 November 2026 — The World in One Day: 35 dated stories, 7 regions: COP31 dawn, Bahrain claims, 186-drone barrage |
| 4 | thepowerofmuse | 99,1504% | 98,93–99,37% | 35 | 7 | 228.325 | Sunday 22 November 2026 — The World in One Day |
| 5 | myhanni | 99,1203% | 98,89–99,35% | 39 | 7 | 418.846 | The Day in World News — Sunday 22 November 2026: 39 stories, 7 regions, 13 illustrated cards, one front page |
| 6 | tidy-pika-44 | 99,1066% | 98,88–99,34% | 37 | 7 | 340.703 | Precise Gradient |
| 7 | ilyayaaa | 99,1059% | 98,87–99,34% | 35 | 6 | 682.433 | Sunday 22 November 2026: 35 stories, 6 regions - COP31 near a deal, Russia's 400-drone barrage on Ukraine, Iran hits US bases in Bahrain |
| 8 | crisp-meteor-21-6813 | 99,0935% | 98,86–99,33% | 36 | 7 | 224.342 | The World in One Day — Sunday 22 November 2026 (36 verified stories, 7 regions) |
| 9 | amber-raven-55 | 99,0787% | 98,84–99,32% | 31 | 6+global | 109.505 | World news — Sunday 22 November 2026 (v4: Claude 31 stories) |
| 10 | iruwae | 99,0650% | 98,82–99,31% | 35 | 7 | 208.862 | Civil Axis |

Garis-garis penting (dari leaderboard yang sama):

| Rank | Handle | Judge rate | Bytes | Catatan |
|------|--------|------------|-------|---------|
| 11 | cggj2663 | 99,0648% | 233.080 | 36 cerita, peta Hormuz yang digambar |
| 15 | fani | 99,0563% | 242.374 | **48 cerita — jumlah terbanyak di top 50** |
| 20 | liddpzz-ops | 99,0172% | 337.962 | 35 cerita, 7 wilayah |
| 30 | coderves | 98,9615% | 789.224 | — |
| 40 | semogaudinjp | 98,9288% | 258.379 | Judul: "COP31 collapses with no deal" |
| 50 | ijeawele-harold-odili | 98,8817% | 137.991 | Garis 50 besar (zona hadiah terakhir) |

### Observasi kuantitatif

- **Jumlah cerita bukan penentu.** Rentang top 50 (dari judul): 27–48 cerita,
  median ~36. #2 hanya 24 cerita tapi peringkat 2; #15 punya 48 cerita tapi
  peringkat 15; #9 punya 31 cerita dan tetap top 10. Sweet spot: **35–39 cerita**.
  Menambah cerita di atas ~40 tidak menaikkan peringkat — malah memaksa teks
  mengecil dan keterbacaan turun.
- **Ukuran file tidak berkorelasi dengan peringkat.** #9 paling ramping
  (109 KB) dan #2 paling gemuk (765 KB) sama-sama top 10. Yang penting:
  tetap di bawah 1 MiB; di luar itu tidak ada keuntungan ukuran.
- **Semua top 10 adalah 12-0-0.** Final heat nanti menilai ulang; peringkat
  dev yang ketat ini berarti entry baru harus benar-benar menonjol secara
  visual untuk masuk 3 besar — selisih 0,17 poin tidak bisa dikejar dengan
  "sedikit lebih banyak cerita".
- **16.098 submission** berarti persaingan jauh lebih padat dari bounty
  21 Nov (9.316 entry). Standar visual top 10 juga lebih tinggi dan lebih
  seragam.

## 2. Formula Pemenang 22 Nov — yang teramati di SEMUA top 10

Struktur halaman depan koran ini nyaris identik di 10/10 entry. Kerangka
universal (dari atas ke bawah):

1. **Top bar** (satu baris kecil): "THE WORLD IN ONE DAY" di kiri +
   "N STORIES · 7 REGIONS · EVERY ONE DATED SUNDAY 22 NOVEMBER 2026" di kanan.
2. **Masthead raksasa**: "Sunday 22 November 2026" — serif tebal, hitam/navy,
   memenuhi lebar halaman. Ini elemen visual terbesar di semua entry.
3. **Sub-headline strip** (merah, italic): 3 berita terbesar dalam satu baris,
   dipisah titik tengah. Hampir selalu: COP31 + Bahrain/Iran + drone Ukraina.
4. **Stats strip** ("by the numbers"): 6 angka besar dengan label kecil.
   Angka yang berulang di top 10: ~200 (negara COP31), 03:00 (deadline
   keberatan COP31), 186 (drone Rusia), 161 (ditembak jatuh), 2 (radar AS),
   723 (kursi Hong Kong), 720/9 (rekor Test India), 16 (kru Sparta II),
   24 (korban kapal Nigeria), 35% (target listrik COP31), $120bn (target
   adaptasi yang dicopot).
5. **Region tabs strip**: pita warna dengan hitungan per wilayah, mis.
   EUROPE 8 · MIDDLE EAST 4 · AMERICAS 7 · ASIA-PACIFIC 9 · AFRICA 3 ·
   OCEANIA 3 · WORLD 2. Ada di 10/10 entry — elemen baru yang tidak sekuat
   ini di 21 Nov.
6. **Timeline strip "THE DAY IN UTC"**: 5–7 peristiwa berjam (01:00 HK polls
   open · 03:00 COP31 objections close · 05:11 Hamas seeks talks · 05:30
   Verstappen wins Vegas · 06:00 COP31 approval due · 08:00 161 of 186
   drones downed · 14:00/16:30/17:00 sport). Ada di 9/10 (#10 memakai
   "clock strip" dengan fungsi sama).
7. **3 kartu besar berilustrasi** (baris pertama, bernomor 1–3): COP31,
   Bahrain/Iran, dan drone Ukraina — ketiganya selalu hadir sebagai kartu
   besar, dengan ilustrasi gambar (bukan foto), badge kepastian, lokasi,
   judul, ringkasan 2–3 baris, dan sumber.
8. **10 kartu menengah berilustrasi** (2 baris × 5, bernomor 4–13): masing-masing
   dengan ilustrasi kecil + badge + lokasi + judul + ringkasan 1–2 baris +
   sumber. Total "13 drawn stories" ini adalah tulang punggung visual.
9. **Peta dunia kecil** (kiri bawah) dengan pin bernomor yang cocok dengan
   nomor cerita 1–13. Label: "WHERE IT HAPPENED — pins match story numbers".
10. **Daftar "ALSO ON SUNDAY 22 NOVEMBER — N MORE STORIES"**: daftar bernomor
    (14–35/39/48) satu baris per cerita: lokasi + judul pendek + sumber.
11. **DATE CHECK box** (bingkai merah, di bawah): menyatakan "wires read up
    to HH:MM UTC", menegaskan semua cerita bertanggal 22 Nov, dan
    MENDAFTAR cerita yang sengaja dikeluarkan karena bertanggal lain.
12. **Footer**: daftar sumber (Reuters, BBC, AP, AFP, Al Jazeera, dst) +
    pernyataan "Pictures and map: original, drawn in code" / "Scenes are
    drawn illustrations, not photographs".
13. **Badge kepastian per cerita**: CONFIRMED / REPORTED / CLAIM / PENDING /
    ONGOING / FORECAST — dengan legenda penjelas ("CLAIM = one side's account,
    labelled as such", "REPORTED = carried by the day's wires", "FORECAST =
    still to happen when drawn").

### Perbandingan dengan formula pemenang 21 Nov

Formula 21 Nov (masthead + headline tanggal + strip angka + 3 kartu besar +
10 kartu kecil + peta + daftar "ALSO ON" + DATE CHECK + sumber per cerita +
badge CONFIRMED/OFFICIAL/REPORTED) **masih berlaku penuh** — semua elemen
itu hadir di 10/10 entry 22 Nov. Yang berubah / berevolusi:

- **Region tabs strip** menjadi elemen wajib baru (10/10). Di 21 Nov elemen
  ini tidak menonjol.
- **Timeline UTC** menjadi strip khusus (9/10), bukan sekadar satu baris.
- **Badge lebih bernuansa**: ditambah PENDING, ONGOING, FORECAST — juri
  tampaknya menghargai kejujuran status ("not yet decided") daripada klaim
  kepastian palsu.
- **"NOT YET DECIDED / NOT YET HAPPENED"** di dalam DATE CHECK: hadir di
  #4, #6, #8, #9, #10 — daftar hal yang BELUM terjadi saat gambar dibuat
  (hasil vote COP31, juara ATP, Liverpool–United). Ini sinyal kejujuran
  yang kuat dan berkorelasi dengan peringkat atas.
- **"Press time" / "wires read to" eksplisit**: semua top 10 menulis jam
  UTC terakhir pembacaan kabel berita (05.30–10.00 UTC). Ini menjadi
  penanda kredibilitas.
- **Palet menyatu total**: semua top 10 memakai kertas krem hangat +
  tinta hitam/navy + aksen merah vermilion. Tidak ada satu pun top 10
  yang memakai palet berbeda. (Ini sekaligus celah — lihat bagian 4.)

### Isi berita yang menjadi konsensus top 10

Tiga cerita besar yang sama di semua kartu #1–3 (urutan bervariasi):

1. **COP31 (Antalya, Turki)** — teks final mendarat saat fajar / dibawa ke
   pemungutan suara; TIDAK menyebut bahan bakar fosil; target listrik 35%
   tahun 2035; target adaptasi $120bn dicopot; mengakui overshoot 1,5°C;
   keberatan ditutup 03:00 GMT; persetujuan ~06:00 GMT.
2. **Bahrain / Iran** — Iran (IRGC) mengklaim rudal+drone menghantam 2 radar
   Patriot AS di Al-Riffa dan Awali; Bahrain menyebut serangan dicegat /
   target situs sipil / tidak ada korban; 2 tanker kena di Hormuz.
   Selalu ber-badge CLAIM — juri menghargai pelabelan klaim sepihak.
3. **Ukraina — 186 drone** — Rusia menembakkan 186 drone semalam, 161
   ditembak jatuh/dijamming, mengenai 18 lokasi; blok apartemen di Dymer
   hancur, orang terjebak. Angka konsensus: **186 / 161**.

Cerita menengah yang berulang (kartu 4–13): Hong Kong votes (723 kursi,
856 kandidat, turnout ~93–98%), Verstappen menang Las Vegas GP, India
720/9 rekor Test di Wellington, kapal kargo Rusia Sparta II terbakar di
Teluk Finlandia (16 kru selamat), kapal Bayelsa Nigeria tenggelam (24 tewas),
Iran mulai rationing listrik, Gaza (serangan van bantuan, 3–4 tewas),
Bolsonaro di ICU, FBI hack database kejahatan, Hong Kong / AUKUS (Marles),
Nepal PM ke Delhi, Paus Leo XIV jamuan 1.300 tamu miskin.

### Akurasi tanggal: juri TIDAK menghukum keras — tapi DATE CHECK wajib ada

Temuan penting: akurasi tanggal sempurna ternyata BUKAN syarat peringkat
atas, tapi *tampilan* ketelitian tanggal adalah syarat.

- #7 (peringkat 7) memakai angka **400+ drone dan 110 misil** — itu adalah
  serangan Kamis–Jumat (19–20 Nov), BUKAN Minggu. Ia juga memasukkan
  serangan Kryvyi Rih, penangkapan 'El Chapo Isidro', dan probe Nvidia
  sebagai cerita Minggu — semuanya dikeluarkan oleh entry lain sebagai
  berita Jumat/Sabtu. Tetap peringkat 7.
- #3 (peringkat 3) memasukkan 'El Chapo Isidro', BepiColombo, dan probe
  Nvidia sebagai cerita Minggu; #9 memasukkan BepiColombo sebagai cerita
  #31. Entry lain secara eksplisit mengeluarkan ketiganya di DATE CHECK.
- #6 memakai angka **148 drone** (bukan 186) dan tetap peringkat 6.

Kesimpulan: juri pairwise tidak memverifikasi tanggal terhadap feed berita —
ia menilai apa yang tampak di gambar. Yang ia hargai adalah: struktur
lengkap, keterbacaan, klaim yang diberi label (CLAIM/REPORTED), dan
keberadaan DATE CHECK yang eksplisit. Namun, untuk entry KITA, tetap pakai
angka yang benar (186/161) karena itu konsensus mayoritas (8/10) dan
menghindari risiko penalti di final heat, di mana penjurian bisa lebih
ketat. Jangan meniru kesalahan tanggal #3/#7 — mereka menang *meskipun*
kesalahan itu, bukan karena kesalahan itu.

## 3. Celah / peluang diferensiasi (yang TIDAK dilakukan top 10)

Semua top 10 konvergen ke satu template yang sama. Itu berarti setiap
penyimpangan yang dieksekusi dengan baik akan terlihat menonjol saat juri
membandingkan dua gambar berdampingan. Celah yang teridentifikasi, diurutkan
dari yang paling menjanjikan:

1. **Palet warna — celah terbesar.** 10/10 memakai kertas krem + tinta
   hitam/navy + merah. Tidak ada satu pun palet alternatif di top 10.
   Palet berbeda yang tetap terasa "koran" (mis. navy gelap sebagai
   latar masthead dengan teks krem, atau kertas biru-abu dingin dengan
   aksen emas/teal) akan langsung membedakan gambar kita dalam duel
   pairwise. Risiko: terlalu gelap bisa mengorbankan keterbacaan — jaga
   kontras teks tetap ≥ 7:1 dan uji di 512 px.
2. **Tidak ada hero dominan.** Semua top 10 memakai 3 kartu besar berukuran
   SAMA. Tidak ada satu pun yang memberi satu cerita (mis. malam drone
   Kyiv, atau serangan Bahrain) porsi ~40% halaman sebagai hero visual.
   Satu hero besar yang kuat + 2 kartu sedang bisa menjadi pembeda
   struktural yang nyata — sekaligus memberi ruang ilustrasi yang lebih
   detail dan mudah dibaca.
3. **Peta kecil dan pasif.** 9/10 menaruh peta kecil di sudut kiri bawah
   dengan pin 1–13. Hanya #10 yang petanya agak besar. Peta besar sebagai
   elemen sentral (mis. setengah lebar halaman, dengan pin bernomor untuk
   SEMUA cerita, bukan hanya 13) belum dipakai siapa pun. Peta besar juga
   membantu juri "melihat" cakupan 7 wilayah secara instan.
4. **Timeline 24 jam yang tipis.** Semua timeline hanya 5–7 peristiwa dalam
   satu strip kecil. Belum ada yang membuat pita timeline 24 jam penuh
   (00–24 UTC, ~12–16 peristiwa berjam) sebagai elemen desain utama.
   Ini cocok dengan judul "The World in One Day" — harinya sendiri yang
   divisualisasikan.
5. **Keterbacaan di 512 px.** Semua top 10 memadatkan 31–48 cerita ke
   1024 px; daftar ALSO ON memakai teks ~11–13 px yang nyaris tidak terbaca
   di 512 px. #2 membuktikan 24 cerita bisa peringkat 2. Entry dengan
   ~30–33 cerita tapi tipografi lebih besar (judul kartu ≥ 20 px, badan
   ≥ 14 px, daftar ≥ 13 px) bisa menang di keterbacaan — kriteria yang
   juri sebut secara eksplisit sebagai "careful picture editor".
6. **Afrika dan Oseania tipis di mana-mana.** Hitungan wilayah top 10:
   Afrika 1–6 (median 3–4), Oseania 2–3 (median 3). #7 hanya punya
   1 cerita Afrika dan tetap peringkat 7 — jadi ini bukan syarat keras.
   Tapi entry yang benar-benar punya 5–6 cerita Afrika NYATA bertanggal
   22 Nov (bukan filler) dan 4–5 Oseania akan terlihat lebih "dunia"
   daripada kompetitor. Syarat: cerita harus nyata dan terverifikasi,
   bukan dipaksakan.
7. **"GLOBAL / WORLD" sebagai kantong.** Banyak entry mengisi 2–6 slot
   dengan bucket "WORLD/GLOBAL" (Bitcoin, Nvidia, dll). Bucket ini terasa
   seperti pengisi. Menggantinya dengan cerita wilayah yang nyata
   memperkuat klaim "7 regions".
8. **Olahraga terkubur.** Olahraga (Verstappen, India 720/9, ATP final,
   Liverpool–United) selalu jadi kartu menengah atau daftar. Hanya #5 yang
   punya strip khusus "SUNDAY'S LATE SPORT". Pita olahraga khusus di bawah
   (atau kolom sport) adalah pembeda kecil yang murah.
9. **"NOT YET" sebagai elemen desain, bukan sekadar baris.** Entry yang
   menulis "Not yet decided" hanya sebagai satu baris di DATE CHECK. Belum
   ada yang memvisualisasikannya (mis. panel "STILL TO COME" dengan 3–4
   peristiwa yang belum terjadi saat press time). Ini memperkuat kejujuran
   tanpa memakan banyak ruang.
10. **Angka yang salah di top 10 adalah peluang.** #7 (400 drone) dan #6
    (148 drone) memakai angka yang bertentangan dengan konsensus 186/161.
    Entry kita yang memakai angka konsensus + sumber yang konsisten di
    semua tempat (stats strip, kartu besar, timeline) akan terlihat lebih
    koheren saat dibandingkan langsung.

### Yang JANGAN ditiru

- Jangan meniru kesalahan tanggal #3/#7 (El Chapo, BepiColombo, Nvidia,
  Kryvyi Rih sebagai cerita Minggu) — mereka menang meskipun itu, dan
  final heat bisa lebih ketat.
- Jangan menambah cerita di atas ~40 hanya demi angka — #15 (48 cerita)
  hanya peringkat 15; teks mengecil dan keterbacaan jatuh.
- Jangan memakai palet yang terlalu jauh dari koran (neon, gradien
  mencolok) — diferensiasi harus tetap terasa "halaman depan koran".
- Jangan mengorbankan 3 kartu besar + 10 kartu menengah — kerangka itu
  terbukti; variasikan di dalamnya, jangan buang kerangkanya.

## 4. Rekomendasi desain konkret untuk entry kita

Target: **masuk 3 besar** (garis #3 saat ini 99,18%; #1 99,24%).
Strategi: **ikuti kerangka pemenang 100%, lalu diferensiasikan di 3 titik
yang terukur** — palet, hero, dan peta+timeline. Jangan bereksperimen di
lebih dari 3 titik sekaligus; juri menghukum gambar yang terasa asing.

### Layout yang direkomendasikan (1024×1024, PNG ≤1 MiB)

```
┌──────────────────────────────────────────────────────────┐
│ TOP BAR: THE WORLD IN ONE DAY | 36 STORIES · 7 REGIONS  │
│          · EVERY ONE DATED SUNDAY 22 NOVEMBER 2026      │
├──────────────────────────────────────────────────────────┤
│ MASTHEAD: Sunday 22 November 2026  (serif tebal, besar)  │
├──────────────────────────────────────────────────────────┤
│ SUB-HEADLINE (merah): COP31 · Bahrain · 186 drones       │
├──────────────────────────────────────────────────────────┤
│ STATS STRIP: 6 angka besar (186 / 161 / 03:00 / 723 /    │
│              720/9 / 16) dengan label kecil              │
├──────────────────────────────────────────────────────────┤
│ REGION TABS: EUROPE n · MIDDLE EAST n · ASIA-PACIFIC n · │
│              AMERICAS n · AFRICA n · OCEANIA n · WORLD n │
├──────────────────────────────────────────────────────────┤
│ TIMELINE "THE DAY IN UTC": 6–7 peristiwa berjam          │
├──────────────────────────────────────────────────────────┤
│ HERO (kiri, ~55% lebar) + 2 KARTU BESAR (kanan, susun)   │
│ Hero: malam drone Kyiv (ilustrasi besar, badge REPORTED) │
│ Kartu 2: COP31  |  Kartu 3: Bahrain (badge CLAIM)        │
├──────────────────────────────────────────────────────────┤
│ 10 KARTU MENENGAH (2 baris × 5) — ilustrasi + badge +    │
│ judul + ringkasan 1–2 baris + sumber                     │
├──────────────────────────────────────────────────────────┤
│ PETA BESAR (kiri, ~45%)  |  ALSO ON SUNDAY 22 NOVEMBER   │
│ pin bernomor 1–13        |  daftar 14–36 (satu baris)    │
├──────────────────────────────────────────────────────────┤
│ DATE CHECK (bingkai merah): wires read to HH:MM UTC +    │
│ daftar excluded + NOT YET DECIDED (3–4 item)             │
├──────────────────────────────────────────────────────────┤
│ FOOTER: sumber + "Pictures and map: original, drawn      │
│ in code" + legenda badge                                 │
└──────────────────────────────────────────────────────────┘
```

### Spesifikasi konten

- **Jumlah cerita: 36** (13 bergambar + 23 daftar). Sweet spot top 10
  adalah 35–39; 36 memberi ruang tipografi yang cukup tanpa terlihat
  lebih sedikit dari kompetitor.
- **Wilayah: 7, dengan hitungan jujur.** Target: Europe 8, Middle East 5,
  Asia-Pacific 8, Americas 5, Africa 4, Oceania 3, World 3. Afrika 4
  butuh riset nyata (jangan filler) — ini salah satu pembeda kita.
- **3 cerita besar (hero + 2 kartu):** (1) Rusia 186 drone ke Ukraina
  (hero, REPORTED), (2) COP31 teks final (REPORTED/ONGOING), (3) Iran
  klaim serang radar AS di Bahrain (CLAIM — wajib ber-badge CLAIM).
- **10 kartu menengah:** Hong Kong votes, Verstappen Las Vegas GP,
  India 720/9, Sparta II terbakar, kapal Bayelsa, Iran rationing listrik,
  Gaza van bantuan, Bolsonaro ICU, FBI hack, Nepal PM ke Delhi (atau
  Paus Leo XIV — pilih berdasarkan verifikasi riset; jangan pakai yang
  tidak terverifikasi tanggalnya).
- **Angka yang dipakai (konsisten di semua tempat):** 186 drone, 161
  ditembak jatuh, 18 lokasi, 03:00 GMT deadline COP31, 35% listrik 2035,
  $120bn adaptasi dicopot, 723 kursi Hong Kong, 856 kandidat, 720/9,
  16 kru Sparta II, 24 korban Bayelsa, 2 radar Patriot.
- **Press time:** tulis eksplisit, mis. "Wires read to 09:00 UTC".
  Semua cerita harus terjadi / pertama dilaporkan pada 22 Nov UTC
  sampai jam itu. Cerita yang hasilnya belum keluar saat press time
  (vote COP31, juara ATP, Liverpool–United) masuk "NOT YET DECIDED",
  BUKAN sebagai hasil.

### Palet (diferensiasi #1)

- **Jangan** memakai krem + hitam + merah yang sama persis dengan 10/10
  top entries. Rekomendasi: kertas **biru-abu dingin terang** (#EDEFF2)
  atau tetap krem tapi dengan **tinta navy sangat gelap (#101E33)** sebagai
  warna dominan masthead + **aksen teal gelap (#0E6B6B)** menggantikan
  sebagian merah, merah vermilion (#D9481C) hanya untuk sub-headline dan
  DATE CHECK. Hasilnya tetap "koran" tapi langsung terlihat berbeda di
  duel pairwise. Uji kontras: teks badan di atas kertas harus ≥ 7:1.
- Alternatif yang lebih berani (hanya jika render pertama terlihat baik):
  masthead navy gelap dengan teks krem — tapi risiko keterbacaan tinggi,
  jadi jadikan opsi v2, bukan v1.

### Elemen wajib (checklist — semua harus ada agar tidak kalah struktural)

- [ ] Top bar dengan jumlah cerita + wilayah + tanggal
- [ ] Masthead tanggal raksasa
- [ ] Sub-headline 3 berita terbesar
- [ ] Stats strip 6 angka
- [ ] Region tabs dengan hitungan per wilayah
- [ ] Timeline "THE DAY IN UTC" (6–7 peristiwa)
- [ ] 3 kartu besar berilustrasi + badge + sumber
- [ ] 10 kartu menengah berilustrasi + badge + sumber
- [ ] Peta dunia dengan pin bernomor (lebih besar dari top 10 biasa)
- [ ] Daftar ALSO ON bernomor dengan sumber per cerita
- [ ] DATE CHECK (bingkai merah) + daftar excluded + NOT YET DECIDED
- [ ] Footer sumber + "original, drawn in code" + legenda badge
- [ ] Badge kepastian di SETIAP cerita bergambar (CONFIRMED / REPORTED /
      CLAIM / PENDING / ONGOING / FORECAST)
- [ ] Sumber di setiap cerita (Reuters, AP, AFP, BBC, Al Jazeera, dst)
- [ ] Tanpa foto berhak cipta; ilustrasi digambar via kode; tanpa wajah
      orang sungguhan buatan AI

### Yang harus dihindari (pelajaran dari top 10)

- Jangan memasukkan sebagai cerita Minggu: serangan 400 drone/110 misil
  (19–20 Nov), gempa Peru (20 Nov), 'El Chapo Isidro' (20 Nov),
  BepiColombo (21 Nov), probe Nvidia (20 Nov), serangan Kryvyi Rih
  (20–21 Nov), KTT Shenzhen (19 Nov), penutupan EU–Indonesia (21 Nov).
  Semua itu masuk daftar excluded di DATE CHECK.
- Jangan menulis hasil yang belum terjadi saat press time sebagai fakta
  (juara ATP, hasil Liverpool–United, hasil vote COP31) — masukkan ke
  "NOT YET DECIDED".
- Jangan memakai angka drone selain 186/161 di mana pun (stats strip,
  kartu, timeline harus konsisten).
- Jangan meniru judul "atlas22b" / "Precise Gradient" / "Civil Axis"
  (judul abstrak tanpa tanggal) — judul kita harus menyebut tanggal dan
  jumlah cerita, seperti mayoritas top 10.

### Rencana iterasi (mengingat Force_Last + kuota 10/hari, 20 total)

- **v1:** kerangka pemenang penuh + palet berbeda + hero + peta besar.
  Target: masuk 50 besar dulu (garis #50: 98,88%).
- **v2 (jika kuota ada):** perbaiki berdasarkan duel — perbesar tipografi
  daftar ALSO ON bila keterbacaan di 512 px bermasalah, atau tambah
  2–3 cerita Afrika/Oseania terverifikasi bila riset menemukan yang kuat.
- Jangan submit v2 hanya demi menambah cerita di atas 40 — bukti
  menunjukkan itu tidak menaikkan peringkat.

---
*Catatan metodologi: analisis ini hanya memakai pola dan struktur (layout,
jumlah cerita, palet, elemen) dari entry lain. Tidak ada teks, judul, angka,
atau ilustrasi entry lain yang disalin ke entry kita. Semua konten berita
entry kita harus berasal dari riset independen dengan sumber primer/kantor
berita dan verifikasi tanggal.*

