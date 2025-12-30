import streamlit as st
import trafilatura
import cloudscraper

st.set_page_config(page_title="EZ-Reference", page_icon="📝")

st.title("📝 EZ-Reference by @denmasagam")

if 'daftar_artikel' not in st.session_state:
    st.session_state['daftar_artikel'] = []

# Form Input
with st.form(key='input_form', clear_on_submit=True):
    st.subheader("➕ Tambah Sumber Baru")
    nama_web = st.text_input("Nama Website")
    url = st.text_input("Link Artikel")
    submit_button = st.form_submit_button(label="Tambahkan ke Daftar")

    if submit_button:
        if nama_web and url:
            with st.spinner('Mengambil data...'):
                try:
                    scraper = cloudscraper.create_scraper()
                    response = scraper.get(url)
                    if response.status_code == 200:
                        teks = trafilatura.extract(response.text)
                        if teks:
                            st.session_state['daftar_artikel'].append({
                                'nama': nama_web,
                                'isi': teks,
                                'url': url
                            })
                            st.toast(f"✅ {nama_web} ditambahkan!")
                        else:
                            st.error("Gagal mengekstrak teks.")
                    else:
                        st.error(f"Error: {response.status_code}")
                except Exception as e:
                    st.error(f"Kesalahan: {e}")
        else:
            st.warning("Isi nama dan link dulu!")

# --- BAGIAN DAFTAR & HAPUS SALAH SATU ---
if st.session_state['daftar_artikel']:
    st.divider()
    st.subheader(f"🗂️ Daftar Koleksi ({len(st.session_state['daftar_artikel'])} Artikel)")
    
    # Menampilkan daftar dengan tombol hapus di sampingnya
    for index, item in enumerate(st.session_state['daftar_artikel']):
        col_teks, col_hapus = st.columns([0.85, 0.15])
        with col_teks:
            st.write(f"**{index + 1}. {item['nama']}**")
            st.caption(f"{item['url'][:60]}...")
        with col_hapus:
            # Tombol hapus spesifik berdasarkan index
            if st.button("❌", key=f"del_{index}"):
                st.session_state['daftar_artikel'].pop(index)
                st.rerun() # Refresh halaman agar daftar terupdate

    # Persiapan file gabungan untuk download
    file_gabungan = ""
    for item in st.session_state['daftar_artikel']:
        file_gabungan += f"Ini sumber dari {item['nama']}:\nURL: {item['url']}\n\n{item['isi']}\n\n"
        file_gabungan += "="*60 + "\n\n"

    st.write("---")
    col_dl, col_clr = st.columns(2)
    with col_dl:
        st.download_button(
            label="📥 Download Semua (.txt)",
            data=file_gabungan,
            file_name="Koleksi_Referensi.txt",
            mime="text/plain"
        )
    with col_clr:
        if st.button("🗑️ Hapus Semua Daftar"):
            st.session_state['daftar_artikel'] = []
            st.rerun()

# Deskripsi
st.markdown("---")
st.caption("Laman ini berguna untuk mengumpulkan banyak artikel menjadi satu file .txt agar mudah dianalisis oleh AI (ChatGPT, Gemini, dsb), menghemat waktu baca tanpa kehilangan esensi referensi.")
