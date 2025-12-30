import streamlit as st
import trafilatura
import cloudscraper

# Pengaturan halaman agar nyaman di HP
st.set_page_config(page_title="Penyaring Teks Artikel", page_icon="📝")

st.title("📝 Ekstraktor Referensi Artikel by Agam Praminsya")
st.info("Format output akan otomatis disesuaikan untuk risetmu.")

# Dua input sesuai permintaanmu
nama_web = st.text_input("1. Masukkan Nama Website", placeholder="Misal: BBC, Nature, dsb")
url = st.text_input("2. Masukkan Link Artikel", placeholder="Tempel link https:// di sini")

if st.button("Proses Teks"):
    if nama_web and url:
        with st.spinner('Sedang mengambil teks...'):
            try:
                # Menggunakan cloudscraper agar tidak diblokir proteksi web
                scraper = cloudscraper.create_scraper()
                response = scraper.get(url)
                
                if response.status_code == 200:
                    hasil_teks = trafilatura.extract(response.text)
                    
                    if hasil_teks:
                        # MEMBUAT FORMAT SESUAI PERMINTAANMU
                        output_final = f"Ini sumber dari {nama_web}:\n\n{hasil_teks}\n\n"
                        output_final += "="*50 # Garis pembatas
                        
                        st.success(f"Berhasil mengekstrak dari {nama_web}!")
                        
                        # Menampilkan hasil di layar (bisa langsung di-copy)
                        st.subheader("Hasil (Siap Copy-Paste):")
                        st.text_area(label="Teks di bawah ini sudah sesuai format:", value=output_final, height=400)
                        
                        # Tombol download untuk jaga-jaga
                        st.download_button(
                            label="📥 Download Hasil sebagai .txt",
                            data=output_final,
                            file_name=f"Riset_{nama_web}.txt",
                            mime="text/plain"
                        )
                    else:
                        st.error("Teks tidak ditemukan. Coba link artikel lain.")
                else:
                    st.error(f"Gagal akses website. Kode Error: {response.status_code}")
            except Exception as e:
                st.error(f"Terjadi kesalahan teknis: {e}")
    else:
        st.warning("Pastikan Nama Web dan Link sudah diisi ya, Gam!")
