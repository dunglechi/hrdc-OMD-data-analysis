"""
Page 1: Data Exploration
Khám phá và hiểu cấu trúc dữ liệu
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Khám Phá Dữ Liệu", page_icon="📊", layout="wide")

# Check if data exists
if st.session_state.df_raw is None:
    st.warning("⚠️ Chưa có dữ liệu! Vui lòng upload file ở trang chủ.")
    if st.button("🏠 Về Trang Chủ"):
        st.switch_page("app.py")
    st.stop()

df = st.session_state.df_raw

# Header
st.markdown("""
<div style="background: linear-gradient(90deg, #0066B2 0%, #00A3E0 100%); padding: 1.5rem; border-radius: 10px; color: white; margin-bottom: 2rem;">
    <h1>📊 Bước 1: Khám Phá Dữ Liệu</h1>
    <p>Hiểu cấu trúc, chất lượng và đặc điểm của dữ liệu</p>
</div>
""", unsafe_allow_html=True)

# Overview metrics
st.markdown("### 📋 Tổng Quan Dữ Liệu")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("📊 Tổng số dòng", f"{len(df):,}")
with col2:
    st.metric("📝 Tổng số cột", len(df.columns))
with col3:
    duplicates = df.duplicated().sum()
    st.metric("🔄 Dòng trùng lặp", duplicates)
with col4:
    missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100)
    st.metric("❌ Missing (%)", f"{missing_pct:.1f}%")
with col5:
    memory_mb = df.memory_usage(deep=True).sum() / 1024 / 1024
    st.metric("💾 Bộ nhớ (MB)", f"{memory_mb:.2f}")

st.markdown("---")

# Data preview
st.markdown("### 👀 Xem Trước Dữ Liệu")

col1, col2 = st.columns([3, 1])

with col1:
    n_rows = st.slider("Số dòng hiển thị", 5, 100, 20)

with col2:
    show_info = st.checkbox("Hiện thông tin cột", value=False)

if show_info:
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(df.head(n_rows), use_container_width=True, height=400)
    with col2:
        st.markdown("**Thông tin các cột:**")
        info_df = pd.DataFrame({
            'Cột': df.columns,
            'Kiểu dữ liệu': df.dtypes.astype(str),
            'Missing': df.isnull().sum(),
            'Missing %': (df.isnull().sum() / len(df) * 100).round(2)
        })
        st.dataframe(info_df, use_container_width=True, height=400)
else:
    st.dataframe(df.head(n_rows), use_container_width=True)

st.markdown("---")

# Column analysis
st.markdown("### 📊 Phân Tích Từng Cột")

selected_col = st.selectbox("Chọn cột để phân tích chi tiết", df.columns)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"**Cột:** `{selected_col}`")
    st.markdown(f"**Kiểu dữ liệu:** {df[selected_col].dtype}")
    st.markdown(f"**Giá trị duy nhất:** {df[selected_col].nunique():,}")
    st.markdown(f"**Missing values:** {df[selected_col].isnull().sum():,} ({df[selected_col].isnull().sum()/len(df)*100:.1f}%)")

with col2:
    st.markdown("**Top 5 giá trị:**")
    if df[selected_col].dtype in ['int64', 'float64']:
        st.write(df[selected_col].describe())
    else:
        st.write(df[selected_col].value_counts().head())

with col3:
    # Visualization based on data type
    if df[selected_col].dtype in ['int64', 'float64']:
        fig = px.histogram(df, x=selected_col, title=f"Phân phối {selected_col}",
                          color_discrete_sequence=['#0066B2'])
        st.plotly_chart(fig, use_container_width=True)
    else:
        top_values = df[selected_col].value_counts().head(10)
        fig = px.bar(x=top_values.index, y=top_values.values,
                    title=f"Top 10 giá trị - {selected_col}",
                    labels={'x': selected_col, 'y': 'Số lượng'},
                    color_discrete_sequence=['#0066B2'])
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Missing values analysis
st.markdown("### ❌ Phân Tích Missing Values")

missing_df = pd.DataFrame({
    'Cột': df.columns,
    'Missing Count': df.isnull().sum(),
    'Missing %': (df.isnull().sum() / len(df) * 100).round(2)
}).sort_values('Missing Count', ascending=False)

missing_df = missing_df[missing_df['Missing Count'] > 0]

if len(missing_df) > 0:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Missing values heatmap
        fig = px.bar(missing_df, x='Cột', y='Missing %',
                    title="Tỷ lệ Missing Values theo cột",
                    color='Missing %',
                    color_continuous_scale=['#90EE90', '#FFD700', '#FF6347'],
                    labels={'Missing %': 'Tỷ lệ Missing (%)'}
                    )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("**Chi tiết Missing Values:**")
        st.dataframe(missing_df, use_container_width=True)
        
        # Recommendations
        st.info("""
        **💡 Gợi ý xử lý:**
        - < 5%: Có thể xóa hoặc điền
        - 5-30%: Nên điền giá trị
        - > 30%: Cân nhắc giữ NULL hoặc tạo flag
        """)
else:
    st.success("✅ Không có missing values trong dataset!")

st.markdown("---")

# Data quality scorecard
st.markdown("### 🎯 Bảng Điểm Chất Lượng Dữ Liệu")

col1, col2, col3, col4 = st.columns(4)

# Calculate scores
completeness = (1 - df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
uniqueness = (1 - duplicates / len(df)) * 100
validity = 100  # Simplified - would need business rules
consistency = 100  # Simplified

with col1:
    st.metric("📊 Completeness", f"{completeness:.1f}%", 
             help="Tỷ lệ dữ liệu không bị thiếu")
with col2:
    st.metric("🔑 Uniqueness", f"{uniqueness:.1f}%",
             help="Tỷ lệ dữ liệu không trùng lặp")
with col3:
    st.metric("✅ Validity", f"{validity:.1f}%",
             help="Tỷ lệ dữ liệu hợp lệ")
with col4:
    st.metric("🎯 Consistency", f"{consistency:.1f}%",
             help="Tỷ lệ dữ liệu nhất quán")

# Overall score
overall_score = (completeness + uniqueness + validity + consistency) / 4

if overall_score >= 90:
    st.success(f"🌟 Điểm tổng thể: {overall_score:.1f}% - Chất lượng dữ liệu TỐT!")
elif overall_score >= 70:
    st.warning(f"⚠️ Điểm tổng thể: {overall_score:.1f}% - Chất lượng dữ liệu TRUNG BÌNH, cần cải thiện")
else:
    st.error(f"❌ Điểm tổng thể: {overall_score:.1f}% - Chất lượng dữ liệu KÉM, cần làm sạch")

st.markdown("---")

# AI Data Quality Assessment
st.markdown("### 🤖 AI Data Quality Assessment")
st.markdown("Sử dụng Gemini AI để phân tích chất lượng dữ liệu và đưa ra khuyến nghị chuyên gia.")

col1, col2 = st.columns([1, 3])

with col1:
    if st.button("🚀 Chạy AI Assessment", use_container_width=True, type="primary"):
        with st.spinner("🤖 AI đang phân tích dữ liệu..."):
            import sys
            sys.path.append('..')
            from gemini_assistant import analyze_data_quality
            
            insights = analyze_data_quality(df, lang='vi')
            st.session_state.ai_insights = insights

with col2:
    if 'ai_insights' in st.session_state and st.session_state.ai_insights:
        st.markdown("**💡 AI Insights:**")
        st.info(st.session_state.ai_insights)
    else:
        st.info("👈 Nhấn nút để nhận phân tích từ AI")

st.markdown("---")

# Navigation
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.button("⬅️ Về Trang Chủ", use_container_width=True):
        st.switch_page("app.py")

with col3:
    if st.button("Tiếp Theo: Làm Sạch Dữ Liệu ➡️", use_container_width=True):
        st.session_state.current_step = 2
        st.switch_page("pages/2_🧹_Data_Cleaning.py")

# Update step
st.session_state.current_step = max(st.session_state.current_step, 1)
