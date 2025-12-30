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

# --- JAVASCRIPT UNTUK DEVICE ID (ANTI-IP RESET) ---
# Skrip ini akan membuat ID unik satu kali dan menyimpannya di browser kamu selamanya.
if 'device_id' not in st.session_state:
    st.session_state['device_id'] = None

components.html(
    """
    <script>
    let deviceId = localStorage.getItem('ez_ref_device_id');
    if (!deviceId) {
        deviceId = 'USER-' + Math.random().toString(36).substr(2, 9).toUpperCase();
        localStorage.setItem('ez_ref_device_id', deviceId);
    }
    window.parent.postMessage({type: 'set_device_id', value: deviceId}, '*');
    </script>
    """,
    height=0,
)

# Menangkap ID dari JavaScript
def handle_message():
    if "device_id_msg" in st.query_params:
        st.session_state['device_id'] = st.query_params["device_id_msg"]

# Trik sederhana menangkap ID di Streamlit Cloud
device_id_input = st.text_input("Device ID terdeteksi:", key="id_detect", value=st.session_state.get('device_id', 'Mendeteksi...'), disabled=True)

def get_usage_count(uid):
    sheet = connect_to_sheets()
    if sheet and uid and uid != "Mendeteksi...":
        try:
            tz_jkt = pytz.timezone('Asia/Jakarta')
            today = datetime.now(tz_jkt).strftime("%Y-%m-%d")
            all_rows = sheet.get_all_values()
            count = 0
            for row in all_rows[1:]:
                if len(row) >= 2:
                    # Kita cek Kolom B (IP/UID) sekarang berisi Device ID
                    if today in str(row[0]) and str(row[1]).strip() == uid:
                        count += 1
            return count
        except: return 0
    return 0

def log_usage(uid, nama_web, url):
    sheet = connect_to_sheets()
    if sheet:
        try:
            tz_jkt = pytz.timezone('Asia/Jakarta')
            today = datetime.now(tz_jkt).strftime("%Y-%m-%d")
            sheet.append_row([f"'{today}", uid, nama_web, url])
            return True
        except: return False
    return False

# --- LOGIKA UTAMA ---
# Menggunakan Query Params untuk sinkronisasi ID dari JS ke Python
query_params = st.query_params
if "uid" in query_params:
    current_uid = query_params["uid"]
else:
    # Mengarahkan ulang satu kali untuk mengunci ID di URL
    st.markdown(f"""
        <script>
        let dId = localStorage.getItem('ez_ref_device_id');
        if (dId) {{
            const url = new URL(window.location.href);
            url.searchParams.set('uid', dId);
            window.parent.location.href = url.href;
        }}
        </script>
    """, unsafe_allow_html=True)
    st.stop()

usage_now = get_usage_count(current_uid)
limit_harian = 20
sisa_kuota = limit_harian - usage_now

st.title("📝 EZ-Reference Pro")
st.caption(f"Sisa Kuota Hari Ini: {max(0, sisa_kuota)} artikel")

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
                            if log_usage(current_uid, nama_web, url):
                                st.session_state['daftar'].append({'nama': nama_web, 'isi': teks, 'url': url})
                                st.rerun()
                        else: st.error("Teks tidak terbaca.")
                    else: st.error(f"Ditolak Website (Status {res.status_code})")
                except Exception as e: st.error(f"Error: {e}")
        else:
            st.warning("Mohon isi semua kolom.")

# Output
if st.session_state['daftar']:
    st.divider()
    gabungan = ""
    for i, item in enumerate(st.session_state['daftar']):
        st.write(f"**{i+1}. {item['nama']}**")
        gabungan += f"Sumber: {item['nama']}\nURL: {item['url']}\n\n{item['isi']}\n\n{'='*50}\n\n"

    js_copy = f"""<script>function copy() {{ navigator.clipboard.writeText(`{gabungan}`); alert('Tersalin!'); }}</script>
    <button onclick="copy()" style="width:100%; padding:10px; background:#4CAF50; color:white; border:none; border-radius:5px; cursor:pointer;">📋 Copy ke Clipboard</button>"""
    components.html(js_copy, height=60)
    st.download_button("📥 Download .txt", data=gabungan, file_name="Riset_Referensi.txt")
