**[INDONESIA]**
📝 EZ-Reference: Multi-Source Collector
Oleh: @denmasagam

**Deskripsi**
EZ-Reference adalah aplikasi berbasis web (Streamlit) yang dirancang untuk mempermudah para peneliti, penulis, dan mahasiswa dalam mengumpulkan referensi dari berbagai artikel di internet secara efisien. Alat ini mengekstrak teks murni dari berbagai sumber web dan menggabungkannya ke dalam satu format yang siap digunakan untuk analisis lebih lanjut menggunakan AI (seperti ChatGPT, Gemini, atau Claude).

**Fitur Utama**
Ekstraksi Teks Otomatis: Mengambil isi artikel tanpa gangguan iklan atau menu navigasi.

Penyamaran Googlebot: Dilengkapi dengan header khusus untuk meningkatkan keberhasilan akses pada situs yang membatasi bot.

Manajemen Koleksi: Menambah, melihat, atau menghapus sumber referensi dalam satu sesi secara fleksibel.

Copy to Clipboard: Menyalin seluruh hasil pengumpulan teks dengan satu klik tombol.

Download .txt: Mengunduh semua referensi yang terkumpul ke dalam satu file teks terorganisir.

**Persyaratan Sistem**
Sebelum menjalankan aplikasi ini, pastikan Anda telah menginstal pustaka berikut yang tertera di requirements.txt:

1. streamlit
2. trafilatura
3. cloudscraper

**Cara Penggunaan**
Input Data: Masukkan nama website dan tempelkan link URL artikel pada kolom yang tersedia.

Tambahkan: Klik tombol "Tambahkan ke Daftar". Aplikasi akan memproses ekstraksi teks secara otomatis.

Kelola: Ulangi langkah di atas untuk sumber lain. Anda bisa melihat daftar koleksi di bagian bawah.

Ambil Hasil: Gunakan tombol "Copy to Clipboard" untuk penggunaan cepat pada LLM AI, atau klik "Download File .txt" untuk menyimpan arsip riset Anda.

**Catatan Penting**
Aplikasi ini tidak menyimpan data secara permanen (bersifat sementara per sesi). Pastikan Anda telah mengunduh atau menyalin teks sebelum menutup tab browser.

Beberapa situs web dengan sistem keamanan tinggi (seperti yang menggunakan Paywall atau proteksi bot ekstrem) mungkin tidak dapat diakses.

**[ENGLISH]**
📝 EZ-Reference: Multi-Source Collector
By: @denmasagam

**Overview**
EZ-Reference is a Streamlit-based web application designed to help researchers, writers, and students efficiently collect references from various internet articles. This tool extracts plain text from multiple web sources and consolidates them into a single format, ready for further analysis using AI (such as ChatGPT, Gemini, or Claude).

**Key Features**
Automated Text Extraction: Retrieves article content without the clutter of ads or navigation menus.

Googlebot Cloaking: Equipped with specific headers to increase access success rates on sites that restrict bots.

Collection Management: Flexibly add, view, or delete reference sources within a single session.

Copy to Clipboard: Copy all collected text results with a single button click.

Download .txt: Download all gathered references into one organized text file.

**Prerequisites**
Before running this application, ensure you have installed the following libraries listed in requirements.txt:

1. streamlit
2. trafilatura
3. cloudscraper

**How to Use**
Data Input: Enter the website name and paste the article URL link into the provided fields.

Add: Click the "Add to List" button. The app will automatically process the text extraction.

Manage: Repeat the steps above for other sources. You can view your collection list at the bottom.

Get Results: Use the "Copy to Clipboard" button for quick use with AI LLMs, or click "Download .txt File" to save your research archive.

**Important Notes**
This application does not store data permanently (data is session-based). Ensure you have downloaded or copied your text before closing the browser tab.

Some websites with high-level security (such as those using Paywalls or extreme bot protection) may not be accessible.
