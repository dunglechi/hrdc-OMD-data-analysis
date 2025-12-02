"""
Page 0: Column Dictionary
Quản lý và chỉnh sửa ý nghĩa các cột
"""

import streamlit as st
import pandas as pd
from column_dictionary import initialize_column_dictionary

st.set_page_config(page_title="Column Dictionary", page_icon="📖", layout="wide")

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
    <h1>📖 Column Dictionary</h1>
    <p>AI tự động phân tích và đoán ý nghĩa các cột. Kiểm tra và sửa nếu cần.</p>
</div>
""", unsafe_allow_html=True)

# Initialize or load column dictionary
col_dict = initialize_column_dictionary(df)

# Summary stats
st.markdown("### 📊 Tổng Quan")

col1, col2, col3, col4 = st.columns(4)

stats = col_dict.get_summary_stats()

with col1:
    st.metric("Tổng số cột", stats['total_columns'])
with col2:
    st.metric("AI đoán", stats['ai_inferred'], 
             help="Số cột được AI tự động đoán ý nghĩa")
with col3:
    st.metric("User sửa", stats['user_edited'],
             help="Số cột đã được user chỉnh sửa")
with col4:
    st.metric("Độ tin cậy TB", f"{stats['avg_confidence']:.0%}",
             help="Độ tin cậy trung bình của AI")

# Reset button
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🔄 Reset & Chạy Lại AI (Áp dụng code mới)", use_container_width=True, type="secondary"):
        # Clear old dictionary
        if 'column_dictionary' in st.session_state:
            del st.session_state.column_dictionary
        if 'column_dict_obj' in st.session_state:
            del st.session_state.column_dict_obj
        
        st.success("✅ Đã xóa dictionary cũ!")
        st.info("🔄 Đang chạy lại AI với code mới...")
        st.rerun()


st.markdown("---")

# Action buttons
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🔄 Re-run AI Detection", use_container_width=True):
        with st.spinner("🤖 AI đang phân tích lại..."):
            col_dict.auto_detect_meanings()
            col_dict.save_to_session()
            st.success("✓ Đã phân tích lại!")
            st.rerun()

with col2:
    if st.button("📥 Import Dictionary", use_container_width=True):
        st.session_state.show_import = True

with col3:
    if st.button("📤 Export Dictionary", use_container_width=True):
        json_str = col_dict.export_to_json()
        st.download_button(
            label="💾 Download JSON",
            data=json_str,
            file_name="column_dictionary.json",
            mime="application/json"
        )

with col4:
    if st.button("✅ Confirm & Continue", use_container_width=True, type="primary"):
        col_dict.save_to_session()
        st.success("✓ Đã lưu! Chuyển sang Data Exploration...")
        st.session_state.current_step = 1
        st.switch_page("pages/1_📊_Data_Exploration.py")

# Import dialog
if st.session_state.get('show_import', False):
    with st.expander("📥 Import Dictionary from JSON", expanded=True):
        uploaded_json = st.file_uploader("Upload JSON file", type=['json'])
        if uploaded_json:
            try:
                json_str = uploaded_json.read().decode('utf-8')
                col_dict.import_from_json(json_str)
                col_dict.save_to_session()
                st.success("✓ Đã import thành công!")
                st.session_state.show_import = False
                st.rerun()
            except Exception as e:
                st.error(f"❌ Lỗi import: {str(e)}")

st.markdown("---")

# Validation Section
st.markdown("### ✅ Validation - Kiểm Tra Định Nghĩa")

issues = []
warnings = []

for col, info in col_dict.dictionary.items():
    # Check confidence
    if info.get('confidence', 0) < 0.5:
        issues.append({
            'column': col,
            'type': 'low_confidence',
            'message': f"Confidence rất thấp ({info.get('confidence', 0):.0%})",
            'suggestion': "Vui lòng kiểm tra và sửa thủ công"
        })
    elif info.get('confidence', 0) < 0.7:
        warnings.append({
            'column': col,
            'type': 'medium_confidence',
            'message': f"Confidence trung bình ({info.get('confidence', 0):.0%})",
            'suggestion': "Nên kiểm tra lại"
        })
    
    # Check common mistakes - TKC
    if 'TKC' in col.upper():
        meaning_lower = info.get('meaning_vi', '').lower()
        if 'khuyến' in meaning_lower or 'khuyên' in meaning_lower:
            issues.append({
                'column': col,
                'type': 'wrong_meaning',
                'message': f"❌ SAI: '{info.get('meaning_vi')}' - TKC = Tài khoản chính, KHÔNG phải Tiền khuyến cáo",
                'suggestion': "Sửa thành: 'Tài khoản chính' hoặc 'Tổng tiền trong tài khoản chính'"
            })

# Display validation results
if issues:
    st.error(f"🚨 Phát hiện {len(issues)} vấn đề NGHIÊM TRỌNG:")
    for issue in issues:
        with st.container():
            st.markdown(f"**{issue['column']}**: {issue['message']}")
            st.info(f"💡 {issue['suggestion']}")
    st.warning("⚠️ **KHÔNG THỂ TIẾP TỤC** cho đến khi sửa các vấn đề trên!")
    
elif warnings:
    st.warning(f"⚠️ Có {len(warnings)} cảnh báo:")
    for warn in warnings:
        st.markdown(f"- **{warn['column']}**: {warn['message']} - {warn['suggestion']}")
    st.info("💡 Bạn có thể tiếp tục nhưng nên kiểm tra lại các cột trên")
    
else:
    st.success("✅ **Tất cả định nghĩa đã được kiểm tra và chính xác!**")
    st.balloons()

st.markdown("---")
st.markdown("### ✏️ Chỉnh Sửa Ý Nghĩa Các Cột")

# Filter options
col1, col2 = st.columns([2, 1])

with col1:
    search = st.text_input("🔍 Tìm kiếm cột", placeholder="Nhập tên cột...")

with col2:
    category_filter = st.selectbox(
        "Lọc theo category",
        ["All"] + list(set(info['category'] for info in col_dict.dictionary.values()))
    )

# Display columns
for col in df.columns:
    # Apply filters
    if search and search.lower() not in col.lower():
        continue
    
    if category_filter != "All" and col_dict.get_category(col) != category_filter:
        continue
    
    col_info = col_dict.dictionary.get(col, {})
    confidence = col_info.get('confidence', 0)
    user_edited = col_info.get('user_edited', False)
    
    # Color code based on confidence
    if user_edited:
        border_color = "#00A3FF"  # Blue for user edited
        badge = "👤 User"
    elif confidence >= 0.8:
        border_color = "#10B981"  # Green for high confidence
        badge = f"🤖 AI ({confidence:.0%})"
    elif confidence >= 0.5:
        border_color = "#F59E0B"  # Orange for medium confidence
        badge = f"⚠️ AI ({confidence:.0%})"
    else:
        border_color = "#EF4444"  # Red for low confidence
        badge = f"❌ AI ({confidence:.0%})"
    
    with st.expander(f"📊 **{col}** - {badge}", expanded=False):
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Column metadata
            st.markdown("**Thông tin cột:**")
            st.markdown(f"- **Data Type**: `{df[col].dtype}`")
            st.markdown(f"- **Unique**: {df[col].nunique():,}")
            st.markdown(f"- **Missing**: {df[col].isnull().sum():,} ({df[col].isnull().sum()/len(df)*100:.1f}%)")
            st.markdown(f"- **Category**: {col_info.get('category', 'N/A')}")
            
            # Sample values
            st.markdown("**Mẫu dữ liệu:**")
            sample = df[col].dropna().head(3).tolist()
            for val in sample:
                st.code(str(val), language=None)
        
        with col2:
            # Editable meaning
            st.markdown("**Ý nghĩa:**")
            
            current_meaning_vi = col_info.get('meaning_vi', col)
            current_meaning_en = col_info.get('meaning_en', col)
            
            new_meaning_vi = st.text_area(
                "Tiếng Việt",
                value=current_meaning_vi,
                key=f"vi_{col}",
                height=60,
                help="Mô tả ý nghĩa của cột bằng tiếng Việt"
            )
            
            new_meaning_en = st.text_input(
                "English",
                value=current_meaning_en,
                key=f"en_{col}",
                help="English meaning of the column"
            )
            
            # Save button
            col_a, col_b = st.columns([1, 1])
            
            with col_a:
                if st.button("💾 Lưu", key=f"save_{col}", use_container_width=True):
                    col_dict.update_meaning(col, new_meaning_vi, new_meaning_en)
                    col_dict.save_to_session()
                    st.success("✓ Đã lưu!")
                    st.rerun()
            
            with col_b:
                if user_edited and st.button("🔄 Reset AI", key=f"reset_{col}", use_container_width=True):
                    # Restore original AI meaning
                    original = col_info.get('original_ai_meaning', col)
                    col_dict.update_meaning(col, original, original)
                    col_dict.dictionary[col]['user_edited'] = False
                    col_dict.save_to_session()
                    st.success("✓ Đã reset!")
                    st.rerun()
            
            # Show AI reasoning
            if 'reasoning' in col_info:
                st.info(f"💡 **AI Reasoning**: {col_info['reasoning']}")

st.markdown("---")

# Navigation
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.button("⬅️ Về Trang Chủ", use_container_width=True):
        st.switch_page("app.py")

with col3:
    if st.button("Tiếp Theo: Data Exploration ➡️", use_container_width=True):
        col_dict.save_to_session()
        st.session_state.current_step = 1
        st.switch_page("pages/1_📊_Data_Exploration.py")

# Update step
st.session_state.current_step = max(st.session_state.current_step, 0)
