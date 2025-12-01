"""
Page 2: Data Cleaning
Làm sạch và chuẩn hóa dữ liệu tương tác
"""

import streamlit as st
import pandas as pd
import sys
sys.path.append('..')
from data_cleaner import VNPTDataCleaner

st.set_page_config(page_title="Data Cleaning", page_icon="🧹", layout="wide")

# Check if data exists
if st.session_state.df_raw is None:
    st.warning("⚠️ Chưa có dữ liệu! Vui lòng upload file ở trang chủ.")
    if st.button("🏠 Về Trang Chủ"):
        st.switch_page("app.py")
    st.stop()

df = st.session_state.df_raw.copy()

# Header
st.markdown("""
<div style="background: linear-gradient(90deg, #0066B2 0%, #00A3E0 100%); padding: 1.5rem; border-radius: 10px; color: white; margin-bottom: 2rem;">
    <h1>🧹 Bước 2: Làm Sạch Dữ Liệu</h1>
    <p>Xử lý missing values, tạo derived columns, và chuẩn hóa dữ liệu</p>
</div>
""", unsafe_allow_html=True)

# Cleaning options
st.markdown("### ⚙️ Tùy Chọn Làm Sạch")

tab1, tab2, tab3 = st.tabs(["❌ Missing Values", "➕ Derived Columns", "✅ Validation"])

with tab1:
    st.markdown("#### Chiến Lược Xử Lý Missing Values")
    
    # Get columns with missing values
    missing_cols = df.columns[df.isnull().any()].tolist()
    
    if missing_cols:
        strategies = {}
        
        for col in missing_cols:
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.markdown(f"**{col}**")
            
            with col2:
                missing_count = df[col].isnull().sum()
                missing_pct = missing_count / len(df) * 100
                st.caption(f"{missing_count:,} missing ({missing_pct:.1f}%)")
            
            with col3:
                if df[col].dtype in ['int64', 'float64']:
                    strategy = st.selectbox(
                        f"Strategy_{col}",
                        ["Keep NULL", "Mean", "Median", "Zero", "Custom Value"],
                        key=f"strategy_{col}",
                        label_visibility="collapsed"
                    )
                else:
                    strategy = st.selectbox(
                        f"Strategy_{col}",
                        ["Keep NULL", "Mode", "Forward Fill", "Custom Value"],
                        key=f"strategy_{col}",
                        label_visibility="collapsed"
                    )
                
                strategies[col] = strategy
        
        # Preview changes
        if st.button("👁️ Xem Trước Thay Đổi", use_container_width=True):
            st.markdown("#### 📋 Preview: Before vs After")
            
            df_preview = df.copy()
            
            for col, strategy in strategies.items():
                if strategy == "Mean":
                    df_preview[col].fillna(df[col].mean(), inplace=True)
                elif strategy == "Median":
                    df_preview[col].fillna(df[col].median(), inplace=True)
                elif strategy == "Mode":
                    df_preview[col].fillna(df[col].mode()[0] if len(df[col].mode()) > 0 else None, inplace=True)
                elif strategy == "Zero":
                    df_preview[col].fillna(0, inplace=True)
                elif strategy == "Forward Fill":
                    df_preview[col].fillna(method='ffill', inplace=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Before (Missing Values)**")
                st.dataframe(df[missing_cols].isnull().sum(), use_container_width=True)
            with col2:
                st.markdown("**After (Missing Values)**")
                st.dataframe(df_preview[missing_cols].isnull().sum(), use_container_width=True)
    
    else:
        st.success("✅ Không có missing values!")

with tab2:
    st.markdown("#### Tạo Các Cột Mới (Derived Columns)")
    
    # Check for required columns
    has_service = st.checkbox("✅ HAS_SERVICE (có service code không?)", value=True)
    has_account_age = st.checkbox("✅ ACCOUNT_AGE (tuổi tài khoản)", value=True)
    has_days_expire = st.checkbox("✅ DAYS_TO_EXPIRE (số ngày đến hết hạn)", value=True)
    has_churn_risk = st.checkbox("✅ CHURN_RISK (rủi ro churn)", value=True)
    has_tkc_segment = st.checkbox("✅ TKC_SEGMENT (phân khúc TKC)", value=True)
    
    if has_churn_risk:
        churn_threshold = st.slider("Ngưỡng churn risk (ngày)", 7, 90, 30)
    
    if has_tkc_segment:
        st.markdown("**TKC Segmentation Bins:**")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            bin1 = st.number_input("None (max)", value=1, min_value=0)
        with col2:
            bin2 = st.number_input("Low (max)", value=5000, min_value=0)
        with col3:
            bin3 = st.number_input("Medium (max)", value=10000, min_value=0)
        with col4:
            bin4 = st.number_input("High (max)", value=20000, min_value=0)

with tab3:
    st.markdown("#### Validation Rules")
    
    validate_phone = st.checkbox("✅ Validate phone numbers (84XXXXXXXXX)", value=True)
    validate_dates = st.checkbox("✅ Validate date logic (activation < expiration)", value=True)
    validate_tkc = st.checkbox("✅ Validate TKC >= 0", value=True)

st.markdown("---")

# Apply cleaning button
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if st.button("🚀 ÁP DỤNG LÀM SẠCH DỮ LIỆU", use_container_width=True, type="primary"):
        with st.spinner("Đang xử lý..."):
            # Initialize cleaner
            cleaner = VNPTDataCleaner()
            
            # Clean data
            df_cleaned = cleaner.clean_data(df)
            
            # Store in session state
            st.session_state.df_cleaned = df_cleaned
            st.session_state.current_step = 3
            
            st.success("✅ Làm sạch dữ liệu thành công!")
            
            # Show summary
            st.markdown("#### 📊 Tóm Tắt Kết Quả")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Dòng ban đầu", f"{len(df):,}")
            with col2:
                st.metric("Dòng sau làm sạch", f"{len(df_cleaned):,}")
            with col3:
                new_cols = len(df_cleaned.columns) - len(df.columns)
                st.metric("Cột mới tạo", f"+{new_cols}")
            
            # Show new columns
            if new_cols > 0:
                new_col_names = [col for col in df_cleaned.columns if col not in df.columns]
                st.info(f"**Cột mới:** {', '.join(new_col_names)}")

# Show cleaned data if exists
if st.session_state.df_cleaned is not None:
    st.markdown("---")
    st.markdown("### ✅ Dữ Liệu Đã Làm Sạch")
    
    df_cleaned = st.session_state.df_cleaned
    
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(df_cleaned.head(20), use_container_width=True)
    with col2:
        st.markdown("**Thống kê:**")
        st.write(f"- Tổng dòng: {len(df_cleaned):,}")
        st.write(f"- Tổng cột: {len(df_cleaned.columns)}")
        st.write(f"- Missing values: {df_cleaned.isnull().sum().sum():,}")
        st.write(f"- Duplicates: {df_cleaned.duplicated().sum():,}")
        
        # Download button
        csv = df_cleaned.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Cleaned Data (CSV)",
            data=csv,
            file_name="cleaned_data.csv",
            mime="text/csv",
            use_container_width=True
        )

st.markdown("---")

# Navigation
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.button("⬅️ Khám Phá Dữ Liệu", use_container_width=True):
        st.switch_page("pages/1_📊_Data_Exploration.py")

with col3:
    if st.session_state.df_cleaned is not None:
        if st.button("Tiếp Theo: Phân Tích Thống Kê ➡️", use_container_width=True):
            st.session_state.current_step = 3
            st.switch_page("pages/3_📈_Statistical_Analysis.py")
    else:
        st.button("Tiếp Theo: Phân Tích Thống Kê ➡️", use_container_width=True, disabled=True)
        st.caption("⚠️ Vui lòng làm sạch dữ liệu trước")
