import streamlit as st
import trafilatura
import cloudscraper

st.set_page_config(page_title="Kolektor Referensi Otomatis", page_icon="📝")

st.title("📝 Kolektor Referensi by Agam Praminsya")

# 1. Inisialisasi daftar artikel di session state
if 'daftar_artikel' not in st.session_state:
    st.session_state['daftar_artikel'] = []

# 2. Form Input dengan Fitur Auto-Clear
with st.form(key='input_form', clear_on_submit=True):
    st.subheader("➕ Tambah Sumber Baru")
    nama_web = st.text_input("Nama Website (Misal: Nature, BBC, dsb)")
    url = st.text_input("Link Artikel (Pastikan ada https://)")
    
    # Tombol submit khusus di dalam form
    submit_button = st.form_submit_button(label="Tambahkan ke Daftar")

    if submit_button:
        if nama_web and url:
            with st.spinner('Sedang mengambil data...'):
                try:
                    scraper = cloudscraper.create_scraper()
                    response = scraper.get(url)
                    if response.status_code == 200:
                        teks = trafilatura.extract(response.text)
                        if teks:
                            # Memasukkan ke list koleksi
                            st.session_state['daftar_artikel'].append({
                                'nama': nama_web,
                                'isi': teks,
                                'url': url
                            })
                            st.toast(f"✅ {nama_web} berhasil ditambahkan!", icon="✔️")
                        else:
                            st.error("Gagal mengambil teks. Website mungkin diproteksi.")
                    else:
                        st.error(f"Gagal tembus. Kode Error: {response.status_code}")
                except Exception as e:
                    st.error(f"Terjadi kesalahan teknis: {e}")
        else:
            st.warning("Mohon isi nama website dan link terlebih dahulu.")

# 3. Menampilkan Koleksi & Tombol Download
if st.session_state['daftar_artikel']:
    st.divider()
    st.subheader(f"🗂️ Daftar Koleksi: {len(st.session_state['daftar_artikel'])} Artikel")
    
    file_gabungan = ""
    for item in st.session_state['daftar_artikel']:
        file_gabungan += f"Ini sumber dari {item['nama']}:\nURL: {item['url']}\n\n{item['isi']}\n\n"
        file_gabungan += "="*60 + "\n\n"
        st.write(f"✅ **{item['nama']}** - {item['url'][:50]}...")

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="📥 Download Semua Referensi (.txt)",
            data=file_gabungan,
            file_name="Koleksi_Referensi_MNY.txt",
            mime="text/plain"
        )
    with col2:
        if st.button("🗑️ Hapus Semua Daftar"):
            st.session_state['daftar_artikel'] = []
            st.rerun()

# 4. Deskripsi Kegunaan (Sesuai Permintaanmu)
st.markdown("---")
st.info("**Tentang Laman Ini:**")
st.caption("""
Laman ini berguna untuk kamu yang suka mencari referensi melalui banyak artikel yang ada di internet, 
tanpa mengorbankan waktu untuk membacanya satu per satu. File .txt yang kamu download, 
bisa kamu masukkan ke LLM AI (seperti ChatGPT, Gemini, Claude, dll) untuk menjelaskan ulang apa 
yang ada dalam referensi kamu tadi. Dengan itu, kamu bisa lebih mudah memahami referensi yang kamu pilih, 
tanpa mengorbankan banyak waktu dan bingung memahami isi bacaan.
""")
