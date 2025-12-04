import streamlit as st
import pandas as pd
import numpy as np
import re
import io
from datetime import datetime
import base64
import requests

# Konfigurasi halaman
st.set_page_config(
    page_title="Generator Rekap Uang Makan",
    page_icon="🍽️",
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
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(79, 172, 254, 0.3);
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
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Gaya sidebar */
    .sidebar .sidebar-content {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 1rem;
    }
    
    /* File uploader */
    .stFileUploader {
        border: 2px dashed rgba(102, 126, 234, 0.5);
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        background: rgba(255, 255, 255, 0.05);
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        border-color: rgba(102, 126, 234, 0.8);
        background: rgba(255, 255, 255, 0.1);
    }
    
    /* Pesan sukses/error */
    .stSuccess {
        background: rgba(76, 175, 80, 0.1);
        border: 1px solid rgba(76, 175, 80, 0.3);
        border-radius: 8px;
    }
    
    .stError {
        background: rgba(244, 67, 54, 0.1);
        border: 1px solid rgba(244, 67, 54, 0.3);
        border-radius: 8px;
    }
    
    /* Styling DataFrame */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

def create_download_link(df, filename, link_text):
    """Membuat tautan unduhan untuk DataFrame sebagai CSV"""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}" class="download-link">{link_text}</a>'
    return href

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🍽️ Generator Rekap Uang Makan</h1>
        <p>Buat laporan rekap uang makan dengan mudah dan cepat</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar untuk konfigurasi
    with st.sidebar:
        st.markdown("### ⚙️ Konfigurasi")
                
        st.markdown("#### 🔐 Autentikasi API Kemenkeu")
        cookie_input = st.text_input("Cookie (cookiesession1)", type="password")
        bearer_token = st.text_area("Bearer Token", height=100)
        
        # Pemilihan jenis fungsi
        fungsi = st.selectbox(
            "Pilih Jenis Fungsi",
            ["agama", "pendidikan", "pppk"],
            index=0,
            help="Pilih jenis fungsi pegawai"
        )
        
        # Konfigurasi hari kerja
        st.markdown("#### 📅 Konfigurasi Hari Kerja")
        hari_kerja_guru = st.number_input("Hari Kerja Guru", min_value=1, max_value=31, value=16)
        hari_kerja_sekolah = st.number_input("Hari Kerja Pegawai Sekolah", min_value=1, max_value=31, value=27)
        hari_kerja_kantor = st.number_input("Hari Kerja Pegawai Kantor", min_value=1, max_value=31, value=23)
        
        st.markdown("---")
        st.markdown("### 📊 Analitik")
        show_analytics = st.checkbox("Tampilkan Dashboard Analitik", value=True)
        
    # Area konten utama
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📁 Unggah File")
        st.markdown("Unggah file Excel yang berisi data kehadiran pegawai")
        
        uploaded_file = st.file_uploader(
            "Pilih file Excel",
            type=['xlsx', 'xls'],
            help="Unggah file Excel uang makan dengan struktur sheet yang sesuai"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    bulan=10
    tahun=2025
    if uploaded_file is not None:
        try:
            # Ekstrak bulan dari nama file
            filename = uploaded_file.name
            bulan_match = filename.split('_')
            if len(bulan_match) >= 3:
                bulan = bulan_match[2]
                tahun = bulan_match[3].split('.')[0]
            else:
                bulan = "TIDAK_DIKETAHUI"
            
            # Tampilkan info file
            with col2:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("### 📋 Informasi File")
                st.write(f"**Nama File:** {filename}")
                st.write(f"**Bulan:** {bulan}")
                st.write(f"**Fungsi:** {fungsi.upper()}")
                st.write(f"**Ukuran:** {uploaded_file.size / 1024:.1f} KB")
                st.markdown('</div>', unsafe_allow_html=True)
            sheet = {'agama':'PNS_AGAMA', 'pendidikan': 'PNS_PENDIDIKAN', 'pppk': 'ULP_PPPK'}
            # Proses data
            with st.spinner("Memproses data..."):
                sheet_name = sheet[fungsi]
                
                # Baca data pegawai
                pns_data = pd.read_excel(uploaded_file, sheet_name=sheet_name, dtype={'nip': 'string'})
                
                # Baca data kalender
                kalender_guru = pd.read_excel(uploaded_file, sheet_name='guru')
                kalender_sekolah = pd.read_excel(uploaded_file, sheet_name='pegawai_sekolah')
                kalender_kantor = pd.read_excel(uploaded_file, sheet_name='kantor')
                
                # Filter hanya hari kerja
                kalender_guru = kalender_guru[kalender_guru['jenis_hari'] == 'K']
                kalender_sekolah = kalender_sekolah[kalender_sekolah['jenis_hari'] == 'K']
                kalender_kantor = kalender_kantor[kalender_kantor['jenis_hari'] == 'K']
                
                # Buat dictionary kalender
                kalender = {
                    str(hari_kerja_guru): kalender_guru,
                    str(hari_kerja_sekolah): kalender_sekolah,
                    str(hari_kerja_kantor): kalender_kantor
                }
            
            # Tampilkan dashboard analitik
            if show_analytics:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("### 📊 Dashboard Analitik")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown(f'<div class="metric-card"><h3>{len(pns_data)}</h3><p>Total Pegawai</p></div>', 
                               unsafe_allow_html=True)
                
                with col2:
                    present_employees = len(pns_data[pns_data['Jumlah Hadir'] == pns_data['Hari efektif']])
                    st.markdown(f'<div class="metric-card"><h3>{present_employees}</h3><p>Hadir Penuh</p></div>', 
                               unsafe_allow_html=True)
                
                with col3:
                    absent_employees = len(pns_data[pns_data['Jumlah tidak hadir'] > 0])
                    st.markdown(f'<div class="metric-card"><h3>{absent_employees}</h3><p>Ada Ketidakhadiran</p></div>', 
                               unsafe_allow_html=True)
                
                with col4:
                    total_absences = pns_data['Jumlah tidak hadir'].sum()
                    st.markdown(f'<div class="metric-card"><h3>{total_absences}</h3><p>Total Hari Tidak Hadir</p></div>', 
                               unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Tampilkan data pegawai
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### 👥 Pratinjau Data Pegawai")
            
            # Tambahkan fungsi pencarian
            search_term = st.text_input("🔍 Cari pegawai berdasarkan nama atau NIP", "")
            if search_term:
                filtered_data = pns_data[
                    pns_data['nama'].str.contains(search_term, case=False, na=False) |
                    pns_data['nip'].str.contains(search_term, case=False, na=False)
                ]
            else:
                filtered_data = pns_data
            
            st.dataframe(
                filtered_data,
                use_container_width=True,
                height=400
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Proses data uang makan
            if st.button("🚀 Generate Data Uang Makan", type="primary"):
                with st.spinner("Membuat rekap uang makan..."):
                    progress_bar = st.progress(0)
                    
                    data = []
                    total_employees = len(pns_data)
                    
                    for idx, karyawan in enumerate(pns_data.values):
                        # Update progress
                        progress_bar.progress((idx + 1) / total_employees)
                        
                        nip = karyawan[3]
                        hari_efektif = str(karyawan[6])
                        jumlah_hadir = karyawan[7]
                        jumlah_absen = karyawan[8]
                        hari_kerja = []
                        keterangan = re.sub(r"[^0-9\-.,]", "", str(karyawan[9]))
                        
                        # Parse tanggal tidak hadir
                        if "," in keterangan:
                            keterangan = keterangan.split(",")
                            for i in keterangan:
                                if i.strip():
                                    hari_kerja.append(int(i))
                        elif "-" in keterangan:
                            keterangan = keterangan.split("-")
                            if len(keterangan) == 2:
                                for i in range(int(keterangan[0]), int(keterangan[1]) + 1):
                                    hari_kerja.append(i)
                        elif "." in keterangan:
                            hari_kerja = keterangan.split(".")
                            for i in range(len(hari_kerja)):
                                if hari_kerja[i].strip():
                                    hari_kerja[i] = int(hari_kerja[i])
                        elif keterangan == '':
                            pass
                        else:
                            if keterangan.strip():
                                hari_kerja = [int(keterangan)]
                        
                        # Generate data untuk hari kerja
                        if hari_efektif in kalender.keys():
                            for kalender_hari in kalender[hari_efektif].values:
                                if kalender_hari[0] not in hari_kerja or hari_kerja == []:
                                    data.append([nip, f"2025-{bulan}-{str(kalender_hari[0]).zfill(2)}"])
                    
                    progress_bar.progress(1.0)
                
                # Tampilkan hasil
                if data:
                    st.success(f"✅ Berhasil membuat {len(data)} record uang makan!")
                    
                    # Buat DataFrame
                    result_df = pd.DataFrame(data, columns=['nip', 'tanggal'])
                    
                    # Tampilkan ringkasan per pegawai
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.markdown("### 📋 Ringkasan Uang Makan")
                    
                    summary_df = result_df.groupby('nip').agg({'tanggal': 'count'}).reset_index()
                    summary_df.columns = ['NIP', 'Hari Uang Makan']
                    
                    # Gabungkan dengan nama pegawai
                    summary_with_names = summary_df.merge(
                        pns_data[['nip', 'nama', 'golongan']], 
                        left_on='NIP', 
                        right_on='nip', 
                        how='left'
                    )[['NIP', 'nama', 'golongan', 'Hari Uang Makan']]
                    summary_with_names.columns = ['NIP', 'Nama Pegawai', 'Golongan', 'Hari Uang Makan']

                    # Tambahkan logika uang makan per orang & pajak
                    summary_with_names['Golongan Utama'] = summary_with_names['Golongan'].apply(lambda x: str(x).split('/')[0] if pd.notnull(x) else '')

                    uang_makan_map = {'IV': 41000, 'III': 37000, 'II': 35000}
                    pajak_map = {'IV': 0.15, 'III': 0.05, 'II': 0.0}

                    summary_with_names['Uang Makan Per Orang'] = summary_with_names['Golongan Utama'].map(uang_makan_map).fillna(0).astype(int)
                    summary_with_names['Pajak (%)'] = summary_with_names['Golongan Utama'].map(pajak_map).fillna(0) * 100
                    summary_with_names['Total Kotor'] = summary_with_names['Hari Uang Makan'] * summary_with_names['Uang Makan Per Orang']
                    summary_with_names['Total Bersih'] = summary_with_names['Total Kotor'] * (1 - summary_with_names['Golongan Utama'].map(pajak_map).fillna(0))

                    # Urutkan kolom agar rapi
                    summary_with_names = summary_with_names[
                        ['NIP', 'Nama Pegawai', 'Golongan', 'Golongan Utama', 'Hari Uang Makan',
                        'Uang Makan Per Orang', 'Pajak (%)', 'Total Kotor', 'Total Bersih']
                    ]

                    # Tampilkan tabel hasil
                    st.dataframe(summary_with_names, use_container_width=True)
                    
                    st.dataframe(summary_with_names.groupby('Golongan Utama').agg({'NIP':'count', 'Hari Uang Makan':'sum', 'Uang Makan Per Orang': 'sum', 'Total Kotor':'sum', 'Total Bersih':'sum'}))
                    
                    st.text(f'Total Kotor: {summary_with_names['Total Kotor'].sum()}')
                    st.text(f'Total Bersih: {summary_with_names['Total Bersih'].sum()}')

                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Opsi unduhan
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.markdown("### 💾 Opsi Unduhan")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Unduh data mentah
                        csv_data = result_df.to_csv(sep="\t", header=False, index=False)
                        st.download_button(
                            label="📥 Unduh Data Mentah (.txt)",
                            data=csv_data,
                            file_name=f'ulp_{fungsi}_{bulan}.txt',
                            mime='text/plain'
                        )
                    
                    with col2:
                        # Unduh ringkasan
                        summary_csv = summary_with_names.to_csv(index=False)
                        st.download_button(
                            label="📊 Unduh Ringkasan (.csv)",
                            data=summary_csv,
                            file_name=f'ringkasan_{fungsi}_{bulan}.csv',
                            mime='text/csv'
                        )
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.warning("⚠️ Tidak ada data uang makan yang dihasilkan. Silakan periksa file input Anda.")
            
            if st.button("📤 Kirim Data ke API Kemenkeu", type="primary"):
                if not cookie_input or not bearer_token:
                    st.error("⚠️ Harap masukkan cookie dan token terlebih dahulu.")
                else:
                    try:
                        headers = {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                                        "(KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
                            "Authorization": f"Bearer {bearer_token}",
                            "Referer": "https://gaji.kemenkeu.go.id/pns/yulian",
                            "Origin": "https://gaji.kemenkeu.go.id",
                        }
                        cookies = {"cookiesession1": cookie_input}                        

                        st.info("🔄 Mengambil data dari endpoint /tayang...")
                        tayang_url = f"https://gaji.kemenkeu.go.id/api/setharikerja/tayang?tahun={tahun}"
                        tayang_res = requests.get(tayang_url, headers=headers, cookies=cookies)
                        
                        if tayang_res.status_code != 200:
                            st.error(f"Gagal mengambil /tayang: {tayang_res.status_code}")
                            st.stop()

                        tayang_data = tayang_res.json()
                        if not tayang_data.get("data"):
                            st.error("Data /tayang kosong atau tidak sesuai format.")
                            st.stop()

                        # Buat dictionary {tgyulian: id}
                        id_lookup = {item["tgyulian"]: item["id"] for item in tayang_data["data"] if "tgyulian" in item}
                        kdyulian_lookup = {item["tgyulian"]: item["kdyulian"] for item in tayang_data["data"] if "kdyulian" in item}
                        print(kdyulian_lookup)

                        st.success(f"✅ Berhasil mengambil {len(id_lookup)} data dari /tayang")

                        # Proses pengiriman
                        st.info("🚀 Mengirim data ke endpoint /simpan ...")
                        progress_bar = st.progress(0)
                        results = []

                        kalender_sekolah = pd.read_excel(uploaded_file, sheet_name='pegawai_sekolah')
                        total = len(kalender_sekolah)
                        base_url = f"https://gaji.kemenkeu.go.id/api/setharikerja/simpan?tahun={tahun}&apa=2"
                        for i, row in kalender_sekolah.iterrows():
                            print(i, total)
                            try:
                                tanggal_int = i+1
                                tgyulian = f"{tahun}-{int(bulan):02d}-{tanggal_int:02d}"
                                
                                # Ambil id dari hasil tayang
                                id_value = id_lookup.get(tgyulian)
                                kdyulian_value = kdyulian_lookup.get(tgyulian)
                                
                                if not id_value:
                                    results.append({
                                        "tanggal": tgyulian,
                                        "jenis_hari": row["jenis_hari"],
                                        "status": "❌ ID tidak ditemukan di /tayang",
                                        "response": ""
                                    })
                                    
                                    progress_bar.progress((i+1) / total)
                                    continue

                                payload = {
                                    "id": id_value,
                                    "kdsatker": "681731",
                                    "tahun": str(tahun),
                                    "tgyulian": tgyulian,
                                    "kdyulian": kdyulian_value,
                                    "nmhari": "",
                                    "kdlibur": row["jenis_hari"],
                                    "ketlibur": "",
                                    "tgrekam": "",
                                    "rekam": 2
                                }
                                print(payload)
                                simpan_res = requests.post(base_url, headers=headers, cookies=cookies, json=payload)
                                status = "✅" if simpan_res.status_code == 200 else f"❌ ({simpan_res.status_code})"
                                results.append({
                                    "tanggal": tgyulian,
                                    "jenis_hari": row["jenis_hari"],
                                    "status": status,
                                    "response": simpan_res.text[:100]
                                })
                            except Exception as e:
                                results.append({
                                    "tanggal": row.get("tanggal", ""),
                                    "jenis_hari": row.get("jenis_hari", ""),
                                    "status": "❌ Error",
                                    "response": str(e)
                                })
                            progress_bar.progress((i+1) / total)

                        st.success("✅ Proses pengiriman selesai!")
                        result_df = pd.DataFrame(results)
                        st.dataframe(result_df, use_container_width=True)

                    except Exception as e:
                        st.error(f"Terjadi kesalahan: {str(e)}")
            
            # Bagian validasi
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### ✅ Validasi Data")
            
            # Periksa pegawai dengan ketidakcocokan
            discrepancies = pns_data[pns_data['Jumlah Hadir'] != pns_data['Hari efektif']]
            
            if len(discrepancies) > 0:
                st.warning(f"Ditemukan {len(discrepancies)} pegawai dengan ketidakcocokan kehadiran:")
                st.dataframe(
                    discrepancies[['nip', 'nama', 'Hari efektif', 'Jumlah Hadir', 'Jumlah tidak hadir', 'Tanggal Tidak Hadir']],
                    use_container_width=True
                )
            else:
                st.success("✅ Semua data kehadiran pegawai sudah konsisten!")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ Error memproses file: {str(e)}")
            st.info("Pastikan file Excel Anda memiliki struktur yang benar dengan sheet yang diperlukan.")
    
    else:
        # Instruksi ketika tidak ada file yang diunggah
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📖 Petunjuk Penggunaan")
        st.markdown("""
        1. **Unggah File Excel**: Pilih file Excel uang makan yang berisi data pegawai
        2. **Konfigurasi Pengaturan**: Sesuaikan hari kerja untuk berbagai jenis pegawai di sidebar
        3. **Tinjau Data**: Periksa pratinjau data pegawai dan dashboard analitik
        4. **Generate Laporan**: Klik tombol generate untuk memproses data uang makan
        5. **Unduh**: Dapatkan hasil dalam format data mentah dan ringkasan
        
        **Sheet Excel yang Diperlukan:**
        - `PNS_AGAMA` atau `PNS_PENDIDIKAN` (data pegawai)
        - `guru` (kalender guru)
        - `pegawai_sekolah` (kalender pegawai sekolah)  
        - `kantor` (kalender pegawai kantor)
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: rgba(255,255,255,0.7); padding: 1rem;'>"
        "Dibuat dengan ❤️ menggunakan Streamlit | Generator Rekap Uang Makan v1.0"
        "</div>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()