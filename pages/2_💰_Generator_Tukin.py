import streamlit as st
import pandas as pd
import numpy as np
import datetime
from dateutil import relativedelta
import base64
import io

# Konfigurasi halaman
st.set_page_config(
    page_title="Sistem Generator PNS",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS kustom untuk desain minimalis
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Gaya global */
    .main {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #ff6b6b 0%, #ffa500 100%);
        min-height: 100vh;
    }
    
    .stApp {
        background: transparent;
    }
    
    /* Gaya header */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .main-header h1 {
        color: white;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.8);
        font-size: 1.1rem;
        font-weight: 400;
    }
    
    /* Gaya kartu */
    .card {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 1.5rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
    }
    
    /* Kartu metrik */
    .metric-card {
        background: linear-gradient(135deg, #ff6b6b 0%, #ffa500 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
    }
    
    .metric-card h3 {
        margin: 0;
        font-size: 2rem;
        font-weight: 600;
    }
    
    .metric-card p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
        font-weight: 400;
    }
    
    /* Gaya tombol */
    .stButton > button {
        background: linear-gradient(135deg, #ff6b6b 0%, #ffa500 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.6);
    }
    
    /* Gaya periode card */
    .periode-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(79, 172, 254, 0.3);
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #ff6b6b 0%, #ffa500 100%);
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

def get_month_name(month_num):
    """Konversi nomor bulan ke nama bulan"""
    months = {
        1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
        5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
        9: "September", 10: "Oktober", 11: "November", 12: "Desember"
    }
    return months.get(month_num, "Tidak Diketahui")

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>💰 Generator Tukin PNS</h1>
        <p>Sistem Otomatis Generator Tunjangan Kinerja PNS</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar untuk konfigurasi
    with st.sidebar:
        st.markdown("### ⚙️ Konfigurasi Tukin")
        
        # Pemilihan fungsi
        fungsi = st.selectbox(
            "Pilih Fungsi",
            ["AGAMA", "PENDIDIKAN"],
            index=0,
            help="Pilih jenis fungsi untuk menentukan kode anak"
        )
        
        kdanak = '03' if fungsi == 'AGAMA' else '02'
        
        st.info(f"Kode Anak: {kdanak}")
        
        st.markdown("---")
        
        # Periode saat ini
        periode_sekarang = datetime.date.today()
        bulan_ini = periode_sekarang.month
        tahun_ini = periode_sekarang.year
        
        st.markdown("### 📅 Periode Saat Ini")
        st.markdown(f"**{get_month_name(bulan_ini)} {tahun_ini}**")
        
        st.markdown("---")
        
        # Konfigurasi pencairan
        st.markdown("### 🗓️ Periode Pencairan")
        
        list_bulan = [1,2,3,4,5,6,7,8,9,10,11,12]
        list_tahun = list(range(2025,2000,-1))
        
        bulan_awal_pencairan = st.selectbox(
            "Bulan Awal Pencairan",
            list_bulan,
            index=bulan_ini-1,
            format_func=lambda x: f"{x:02d} - {get_month_name(x)}"
        )
        
        tahun_awal_pencairan = st.selectbox(
            "Tahun Awal Pencairan",
            list_tahun,
            index=0
        )
        
        apakah_bulan_yang_sama = st.checkbox(
            "Pencairan Bulan yang Sama",
            value=True,
            help="Centang jika pencairan hanya untuk satu bulan"
        )
        
        if apakah_bulan_yang_sama:
            bulan_akhir_pencairan = bulan_awal_pencairan
            tahun_akhir_pencairan = tahun_awal_pencairan
            filename = f'tukin_{kdanak}_{str(bulan_awal_pencairan).zfill(2)}{tahun_awal_pencairan}.txt'
        else:
            st.markdown("#### Periode Akhir")
            
            # Filter bulan dan tahun akhir
            list_bulan_akhir = [i for i in list_bulan if i >= bulan_awal_pencairan]
            list_tahun_akhir = [i for i in list_tahun if i >= tahun_awal_pencairan]
            
            bulan_akhir_pencairan = st.selectbox(
                "Bulan Akhir Pencairan",
                list_bulan_akhir,
                index=0,
                format_func=lambda x: f"{x:02d} - {get_month_name(x)}"
            )
            
            tahun_akhir_pencairan = st.selectbox(
                "Tahun Akhir Pencairan",
                list_tahun_akhir,
                index=0
            )
            
            filename = f'tukin_{kdanak}_{str(bulan_awal_pencairan).zfill(2)}{tahun_awal_pencairan}_{str(bulan_akhir_pencairan).zfill(2)}{tahun_akhir_pencairan}.txt'
    
    # Area konten utama
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📁 Upload File Tukin")
        st.markdown("Upload file Excel yang berisi data Tukin PNS")
        
        uploaded_tukin_file = st.file_uploader(
            "Pilih file Excel Tukin",
            type=['xlsx', 'xls'],
            help="File Excel dengan sheet 'LUAR_KANTORKU'"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📊 Upload Database PNS")
        st.markdown("Upload file CSV database PNS")
        
        uploaded_db_file = st.file_uploader(
            "Pilih file CSV Database PNS",
            type=['csv'],
            help="File CSV dengan kolom 'nip' dan 'kdanak'"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📋 Informasi Konfigurasi")
        st.write(f"**Fungsi:** {fungsi}")
        st.write(f"**Kode Anak:** {kdanak}")
        st.write(f"**File Output:** {filename}")
        
        # Tampilkan periode
        st.markdown('<div class="periode-card">', unsafe_allow_html=True)
        st.markdown("**Periode Pencairan:**")
        if apakah_bulan_yang_sama:
            st.markdown(f"{get_month_name(bulan_awal_pencairan)} {tahun_awal_pencairan}")
        else:
            st.markdown(f"{get_month_name(bulan_awal_pencairan)} {tahun_awal_pencairan} - {get_month_name(bulan_akhir_pencairan)} {tahun_akhir_pencairan}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Proses data jika kedua file telah diupload
    if uploaded_tukin_file is not None and uploaded_db_file is not None:
        try:
            # Baca data
            with st.spinner("Membaca file..."):
                df_tukin = pd.read_excel(
                    uploaded_tukin_file, 
                    sheet_name='LUAR_KANTORKU',
                    header=None, 
                    dtype=str
                )
                
                db_pns = pd.read_csv(uploaded_db_file, dtype='string')
            
            # Tampilkan preview data
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### 👀 Preview Data Tukin")
            st.dataframe(df_tukin.head(), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### 👥 Preview Database PNS")
            st.dataframe(db_pns.head(), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Analytics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f'<div class="metric-card"><h3>{len(df_tukin)}</h3><p>Total Data Tukin</p></div>', 
                           unsafe_allow_html=True)
            
            with col2:
                st.markdown(f'<div class="metric-card"><h3>{len(db_pns)}</h3><p>Total Database PNS</p></div>', 
                           unsafe_allow_html=True)
            
            with col3:
                agama_count = len(db_pns[db_pns['kdanak'] == '03']) if 'kdanak' in db_pns.columns else 0
                st.markdown(f'<div class="metric-card"><h3>{agama_count}</h3><p>PNS Agama</p></div>', 
                           unsafe_allow_html=True)
            
            with col4:
                pendidikan_count = len(db_pns[db_pns['kdanak'] == '02']) if 'kdanak' in db_pns.columns else 0
                st.markdown(f'<div class="metric-card"><h3>{pendidikan_count}</h3><p>PNS Pendidikan</p></div>', 
                           unsafe_allow_html=True)
            
            # Tombol proses
            if st.button("🚀 Generate Data Tukin", type="primary"):
                with st.spinner("Memproses data Tukin..."):
                    progress_bar = st.progress(0)
                    
                    # Update progress
                    progress_bar.progress(0.2)
                    
                    # Update kolom periode
                    df_tukin.iloc[:, 1] = str(bulan_ini).zfill(2)
                    df_tukin.iloc[:, 2] = str(tahun_ini).zfill(4)
                    df_tukin.iloc[:, 14] = str(bulan_awal_pencairan).zfill(2)
                    df_tukin.iloc[:, 15] = str(tahun_awal_pencairan).zfill(4)
                    df_tukin.iloc[:, 16] = str(bulan_akhir_pencairan).zfill(2)
                    df_tukin.iloc[:, 17] = str(tahun_akhir_pencairan).zfill(4)
                    
                    progress_bar.progress(0.5)
                    
                    # Merge dengan database PNS
                    if 'nip' in db_pns.columns and 'kdanak' in db_pns.columns:
                        df_merge = df_tukin.merge(
                            db_pns[['nip', 'kdanak']], 
                            left_on=3, 
                            right_on='nip', 
                            how='left'
                        )
                        
                        progress_bar.progress(0.7)
                        
                        # Filter berdasarkan kdanak
                        df_result = df_merge[df_merge['kdanak'] == kdanak].iloc[:, :-2]
                        
                        progress_bar.progress(1.0)
                        
                        if len(df_result) > 0:
                            st.success(f"✅ Berhasil memproses {len(df_result)} data Tukin untuk fungsi {fungsi}!")
                            
                            # Tampilkan hasil
                            st.markdown('<div class="card">', unsafe_allow_html=True)
                            st.markdown("### 📊 Hasil Data Tukin")
                            st.dataframe(df_result.head(10), use_container_width=True)
                            
                            if len(df_result) > 10:
                                st.info(f"Menampilkan 10 data pertama dari {len(df_result)} total data")
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                            # Download
                            st.markdown('<div class="card">', unsafe_allow_html=True)
                            st.markdown("### 💾 Download Hasil")
                            
                            # Konversi ke format tab-separated
                            output = io.StringIO()
                            df_result.to_csv(output, sep='\t', header=False, index=False)
                            result_data = output.getvalue()
                            
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.download_button(
                                    label="📥 Download File Tukin (.txt)",
                                    data=result_data,
                                    file_name=filename,
                                    mime='text/plain'
                                )
                            
                            with col2:
                                # Download as CSV for backup
                                csv_data = df_result.to_csv(index=False)
                                st.download_button(
                                    label="📊 Download Backup (.csv)",
                                    data=csv_data,
                                    file_name=filename.replace('.txt', '.csv'),
                                    mime='text/csv'
                                )
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                        else:
                            st.warning(f"⚠️ Tidak ditemukan data untuk fungsi {fungsi} dengan kode anak {kdanak}")
                    else:
                        st.error("❌ Database PNS harus memiliki kolom 'nip' dan 'kdanak'")
                        
        except Exception as e:
            st.error(f"❌ Error memproses file: {str(e)}")
            st.info("Pastikan file Excel memiliki sheet 'LUAR_KANTORKU' dan file CSV memiliki struktur yang benar")
    
    else:
        # Instruksi
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📖 Petunjuk Penggunaan Generator Tukin")
        st.markdown("""
        1. **Pilih Fungsi**: Pilih antara "AGAMA" atau "PENDIDIKAN" di sidebar
        2. **Atur Periode**: Tentukan periode pencairan tukin
        3. **Upload File Tukin**: Upload file Excel dengan sheet 'LUAR_KANTORKU'
        4. **Upload Database PNS**: Upload file CSV dengan kolom 'nip' dan 'kdanak'
        5. **Generate**: Klik tombol generate untuk memproses data
        6. **Download**: Unduh hasil dalam format .txt atau .csv
        
        **Struktur File yang Diperlukan:**
        - **File Excel Tukin**: Harus memiliki sheet bernama 'LUAR_KANTORKU'
        - **File CSV Database**: Harus memiliki kolom 'nip' dan 'kdanak'
        
        **Kode Anak:**
        - AGAMA: 03
        - PENDIDIKAN: 02
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: rgba(255,255,255,0.7); padding: 1rem;'>"
        "Generator Tukin PNS v1.0 | Dibuat dengan ❤️ menggunakan Streamlit"
        "</div>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()