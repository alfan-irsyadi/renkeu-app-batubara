import streamlit as st
import pandas as pd
import requests
import urllib3
import io
from datetime import datetime

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Page config
st.set_page_config(
    page_title="ADK Tunjangan Kinerja",
    page_icon="🏢",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(to bottom right, #EFF6FF, #E0E7FF);
    }
    .stButton>button {
        width: 100%;
        background-color: #4F46E5;
        color: white;
        font-weight: bold;
        padding: 0.75rem;
        border-radius: 0.5rem;
    }
    .stButton>button:hover {
        background-color: #4338CA;
    }
    div[data-testid="stExpander"] {
        background-color: white;
        border-radius: 0.5rem;
        border: 1px solid #E5E7EB;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("🏢 Aplikasi ADK Tunjangan Kinerja")
st.markdown("**Ekstrak dan proses data tunjangan kinerja dari sistem Gaji Kemenkeu**")
st.markdown("---")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Konfigurasi")
    
    bearer = st.text_area(
        "Bearer Token *",
        height=150,
        help="Masukkan bearer token dari sistem Gaji Kemenkeu"
    )
    
    kdsatker = st.text_input(
        "Kode Satker *",
        value="681731",
        help="Kode satuan kerja"
    )
    
    kdanak = st.text_input(
        "Kode Anak *",
        value="P3",
        help="Kode anak satker"
    )
    
    start_tukin = st.number_input(
        "Mulai Tukin dibayar (bulan) *",
        help="Contoh: Tukin Januari 2025 dibayarkan bulan 2. Maka Input 2",
        value=2
    )
    
    end_tukin = st.number_input(
        "Terakhir Tukin dibayar (bulan) *",
        help="Contoh: Tukin Oktober 2025 dibayarkan bulan 11. Maka Input 11",
        value=11
    )
    
    cookies_session = st.text_input(
        "Cookie Session *",
        help="Cookie session dari browser"
    )
    
    st.markdown("---")
    
    st.info("""
    **📌 Catatan:**
    - Data diambil dari bulan 2-11 tahun 2025
    - Setiap pegawai = 12 baris data
    - Format: Rutin, THR, Gaji Ke-13
    """)

# Main content
if not bearer or not cookies_session:
    st.warning("⚠️ Silakan lengkapi Bearer Token dan Cookie Session di sidebar untuk memulai")
    st.info("""
    **Cara mendapatkan Bearer Token & Cookie:**
    1. Buka https://gaji.kemenkeu.go.id di browser
    2. Login ke sistem
    3. Buka Developer Tools (F12)
    4. Pergi ke tab Network
    5. Refresh halaman
    6. Cari request ke API, lihat di Headers:
       - Authorization: Bearer [token]
       - Cookie: cookiesession1=[value]
    """)
else:
    # Process button
    if st.button("🚀 Proses Data", type="primary"):
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Create session
            session = requests.Session()
            session.headers.update({
                "User-Agent": (
                    "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/142.0.0.0 Mobile Safari/537.36"
                )
            })
            
            # Set cookie
            session.cookies.set(
                "cookiesession1",
                cookies_session,
                domain="gaji.kemenkeu.go.id",
                path="/"
            )
            
            # Headers
            headers = {
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": "en-US,en;q=0.6",
                "Authorization": f"Bearer {bearer}",
                "Referer": "https://gaji.kemenkeu.go.id/pns/prosestukin",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
            }
            
            # Step 1: Get main data
            status_text.info("📥 Mengambil data tukin dari bulan 2-11...")
            progress_bar.progress(10)
            
            data = []
            for i in range(start_tukin, end_tukin+1):
                url = (
                    "https://gaji.kemenkeu.go.id/api/tukin/daftartukin"
                    f"?kdsatker={kdsatker}&kdanak={kdanak}&bulan={str(i).zfill(2)}&tahun=2025"
                )
                response = session.get(url, headers=headers, verify=False)
                
                if response.status_code == 200:
                    response_data = response.json().get('data', [])
                    data.extend(response_data)
                    status_text.info(f"📥 Mengambil data bulan {i}... ({len(data)} records)")
                else:
                    st.error(f"❌ Error pada bulan {i}: Status {response.status_code}")
                
                progress_bar.progress(10 + (i - 1) * 5)
            
            if not data:
                st.error("❌ Tidak ada data yang ditemukan!")
                st.stop()
            
            df = pd.DataFrame(data)
            df = df[df.nmstatus == 'Setuju Uang Makan/Lembur/Tukin - PPK']
            
            st.success(f"✅ Berhasil mengambil {len(df)} data tukin yang disetujui")
            progress_bar.progress(60)
            
            # Step 2: Get detail data
            status_text.info("📊 Mengambil detail pegawai...")
            
            data_excel = []
            total_ids = len(df.id)
            
            for idx, id_val in enumerate(df.id):
                url = f"https://gaji.kemenkeu.go.id/api/tukin/exceldetilpegawaitukin?id={id_val}&kdsatker={kdsatker}&jpns=4"
                response = session.get(url, headers=headers, verify=False)
                
                if response.status_code == 200:
                    detail_data = response.json().get('data', [])
                    data_excel.extend(detail_data)
                    status_text.info(f"📊 Memproses detail... {idx+1}/{total_ids}")
                else:
                    st.warning(f"⚠️ Gagal mengambil detail ID {id_val}")
                
                progress_bar.progress(60 + int((idx + 1) / total_ids * 20))
            
            if not data_excel:
                st.error("❌ Tidak ada detail data yang ditemukan!")
                st.stop()
            
            df_excel = pd.DataFrame(data_excel)
            df_excel = df_excel.sort_values(by='nama_pegawai')
            
            progress_bar.progress(80)
            status_text.info("⚙️ Memproses data sesuai template...")
            
            # Step 3: Process data with template
            df = df_excel.copy()
            
            # Convert to numeric
            cols_to_numeric = ['kotor', 'potongan', 'bersih', 'pajak', 'bulan_awal', 'bulan_akhir', 'jenis_tukin']
            for col in cols_to_numeric:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
            # Template structure
            template_structure = [
                {'bulan': 1, 'kode': 'rtn', 'nama': 'Rutin', 'order': 1},
                {'bulan': 2, 'kode': 'rtn', 'nama': 'Rutin', 'order': 2},
                {'bulan': 2, 'kode': 'thr', 'nama': 'THR', 'order': 3},
                {'bulan': 3, 'kode': 'rtn', 'nama': 'Rutin', 'order': 4},
                {'bulan': 4, 'kode': 'rtn', 'nama': 'Rutin', 'order': 5},
                {'bulan': 5, 'kode': 'rtn', 'nama': 'Rutin', 'order': 6},
                {'bulan': 5, 'kode': 'k13', 'nama': 'Bulan Ke-13', 'order': 7},
                {'bulan': 6, 'kode': 'rtn', 'nama': 'Rutin', 'order': 8},
                {'bulan': 7, 'kode': 'rtn', 'nama': 'Rutin', 'order': 9},
                {'bulan': 8, 'kode': 'rtn', 'nama': 'Rutin', 'order': 10},
                {'bulan': 9, 'kode': 'rtn', 'nama': 'Rutin', 'order': 11},
                {'bulan': 10, 'kode': 'rtn', 'nama': 'Rutin', 'order': 12}
            ]
            
            # Process each employee
            unique_employees = df[['kdsatker', 'nip', 'nama_pegawai']].drop_duplicates()
            final_rows = []
            
            for _, emp in unique_employees.iterrows():
                nip = emp['nip']
                nama = emp['nama_pegawai']
                kdsatker_emp = emp['kdsatker']
                
                emp_data = df[df['nip'] == nip]
                filled_data = {}
                
                for _, row in emp_data.iterrows():
                    jenis_tukin = str(int(row['jenis_tukin']))
                    start = int(row['bulan_awal'])
                    end = int(row['bulan_akhir'])
                    
                    durasi = end - start + 1
                    if durasi < 1: durasi = 1
                    
                    vals = {
                        'kotor': row['kotor'],
                        'potongan': row['potongan'],
                        'bersih': row['bersih'],
                        'pajak': row['pajak']
                    }
                    
                    if jenis_tukin == '2':  # RUTIN
                        for b in range(start, end + 1):
                            if 1 <= b <= 10:
                                filled_data[(b, 'rtn')] = {
                                    'kotor': vals['kotor'] / durasi,
                                    'potongan': vals['potongan'] / durasi,
                                    'bersih': vals['bersih'] / durasi,
                                    'pajak': vals['pajak'] / durasi
                                }
                    elif jenis_tukin == '4':  # THR
                        filled_data[(2, 'thr')] = vals
                    elif jenis_tukin == '5':  # K13
                        filled_data[(5, 'k13')] = vals
                
                # Apply template
                for item in template_structure:
                    bulan = item['bulan']
                    kode = item['kode']
                    key = (bulan, kode)
                    
                    row_res = {
                        'kdsatker': kdsatker_emp,
                        'nip': nip,
                        'nama_pegawai': nama,
                        'bulan': bulan,
                        'kode_jenis_bayar': kode,
                        'jenis_bayar': item['nama'],
                        'sort_order': item['order']
                    }
                    
                    if key in filled_data:
                        data_uang = filled_data[key]
                        row_res['kotor'] = data_uang['kotor']
                        row_res['potongan'] = data_uang['potongan']
                        row_res['bersih'] = data_uang['bersih']
                        row_res['pajak'] = data_uang['pajak']
                    else:
                        row_res['kotor'] = 0
                        row_res['potongan'] = 0
                        row_res['bersih'] = 0
                        row_res['pajak'] = 0
                    
                    final_rows.append(row_res)
            
            # Create final dataframe
            df_final = pd.DataFrame(final_rows)
            
            # Format numbers
            cols_uang = ['kotor', 'potongan', 'bersih', 'pajak']
            df_final[cols_uang] = df_final[cols_uang].round(0).astype(int)
            
            # Sort
            df_final = df_final.sort_values(by=['nip', 'sort_order'], ascending=[True, True])
            df_view = df_final.drop(columns=['sort_order'])
            
            progress_bar.progress(100)
            status_text.success("✅ Proses selesai!")
            
            # Display results
            st.success("🎉 Data berhasil diproses!")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Pegawai", len(unique_employees))
            with col2:
                st.metric("Total Baris Data", len(df_view))
            with col3:
                st.metric("Bulan Diproses", "2-11 (2025)")
            
            # Show preview
            with st.expander("👁️ Preview Data (20 baris pertama)", expanded=True):
                st.dataframe(df_view.head(20), use_container_width=True)
            
            # Download button
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_view.to_excel(writer, index=False, sheet_name='Data ADK')
            
            excel_data = output.getvalue()
            filename = f"{kdsatker}_{kdanak}_Data_ADK_Penghasilan_Lain_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            
            st.download_button(
                label="📥 Download Excel",
                data=excel_data,
                file_name=filename,
                mime="application/vnd.openxmlsx-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
            
        except Exception as e:
            st.error(f"❌ Terjadi kesalahan: {str(e)}")
            st.exception(e)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6B7280; padding: 1rem;'>
    <p>© 2025 Aplikasi ADK Tunjangan Kinerja | Kemenkeu</p>
</div>
""", unsafe_allow_html=True)