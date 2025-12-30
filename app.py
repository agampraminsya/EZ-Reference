import streamlit as st
import trafilatura
import cloudscraper

st.set_page_config(page_title="EZ-Reference Pro", page_icon="📝")

# --- HEADER & DESKRIPSI ---
st.title("📝 EZ-Reference v1.0")
st.caption("Alat riset otomatis by @denmasagam v1.0")

if 'daftar_artikel' not in st.session_state:
    st.session_state['daftar_artikel'] = []

# --- FORM INPUT ---
with st.form(key='input_form', clear_on_submit=True):
    st.subheader("➕ Tambah Referensi Baru")
    nama_web = st.text_input("Nama Website")
    url = st.text_input("Link Artikel")
    submit_button = st.form_submit_button(label="Tambahkan ke Daftar")

    if submit_button:
        if nama_web and url:
            with st.spinner('Menjalankan taktik Googlebot...'):
                try:
                    # Inisialisasi Scraper
                    scraper = cloudscraper.create_scraper()
                    
                    # LOGIKA PENYAMARAN (Googlebot & Referer)
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
                        'Referer': 'https://www.google.com/',
                        'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7'
                    }
                    
                    response = scraper.get(url, headers=headers, timeout=15)
                    
                    if response.status_code == 200:
                        teks = trafilatura.extract(response.text)
                        if teks:
                            st.session_state['daftar_artikel'].append({
                                'nama': nama_web,
                                'isi': teks,
                                'url': url
                            })
                            st.toast(f"✅ Berhasil menembus {nama_web}!", icon="🚀")
                        else:
                            st.error("Konten tidak ditemukan. Mungkin website menggunakan skrip dinamis yang sangat berat.")
                    else:
                        st.error(f"Gagal akses (Status: {response.status_code}). Website ini sangat ketat.")
                except Exception as e:
                    st.error(f"Kesalahan teknis: {e}")
        else:
            st.warning("Nama web dan Link tidak boleh kosong, Gam!")

# --- DAFTAR KOLEKSI & MANAJEMEN ---
if st.session_state['daftar_artikel']:
    st.divider()
    st.subheader(f"🗂️ Koleksi Riset ({len(st.session_state['daftar_artikel'])} Sumber)")
    
    file_gabungan = ""
    for index, item in enumerate(st.session_state['daftar_artikel']):
        col_info, col_del = st.columns([0.8, 0.2])
        with col_info:
            st.write(f"**{index+1}. {item['nama']}**")
            st.caption(item['url'])
        with col_del:
            if st.button("Hapus", key=f"btn_{index}"):
                st.session_state['daftar_artikel'].pop(index)
                st.rerun()
        
        # Gabungkan teks untuk download
        file_gabungan += f"Ini sumber dari {item['nama']}:\nURL: {item['url']}\n\n{item['isi']}\n\n"
        file_gabungan += "="*60 + "\n\n"

    st.write("---")
    c1, c2 = st.columns(2)
    with c1:
        st.download_button("📥 Download File .txt", data=file_gabungan, file_name="Referensi.txt")
    with c2:
        if st.button("🗑️ Kosongkan Semua"):
            st.session_state['daftar_artikel'] = []
            st.rerun()

# --- FOOTER ---
st.markdown("---")
st.info("**Tentang Laman Ini:**")
st.caption("Laman ini mempermudah pengumpulan referensi artikel internet tanpa membuang waktu membaca satu per satu. File .txt yang diunduh bisa dimasukkan ke LLM AI (ChatGPT, Gemini, Claude) untuk dijelaskan ulang.")
