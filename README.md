# m3u8_to_mp4

## 📘 Introduction
Το **m3u8_to_mp4** είναι ένα Python script που μετατρέπει αρχεία HLS playlist (`.m3u8`) σε ενιαία αρχεία βίντεο `.mp4`.  
Είναι χρήσιμο όταν χρειάζεσαι να κατεβάσεις ή να αποθηκεύσεις streams ως κανονικό MP4 αρχείο.

---

## ✨ Features
- Μετατροπή από URL ή τοπικό `.m3u8` σε `.mp4`
- Αυτόματο κατέβασμα των segments
- Συγχώνευση όλων των segments σε ένα τελικό MP4
- Απλή, καθαρή υλοποίηση σε Python
- Βάση για μελλοντικές επεκτάσεις (π.χ. επιλογή ποιότητας, logging κ.λπ.)

---

## 🔧 Installation

Βεβαιώσου ότι έχεις εγκατεστημένη Python 3.7+.

```bash
git clone https://github.com/giannis10/m3u8_to_mp4.git
cd m3u8_to_mp4
pip install -r requirements.txt
