import streamlit as st
import trafilatura
import cloudscraper

st.set_page_config(page_title="Kolektor Referensi", page_icon="📚")

st.title("📚 Kolektor Referensi by Agam Praminsya")
st.write("Tambahkan beberapa artikel, lalu download semuanya jadi satu file.")

# 1. Inisialisasi "Kantong Ajaib" (Session State)
if 'daftar_artikel' not in st.session_state:
    st.session_state['daftar_artikel'] = []

# Bagian Input
with st.expander("➕ Tambah Artikel Baru", expanded=True):
    nama_web = st.text_input("Nama Website", placeholder="Misal: Nature, BBC")
    url = st.text_input("Link Artikel", placeholder="https://...")
    
    if st.button("Tambahkan ke Daftar"):
        if nama_web and url:
            with st.spinner('Sedang mengambil data...'):
                try:
                    scraper = cloudscraper.create_scraper()
                    response = scraper.get(url)
                    if response.status_code == 200:
                        teks = trafilatura.extract(response.text)
                        if teks:
                            # Simpan ke dalam list
                            st.session_state['daftar_artikel'].append({
                                'nama': nama_web,
                                'isi': teks,
                                'url': url
                            })
                            st.success(f"✅ {nama_web} berhasil ditambahkan!")
                        else:
                            st.error("Gagal mengambil teks.")
                    else:
                        st.error(f"Error web: {response.status_code}")
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")
        else:
            st.warning("Isi nama dan link dulu ya!")

st.divider()

# 2. Menampilkan Daftar yang Sudah Terkumpul
if st.session_state['daftar_artikel']:
    st.subheader(f"🗂️ Daftar Referensi ({len(st.session_state['daftar_artikel'])} artikel)")
    
    # Membuat isi file gabungan
    file_gabungan = ""
    for item in st.session_state['daftar_artikel']:
        file_gabungan += f"Ini sumber dari {item['nama']}:\nURL: {item['url']}\n\n{item['isi']}\n\n"
        file_gabungan += "="*60 + "\n\n"
        st.text(f"• {item['nama']} ({item['url'][:30]}...)")

    # 3. Tombol Aksi untuk Semua Artikel
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            label="📥 Download Semua (.txt)",
            data=file_gabungan,
            file_name="Semua_Referensi.txt",
            mime="text/plain"
        )
    
    with col2:
        if st.button("🗑️ Kosongkan Daftar"):
            st.session_state['daftar_artikel'] = []
            st.rerun()
else:
    st.info("Belum ada artikel yang ditambahkan. Masukkan link di atas!")
