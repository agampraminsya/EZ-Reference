import streamlit as st
import trafilatura
import cloudscraper

# Pengaturan Tampilan Web
st.set_page_config(page_title="Pencabut Teks Artikel", page_icon="📝")

st.title("📝 Ekstraktor Artikel Referensi")
st.write("Gunakan alat ini untuk mengambil referensi tulisan IDN Times kamu.")

# Input User
nama_web = st.text_input("1. Nama Website", placeholder="Contoh: BBC Science")
url = st.text_input("2. Link Artikel", placeholder="https://...")

if st.button("Ambil Teks Utuh"):
    if nama_web and url:
        with st.spinner('Sedang memproses...'):
            try:
                scraper = cloudscraper.create_scraper()
                response = scraper.get(url)
                
                if response.status_code == 200:
                    hasil_teks = trafilatura.extract(response.text)
                    
                    if hasil_teks:
                        # Menampilkan hasil di web
                        st.subheader(f"Sumber: {nama_web}")
                        st.text_area("Hasil Ekstraksi:", hasil_teks, height=300)
                        
                        # Tombol Download (Sebagai pengganti simpan otomatis ke MNY.txt)
                        format_file = f"Ini sumber dari {nama_web}:\nURL: {url}\n\n{hasil_teks}\n"
                        st.download_button(
                            label="📥 Download sebagai .txt",
                            data=format_file,
                            file_name=f"{nama_web}.txt",
                            mime="text/plain"
                        )
                    else:
                        st.error("Gagal mengambil teks. Website mungkin menggunakan format yang tidak terbaca.")
                else:
                    st.error(f"Gagal tembus proteksi. Error code: {response.status_code}")
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")
    else:
        st.warning("Mohon isi nama website dan link terlebih dahulu.")
