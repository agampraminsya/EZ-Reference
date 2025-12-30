import streamlit as st
import trafilatura
import cloudscraper
import streamlit.components.v1 as components
import random
import time

st.set_page_config(page_title="EZ-Reference Pro", page_icon="📝")

# --- DATABASE IDENTITAS (RANDOM AGENT) ---
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
]

st.title("📝 EZ-Reference Pro (Anti-Bot Edition)")
st.caption("Batas: 10 Artikel per Sesi | Max 20 Artikel per Hari")

# Inisialisasi State
if 'daftar_artikel' not in st.session_state:
    st.session_state['daftar_artikel'] = []
if 'total_generated' not in st.session_state:
    st.session_state['total_generated'] = 0

# --- CEK COOLDOWN GLOBAL (SIMULASI) ---
if st.session_state['total_generated'] >= 20:
    st.error("🚨 Kamu sudah mencapai batas maksimal 20 artikel per hari. Silakan kembali besok!")
    st.stop() # Hentikan aplikasi untuk user ini

# --- FORM INPUT ---
with st.form(key='input_form', clear_on_submit=True):
    st.subheader("➕ Tambah Sumber Baru")
    nama_web = st.text_input("Nama Website")
    url = st.text_input("Link Artikel")
    submit_button = st.form_submit_button(label="Tambahkan ke Daftar")

    if submit_button:
        # Cek Batasan Sesi (10 Artikel)
        if len(st.session_state['daftar_artikel']) >= 10:
            st.warning("⚠️ Batas maksimal per sesi adalah 10 artikel. Silakan download dulu, lalu hapus daftar.")
        elif nama_web and url:
            with st.spinner('Sedang memproses... (Memberikan jeda agar aman)'):
                try:
                    # Taktik 1: Jeda Acak (Human-like behavior)
                    time.sleep(random.uniform(1, 3))
                    
                    # Taktik 2: Pilih Identitas Acak
                    agent = random.choice(USER_AGENTS)
                    scraper = cloudscraper.create_scraper()
                    headers = {
                        'User-Agent': agent,
                        'Referer': 'https://www.google.com/',
                    }
                    
                    response = scraper.get(url, headers=headers, timeout=15)
                    
                    if response.status_code == 200:
                        teks = trafilatura.extract(response.text)
                        if teks:
                            st.session_state['daftar_artikel'].append({'nama': nama_web, 'isi': teks, 'url': url})
                            st.session_state['total_generated'] += 1
                            st.toast(f"✅ Berhasil! (Identitas: {agent[:20]}...)")
                        else:
                            st.error("Teks tidak terbaca.")
                    else:
                        st.error(f"Ditolak Website (Status: {response.status_code})")
                except Exception as e:
                    st.error(f"Kesalahan: {e}")
        else:
            st.warning("Isi data dulu ya, Gam!")

# --- MANAJEMEN DAFTAR ---
if st.session_state['daftar_artikel']:
    st.divider()
    file_gabungan = ""
    for index, item in enumerate(st.session_state['daftar_artikel']):
        c1, c2 = st.columns([0.8, 0.2])
        c1.write(f"**{index+1}. {item['nama']}**")
        if c2.button("Hapus", key=f"del_{index}"):
            st.session_state['daftar_artikel'].pop(index)
            st.rerun()
        file_gabungan += f"Sumber: {item['nama']}\nURL: {item['url']}\n\n{item['isi']}\n\n{'='*50}\n\n"

    # Tombol Copy (JS)
    copy_js = f"""<script>function copy() {{ navigator.clipboard.writeText(`{file_gabungan}`); alert('Teks tersalin!'); }}</script>
    <button onclick="copy()" style="width:100%; padding:10px; background:#4CAF50; color:white; border:none; border-radius:5px;">📋 Copy Semua Teks</button>"""
    components.html(copy_js, height=60)
    
    st.download_button("📥 Download .txt", data=file_gabungan, file_name="Riset_Referensi.txt")
    if st.button("🗑️ Bersihkan Sesi"):
        st.session_state['daftar_artikel'] = []
        st.rerun()

st.markdown("---")
st.caption("Peringatan: Alat ini menggunakan rotasi identitas untuk keamanan IP.")
