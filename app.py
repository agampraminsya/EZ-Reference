import streamlit as st
import trafilatura
import cloudscraper
import streamlit.components.v1 as components

st.set_page_config(page_title="EZ-Reference", page_icon="📝")

st.title("📝 EZ-Reference: Multi-Source Collector")
st.caption(f"EZ-Reference: Partner resetmu | by @denmasagam v1.0")

if 'daftar_artikel' not in st.session_state:
    st.session_state['daftar_artikel'] = []

# --- FORM INPUT ---
with st.form(key='input_form', clear_on_submit=True):
    st.subheader("➕ Tambah Sumber Baru")
    nama_web = st.text_input("Nama Website (Misal: Nature, BBC, Kompas)")
    url = st.text_input("Link Artikel")
    submit_button = st.form_submit_button(label="Tambahkan ke Daftar")

    if submit_button:
        if nama_web and url:
            with st.spinner('Sabar yaa, masih diproses.'):
                try:
                    scraper = cloudscraper.create_scraper()
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
                            st.toast(f"✅ {nama_web} berhasil dikoleksi!", icon="🚀")
                        else:
                            st.error("Teks tidak terbaca, web ini memiliki sistem pengaman tertentu. Coba pilih web lain.")
                    else:
                        st.error(f"Status {response.status_code}: Website ini memblokir akses kami, mohon maaf ya. Coba pilih web lain.")
                except Exception as e:
                    st.error(f"Kesalahan teknis: {e}")
        else:
            st.warning("Data harus diisi lengkap ya!")

# --- MANAJEMEN DAFTAR & OUTPUT ---
if st.session_state['daftar_artikel']:
    st.divider()
    st.subheader(f"🗂️ Koleksi Riset ({len(st.session_state['daftar_artikel'])} Sumber)")
    
    file_gabungan = ""
    for index, item in enumerate(st.session_state['daftar_artikel']):
        c_info, c_del = st.columns([0.8, 0.2])
        with c_info:
            st.write(f"**{index+1}. {item['nama']}**")
            st.caption(item['url'])
        with c_del:
            if st.button("Hapus", key=f"del_{index}"):
                st.session_state['daftar_artikel'].pop(index)
                st.rerun()
        
        file_gabungan += f"Ini sumber dari {item['nama']}:\nURL: {item['url']}\n\n{item['isi']}\n\n"
        file_gabungan += "="*60 + "\n\n"

    # --- KOTAKAN HASIL & TOMBOL COPY ---
    st.subheader("Hasil Copy-an")
    
    # Tombol Copy Menggunakan JavaScript
    # Link Streamlit Cloud sudah otomatis HTTPS, jadi fitur clipboard ini akan jalan.
    copy_code = f"""
    <script>
    function copyToClipboard() {{
        const text = `{file_gabungan}`;
        navigator.clipboard.writeText(text).then(() => {{
            alert('Teks berhasil disalin ke Clipboard!');
        }});
    }}
    </script>
    <button onclick="copyToClipboard()" style="
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 16px;
        width: 100%;
        margin-bottom: 10px;
    ">📋 Copy to Clipboard (Otomatis)</button>
    """
    components.html(copy_code, height=60)

    st.text_area(
        label="Hasil Teks (Visualisasi):", 
        value=file_gabungan, 
        height=300
    )

    st.write("---")
    col_dl, col_clr = st.columns(2)
    with col_dl:
        st.download_button(
            label="📥 Download File .txt", 
            data=file_gabungan, 
            file_name="EZ_Reference_Riset.txt"
        )
    with col_clr:
        if st.button("🗑️ Kosongkan Semua"):
            st.session_state['daftar_artikel'] = []
            st.rerun()

# --- FOOTER ---
st.markdown("---")
st.info("**Tentang Laman Ini:**")
st.caption("Laman ini mempermudah pengumpulan referensi artikel internet tanpa membuang waktu membaca satu per satu. File .txt yang diunduh bisa dimasukkan ke LLM AI (ChatGPT, Gemini, Claude) untuk dijelaskan ulang.")
