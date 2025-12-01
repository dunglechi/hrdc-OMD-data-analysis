"""
Page 4: Visualization
Tạo biểu đồ tương tác
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Visualization", page_icon="📉", layout="wide")

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
    <h1>📉 Bước 4: Trực Quan Hóa Dữ Liệu</h1>
    <p>Tạo biểu đồ tương tác để khám phá insights</p>
</div>
""", unsafe_allow_html=True)

# Chart selector
st.markdown("### 📊 Chọn Loại Biểu Đồ")

chart_type = st.selectbox(
    "Loại biểu đồ",
    ["TKC Distribution", "Service Adoption", "Churn Risk", "Geographic Distribution", 
     "Staff Performance", "Temporal Trends", "Custom Chart"]
)

st.markdown("---")

# VNPT Colors
VNPT_BLUE = '#0066B2'
VNPT_COLORS = ['#0066B2', '#00A3E0', '#0080C0', '#004D99', '#003366']

if chart_type == "TKC Distribution":
    st.markdown("### 💰 Phân Bố TKC")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Histogram
        fig = px.histogram(
            df, 
            x='TOTAL_TKC',
            nbins=50,
            title="TKC Distribution (Histogram)",
            color_discrete_sequence=[VNPT_BLUE],
            labels={'TOTAL_TKC': 'Total TKC (VNĐ)'}
        )
        fig.add_vline(x=df['TOTAL_TKC'].mean(), line_dash="dash", line_color="red",
                     annotation_text=f"Mean: {df['TOTAL_TKC'].mean():,.0f}")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Pie chart
        if 'TKC_SEGMENT' in df.columns:
            segment_counts = df['TKC_SEGMENT'].value_counts()
            fig = px.pie(
                values=segment_counts.values,
                names=segment_counts.index,
                title="TKC Segments",
                color_discrete_sequence=VNPT_COLORS
            )
            st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Service Adoption":
    st.markdown("### 📱 Service Adoption")
    
    if 'HAS_SERVICE' in df.columns:
        service_counts = df['HAS_SERVICE'].value_counts()
        
        fig = px.bar(
            x=['With Service', 'No Service'],
            y=[service_counts.get(True, 0), service_counts.get(False, 0)],
            title="Service Adoption Rate",
            labels={'x': 'Status', 'y': 'Number of Customers'},
            color=['With Service', 'No Service'],
            color_discrete_map={'With Service': VNPT_BLUE, 'No Service': '#CCCCCC'}
        )
        
        # Add percentages
        total = len(df)
        fig.update_traces(
            text=[f"{service_counts.get(True, 0)/total*100:.1f}%", 
                  f"{service_counts.get(False, 0)/total*100:.1f}%"],
            textposition='outside'
        )
        
        st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Churn Risk":
    st.markdown("### ⚠️ Churn Risk Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'CHURN_RISK' in df.columns:
            churn_counts = df['CHURN_RISK'].value_counts()
            
            fig = px.bar(
                x=churn_counts.index,
                y=churn_counts.values,
                title="Churn Risk Distribution",
                labels={'x': 'Risk Level', 'y': 'Number of Customers'},
                color=churn_counts.index,
                color_discrete_map={'High': '#FF4444', 'Low': '#44FF44'}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if 'DAYS_TO_EXPIRE' in df.columns:
            days_filtered = df[df['DAYS_TO_EXPIRE'] < 100]['DAYS_TO_EXPIRE']
            
            fig = px.histogram(
                days_filtered,
                nbins=30,
                title="Days to Expiration (<100 days)",
                color_discrete_sequence=[VNPT_BLUE],
                labels={'value': 'Days to Expire'}
            )
            fig.add_vline(x=30, line_dash="dash", line_color="red",
                         annotation_text="30-day threshold")
            st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Geographic Distribution":
    st.markdown("### 🗺️ Phân Bố Địa Lý")
    
    if 'PROVINCE_NAME' in df.columns:
        province_counts = df['PROVINCE_NAME'].value_counts().head(10)
        
        fig = px.bar(
            y=province_counts.index,
            x=province_counts.values,
            orientation='h',
            title="Top 10 Provinces by Customer Count",
            labels={'x': 'Number of Customers', 'y': 'Province'},
            color_discrete_sequence=[VNPT_BLUE]
        )
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Staff Performance":
    st.markdown("### 👥 Staff Performance")
    
    if 'STAFF_CODE' in df.columns:
        staff_stats = df[df['STAFF_CODE'] != 'UNASSIGNED'].groupby('STAFF_CODE').size().sort_values(ascending=False).head(10)
        
        fig = px.bar(
            x=staff_stats.index,
            y=staff_stats.values,
            title="Top 10 Staff by Customer Count",
            labels={'x': 'Staff Code', 'y': 'Number of Customers'},
            color_discrete_sequence=[VNPT_BLUE]
        )
        st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Temporal Trends":
    st.markdown("### 📅 Temporal Trends")
    
    if 'DATE_ENTER_ACTIVE' in df.columns:
        df['activation_month'] = pd.to_datetime(df['DATE_ENTER_ACTIVE']).dt.to_period('M')
        monthly_data = df.groupby('activation_month').size().tail(24)
        
        # Convert Period to string for plotting
        monthly_df = pd.DataFrame({
            'Month': [str(m) for m in monthly_data.index],
            'Activations': monthly_data.values
        })
        
        fig = px.line(
            monthly_df,
            x='Month',
            y='Activations',
            title="Customer Activation Trend (Last 24 Months)",
            markers=True,
            color_discrete_sequence=[VNPT_BLUE]
        )
        st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Custom Chart":
    st.markdown("### 🎨 Custom Chart Builder")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        chart_style = st.selectbox("Chart Type", ["Bar", "Line", "Scatter", "Box", "Histogram"])
    
    with col2:
        x_col = st.selectbox("X Axis", df.columns)
    
    with col3:
        if chart_style in ["Bar", "Line", "Scatter", "Box"]:
            y_col = st.selectbox("Y Axis", df.select_dtypes(include=['int64', 'float64']).columns)
    
    if st.button("🎨 Generate Chart", use_container_width=True):
        try:
            if chart_style == "Bar":
                fig = px.bar(df, x=x_col, y=y_col, color_discrete_sequence=[VNPT_BLUE])
            elif chart_style == "Line":
                fig = px.line(df, x=x_col, y=y_col, color_discrete_sequence=[VNPT_BLUE])
            elif chart_style == "Scatter":
                fig = px.scatter(df, x=x_col, y=y_col, color_discrete_sequence=[VNPT_BLUE])
            elif chart_style == "Box":
                fig = px.box(df, x=x_col, y=y_col, color_discrete_sequence=[VNPT_BLUE])
            elif chart_style == "Histogram":
                fig = px.histogram(df, x=x_col, color_discrete_sequence=[VNPT_BLUE])
            
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating chart: {str(e)}")

st.markdown("---")

# Navigation
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.button("⬅️ Phân Tích Thống Kê", use_container_width=True):
        st.switch_page("pages/3_📈_Statistical_Analysis.py")

with col3:
    if st.button("Tiếp Theo: Export Results ➡️", use_container_width=True):
        st.session_state.current_step = 5
        st.info("Export page coming soon! Use download buttons in other pages.")

st.session_state.current_step = max(st.session_state.current_step, 4)
