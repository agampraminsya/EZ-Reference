import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import trafilatura
import cloudscraper
import streamlit.components.v1 as components
from datetime import datetime
import random
import time

st.set_page_config(page_title="EZ-Reference Pro", page_icon="📝")

# --- KONEKSI DATABASE GOOGLE SHEETS ---
@st.cache_resource
def connect_to_sheets():
    scope = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
    client = gspread.authorize(creds)
    # PASTIKAN NAMA SHEET INI SAMA DENGAN YANG KAMU BUAT
    return client.open("Database_EZ_Reference").sheet1

def get_user_ip():
    # Mengambil IP asli user di Streamlit Cloud
    return st.context.headers.get("X-Forwarded-For", "127.0.0.1").split(",")[0]

def check_daily_limit(ip):
    try:
        sheet = connect_to_sheets()
        today = datetime.now().strftime("%Y-%m-%d")
        records = sheet.get_all_records()
        count = sum(1 for row in records if str(row['ip_address']) == ip and str(row['tanggal']) == today)
        return count
    except:
        return 0

def log_to_sheets(ip, nama_web, url):
    try:
        sheet = connect_to_sheets()
        today = datetime.now().strftime("%Y-%m-%d")
        sheet.append_row([today, ip, nama_web, url])
    except:
        pass

# --- LOGIKA APLIKASI ---
user_ip = get_user_ip()
usage_count = check_daily_limit(user_ip)

st.title("📝 EZ-Reference: Anti-Curang Edition")
st.caption(f"IP Kamu: {user_ip} | Penggunaan Hari Ini: {usage_count}/20")

if usage_count >= 20:
    st.error("🚨 Batas 20 artikel per hari tercapai. Sistem mencatat IP kamu. Silakan kembali besok!")
    st.stop()

if 'daftar' not in st.session_state:
    st.session_state['daftar'] = []

# Form Input
with st.form(key='my_form', clear_on_submit=True):
    nama_web = st.text_input("Nama Website")
    url = st.text_input("Link Artikel")
    if st.form_submit_button("Tambahkan ke Daftar"):
        if len(st.session_state['daftar']) >= 10:
            st.warning("Maksimal 10 artikel per sesi download.")
        elif nama_web and url:
            with st.spinner('Menyamar sebagai Googlebot...'):
                time.sleep(random.uniform(1, 2)) # Jeda manusiawi
                scraper = cloudscraper.create_scraper()
                headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)', 'Referer': 'https://www.google.com/'}
                try:
                    res = scraper.get(url, headers=headers, timeout=15)
                    if res.status_code == 200:
                        teks = trafilatura.extract(res.text)
                        if teks:
                            st.session_state['daftar'].append({'nama': nama_web, 'isi': teks, 'url': url})
                            log_to_sheets(user_ip, nama_web, url) # Catat ke Google Sheets
                            st.rerun()
                        else: st.error("Teks tidak terbaca.")
                    else: st.error(f"Ditolak (Status {res.status_code})")
                except Exception as e: st.error(f"Error: {e}")

# --- OUTPUT & MANAJEMEN ---
if st.session_state['daftar']:
    st.divider()
    gabungan = ""
    for i, item in enumerate(st.session_state['daftar']):
        c1, c2 = st.columns([0.8, 0.2])
        c1.write(f"**{i+1}. {item['nama']}**")
        if c2.button("Hapus", key=f"h_{i}"):
            st.session_state['daftar'].pop(i)
            st.rerun()
        gabungan += f"Sumber: {item['nama']}\nURL: {item['url']}\n\n{item['isi']}\n\n{'='*50}\n\n"

    # Tombol Copy JS
    js_copy = f"""<script>function copy() {{ navigator.clipboard.writeText(`{gabungan}`); alert('Tersalin!'); }}</script>
    <button onclick="copy()" style="width:100%; padding:10px; background:#4CAF50; color:white; border:none; border-radius:5px; cursor:pointer;">📋 Copy Semua ke Clipboard</button>"""
    components.html(js_copy, height=60)
    
    st.download_button("📥 Download .txt", data=gabungan, file_name="Riset_Referensi.txt")
    if st.button("🗑️ Kosongkan Sesi"):
        st.session_state['daftar'] = []
        st.rerun()

st.markdown("---")
st.info("**Deskripsi:** Laman ini membantu pengumpulan referensi cepat melalui untuk dianalisis lebih lanjut oleh AI. Batas 20 artikel/hari diterapkan untuk menjaga kesehatan IP server.")
