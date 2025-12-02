"""
Page 3: Statistical Analysis
Phân tích thống kê tương tác
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
sys.path.append('..')
from statistical_analyzer import VNPTStatisticalAnalyzer

st.set_page_config(page_title="Phân Tích Thống Kê", page_icon="📈", layout="wide")

# Check if cleaned data exists
if st.session_state.df_cleaned is None:
    st.warning("⚠️ Chưa có dữ liệu đã làm sạch! Vui lòng hoàn tất bước Data Cleaning.")
    if st.button("🧹 Đến Data Cleaning"):
        st.switch_page("pages/2_🧹_Data_Cleaning.py")
    st.stop()

df = st.session_state.df_cleaned

# Header
st.markdown("""
<div style="background: linear-gradient(90deg, #0066B2 0%, #00A3E0 100%); padding: 1.5rem; border-radius: 10px; color: white; margin-bottom: 2rem;">
    <h1>📈 Bước 3: Phân Tích Thống Kê</h1>
    <p>Khám phá insights và patterns trong dữ liệu</p>
</div>
""", unsafe_allow_html=True)

# Run analysis if not done
if st.session_state.stats is None:
    with st.spinner("Đang phân tích dữ liệu..."):
        analyzer = VNPTStatisticalAnalyzer(df)
        stats = analyzer.analyze_all()
        st.session_state.stats = stats

stats = st.session_state.stats

# Key Metrics
st.markdown("### 📊 Chỉ Số Chính")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "👥 Tổng Khách Hàng", 
        f"{stats['overview']['total_customers']:,}",
        help="Tổng số khách hàng trong dữ liệu"
    )
with col2:
    adoption_rate = stats['service_analysis']['adoption_rate'] * 100
    st.metric(
        "📱 Service Adoption", 
        f"{adoption_rate:.1f}%",
        help="Tỷ lệ khách hàng đã kích hoạt dịch vụ (Data, Voice, SMS...)"
    )
with col3:
    churn_pct = stats['churn_analysis']['high_risk_percentage'] * 100
    st.metric(
        "⚠️ High Churn Risk", 
        f"{churn_pct:.1f}%", 
        delta=f"-{100-churn_pct:.1f}%",
        help="Tỷ lệ khách hàng có nguy cơ rời mạng cao (sắp hết hạn hoặc TKC thấp)"
    )
with col4:
    avg_tkc = stats['tkc_analysis']['descriptive_stats']['mean']
    st.metric(
        "💰 Avg TKC", 
        f"{avg_tkc:,.0f} VNĐ",
        help="Số tiền trung bình trong Tài Khoản Chính của khách hàng"
    )
with col5:
    avg_age = stats['temporal_trends']['avg_account_age_days']
    st.metric(
        "📅 Avg Account Age", 
        f"{avg_age:.0f} days",
        help="Số ngày trung bình từ khi kích hoạt tài khoản đến nay"
    )

st.markdown("---")

# Tabs for different analyses
tab1, tab2, tab3, tab4 = st.tabs(["💰 TKC Analysis", "📱 Service Analysis", "⚠️ Churn Analysis", "👥 Segmentation"])

with tab1:
    st.markdown("### 💰 Phân Tích TKC (Tài Khoản Chính)")
    st.caption("TKC = Tài khoản chính - Số tiền khách hàng còn lại trong tài khoản")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Thống Kê Mô Tả")
        desc_stats = stats['tkc_analysis']['descriptive_stats']
        
        # Add help expander
        with st.expander("📖 Giải thích các chỉ số", expanded=False):
            st.markdown("""
            - **Mean** (Trung bình): Tổng TKC / Số khách hàng
            - **Median** (Trung vị): Giá trị ở giữa khi sắp xếp TKC
            - **Std Dev** (Độ lệch chuẩn): Mức độ phân tán của TKC
            - **Min**: TKC thấp nhất
            - **Max**: TKC cao nhất  
            - **Q25** (Phân vị 25%): 25% khách hàng có TKC ≤ giá trị này
            - **Q75** (Phân vị 75%): 75% khách hàng có TKC ≤ giá trị này
            """)
        
        stats_df = pd.DataFrame({
            'Metric': ['Mean', 'Median', 'Std Dev', 'Min', 'Max', 'Q25', 'Q75'],
            'Value': [
                f"{desc_stats['mean']:,.2f}",
                f"{desc_stats['median']:,.2f}",
                f"{desc_stats['std']:,.2f}",
                f"{desc_stats['min']:,.2f}",
                f"{desc_stats['max']:,.2f}",
                f"{desc_stats['q25']:,.2f}",
                f"{desc_stats['q75']:,.2f}"
            ]
        })
        st.dataframe(stats_df, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("#### Phân Bố Segments")
        segment_dist = stats['tkc_analysis']['segment_distribution']
        
        fig = px.pie(
            values=list(segment_dist.values()),
            names=list(segment_dist.keys()),
            title="TKC Segments Distribution",
            color_discrete_sequence=['#0066B2', '#00A3E0', '#0080C0', '#004D99']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # TKC insights
    st.info(f"""
    **💡 Insights:**
    - {stats['tkc_analysis']['customers_with_zero_tkc']:,} khách hàng có TKC = 0
    - {stats['tkc_analysis']['customers_with_max_tkc']:,} khách hàng có TKC = 20,000 (max)
    - Tổng giá trị TKC: {stats['tkc_analysis']['total_tkc_value']:,.0f} VNĐ
    """)
    
    # AI Analysis
    st.markdown("---")
    st.markdown("#### 🤖 AI Business Insights")
    
    if st.button("🔮 Phân Tích Bằng Gen AI", key="ai_tkc", use_container_width=True):
        with st.spinner("🤖 AI đang phân tích..."):
            from gemini_assistant import interpret_chart
            
            # Prepare TKC data summary
            tkc_summary = {
                'type': 'TKC Distribution & Segments',
                'mean': stats['tkc_analysis']['descriptive_stats']['mean'],
                'median': stats['tkc_analysis']['descriptive_stats']['median'],
                'segments': stats['tkc_analysis']['segment_distribution'],
                'zero_tkc': stats['tkc_analysis']['customers_with_zero_tkc'],
                'max_tkc': stats['tkc_analysis']['customers_with_max_tkc'],
                'total_value': stats['tkc_analysis']['total_tkc_value']
            }
            
            ai_insights = interpret_chart('TKC Analysis', tkc_summary, 'vi')
            st.markdown(ai_insights)


with tab2:
    st.markdown("### 📱 Phân Tích Service Adoption")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Service adoption chart
        adoption_data = {
            'Status': ['With Service', 'No Service'],
            'Count': [
                stats['service_analysis']['customers_with_service'],
                stats['service_analysis']['customers_without_service']
            ]
        }
        
        fig = px.bar(
            adoption_data,
            x='Status',
            y='Count',
            title="Service Adoption Status",
            color='Status',
            color_discrete_map={'With Service': '#0066B2', 'No Service': '#CCCCCC'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Service Statistics")
        st.metric("Customers with Service", f"{stats['service_analysis']['customers_with_service']:,}")
        st.metric("Customers without Service", f"{stats['service_analysis']['customers_without_service']:,}")
        st.metric("Avg TKC (with service)", f"{stats['service_analysis']['avg_tkc_with_service']:,.0f} VNĐ")
        st.metric("Avg TKC (no service)", f"{stats['service_analysis']['avg_tkc_without_service']:,.0f} VNĐ")
    
    # AI Analysis
    st.markdown("---")
    if st.button("🔮 AI Phân Tích Service Adoption", key="ai_service", use_container_width=True):
        with st.spinner("🤖 AI đang phân tích..."):
            from gemini_assistant import interpret_chart
            
            service_summary = {
                'type': 'Service Adoption Analysis',
                'adoption_rate': stats['service_analysis']['adoption_rate'],
                'with_service': stats['service_analysis']['customers_with_service'],
                'without_service': stats['service_analysis']['customers_without_service'],
                'avg_tkc_with': stats['service_analysis']['avg_tkc_with_service'],
                'avg_tkc_without': stats['service_analysis']['avg_tkc_without_service']
            }
            
            ai_insights = interpret_chart('Service Adoption', service_summary, 'vi')
            st.markdown(ai_insights)


with tab3:
    st.markdown("### ⚠️ Phân Tích Churn Risk")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Churn Risk Distribution")
        st.metric("High Risk Customers", f"{stats['churn_analysis']['high_risk_count']:,}")
        st.metric("High Risk %", f"{stats['churn_analysis']['high_risk_percentage']*100:.1f}%")
        st.metric("Avg Days to Expire", f"{stats['churn_analysis']['avg_days_to_expire']:.0f} days")
    
    with col2:
        st.markdown("#### Expiration Timeline")
        exp_data = {
            'Timeline': ['< 7 days', '< 30 days', 'Expired'],
            'Count': [
                stats['churn_analysis']['expiring_within_7_days'],
                stats['churn_analysis']['expiring_within_30_days'],
                stats['churn_analysis']['already_expired']
            ]
        }
        
        fig = px.bar(
            exp_data,
            x='Timeline',
            y='Count',
            title="Customers by Expiration Timeline",
            color='Timeline',
            color_discrete_sequence=['#FF4444', '#FFA500', '#666666']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.error(f"""
    **🚨 CRITICAL ALERT:**
    - {stats['churn_analysis']['high_risk_count']:,} customers at HIGH CHURN RISK
    - {stats['churn_analysis']['expiring_within_7_days']:,} expiring within 7 days
    - **Action Required**: Urgent retention campaign needed!
    """)
    
    # AI Churn Strategy
    st.markdown("---")
    if st.button("🔮 AI Chiến Lược Giữ Chân Khách Hàng", key="ai_churn", use_container_width=True, type="primary"):
        with st.spinner("🤖 AI đang phân tích chiến lược..."):
            from gemini_assistant import get_ai_response
            
            churn_context = {
                'high_risk_count': stats['churn_analysis']['high_risk_count'],
                'high_risk_pct': stats['churn_analysis']['high_risk_percentage'],
                'expiring_7d': stats['churn_analysis']['expiring_within_7_days'],
                'expiring_30d': stats['churn_analysis']['expiring_within_30_days'],
                'already_expired': stats['churn_analysis']['already_expired'],
                'avg_days_to_expire': stats['churn_analysis']['avg_days_to_expire']
            }
            
            question = f"""
            Phân tích tình hình churn và đưa ra chiến lược giữ chân cụ thể:
            - {churn_context['high_risk_count']:,} khách hàng nguy cơ cao
            - {churn_context['expiring_7d']:,} sắp hết hạn trong 7 ngày
            - {churn_context['expiring_30d']:,} sắp hết hạn trong 30 ngày
            
            Hãy đưa ra:
            1. Root causes (nguyên nhân gốc rễ)
            2. Immediate actions (7 ngày) - cụ thể, có số liệu
            3. Short-term strategy (30 ngày)
            4. Expected ROI và KPIs cần theo dõi
            """
            
            ai_strategy = get_ai_response(question, churn_context, 'vi')
            st.markdown(ai_strategy)


with tab4:
    st.markdown("### 👥 Customer Segmentation")
    
    # Segment matrix
    segment_matrix = stats['segmentation']['segment_matrix']
    
    # Convert to DataFrame for display
    segment_data = []
    for key, value in segment_matrix.items():
        parts = key.split('_')
        tkc_seg = parts[0]
        service_status = 'With Service' if 'with_service' in key else 'No Service'
        segment_data.append({
            'TKC Segment': tkc_seg,
            'Service Status': service_status,
            'Customer Count': value['customer_count'],
            'Avg TKC': f"{value['avg_tkc']:,.0f}",
            'Churn Risk Rate': f"{value['churn_risk_rate']*100:.1f}%"
        })
    
    segment_df = pd.DataFrame(segment_data)
    st.dataframe(segment_df, use_container_width=True, hide_index=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.success(f"🌟 High Value Customers: {stats['segmentation']['high_value_customers']:,}")
    with col2:
        st.warning(f"⚠️ At-Risk High Value: {stats['segmentation']['at_risk_high_value']:,}")
    
    # AI Marketing Strategy
    st.markdown("---")
    if st.button("🔮 AI Chiến Lược Marketing Cho Từng Segment", key="ai_segment", use_container_width=True):
        with st.spinner("🤖 AI đang tạo chiến lược marketing..."):
            from gemini_assistant import get_ai_response
            
            segment_context = {
                'segment_matrix': stats['segmentation']['segment_matrix'],
                'high_value': stats['segmentation']['high_value_customers'],
                'at_risk_high_value': stats['segmentation']['at_risk_high_value']
            }
            
            question = """
            Tạo chiến lược marketing chi tiết cho TỪNG segment khách hàng.
            
            Cho mỗi segment, hãy cung cấp:
            1. Profile & đặc điểm khách hàng
            2. Value Proposition (lợi ích chính)
            3. Channels (SMS, Email, Call...) và lý do
            4. Offers cụ thể (ưu đãi, khuyến mãi)
            5. Messaging (nội dung truyền thông)
            6. Budget allocation (% ngân sách)
            7. KPIs mục tiêu (conversion, retention rate)
            
            Ví dụ campaigns cụ thể cho VNPT.
            """
            
            ai_strategy = get_ai_response(question, segment_context, 'vi')
            st.markdown(ai_strategy)


st.markdown("---")

# Business Insights
st.markdown("### 💡 Business Insights")

insights = st.session_state.stats.get('insights', [])

if insights:
    for i, insight in enumerate(insights, 1):
        severity_color = {
            'Critical': '🔴',
            'High': '🟠',
            'Medium': '🟡',
            'Low': '🟢'
        }
        
        icon = severity_color.get(insight['severity'], '📌')
        
        with st.expander(f"{icon} {i}. [{insight['severity']}] {insight['category']}", expanded=True):
            st.markdown(f"**Insight:** {insight['insight']}")
            st.markdown(f"**Recommendation:** {insight['recommendation']}")

st.markdown("---")

# Navigation
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.button("⬅️ Làm Sạch Dữ Liệu", use_container_width=True):
        st.switch_page("pages/2_🧹_Data_Cleaning.py")

with col3:
    if st.button("Tiếp Theo: Visualization ➡️", use_container_width=True):
        st.session_state.current_step = 4
        st.switch_page("pages/4_📉_Visualization.py")

st.session_state.current_step = max(st.session_state.current_step, 3)
