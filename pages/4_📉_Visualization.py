"""
Page 4: Visualization - Unified Dashboard
Hiển thị tất cả biểu đồ trên một trang
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Trực Quan Hóa", page_icon="📉", layout="wide")

# Check if data exists
if st.session_state.df_cleaned is None:
    st.warning("⚠️ Chưa có dữ liệu! Vui lòng hoàn tất các bước trước.")
    if st.button("🏠 Về Trang Chủ"):
        st.switch_page("app.py")
    st.stop()

df = st.session_state.df_cleaned

# Header
st.markdown("""
<div style="background: linear-gradient(90deg, #0066B2 0%, #00A3E0 100%); padding: 1.5rem; border-radius: 10px; color: white; margin-bottom: 2rem;">
    <h1>📉 Bước 4: Dashboard Trực Quan Hóa</h1>
    <p>Tổng quan toàn bộ phân tích qua biểu đồ tương tác</p>
</div>
""", unsafe_allow_html=True)

# VNPT Colors
VNPT_BLUE = '#0066B2'
VNPT_COLORS = ['#0066B2', '#00A3E0', '#0080C0', '#004D99', '#003366']

# =============================================================================
# SECTION 1: TKC ANALYSIS
# =============================================================================
st.markdown("## 💰 Phân Tích TKC (Tài Khoản Chính)")
st.caption("Phân bố số dư tài khoản và phân khúc khách hàng")

col1, col2 = st.columns(2)

with col1:
    # TKC Distribution Histogram
    fig = px.histogram(
        df, 
        x='TOTAL_TKC',
        nbins=50,
        title="Phân Bố TKC (Histogram)",
        color_discrete_sequence=[VNPT_BLUE],
        labels={'TOTAL_TKC': 'Tổng TKC (VNĐ)'}
    )
    fig.add_vline(x=df['TOTAL_TKC'].mean(), line_dash="dash", line_color="red",
                 annotation_text=f"TB: {df['TOTAL_TKC'].mean():,.0f}")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # TKC Segments Pie Chart
    if 'TKC_SEGMENT' in df.columns:
        segment_counts = df['TKC_SEGMENT'].value_counts()
        fig = px.pie(
            values=segment_counts.values,
            names=segment_counts.index,
            title="Phân Khúc TKC",
            color_discrete_sequence=VNPT_COLORS
        )
        st.plotly_chart(fig, use_container_width=True)

# AI Insights for TKC
with st.expander("🤖 AI Phân Tích TKC", expanded=False):
    if st.button("🔮 Tạo AI Insights", key="ai_tkc"):
        with st.spinner("🤖 AI đang phân tích..."):
            from gemini_assistant import interpret_chart
            
            tkc_data = {
                'mean': df['TOTAL_TKC'].mean(),
                'median': df['TOTAL_TKC'].median(),
                'std': df['TOTAL_TKC'].std(),
                'segments': df['TKC_SEGMENT'].value_counts().to_dict() if 'TKC_SEGMENT' in df.columns else {}
            }
            
            ai_insights = interpret_chart('TKC Distribution', tkc_data, 'vi')
            st.markdown(ai_insights)

st.markdown("---")

# =============================================================================
# SECTION 2: SERVICE ADOPTION
# =============================================================================
st.markdown("## 📱 Phân Tích Service Adoption")
st.caption("Tỷ lệ kích hoạt dịch vụ và so sánh TKC")

col1, col2 = st.columns(2)

with col1:
    # Service Adoption Bar Chart
    if 'HAS_SERVICE' in df.columns:
        service_counts = df['HAS_SERVICE'].value_counts()
        total = len(df)
        
        fig = px.bar(
            x=['Có Dịch Vụ', 'Chưa Có'],
            y=[service_counts.get(True, 0), service_counts.get(False, 0)],
            title="Tỷ Lệ Kích Hoạt Dịch Vụ",
            labels={'x': 'Trạng Thái', 'y': 'Số Khách Hàng'},
            color=['Có Dịch Vụ', 'Chưa Có'],
            color_discrete_map={'Có Dịch Vụ': VNPT_BLUE, 'Chưa Có': '#CCCCCC'}
        )
        
        fig.update_traces(
            text=[f"{service_counts.get(True, 0)/total*100:.1f}%", 
                  f"{service_counts.get(False, 0)/total*100:.1f}%"],
            textposition='outside'
        )
        
        st.plotly_chart(fig, use_container_width=True)

with col2:
    # TKC by Service Status
    if 'HAS_SERVICE' in df.columns:
        fig = px.box(
            df,
            x='HAS_SERVICE',
            y='TOTAL_TKC',
            title="So Sánh TKC: Có/Không Dịch Vụ",
            labels={'HAS_SERVICE': 'Có Dịch Vụ', 'TOTAL_TKC': 'TKC (VNĐ)'},
            color='HAS_SERVICE',
            color_discrete_map={True: VNPT_BLUE, False: '#CCCCCC'}
        )
        st.plotly_chart(fig, use_container_width=True)

# AI Insights for Service
with st.expander("🤖 AI Phân Tích Service Adoption", expanded=False):
    if st.button("🔮 Tạo AI Insights", key="ai_service"):
        with st.spinner("🤖 AI đang phân tích..."):
            from gemini_assistant import interpret_chart
            
            service_data = {
                'with_service': service_counts.get(True, 0),
                'without_service': service_counts.get(False, 0),
                'adoption_rate': service_counts.get(True, 0) / total * 100
            }
            
            ai_insights = interpret_chart('Service Adoption', service_data, 'vi')
            st.markdown(ai_insights)

st.markdown("---")

# =============================================================================
# SECTION 3: CHURN RISK ANALYSIS
# =============================================================================
st.markdown("## ⚠️ Phân Tích Rủi Ro Rời Mạng (Churn)")
st.caption("Phân bố rủi ro và thời gian đến hết hạn")

col1, col2 = st.columns(2)

with col1:
    # Churn Risk Distribution
    if 'CHURN_RISK' in df.columns:
        churn_counts = df['CHURN_RISK'].value_counts()
        
        fig = px.bar(
            x=churn_counts.index,
            y=churn_counts.values,
            title="Phân Bố Mức Độ Rủi Ro",
            labels={'x': 'Mức Độ Rủi Ro', 'y': 'Số Khách Hàng'},
            color=churn_counts.index,
            color_discrete_map={'High': '#FF4444', 'Low': '#44FF44'}
        )
        st.plotly_chart(fig, use_container_width=True)

with col2:
    # Days to Expiration
    if 'DAYS_TO_EXPIRE' in df.columns:
        days_filtered = df[df['DAYS_TO_EXPIRE'] < 100]['DAYS_TO_EXPIRE']
        
        fig = px.histogram(
            days_filtered,
            nbins=30,
            title="Số Ngày Đến Hết Hạn (<100 ngày)",
            color_discrete_sequence=[VNPT_BLUE],
            labels={'value': 'Số Ngày'}
        )
        fig.add_vline(x=30, line_dash="dash", line_color="red",
                     annotation_text="Ngưỡng 30 ngày")
        st.plotly_chart(fig, use_container_width=True)

# AI Insights for Churn
with st.expander("🤖 AI Chiến Lược Giữ Chân Khách Hàng", expanded=False):
    if st.button("🔮 Tạo AI Strategy", key="ai_churn", type="primary"):
        with st.spinner("🤖 AI đang tạo chiến lược..."):
            from gemini_assistant import get_ai_response
            
            churn_data = {
                'high_risk': len(df[df['CHURN_RISK'] == 'High']) if 'CHURN_RISK' in df.columns else 0,
                'expiring_30d': len(df[df['DAYS_TO_EXPIRE'] < 30]) if 'DAYS_TO_EXPIRE' in df.columns else 0,
                'expiring_7d': len(df[df['DAYS_TO_EXPIRE'] < 7]) if 'DAYS_TO_EXPIRE' in df.columns else 0
            }
            
            question = f"""
            Phân tích churn và đưa ra chiến lược:
            - {churn_data['high_risk']:,} khách nguy cơ cao
            - {churn_data['expiring_7d']:,} hết hạn trong 7 ngày
            - {churn_data['expiring_30d']:,} hết hạn trong 30 ngày
            
            Đưa ra: Root causes, Immediate actions (7d), Strategy (30d), ROI dự kiến
            """
            
            ai_strategy = get_ai_response(question, churn_data, 'vi')
            st.markdown(ai_strategy)

st.markdown("---")

# =============================================================================
# SECTION 4: GEOGRAPHIC DISTRIBUTION
# =============================================================================
st.markdown("## 🗺️ Phân Bố Địa Lý")
st.caption("Top tỉnh/thành phố theo số lượng khách hàng")

if 'PROVINCE_NAME' in df.columns:
    province_counts = df['PROVINCE_NAME'].value_counts().head(10)
    
    fig = px.bar(
        y=province_counts.index,
        x=province_counts.values,
        orientation='h',
        title="Top 10 Tỉnh/Thành Phố",
        labels={'x': 'Số Khách Hàng', 'y': 'Tỉnh/Thành Phố'},
        color_discrete_sequence=[VNPT_BLUE]
    )
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Không có dữ liệu địa lý (PROVINCE_NAME)")

st.markdown("---")

# =============================================================================
# SECTION 5: TEMPORAL TRENDS
# =============================================================================
st.markdown("## 📅 Xu Hướng Theo Thời Gian")
st.caption("Số lượng kích hoạt theo tháng (24 tháng gần nhất)")

if 'DATE_ENTER_ACTIVE' in df.columns:
    df['activation_month'] = pd.to_datetime(df['DATE_ENTER_ACTIVE']).dt.to_period('M')
    monthly_data = df.groupby('activation_month').size().tail(24)
    
    monthly_df = pd.DataFrame({
        'Tháng': [str(m) for m in monthly_data.index],
        'Số Kích Hoạt': monthly_data.values
    })
    
    fig = px.line(
        monthly_df,
        x='Tháng',
        y='Số Kích Hoạt',
        title="Xu Hướng Kích Hoạt Khách Hàng",
        markers=True,
        color_discrete_sequence=[VNPT_BLUE]
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Không có dữ liệu thời gian (DATE_ENTER_ACTIVE)")

st.markdown("---")

# =============================================================================
# SECTION 6: STAFF PERFORMANCE (if available)
# =============================================================================
if 'STAFF_CODE' in df.columns:
    st.markdown("## 👥 Hiệu Suất Nhân Viên")
    st.caption("Top 10 nhân viên theo số lượng khách hàng quản lý")
    
    staff_stats = df[df['STAFF_CODE'] != 'UNASSIGNED'].groupby('STAFF_CODE').size().sort_values(ascending=False).head(10)
    
    fig = px.bar(
        x=staff_stats.index,
        y=staff_stats.values,
        title="Top 10 Nhân Viên",
        labels={'x': 'Mã Nhân Viên', 'y': 'Số Khách Hàng'},
        color_discrete_sequence=[VNPT_BLUE]
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")

# =============================================================================
# OVERALL AI INSIGHTS
# =============================================================================
st.markdown("## 🤖 Tổng Hợp AI Insights")

if st.button("🔮 Tạo Báo Cáo Tổng Hợp Từ AI", use_container_width=True, type="primary"):
    with st.spinner("🤖 AI đang tạo báo cáo tổng hợp..."):
        from gemini_assistant import get_ai_response
        
        overall_context = {
            'total_customers': len(df),
            'avg_tkc': df['TOTAL_TKC'].mean(),
            'service_adoption': df['HAS_SERVICE'].sum() / len(df) * 100 if 'HAS_SERVICE' in df.columns else 0,
            'high_risk_churn': len(df[df['CHURN_RISK'] == 'High']) if 'CHURN_RISK' in df.columns else 0
        }
        
        question = """
        Dựa trên TẤT CẢ biểu đồ trên dashboard, hãy tạo báo cáo tổng hợp:
        
        1. **Executive Summary** (3-5 điểm chính)
        2. **Key Findings** (insights quan trọng nhất)
        3. **Opportunities** (cơ hội kinh doanh)
        4. **Risks** (rủi ro cần lưu ý)
        5. **Action Plan** (3-5 hành động ưu tiên, có timeline)
        
        Format: Markdown, có emoji, số liệu cụ thể, actionable.
        """
        
        ai_report = get_ai_response(question, overall_context, 'vi')
        st.markdown(ai_report)

st.markdown("---")

# Navigation
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.button("⬅️ Phân Tích Thống Kê", use_container_width=True):
        st.switch_page("pages/3_📈_Statistical_Analysis.py")

with col3:
    if st.button("Tiếp Theo: AI Analysis ➡️", use_container_width=True):
        st.session_state.current_step = 5
        st.switch_page("pages/5_🤖_AI_Analysis.py")

st.session_state.current_step = max(st.session_state.current_step, 4)
