"""
Hệ thống giải thích thuật ngữ và hướng dẫn cho người dùng không chuyên
User-friendly explanations for non-technical users
"""

# Giải thích các thuật ngữ kỹ thuật
TERM_EXPLANATIONS = {
    'vi': {
        # Data Cleaning Terms
        'missing_values': {
            'term': 'Giá trị thiếu (Missing Values)',
            'explain': 'Là những ô trống trong bảng dữ liệu - nơi không có thông tin.',
            'example': 'Ví dụ: Một khách hàng không có số điện thoại được ghi nhận.',
            'why_important': 'Quan trọng vì: Dữ liệu thiếu có thể làm sai lệch kết quả phân tích.'
        },
        'keep_null': {
            'term': 'Giữ nguyên (Keep NULL)',
            'explain': 'Để trống các ô không có dữ liệu, không thay đổi gì.',
            'when_use': 'Dùng khi: Bạn muốn xem rõ dữ liệu nào đang thiếu.'
        },
        'mode': {
            'term': 'Giá trị phổ biến nhất (Mode)',
            'explain': 'Điền vào ô trống bằng giá trị xuất hiện nhiều nhất.',
            'example': 'Ví dụ: Nếu 100 người có TKC = 0, thì điền 0 vào các ô trống về TKC.',
            'when_use': 'Dùng khi: Muốn điền giá trị "an toàn" nhất.'
        },
        'forward_fill': {
            'term': 'Sao chép từ trên xuống (Forward Fill)',
            'explain': 'Điền ô trống bằng giá trị của ô phía trên.',
            'example': 'Ví dụ: Nếu dòng 1 có "Hà Nội", dòng 2 trống → Điền "Hà Nội" vào dòng 2.',
            'when_use': 'Dùng khi: Dữ liệu có xu hướng giống nhau theo thời gian.'
        },
        'custom_value': {
            'term': 'Giá trị tùy chỉnh (Custom Value)',
            'explain': 'Bạn tự chọn một giá trị để điền vào tất cả ô trống.',
            'example': 'Ví dụ: Điền "Không rõ" vào tất cả ô trống về địa chỉ.',
            'when_use': 'Dùng khi: Bạn muốn đánh dấu rõ ràng dữ liệu thiếu.'
        },
        
        # Derived Columns
        'derived_columns': {
            'term': 'Cột tính toán (Derived Columns)',
            'explain': 'Là các cột mới được tạo ra từ dữ liệu hiện có.',
            'example': 'Ví dụ: Từ ngày kích hoạt và ngày hết hạn → Tính "Tuổi tài khoản".',
            'why_important': 'Quan trọng vì: Giúp phân tích sâu hơn mà không cần dữ liệu mới.'
        },
        'has_service': {
            'term': 'Có dịch vụ (HAS_SERVICE)',
            'explain': 'Kiểm tra xem khách hàng có đăng ký dịch vụ nào không.',
            'values': 'True = Có dịch vụ | False = Không có dịch vụ',
            'use_case': 'Dùng để: Phân biệt khách hàng đang dùng và không dùng dịch vụ.'
        },
        'account_age': {
            'term': 'Tuổi tài khoản (ACCOUNT_AGE)',
            'explain': 'Số ngày từ khi kích hoạt tài khoản đến hôm nay.',
            'example': 'Ví dụ: Kích hoạt ngày 1/1/2024, hôm nay 1/12/2024 → Tuổi = 335 ngày.',
            'use_case': 'Dùng để: Biết khách hàng mới hay cũ, trung thành hay không.'
        },
        'days_to_expire': {
            'term': 'Số ngày đến hết hạn (DAYS_TO_EXPIRE)',
            'explain': 'Còn bao nhiêu ngày nữa tài khoản sẽ hết hạn.',
            'example': 'Ví dụ: Hết hạn 10/12/2024, hôm nay 1/12/2024 → Còn 9 ngày.',
            'use_case': 'Dùng để: Cảnh báo khách hàng sắp hết hạn cần gia hạn.'
        },
        'churn_risk': {
            'term': 'Nguy cơ rời mạng (CHURN_RISK)',
            'explain': 'Đánh giá khả năng khách hàng sẽ ngừng sử dụng dịch vụ.',
            'levels': 'High = Nguy cơ cao | Low = Nguy cơ thấp',
            'criteria': 'Dựa trên: TKC thấp, sắp hết hạn, không có dịch vụ.',
            'use_case': 'Dùng để: Ưu tiên chăm sóc khách hàng có nguy cơ cao.'
        },
        'tkc_segment': {
            'term': 'Phân khúc TKC (TKC_SEGMENT)',
            'explain': 'Chia khách hàng thành nhóm dựa trên số tiền trong tài khoản.',
            'levels': 'None = 0đ | Low = 1-5K | Medium = 5-10K | High = >10K',
            'use_case': 'Dùng để: Tạo chương trình khuyến mãi phù hợp từng nhóm.'
        },
        
        # Validation
        'validation': {
            'term': 'Kiểm tra tính hợp lệ (Validation)',
            'explain': 'Xác minh dữ liệu có đúng định dạng và logic không.',
            'example': 'Ví dụ: Số điện thoại phải có 10 số, ngày kích hoạt phải trước ngày hết hạn.',
            'why_important': 'Quan trọng vì: Dữ liệu sai sẽ cho kết quả phân tích sai.'
        },
        'phone_validation': {
            'term': 'Kiểm tra số điện thoại',
            'explain': 'Đảm bảo số điện thoại đúng định dạng 84XXXXXXXXX (10-11 số).',
            'example': 'Đúng: 84912345678 | Sai: 123456',
            'action': 'Hệ thống sẽ đánh dấu các số không hợp lệ.'
        },
        'date_logic': {
            'term': 'Kiểm tra logic ngày tháng',
            'explain': 'Đảm bảo ngày kích hoạt phải trước ngày hết hạn.',
            'example': 'Đúng: Kích hoạt 1/1 - Hết hạn 31/12 | Sai: Kích hoạt 31/12 - Hết hạn 1/1',
            'action': 'Hệ thống sẽ cảnh báo các trường hợp bất thường.'
        },
        'tkc_validation': {
            'term': 'Kiểm tra TKC ≥ 0',
            'explain': 'Đảm bảo số tiền trong tài khoản không âm.',
            'example': 'Đúng: TKC = 0 hoặc 5000 | Sai: TKC = -1000',
            'action': 'Hệ thống sẽ đánh dấu các giá trị âm.'
        },
        
        # AI/ML Terms
        'churn_prediction': {
            'term': 'Dự báo rời mạng (Churn Prediction)',
            'explain': 'Sử dụng AI để dự đoán khách hàng nào có khả năng ngừng dùng dịch vụ.',
            'how_it_works': 'Máy tính học từ dữ liệu cũ để nhận biết dấu hiệu rời mạng.',
            'output': 'Kết quả: Xác suất từ 0-100% (càng cao càng nguy hiểm).',
            'use_case': 'Dùng để: Chủ động liên hệ giữ chân khách hàng trước khi họ rời đi.'
        },
        'random_forest': {
            'term': 'Mô hình Random Forest',
            'explain': 'Là một thuật toán AI giống như "bỏ phiếu của nhiều chuyên gia".',
            'how_it_works': 'Tạo ra nhiều "cây quyết định", mỗi cây đưa ra dự đoán, sau đó lấy kết quả phổ biến nhất.',
            'accuracy': 'Độ chính xác: 85-90% (rất tốt cho dự báo rời mạng).',
            'why_use': 'Ưu điểm: Chính xác cao, dễ hiểu, ít bị sai lệch.'
        },
        'accuracy': {
            'term': 'Độ chính xác (Accuracy)',
            'explain': 'Tỷ lệ % dự đoán đúng của mô hình AI.',
            'example': 'Ví dụ: Accuracy 90% = Dự đoán đúng 90/100 trường hợp.',
            'good_score': 'Điểm tốt: >80% là tốt, >90% là rất tốt.',
            'use_case': 'Dùng để: Đánh giá mô hình AI có đáng tin cậy không.'
        },
        'f1_score': {
            'term': 'Điểm F1 (F1 Score)',
            'explain': 'Đánh giá cân bằng giữa "bắt đúng" và "không bắt nhầm".',
            'range': 'Giá trị: 0-1 (càng gần 1 càng tốt).',
            'example': 'F1 = 0.85 nghĩa là mô hình rất cân bằng.',
            'why_important': 'Quan trọng vì: Accuracy cao nhưng F1 thấp = Mô hình thiên lệch.'
        },
        
        # Customer Segmentation
        'customer_segmentation': {
            'term': 'Phân khúc khách hàng (Customer Segmentation)',
            'explain': 'Chia khách hàng thành các nhóm có đặc điểm giống nhau.',
            'how_it_works': 'AI tự động tìm ra các nhóm dựa trên TKC, tuổi tài khoản, dịch vụ...',
            'output': 'Kết quả: 4-8 nhóm khách hàng khác nhau.',
            'use_case': 'Dùng để: Tạo chiến lược marketing riêng cho từng nhóm.'
        },
        'kmeans': {
            'term': 'Thuật toán K-Means',
            'explain': 'Là phương pháp AI để nhóm khách hàng giống nhau lại với nhau.',
            'how_it_works': 'Tìm "tâm" của mỗi nhóm, sau đó gán khách hàng vào nhóm gần nhất.',
            'example': 'Ví dụ: Nhóm 1 = TKC cao, Nhóm 2 = TKC thấp nhưng dùng nhiều dịch vụ.',
            'why_use': 'Ưu điểm: Nhanh, dễ hiểu, phù hợp với dữ liệu khách hàng.'
        },
        'pca': {
            'term': 'Trực quan hóa PCA',
            'explain': 'Chuyển dữ liệu phức tạp thành biểu đồ 2D dễ nhìn.',
            'how_it_works': 'Giảm nhiều thông tin xuống 2 trục chính để vẽ biểu đồ.',
            'output': 'Kết quả: Biểu đồ scatter plot với các nhóm màu khác nhau.',
            'use_case': 'Dùng để: Xem trực quan các nhóm khách hàng phân bố như thế nào.'
        },
        
        # Anomaly Detection
        'anomaly_detection': {
            'term': 'Phát hiện bất thường (Anomaly Detection)',
            'explain': 'Tìm ra những khách hàng có hành vi khác biệt so với đa số.',
            'how_it_works': 'AI học pattern của khách hàng bình thường, sau đó tìm ra người khác biệt.',
            'output': 'Kết quả: Danh sách khách hàng bất thường (có thể là VIP hoặc gian lận).',
            'use_case': 'Dùng để: Phát hiện VIP cần chăm sóc đặc biệt hoặc phát hiện gian lận.'
        },
        'isolation_forest': {
            'term': 'Thuật toán Isolation Forest',
            'explain': 'Phương pháp AI để tìm "người khác biệt" trong đám đông.',
            'how_it_works': 'Dữ liệu bất thường dễ bị "cô lập" hơn dữ liệu bình thường.',
            'example': 'Ví dụ: Khách hàng có TKC 10 triệu trong khi đa số có 0-5K.',
            'why_use': 'Ưu điểm: Nhanh, không cần dữ liệu huấn luyện trước.'
        },
        'anomaly_score': {
            'term': 'Điểm bất thường (Anomaly Score)',
            'explain': 'Số đo mức độ "khác biệt" của một khách hàng.',
            'range': 'Giá trị: -1 đến 0 (càng âm càng bất thường).',
            'threshold': 'Ngưỡng: Điểm < -0.5 thường được coi là bất thường.',
            'use_case': 'Dùng để: Xếp hạng khách hàng theo mức độ bất thường.'
        },
        
        # Feature Importance
        'feature_importance': {
            'term': 'Độ quan trọng của yếu tố (Feature Importance)',
            'explain': 'Cho biết yếu tố nào ảnh hưởng nhiều nhất đến kết quả dự đoán.',
            'how_it_works': 'AI tính toán xem loại bỏ yếu tố nào làm giảm độ chính xác nhiều nhất.',
            'output': 'Kết quả: Biểu đồ xếp hạng các yếu tố từ quan trọng nhất đến ít quan trọng nhất.',
            'use_case': 'Dùng để: Biết nên tập trung vào yếu tố nào khi giữ chân khách hàng.'
        },
        
        # Model Comparison
        'model_comparison': {
            'term': 'So sánh mô hình (Model Comparison)',
            'explain': 'Thử nghiệm nhiều thuật toán AI khác nhau để chọn ra cái tốt nhất.',
            'models': 'Các mô hình: Random Forest, Gradient Boosting, Logistic Regression.',
            'metrics': 'Tiêu chí: Accuracy (độ chính xác), F1 Score (độ cân bằng).',
            'use_case': 'Dùng để: Đảm bảo đang dùng mô hình AI tốt nhất có thể.'
        }
    }
}

# Hướng dẫn sử dụng từng tính năng
FEATURE_GUIDES = {
    'vi': {
        'data_cleaning': {
            'title': '🧹 Hướng dẫn: Làm sạch dữ liệu',
            'steps': [
                '**Bước 1**: Xem tab "Missing Values" - Kiểm tra cột nào đang thiếu dữ liệu',
                '**Bước 2**: Chọn cách xử lý cho từng cột (Keep NULL, Mode, Forward Fill, hoặc Custom)',
                '**Bước 3**: Xem tab "Derived Columns" - Chọn các cột tính toán muốn tạo',
                '**Bước 4**: Xem tab "Validation" - Bật các quy tắc kiểm tra dữ liệu',
                '**Bước 5**: Nhấn "ÁP DỤNG LÀM SẠCH DỮ LIỆU" và xem kết quả'
            ],
            'tips': [
                '💡 **Mẹo**: Nên chọn "Mode" cho các cột số liệu (TKC, tuổi...)',
                '💡 **Mẹo**: Nên chọn "Keep NULL" nếu muốn xem rõ dữ liệu thiếu ở đâu',
                '💡 **Mẹo**: Luôn bật Validation để phát hiện lỗi dữ liệu'
            ],
            'common_mistakes': [
                '⚠️ **Lỗi thường gặp**: Điền "0" vào cột text (nên dùng "Không rõ")',
                '⚠️ **Lỗi thường gặp**: Không kiểm tra kết quả sau khi làm sạch'
            ]
        },
        'churn_prediction': {
            'title': '🎯 Hướng dẫn: Dự báo rời mạng',
            'what_is_it': 'Tính năng này giúp bạn biết khách hàng nào có nguy cơ ngừng sử dụng dịch vụ.',
            'steps': [
                '**Bước 1**: Nhấn nút "🚀 Train Model" - Máy tính sẽ học từ dữ liệu (mất 5-10 giây)',
                '**Bước 2**: Xem chỉ số Accuracy và F1 Score (>80% là tốt)',
                '**Bước 3**: Xem biểu đồ phân bố xác suất rời mạng',
                '**Bước 4**: Xem danh sách Top 100 khách hàng nguy cơ cao nhất',
                '**Bước 5**: Tải xuống file CSV để liên hệ khách hàng'
            ],
            'how_to_read': [
                '📊 **Xác suất rời mạng**: 0-30% = An toàn | 30-50% = Cảnh báo | 50-70% = Nguy hiểm | >70% = Rất nguy hiểm',
                '📊 **Risk Segments**: Low (xanh) = OK | Medium (vàng) = Theo dõi | High (cam) = Ưu tiên | Critical (đỏ) = Khẩn cấp'
            ],
            'actions': [
                '✅ **Hành động**: Liên hệ khách hàng có xác suất >70% trong vòng 7 ngày',
                '✅ **Hành động**: Tặng khuyến mãi cho nhóm 50-70%',
                '✅ **Hành động**: Theo dõi nhóm 30-50% hàng tháng'
            ]
        },
        'customer_segmentation': {
            'title': '👥 Hướng dẫn: Phân khúc khách hàng',
            'what_is_it': 'Chia khách hàng thành các nhóm có đặc điểm giống nhau để chăm sóc phù hợp.',
            'steps': [
                '**Bước 1**: Chọn số lượng nhóm muốn chia (khuyến nghị: 4 nhóm)',
                '**Bước 2**: Nhấn "🎨 Run Segmentation" - Máy tính sẽ tự động phân nhóm',
                '**Bước 3**: Xem biểu đồ PCA để thấy các nhóm phân bố',
                '**Bước 4**: Xem bảng đặc điểm của từng nhóm',
                '**Bước 5**: Tạo chiến lược riêng cho mỗi nhóm'
            ],
            'typical_segments': [
                '🌟 **Nhóm VIP**: TKC cao + Có dịch vụ → Chăm sóc đặc biệt, ưu đãi độc quyền',
                '💎 **Nhóm Tiềm năng**: TKC cao + Chưa dùng dịch vụ → Khuyến khích kích hoạt',
                '📈 **Nhóm Tích cực**: TKC thấp + Dùng nhiều dịch vụ → Ưu đãi nạp tiền',
                '⚠️ **Nhóm Nguy cơ**: TKC thấp + Không dịch vụ → Chiến dịch giữ chân'
            ],
            'how_to_use': [
                '💼 **Ứng dụng**: Tạo 4 chương trình marketing khác nhau cho 4 nhóm',
                '💼 **Ứng dụng**: Phân bổ ngân sách: VIP 40%, Tiềm năng 30%, Tích cực 20%, Nguy cơ 10%',
                '💼 **Ứng dụng**: Giao khách hàng cho nhân viên phù hợp với chuyên môn'
            ]
        },
        'anomaly_detection': {
            'title': '🔍 Hướng dẫn: Phát hiện bất thường',
            'what_is_it': 'Tìm ra những khách hàng "đặc biệt" - có thể là VIP hoặc có vấn đề.',
            'steps': [
                '**Bước 1**: Chọn tỷ lệ % bất thường muốn tìm (khuyến nghị: 5%)',
                '**Bước 2**: Nhấn "🔎 Detect Anomalies"',
                '**Bước 3**: Xem biểu đồ phân bố điểm bất thường',
                '**Bước 4**: Xem danh sách Top 50 khách hàng bất thường nhất',
                '**Bước 5**: Phân loại thủ công: VIP, Gian lận, hoặc Lỗi dữ liệu'
            ],
            'how_to_classify': [
                '⭐ **VIP**: TKC rất cao, dùng nhiều dịch vụ → Chăm sóc đặc biệt, account manager riêng',
                '🚨 **Gian lận**: Pattern lạ, giao dịch bất thường → Kiểm tra bảo mật',
                '🔧 **Lỗi dữ liệu**: Giá trị không hợp lý → Sửa dữ liệu'
            ],
            'actions': [
                '✅ **Với VIP**: Tạo chương trình khách hàng thân thiết cao cấp',
                '✅ **Với Gian lận**: Xác minh danh tính, kiểm tra lịch sử giao dịch',
                '✅ **Với Lỗi dữ liệu**: Liên hệ bộ phận IT để sửa'
            ]
        }
    }
}

def get_explanation(term, lang='vi'):
    """Lấy giải thích cho một thuật ngữ"""
    return TERM_EXPLANATIONS.get(lang, {}).get(term, {})

def get_guide(feature, lang='vi'):
    """Lấy hướng dẫn cho một tính năng"""
    return FEATURE_GUIDES.get(lang, {}).get(feature, {})

def show_help_box(term, lang='vi'):
    """Tạo help box cho một thuật ngữ (dùng trong Streamlit)"""
    import streamlit as st
    
    explanation = get_explanation(term, lang)
    if not explanation:
        return
    
    with st.expander(f"❓ {explanation.get('term', term)}"):
        if 'explain' in explanation:
            st.write(f"**Giải thích**: {explanation['explain']}")
        if 'example' in explanation:
            st.info(f"📝 {explanation['example']}")
        if 'how_it_works' in explanation:
            st.write(f"**Cách hoạt động**: {explanation['how_it_works']}")
        if 'when_use' in explanation:
            st.success(f"✅ {explanation['when_use']}")
        if 'why_important' in explanation:
            st.warning(f"⚠️ {explanation['why_important']}")
        if 'use_case' in explanation:
            st.write(f"**Ứng dụng**: {explanation['use_case']}")

def show_feature_guide(feature, lang='vi'):
    """Hiển thị hướng dẫn chi tiết cho một tính năng"""
    import streamlit as st
    
    guide = get_guide(feature, lang)
    if not guide:
        return
    
    st.markdown(f"## {guide.get('title', '')}")
    
    if 'what_is_it' in guide:
        st.info(f"💡 **Đây là gì?** {guide['what_is_it']}")
    
    if 'steps' in guide:
        st.markdown("### 📋 Các bước thực hiện:")
        for step in guide['steps']:
            st.markdown(f"- {step}")
    
    if 'how_to_read' in guide:
        st.markdown("### 📊 Cách đọc kết quả:")
        for item in guide['how_to_read']:
            st.markdown(f"- {item}")
    
    if 'typical_segments' in guide:
        st.markdown("### 🎯 Các nhóm điển hình:")
        for segment in guide['typical_segments']:
            st.markdown(f"- {segment}")
    
    if 'how_to_classify' in guide:
        st.markdown("### 🏷️ Cách phân loại:")
        for item in guide['how_to_classify']:
            st.markdown(f"- {item}")
    
    if 'how_to_use' in guide:
        st.markdown("### 💼 Cách sử dụng:")
        for item in guide['how_to_use']:
            st.markdown(f"- {item}")
    
    if 'actions' in guide:
        st.markdown("### ✅ Hành động cần làm:")
        for action in guide['actions']:
            st.markdown(f"- {action}")
    
    if 'tips' in guide:
        st.markdown("### 💡 Mẹo hữu ích:")
        for tip in guide['tips']:
            st.success(tip)
    
    if 'common_mistakes' in guide:
        st.markdown("### ⚠️ Lỗi thường gặp:")
        for mistake in guide['common_mistakes']:
            st.warning(mistake)
