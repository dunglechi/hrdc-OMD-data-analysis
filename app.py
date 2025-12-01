import streamlit as st
import pandas as pd
from pathlib import Path
import sys
from translations import get_text, get_lang, set_lang

# Page config
st.set_page_config(
    page_title="VNPT HRDC Data Analysis Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enterprise Minimal Analytics UI - Custom CSS
st.markdown("""
<style>
    /* Import Inter font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Main container */
    .block-container {
        padding: 2rem 3rem;
        max-width: 1400px;
    }
    
    /* Sidebar - Enterprise style */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #DDE3E9;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding: 2rem 1.5rem;
    }
    
    /* Page title styles */
    .page-title {
        font-size: 2.25rem;
        font-weight: 700;
        color: #0066B2;
        margin: 0.5rem 0;
        line-height: 1.2;
    }
    
    .page-subtitle {
        font-size: 1.1rem;
        font-weight: 400;
        color: #6B7280;
        margin: 0;
    }
    
    /* Language toggle */
    .language-section {
        margin-bottom: 1.5rem;
    }
    
    .stButton > button {
        background-color: #FFFFFF;
        color: #1A1A1A;
        border: 1px solid #DDE3E9;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        font-size: 0.9rem;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background-color: #E6F1FA;
        border-color: #0066B2;
        color: #0066B2;
    }
    
    .stButton > button[kind="primary"] {
        background-color: #0066B2;
        color: #FFFFFF;
        border-color: #0066B2;
    }
    
    .stButton > button[kind="primary"]:hover {
        background-color: #004D99;
        border-color: #004D99;
    }
    
    /* Workflow section */
    .workflow-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #1A1A1A;
        margin: 1.5rem 0 1rem 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .workflow-step {
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        border-radius: 6px;
        font-size: 0.9rem;
        font-weight: 500;
        color: #1A1A1A;
        background: #F5F7F9;
        border-left: 3px solid transparent;
        transition: all 0.2s ease;
    }
    
    .workflow-step:hover {
        background: #E6F1FA;
        border-left-color: #0066B2;
    }
    
    .workflow-step.active {
        background: #E6F1FA;
        border-left-color: #0066B2;
        color: #0066B2;
    }
    
    /* Section titles */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .kpi-card {
        background: #FFFFFF;
        border: 1px solid #DDE3E9;
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
        transition: all 0.2s ease;
    }
    
    .kpi-card:hover {
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.08);
        border-color: #0066B2;
    }
    
    .kpi-icon {
        font-size: 2rem;
        margin-bottom: 0.75rem;
        color: #0066B2;
    }
    
    .kpi-title {
        font-size: 0.9rem;
        font-weight: 600;
        color: #1A1A1A;
        margin-bottom: 0.25rem;
    }
    
    .kpi-desc {
        font-size: 0.85rem;
        font-weight: 400;
        color: #6B7280;
        line-height: 1.4;
    }
    
    /* Section titles */
    h2, h3 {
        font-weight: 600;
        color: #1A1A1A;
    }
    
    h2 {
        font-size: 1.5rem;
        margin: 2rem 0 1rem 0;
    }
    
    h3 {
        font-size: 1.25rem;
        margin: 1.5rem 0 1rem 0;
    }
    
    /* Welcome card - Clean design */
    .welcome-card {
        background: #FFFFFF;
        border: 1px solid #DDE3E9;
        border-radius: 8px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
    }
    
    .welcome-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1A1A1A;
        margin: 0 0 1rem 0;
    }
    
    .welcome-intro {
        font-size: 1rem;
        color: #6B7280;
        margin-bottom: 1.5rem;
        line-height: 1.6;
    }
    
    .feature-section {
        margin: 1.5rem 0;
    }
    
    .feature-title {
        font-size: 1rem;
        font-weight: 600;
        color: #1A1A1A;
        margin-bottom: 0.75rem;
    }
    
    .feature-list {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    
    .feature-item {
        padding: 0.5rem 0;
        color: #1A1A1A;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    .feature-item::before {
        content: "✓";
        color: #0066B2;
        font-weight: 600;
        margin-right: 0.75rem;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 1.75rem;
        font-weight: 600;
        color: #0066B2;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.85rem;
        font-weight: 500;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Info boxes */
    .stInfo {
        background-color: #E6F1FA;
        border-left: 4px solid #0066B2;
        padding: 1rem;
        border-radius: 6px;
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background: #F5F7F9;
        border: 2px dashed #DDE3E9;
        border-radius: 8px;
        padding: 2rem;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #0066B2;
        background: #E6F1FA;
    }
    
    /* Dataframe */
    .dataframe {
        font-size: 0.9rem;
    }
    
    .dataframe thead th {
        background-color: #F5F7F9;
        color: #1A1A1A;
        font-weight: 600;
        border-bottom: 2px solid #DDE3E9;
    }
    
    .dataframe tbody tr:nth-child(even) {
        background-color: #FAFBFC;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 1rem;
        margin-top: 3rem;
        border-top: 1px solid #DDE3E9;
        color: #6B7280;
        font-size: 0.85rem;
    }
    
    .footer-brand {
        color: #0066B2;
        font-weight: 600;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #F5F7F9;
        border-radius: 6px;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'df_raw' not in st.session_state:
    st.session_state.df_raw = None
if 'df_cleaned' not in st.session_state:
    st.session_state.df_cleaned = None
if 'stats' not in st.session_state:
    st.session_state.stats = None
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1

# ==================== SIDEBAR ====================
with st.sidebar:
    # Language toggle
    st.markdown('<div class="language-section">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🇻🇳 VN", use_container_width=True, 
                    type="primary" if get_lang() == 'vi' else "secondary"):
            set_lang('vi')
            st.rerun()
    with col2:
        if st.button("🇬🇧 EN", use_container_width=True,
                    type="primary" if get_lang() == 'en' else "secondary"):
            set_lang('en')
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Workflow
    lang = get_lang()
    workflow_title = "QUY TRÌNH PHÂN TÍCH" if lang == 'vi' else "ANALYSIS WORKFLOW"
    st.markdown(f'<div class="workflow-title">{workflow_title}</div>', unsafe_allow_html=True)
    
    steps = [
        ("📊", "Khám phá dữ liệu" if lang == 'vi' else "Data Exploration"),
        ("🧹", "Làm sạch dữ liệu" if lang == 'vi' else "Data Cleaning"),
        ("📈", "Phân tích thống kê" if lang == 'vi' else "Statistical Analysis"),
        ("📉", "Trực quan hóa" if lang == 'vi' else "Visualization"),
        ("🤖", "Phân tích AI" if lang == 'vi' else "AI Analysis")
    ]
    
    for i, (icon, name) in enumerate(steps, 1):
        status = "✓" if i < st.session_state.current_step else "●" if i == st.session_state.current_step else "○"
        active_class = "active" if i == st.session_state.current_step else ""
        st.markdown(f'<div class="workflow-step {active_class}">{status} {icon} {name}</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Quick guide
    if lang == 'vi':
        st.caption("""
        **Hướng dẫn nhanh:**
        
        1. Upload file Excel (.xlsx)
        2. Khám phá cấu trúc dữ liệu
        3. Làm sạch và chuẩn hóa
        4. Phân tích thống kê
        5. Tạo biểu đồ tương tác
        6. Nhận khuyến nghị từ AI
        """)
    else:
        st.caption("""
        **Quick Guide:**
        
        1. Upload Excel file (.xlsx)
        2. Explore data structure
        3. Clean and standardize
        4. Statistical analysis
        5. Create interactive charts
        6. Get AI recommendations
        """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Conversational AI Assistant
    if st.session_state.df_raw is not None:
        from conversational_ai import initialize_conversational_assistant, create_ai_chat_widget
        
        assistant = initialize_conversational_assistant()
        
        # Prepare data summary for context
        data_summary = {
            'rows': len(st.session_state.df_raw),
            'columns': len(st.session_state.df_raw.columns),
            'missing_pct': round((st.session_state.df_raw.isnull().sum().sum() / 
                                 (len(st.session_state.df_raw) * len(st.session_state.df_raw.columns)) * 100), 2),
            'has_cleaned_data': st.session_state.df_cleaned is not None
        }
        
        with st.expander("🤖 AI Chat Assistant", expanded=False):
            create_ai_chat_widget(
                assistant=assistant,
                current_page="Home",
                data_summary=data_summary
            )


# ==================== MAIN CONTENT ====================
lang = get_lang()

# Header - Logo on top, centered
st.markdown("""
<div style="text-align: center; padding: 2rem 0 1rem 0;">
    <img src="https://i.ibb.co/zTBb066t/HRDC-logo-ngang.png" style="max-width: 400px; width: 100%; height: auto;">
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="text-align: center; margin-bottom: 2rem;">
    <div class="page-title">VNPT Data Analysis Platform</div>
    <div class="page-subtitle">Nền tảng phân tích dữ liệu chuyên nghiệp</div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("<br>", unsafe_allow_html=True)

# KPI Cards
st.markdown("""
<div class="kpi-grid">
    <div class="kpi-card">
        <div class="kpi-icon">📤</div>
        <div class="kpi-title">Upload</div>
        <div class="kpi-desc">Tải lên file Excel để bắt đầu phân tích dữ liệu</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon">🔍</div>
        <div class="kpi-title">Analyze</div>
        <div class="kpi-desc">Khám phá, làm sạch và phân tích dữ liệu</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon">🤖</div>
        <div class="kpi-title">AI Insights</div>
        <div class="kpi-desc">Nhận khuyến nghị từ Machine Learning</div>
    </div>
</div>
""", unsafe_allow_html=True)

# File upload section
st.markdown("## Upload Dữ Liệu" if lang == 'vi' else "## Upload Data")

uploaded_file = st.file_uploader(
    "Chọn file Excel (.xlsx)" if lang == 'vi' else "Choose Excel file (.xlsx)",
    type=['xlsx'],
    help="Upload file Excel chứa dữ liệu cần phân tích" if lang == 'vi' else "Upload Excel file with data to analyze"
)

if uploaded_file is not None:
    try:
        # Load data
        with st.spinner("Đang tải dữ liệu..." if lang == 'vi' else "Loading data..."):
            df = pd.read_excel(uploaded_file)
            st.session_state.df_raw = df
            st.session_state.current_step = 0  # Start at Column Dictionary
        
        st.success(f"✓ Đã tải {len(df):,} dòng dữ liệu" if lang == 'vi' else f"✓ Loaded {len(df):,} rows")
        
        # Check if column dictionary exists
        if 'column_dictionary' not in st.session_state or not st.session_state.column_dictionary:
            st.warning("⚠️ **Bước quan trọng**: Bạn cần định nghĩa ý nghĩa các cột trước khi phân tích!")
            st.info("📖 Đang chuyển sang Column Dictionary...")
            
            # Show brief preview
            st.markdown("**Preview dữ liệu:**")
            st.dataframe(df.head(3), use_container_width=True)
            
            # Auto-redirect after 3 seconds
            import time
            time.sleep(2)
            st.switch_page("pages/0_📖_Column_Dictionary.py")
            st.stop()
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Dòng" if lang == 'vi' else "Rows", f"{len(df):,}")
        with col2:
            st.metric("Cột" if lang == 'vi' else "Columns", len(df.columns))
        with col3:
            st.metric("Kích thước" if lang == 'vi' else "Size", f"{uploaded_file.size / 1024:.1f} KB")
        with col4:
            duplicates = df.duplicated().sum()
            st.metric("Trùng lặp" if lang == 'vi' else "Duplicates", duplicates)
        
        # Data preview
        with st.expander("👁️ Xem trước dữ liệu" if lang == 'vi' else "👁️ Preview data", expanded=False):
            st.dataframe(df.head(10), use_container_width=True)
        
        # Next step
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 2])
        with col1:
            if st.button("Bắt đầu phân tích →" if lang == 'vi' else "Start analysis →", 
                        use_container_width=True, type="primary"):
                st.switch_page("pages/0_📖_Column_Dictionary.py")
        with col2:
            st.info("👈 Sử dụng menu bên trái để điều hướng" if lang == 'vi' else "👈 Use left menu to navigate")
        
    except Exception as e:
        st.error(f"Lỗi: {str(e)}" if lang == 'vi' else f"Error: {str(e)}")

else:
    # Welcome section
    if lang == 'vi':
        st.markdown("""
        <div class="welcome-card">
            <div class="welcome-title">Chào mừng đến với VNPT Data Analysis Platform</div>
            <div class="welcome-intro">
                Nền tảng phân tích dữ liệu tương tác được thiết kế cho đào tạo và phân tích chuyên nghiệp tại VNPT HRDC.
            </div>
            
            <div class="feature-section">
                <div class="feature-title">Tính năng chính</div>
                <ul class="feature-list">
                    <li class="feature-item">Khám phá và đánh giá chất lượng dữ liệu tự động</li>
                    <li class="feature-item">Làm sạch dữ liệu với các chiến lược tùy chỉnh</li>
                    <li class="feature-item">Phân tích thống kê chuyên sâu với 8 danh mục</li>
                    <li class="feature-item">Trực quan hóa dữ liệu với biểu đồ Plotly tương tác</li>
                    <li class="feature-item">AI/ML: Dự báo rời mạng, phân khúc khách hàng, phát hiện bất thường</li>
                    <li class="feature-item">Khuyến nghị chuyên gia tự động dựa trên kết quả phân tích</li>
                </ul>
            </div>
            
            <div class="feature-section">
                <div class="feature-title">Bắt đầu</div>
                <p class="feature-item" style="padding-left: 0;">Upload file Excel của bạn ở phần trên để bắt đầu phân tích dữ liệu.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="welcome-card">
            <div class="welcome-title">Welcome to VNPT Data Analysis Platform</div>
            <div class="welcome-intro">
                Interactive data analysis platform designed for training and professional analysis at VNPT HRDC.
            </div>
            
            <div class="feature-section">
                <div class="feature-title">Key Features</div>
                <ul class="feature-list">
                    <li class="feature-item">Automated data exploration and quality assessment</li>
                    <li class="feature-item">Data cleaning with customizable strategies</li>
                    <li class="feature-item">In-depth statistical analysis with 8 categories</li>
                    <li class="feature-item">Data visualization with interactive Plotly charts</li>
                    <li class="feature-item">AI/ML: Churn prediction, customer segmentation, anomaly detection</li>
                    <li class="feature-item">Automated expert recommendations based on analysis results</li>
                </ul>
            </div>
            
            <div class="feature-section">
                <div class="feature-title">Get Started</div>
                <p class="feature-item" style="padding-left: 0;">Upload your Excel file above to start analyzing your data.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Sample data button
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🎲 Tải dữ liệu mẫu" if lang == 'vi' else "🎲 Load sample data", use_container_width=False):
        sample_file = Path("data/raw_data.xlsx")
        if sample_file.exists():
            df = pd.read_excel(sample_file)
            st.session_state.df_raw = df
            st.session_state.current_step = 1
            st.rerun()
        else:
            st.warning("Không tìm thấy dữ liệu mẫu" if lang == 'vi' else "Sample data not found")

# Footer
st.markdown("""
<div class="footer">
    <p><span class="footer-brand">VNPT HRDC</span> Portal Team | Powered by Streamlit</p>
    <p>© 2025 VNPT Corporation - Internal Use Only</p>
</div>
""", unsafe_allow_html=True)
