import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import trafilatura
import cloudscraper
import streamlit.components.v1 as components
from datetime import datetime
import pytz
import random
import time

st.set_page_config(page_title="EZ-Reference Pro", page_icon="📝")

# --- KONEKSI DATABASE ---
@st.cache_resource
def connect_to_sheets():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    try:
        creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
        client = gspread.authorize(creds)
        return client.open("Database_EZ_Reference").sheet1
    except Exception as e:
        st.error(f"Gagal koneksi database: {e}")
        return None

# --- LOGIKA IDENTITAS (UID) ---
# Mengambil ID dari alamat URL
uid = st.query_params.get("uid")

if not uid:
    st.warning("🔒 Mengaktifkan Sistem Keamanan Kuota...")
    # Skrip JS untuk membuat ID dan menyimpannya secara permanen di browser
    components.html(
        """
        <script>
        let deviceId = localStorage.getItem('ez_ref_uid');
        if (!deviceId) {
            deviceId = 'GAM-' + Math.random().toString(36).substr(2, 9).toUpperCase();
            localStorage.setItem('ez_ref_uid', deviceId);
        }
        // Mengarahkan URL agar menyertakan UID tersebut
        const url = new URL(window.location.href);
        url.searchParams.set('uid', deviceId);
        window.parent.location.href = url.href;
        </script>
        """,
        height=100,
    )
    st.info("Sedang menyiapkan identitas perangkatmu, tunggu sebentar...")
    st.stop()

# --- FUNGSI DATABASE ---
def get_usage_count(user_id):
    sheet = connect_to_sheets()
    if sheet:
        try:
            tz_jkt = pytz.timezone('Asia/Jakarta')
            today = datetime.now(tz_jkt).strftime("%Y-%m-%d")
            all_rows = sheet.get_all_values()
            count = 0
            for row in all_rows[1:]:
                # Cek Kolom A (Tanggal) dan Kolom B (UID)
                if len(row) >= 2:
                    if today in str(row[0]) and str(row[1]).strip() == user_id:
                        count += 1
            return count
        except: return 0
    return 0

def log_usage(user_id, nama_web, url):
    sheet = connect_to_sheets()
    if sheet:
        try:
            tz_jkt = pytz.timezone('Asia/Jakarta')
            today = datetime.now(tz_jkt).strftime("%Y-%m-%d")
            # Pakai tanda petik agar format tanggal tidak dirubah Google
            sheet.append_row([f"'{today}", user_id, nama_web, url])
            return True
        except: return False
    return False

# --- LOGIKA UTAMA ---
usage_now = get_usage_count(uid)
limit_harian = 20
sisa_kuota = limit_harian - usage_now

st.title("📝 EZ-Reference Pro")
st.caption(f"ID Perangkat: {uid} | Sisa Kuota: {max(0, sisa_kuota)}")

if sisa_kuota <= 0:
    st.error("🚨 Batas harian 20 artikel tercapai. Silakan kembali besok!")
    st.stop()

if 'daftar' not in st.session_state:
    st.session_state['daftar'] = []

# Form Input
with st.form(key='input_form', clear_on_submit=True):
    st.subheader("➕ Tambah Sumber Baru")
    nama_web = st.text_input("Nama Website")
    url = st.text_input("Link Artikel")
    submit = st.form_submit_button("Tambahkan")

    if submit:
        if nama_web and url:
            with st.spinner('Memproses...'):
                time.sleep(1)
                scraper = cloudscraper.create_scraper()
                headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1)', 'Referer': 'https://www.google.com/'}
                try:
                    res = scraper.get(url, headers=headers, timeout=15)
                    if res.status_code == 200:
                        teks = trafilatura.extract(res.text)
                        if teks:
                            if log_usage(uid, nama_web, url):
                                st.session_state['daftar'].append({'nama': nama_web, 'isi': teks, 'url': url})
                                st.rerun()
                        else: st.error("Teks tidak terbaca.")
                    else: st.error(f"Ditolak Website (Status {res.status_code})")
                except Exception as e: st.error(f"Error: {e}")
        else:
            st.warning("Mohon isi semua kolom, Gam!")

# Output
if st.session_state['daftar']:
    st.divider()
    gabungan = ""
    for i, item in enumerate(st.session_state['daftar']):
        st.write(f"**{i+1}. {item['nama']}**")
        gabungan += f"Sumber: {item['nama']}\nURL: {item['url']}\n\n{item['isi']}\n\n{'='*50}\n\n"

    # Tombol Copy (JavaScript)
    js_copy = f"""<script>function copy() {{ navigator.clipboard.writeText(`{gabungan}`); alert('Tersalin!'); }}</script>
    <button onclick="copy()" style="width:100%; padding:10px; background:#4CAF50; color:white; border:none; border-radius:5px; cursor:pointer;">📋 Copy ke Clipboard</button>"""
    components.html(js_copy, height=60)
    st.download_button("📥 Download .txt", data=gabungan, file_name="Riset_Referensi.txt")
