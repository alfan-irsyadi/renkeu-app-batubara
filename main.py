import streamlit as st

# Konfigurasi halaman
st.set_page_config(
    page_title="RenkeuGen - Generator Data Rencana Keuangan PNS",
    page_icon="📊",
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
        background: linear-gradient(135deg, #2196F3 0%, #21CBF3 50%, #1976D2 100%);
        min-height: 100vh;
    }
    
    .stApp {
        background: transparent;
    }
    
    /* Gaya header */
    .main-header {
        text-align: center;
        padding: 3rem 0;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border-radius: 24px;
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .main-header h1 {
        color: white;
        font-weight: 700;
        font-size: 3.5rem;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
        letter-spacing: -0.02em;
    }
    
    .main-header .subtitle {
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.4rem;
        font-weight: 500;
        margin-bottom: 0.8rem;
        letter-spacing: 0.5px;
    }
    
    .main-header .description {
        color: rgba(255, 255, 255, 0.85);
        font-size: 1rem;
        font-weight: 400;
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.6;
    }
    
    /* Gaya kartu fitur */
    .feature-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 2rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #2196F3, #21CBF3);
    }
    
    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
    }
    
    .feature-card h3 {
        color: #1565C0;
        font-size: 1.8rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .feature-card p {
        color: #546E7A;
        font-size: 1.1rem;
        line-height: 1.6;
        margin-bottom: 1.5rem;
    }
    
    /* Icon styling */
    .feature-icon {
        font-size: 3.5rem;
        margin-bottom: 1.2rem;
        display: block;
        background: linear-gradient(45deg, #2196F3, #21CBF3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Gaya tombol navigasi */
    .stButton > button {
        background: linear-gradient(135deg, #2196F3 0%, #21CBF3 100%);
        color: white;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 25px;
        font-weight: 500;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(33, 150, 243, 0.4);
        letter-spacing: 0.3px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(33, 150, 243, 0.6);
    }
    
    /* Info section */
    .info-section {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 1.5rem;
    }
    
    .info-section h3 {
        color: #1565C0;
        font-weight: 600;
        margin-bottom: 1rem;
        font-size: 1.3rem;
    }
    
    .info-section p {
        color: #546E7A;
        line-height: 1.6;
        font-size: 0.95rem;
    }
    
    .info-section ul {
        color: #546E7A;
        line-height: 1.8;
    }
    
    .info-section li {
        margin-bottom: 0.5rem;
    }
    
    /* Stats cards */
    .stats-card {
        background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
        color: white;
        padding: 1.8rem;
        border-radius: 16px;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.3);
        transition: transform 0.3s ease;
    }
    
    .stats-card:hover {
        transform: translateY(-5px);
    }
    
    .stats-card h4 {
        margin: 0;
        font-size: 2rem;
        font-weight: 700;
    }
    
    .stats-card p {
        margin: 0.8rem 0 0 0;
        opacity: 0.9;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    /* Benefit cards */
    .benefit-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
        margin-bottom: 1rem;
        border-left: 4px solid #2196F3;
        transition: transform 0.3s ease;
    }
    
    .benefit-card:hover {
        transform: translateX(5px);
    }
    
    .benefit-card h4 {
        color: #1565C0;
        margin-bottom: 0.5rem;
        font-size: 1.1rem;
        font-weight: 600;
    }
    
    .benefit-card p {
        color: #546E7A;
        margin: 0;
        font-size: 0.9rem;
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header utama dengan branding yang kuat
    st.markdown("""
    <div class="main-header">
        <h1>📊 RenkeuGen</h1>
        <div class="subtitle">Generator Data Rencana Keuangan PNS</div>
        <div class="description">
            Platform utilitas terpadu untuk otomatisasi pembuatan data keuangan PNS. 
            Sederhanakan proses administrasi dan tingkatkan efisiensi kerja Anda.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Statistik sistem yang menarik
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="stats-card"><h4>99%</h4><p>Otomatisasi Proses</p></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="stats-card"><h4>10x</h4><p>Lebih Cepat</p></div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="stats-card"><h4>2</h4><p>Modul Lengkap</p></div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="stats-card"><h4>24/7</h4><p>Siap Digunakan</p></div>', unsafe_allow_html=True)
    
    # Fitur utama dengan penekanan pada manfaat
    st.markdown("## 🚀 Solusi Otomatisasi Data Keuangan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🍽️</div>
            <h3>Generator Uang Makan</h3>
            <p>Otomatisasi lengkap untuk rekap uang makan PNS. Integrasikan data kehadiran dengan kalender kerja, 
            hasilkan laporan akurat dalam hitungan detik. Mendukung berbagai jenis pegawai dengan konfigurasi fleksibel.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🍽️ Mulai Generator Uang Makan", key="uang_makan", use_container_width=True):
            st.switch_page("pages/1_🍽️_Generator_Uang_Makan.py")
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💰</div>
            <h3>Generator Tukin PNS</h3>
            <p>Proses Tunjangan Kinerja dengan sistem periode yang cerdas. Kelola data Agama dan Pendidikan 
            dengan kode anak otomatis. Tingkatkan akurasi dan efisiensi pengelolaan tukin organisasi Anda.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("💰 Mulai Generator Tukin", key="tukin", use_container_width=True):
            st.switch_page("pages/2_💰_Generator_Tukin.py")
    
    # Section manfaat dan informasi yang relevan dengan renkeu
    st.markdown("## 🎯 Mengapa Memilih RenkeuGen?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-section">
            <h3>💡 Keunggulan Utilitas</h3>
            <div class="benefit-card">
                <h4>⚡ Proses Super Cepat</h4>
                <p>Otomatisasi penuh mengurangi waktu pemrosesan dari jam menjadi menit</p>
            </div>
            <div class="benefit-card">
                <h4>🎯 Akurasi Tinggi</h4>
                <p>Validasi data otomatis meminimalkan kesalahan manual</p>
            </div>
            <div class="benefit-card">
                <h4>📱 Interface Intuitif</h4>
                <p>Desain user-friendly memudahkan penggunaan tanpa training khusus</p>
            </div>
            <div class="benefit-card">
                <h4>📊 Laporan Lengkap</h4>
                <p>Dashboard analitik memberikan insight mendalam tentang data</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-section">
            <h3>🏢 Manfaat untuk Rencana Keuangan</h3>
            <ul>
                <li><strong>Efisiensi Operasional:</strong> Menghemat waktu staf administrasi hingga 80%</li>
                <li><strong>Transparansi Data:</strong> Tracking dan audit trail yang komprehensif</li>
                <li><strong>Konsistensi Format:</strong> Standarisasi output sesuai regulasi terbaru</li>
                <li><strong>Skalabilitas:</strong> Dapat menangani volume data besar dengan performa stabil</li>
                <li><strong>Integrasi Mudah:</strong> Compatible dengan sistem keuangan existing</li>
                <li><strong>Backup Otomatis:</strong> Multiple format export untuk keamanan data</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Section panduan cepat
    st.markdown("## 📚 Panduan Cepat Memulai")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="info-section">
            <h3>1️⃣ Persiapan Data</h3>
            <p>Pastikan file Excel dan CSV Anda sudah sesuai format yang diperlukan. 
            Sistem akan memberikan validasi otomatis untuk memastikan integritas data.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-section">
            <h3>2️⃣ Upload & Konfigurasi</h3>
            <p>Upload file data dan lakukan konfigurasi periode sesuai kebutuhan. 
            Interface intuitif akan memandu Anda step-by-step.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="info-section">
            <h3>3️⃣ Generate & Download</h3>
            <p>Klik tombol generate dan dapatkan hasil dalam berbagai format. 
            Sistem akan menyediakan preview dan analytics sebelum download.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer dengan informasi kontak dan versioning
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: rgba(255,255,255,0.8); padding: 2rem;'>
        <h4 style='color: white; margin-bottom: 1rem;'>RenkeuGen v2.0</h4>
        <p style='margin-bottom: 0.5rem;'>Platform Utilitas Generator Data Rencana Keuangan PNS</p>
        <p style='font-size: 0.9rem; opacity: 0.7;'>
            Dikembangkan dengan teknologi modern untuk mendukung digitalisasi administrasi PNS
        </p>
        <p style='font-size: 0.8rem; opacity: 0.6; margin-top: 1rem;'>
            © 2025 - Sistem Generator Data Keuangan | Streamlit Powered
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()