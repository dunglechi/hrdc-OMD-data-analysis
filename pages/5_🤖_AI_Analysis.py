"""
Page 5: AI-Powered Analysis
Machine Learning phân tích chuyên sâu
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, IsolationForest
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, classification_report
from sklearn.decomposition import PCA
import sys
sys.path.append('..')
from translations import get_text, get_lang

st.set_page_config(page_title="Phân Tích AI", page_icon="🤖", layout="wide")

# Initialize session state if not exists
if 'df_cleaned' not in st.session_state:
    st.session_state.df_cleaned = None

# Check if cleaned data exists
if st.session_state.df_cleaned is None:
    st.warning("⚠️ Chưa có dữ liệu đã làm sạch! Vui lòng hoàn tất bước Data Cleaning.")
    if st.button("🧹 Đến Data Cleaning"):
        st.switch_page("pages/2_🧹_Data_Cleaning.py")
    st.stop()

df = st.session_state.df_cleaned.copy()
lang = get_lang()

# Header
st.markdown("""
<div style="background: linear-gradient(90deg, #0066B2 0%, #00A3E0 100%); padding: 1.5rem; border-radius: 10px; color: white; margin-bottom: 2rem;">
    <h1>🤖 AI-Powered Analysis</h1>
    <p>Phân tích chuyên sâu với Machine Learning</p>
</div>
""", unsafe_allow_html=True)

# VNPT Colors
VNPT_BLUE = '#0066B2'
VNPT_COLORS = ['#0066B2', '#00A3E0', '#0080C0', '#004D99', '#003366']

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎯 Churn Prediction", 
    "👥 Customer Segmentation", 
    "🔍 Anomaly Detection",
    "🏆 Model Comparison",
    "📊 Feature Importance"
])

# ============= TAB 1: CHURN PREDICTION =============
with tab1:
    st.markdown("### 🎯 Churn Prediction - Dự Đoán Khách Hàng Rời Bỏ")
    
    st.info("""
    **Mục đích**: Dự đoán khách hàng nào có nguy cơ cao rời bỏ dịch vụ  
    **Model**: Random Forest Classifier  
    **Features**: TOTAL_TKC, ACCOUNT_AGE, DAYS_TO_EXPIRE, HAS_SERVICE
    """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("🚀 Train Churn Prediction Model", use_container_width=True, type="primary"):
            with st.spinner("Đang training model..."):
                # Prepare features
                feature_cols = ['TOTAL_TKC', 'ACCOUNT_AGE', 'DAYS_TO_EXPIRE']
                
                # Add HAS_SERVICE as numeric
                df['HAS_SERVICE_NUM'] = df['HAS_SERVICE'].astype(int)
                feature_cols.append('HAS_SERVICE_NUM')
                
                X = df[feature_cols].fillna(0)
                y = (df['CHURN_RISK'] == 'High').astype(int)
                
                # Train/test split
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                
                # Train model
                model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
                model.fit(X_train, y_train)
                
                # Predictions
                y_pred = model.predict(X_test)
                y_pred_proba = model.predict_proba(X_test)[:, 1]
                
                # Full dataset predictions
                churn_probs = model.predict_proba(X)[:, 1]
                df['CHURN_PROBABILITY'] = churn_probs
                df['PREDICTED_CHURN'] = (churn_probs > 0.5).astype(int)
                
                # Store in session
                st.session_state.churn_model = model
                st.session_state.df_with_predictions = df
                
                # Metrics
                accuracy = accuracy_score(y_test, y_pred)
                f1 = f1_score(y_test, y_pred)
                
                st.success(f"✅ Model trained successfully!")
                
                col_m1, col_m2, col_m3 = st.columns(3)
                with col_m1:
                    st.metric("Accuracy", f"{accuracy*100:.1f}%")
                with col_m2:
                    st.metric("F1 Score", f"{f1:.3f}")
                with col_m3:
                    high_risk = (churn_probs > 0.7).sum()
                    st.metric("High Risk Customers", f"{high_risk:,}")
    
    with col2:
        st.markdown("**Model Parameters:**")
        st.write("- Estimators: 100")
        st.write("- Max Depth: 10")
        st.write("- Train/Test: 80/20")
        st.write("- Random State: 42")
    
    # Show results if model exists
    if 'churn_model' in st.session_state:
        st.markdown("---")
        st.markdown("### 📊 Prediction Results")
        
        df_pred = st.session_state.df_with_predictions
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Probability distribution
            fig = px.histogram(
                df_pred, 
                x='CHURN_PROBABILITY',
                nbins=50,
                title="Churn Probability Distribution",
                color_discrete_sequence=[VNPT_BLUE],
                labels={'CHURN_PROBABILITY': 'Churn Probability'}
            )
            fig.add_vline(x=0.5, line_dash="dash", line_color="red", annotation_text="Threshold: 0.5")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Risk segments
            df_pred['RISK_SEGMENT'] = pd.cut(
                df_pred['CHURN_PROBABILITY'],
                bins=[0, 0.3, 0.5, 0.7, 1.0],
                labels=['Low', 'Medium', 'High', 'Critical']
            )
            
            risk_counts = df_pred['RISK_SEGMENT'].value_counts()
            
            fig = px.pie(
                values=risk_counts.values,
                names=risk_counts.index,
                title="Risk Segments",
                color_discrete_sequence=['#44FF44', '#FFD700', '#FFA500', '#FF4444']
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Top high-risk customers
        st.markdown("### 🚨 Top 100 High-Risk Customers")
        
        top_risk = df_pred.nlargest(100, 'CHURN_PROBABILITY')[
            ['Phone number', 'CHURN_PROBABILITY', 'TOTAL_TKC', 'ACCOUNT_AGE', 'DAYS_TO_EXPIRE', 'HAS_SERVICE']
        ]
        top_risk['CHURN_PROBABILITY'] = (top_risk['CHURN_PROBABILITY'] * 100).round(1).astype(str) + '%'
        
        st.dataframe(top_risk, use_container_width=True, hide_index=True)
        
        # Download button
        csv = top_risk.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download High-Risk Customers (CSV)",
            data=csv,
            file_name="high_risk_customers.csv",
            mime="text/csv",
            use_container_width=True
        )

# ============= TAB 2: CUSTOMER SEGMENTATION =============
with tab2:
    st.markdown("### 👥 Customer Segmentation - Phân Khúc Khách Hàng Tự Động")
    
    st.info("""
    **Mục đích**: Tự động phân nhóm khách hàng thành các segments  
    **Algorithm**: K-Means Clustering  
    **Features**: TOTAL_TKC, ACCOUNT_AGE, HAS_SERVICE, CHURN_RISK
    """)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        n_clusters = st.slider("Số lượng segments", 2, 8, 4)
    
    with col2:
        if st.button("🎨 Run Segmentation", use_container_width=True, type="primary"):
            with st.spinner("Đang phân khúc khách hàng..."):
                # Prepare features
                features_seg = ['TOTAL_TKC', 'ACCOUNT_AGE']
                df['HAS_SERVICE_NUM'] = df['HAS_SERVICE'].astype(int)
                df['CHURN_RISK_NUM'] = (df['CHURN_RISK'] == 'High').astype(int)
                features_seg.extend(['HAS_SERVICE_NUM', 'CHURN_RISK_NUM'])
                
                X_seg = df[features_seg].fillna(0)
                
                # Standardize
                scaler = StandardScaler()
                X_scaled = scaler.fit_transform(X_seg)
                
                # K-Means
                kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
                df['AI_SEGMENT'] = kmeans.fit_predict(X_scaled)
                
                # PCA for visualization
                pca = PCA(n_components=2)
                X_pca = pca.fit_transform(X_scaled)
                df['PCA1'] = X_pca[:, 0]
                df['PCA2'] = X_pca[:, 1]
                
                # Store
                st.session_state.segmentation_df = df
                st.session_state.kmeans_model = kmeans
                
                st.success(f"✅ Đã phân khúc thành {n_clusters} segments!")
    
    # Show results
    if 'segmentation_df' in st.session_state:
        df_seg = st.session_state.segmentation_df
        
        st.markdown("---")
        st.markdown("### 📊 Segmentation Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 2D scatter plot
            fig = px.scatter(
                df_seg,
                x='PCA1',
                y='PCA2',
                color='AI_SEGMENT',
                title="Customer Segments (PCA Visualization)",
                color_continuous_scale=VNPT_COLORS,
                labels={'AI_SEGMENT': 'Segment'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Segment sizes
            segment_counts = df_seg['AI_SEGMENT'].value_counts().sort_index()
            
            fig = px.bar(
                x=[f"Segment {i}" for i in segment_counts.index],
                y=segment_counts.values,
                title="Segment Sizes",
                color=segment_counts.values,
                color_continuous_scale=VNPT_COLORS,
                labels={'x': 'Segment', 'y': 'Number of Customers'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Segment characteristics
        st.markdown("### 📋 Segment Characteristics")
        
        segment_stats = df_seg.groupby('AI_SEGMENT').agg({
            'Phone number': 'count',
            'TOTAL_TKC': 'mean',
            'ACCOUNT_AGE': 'mean',
            'HAS_SERVICE': lambda x: x.sum() / len(x) * 100,
            'CHURN_RISK_NUM': lambda x: x.sum() / len(x) * 100
        }).round(2)
        
        segment_stats.columns = ['Customer Count', 'Avg TKC', 'Avg Account Age', 'Service Rate (%)', 'High Churn Risk (%)']
        segment_stats.index = [f"Segment {i}" for i in segment_stats.index]
        
        st.dataframe(segment_stats, use_container_width=True)

# ============= TAB 3: ANOMALY DETECTION =============
with tab3:
    st.markdown("### 🔍 Anomaly Detection - Phát Hiện Bất Thường")
    
    st.info("""
    **Mục đích**: Tìm khách hàng có hành vi bất thường  
    **Algorithm**: Isolation Forest  
    **Use case**: Fraud detection, special cases
    """)
    
    contamination = st.slider("Contamination (% anomalies)", 1, 20, 5) / 100
    
    if st.button("🔎 Detect Anomalies", use_container_width=True, type="primary"):
        with st.spinner("Đang phát hiện anomalies..."):
            # Features
            features_anom = ['TOTAL_TKC', 'ACCOUNT_AGE', 'DAYS_TO_EXPIRE']
            X_anom = df[features_anom].fillna(0)
            
            # Isolation Forest
            iso_forest = IsolationForest(contamination=contamination, random_state=42)
            df['ANOMALY'] = iso_forest.fit_predict(X_anom)
            df['ANOMALY_SCORE'] = iso_forest.score_samples(X_anom)
            
            # Store
            st.session_state.anomaly_df = df
            
            anomaly_count = (df['ANOMALY'] == -1).sum()
            st.success(f"✅ Detected {anomaly_count:,} anomalies ({anomaly_count/len(df)*100:.1f}%)")
    
    # Show results
    if 'anomaly_df' in st.session_state:
        df_anom = st.session_state.anomaly_df
        
        st.markdown("---")
        st.markdown("### 📊 Anomaly Detection Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Anomaly score distribution
            fig = px.histogram(
                df_anom,
                x='ANOMALY_SCORE',
                color='ANOMALY',
                title="Anomaly Score Distribution",
                color_discrete_map={1: '#44FF44', -1: '#FF4444'},
                labels={'ANOMALY': 'Type', 'ANOMALY_SCORE': 'Anomaly Score'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Anomaly counts
            anom_counts = df_anom['ANOMALY'].value_counts()
            
            fig = px.pie(
                values=anom_counts.values,
                names=['Normal' if x == 1 else 'Anomaly' for x in anom_counts.index],
                title="Normal vs Anomaly",
                color_discrete_sequence=['#44FF44', '#FF4444']
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Top anomalies
        st.markdown("### 🚨 Top 50 Anomalies")
        
        anomalies = df_anom[df_anom['ANOMALY'] == -1].nsmallest(50, 'ANOMALY_SCORE')[
            ['Phone number', 'ANOMALY_SCORE', 'TOTAL_TKC', 'ACCOUNT_AGE', 'DAYS_TO_EXPIRE']
        ]
        
        st.dataframe(anomalies, use_container_width=True, hide_index=True)

# ============= TAB 4: MODEL COMPARISON =============
with tab4:
    st.markdown("### 🏆 AutoML Model Comparison")
    
    st.info("""
    **Mục đích**: So sánh hiệu suất của nhiều ML models  
    **Models**: Random Forest, Gradient Boosting, Logistic Regression  
    **Target**: Churn Risk (High/Low)
    """)
    
    if st.button("🏁 Compare Models", use_container_width=True, type="primary"):
        with st.spinner("Training multiple models..."):
            # Prepare data
            feature_cols = ['TOTAL_TKC', 'ACCOUNT_AGE', 'DAYS_TO_EXPIRE', 'HAS_SERVICE_NUM']
            df['HAS_SERVICE_NUM'] = df['HAS_SERVICE'].astype(int)
            
            X = df[feature_cols].fillna(0)
            y = (df['CHURN_RISK'] == 'High').astype(int)
            
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Models
            models = {
                'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
                'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
                'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000)
            }
            
            results = []
            
            for name, model in models.items():
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                
                acc = accuracy_score(y_test, y_pred)
                f1 = f1_score(y_test, y_pred)
                
                results.append({
                    'Model': name,
                    'Accuracy': f"{acc*100:.2f}%",
                    'F1 Score': f"{f1:.3f}",
                    'Accuracy_num': acc,
                    'F1_num': f1
                })
            
            results_df = pd.DataFrame(results)
            st.session_state.model_comparison = results_df
            
            st.success("✅ Model comparison completed!")
    
    # Show results
    if 'model_comparison' in st.session_state:
        results_df = st.session_state.model_comparison
        
        st.markdown("---")
        st.markdown("### 📊 Comparison Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Table
            display_df = results_df[['Model', 'Accuracy', 'F1 Score']]
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            # Best model
            best_model = results_df.loc[results_df['Accuracy_num'].idxmax(), 'Model']
            st.success(f"🏆 Best Model: **{best_model}**")
        
        with col2:
            # Bar chart
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                name='Accuracy',
                x=results_df['Model'],
                y=results_df['Accuracy_num'],
                marker_color=VNPT_BLUE
            ))
            
            fig.add_trace(go.Bar(
                name='F1 Score',
                x=results_df['Model'],
                y=results_df['F1_num'],
                marker_color='#00A3E0'
            ))
            
            fig.update_layout(
                title="Model Performance Comparison",
                barmode='group',
                yaxis_title="Score"
            )
            
            st.plotly_chart(fig, use_container_width=True)

# ============= TAB 5: FEATURE IMPORTANCE =============
with tab5:
    st.markdown("### 📊 Feature Importance Analysis")
    
    st.info("""
    **Mục đích**: Xác định features nào quan trọng nhất  
    **Model**: Random Forest Feature Importance  
    **Insight**: Hiểu yếu tố nào ảnh hưởng đến churn
    """)
    
    if 'churn_model' in st.session_state:
        model = st.session_state.churn_model
        
        # Feature importance
        feature_names = ['TOTAL_TKC', 'ACCOUNT_AGE', 'DAYS_TO_EXPIRE', 'HAS_SERVICE']
        importances = model.feature_importances_
        
        importance_df = pd.DataFrame({
            'Feature': feature_names,
            'Importance': importances
        }).sort_values('Importance', ascending=False)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Bar chart
            fig = px.bar(
                importance_df,
                x='Importance',
                y='Feature',
                orientation='h',
                title="Feature Importance",
                color='Importance',
                color_continuous_scale=[[0, '#90EE90'], [1, VNPT_BLUE]]
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("**Importance Scores:**")
            for idx, row in importance_df.iterrows():
                st.metric(row['Feature'], f"{row['Importance']:.3f}")
        
        # Interpretation
        st.markdown("---")
        st.markdown("### 💡 Interpretation")
        
        top_feature = importance_df.iloc[0]
        
        st.success(f"""
        **Most Important Feature**: `{top_feature['Feature']}` (importance: {top_feature['Importance']:.3f})
        
        This feature has the highest impact on predicting customer churn.
        Focus on this metric when designing retention strategies.
        """)
    
    else:
        st.warning("⚠️ Please train the Churn Prediction model first (Tab 1)")

st.markdown("---")

# Navigation
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.button("⬅️ Visualization", use_container_width=True):
        st.switch_page("pages/4_📉_Visualization.py")

with col3:
    st.info("✅ All analysis complete!")

st.session_state.current_step = max(st.session_state.current_step, 5)
