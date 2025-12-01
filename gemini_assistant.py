"""
Gemini AI Assistant Module
Provides context-aware data analysis insights and recommendations
"""

import os
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables
load_dotenv()

def initialize_gemini():
    """Initialize Gemini AI with API key"""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    return model

# Initialize model globally
try:
    model = initialize_gemini()
except Exception as e:
    print(f"Warning: Could not initialize Gemini: {e}")
    model = None

def analyze_data_quality(df: pd.DataFrame, lang='vi', column_dict=None) -> str:
    """
    Phân tích chất lượng dữ liệu và đưa ra khuyến nghị
    
    Args:
        df: DataFrame cần phân tích
        lang: Ngôn ngữ ('vi' hoặc 'en')
        column_dict: ColumnDictionary instance (optional)
    
    Returns:
        str: Phân tích chi tiết về chất lượng dữ liệu
    """
    if model is None:
        return "⚠️ Gemini AI chưa được khởi tạo. Vui lòng kiểm tra API key."
    
    # Prepare data summary
    total_rows = len(df)
    total_cols = len(df.columns)
    missing_summary = df.isnull().sum()
    missing_pct = (missing_summary / total_rows * 100).round(2)
    duplicates = df.duplicated().sum()
    
    # Add column meanings if available
    column_context = ""
    if column_dict:
        column_context = "\n\nÝ nghĩa các cột:\n"
        for col in df.columns:
            meaning = column_dict.get_meaning(col, lang)
            category = column_dict.get_category(col)
            column_context += f"- {col}: {meaning} ({category})\n"
    
    # Create context for AI
    context = f"""
    Bạn là chuyên gia phân tích dữ liệu cho VNPT HRDC. Phân tích chất lượng dữ liệu sau:
    
    - Tổng số dòng: {total_rows:,}
    - Tổng số cột: {total_cols}
    - Số dòng trùng lặp: {duplicates}
    {column_context}
    
    Các cột thiếu dữ liệu:
    {missing_summary[missing_summary > 0].to_dict()}
    
    Tỷ lệ thiếu (%):
    {missing_pct[missing_pct > 0].to_dict()}
    
    Kiểu dữ liệu:
    {df.dtypes.to_dict()}
    
    Hãy đưa ra:
    1. Đánh giá tổng quan về chất lượng dữ liệu (điểm từ 1-10)
    2. 3-5 vấn đề quan trọng nhất cần xử lý (ưu tiên dựa trên ý nghĩa cột)
    3. Ưu tiên xử lý (P0 = Khẩn cấp, P1 = Cao, P2 = Trung bình)
    4. Khuyến nghị cụ thể cho từng vấn đề
    
    Trả lời bằng tiếng Việt, ngắn gọn, dễ hiểu cho người không chuyên.
    """
    
    try:
        response = model.generate_content(context)
        return response.text
    except Exception as e:
        return f"❌ Lỗi khi gọi Gemini AI: {str(e)}"

def suggest_cleaning_strategies(df: pd.DataFrame, column: str, lang='vi') -> str:
    """
    Gợi ý chiến lược làm sạch cho một cột cụ thể
    
    Args:
        df: DataFrame
        column: Tên cột cần làm sạch
        lang: Ngôn ngữ
    
    Returns:
        str: Gợi ý chiến lược làm sạch
    """
    if model is None:
        return "⚠️ Gemini AI chưa được khởi tạo."
    
    if column not in df.columns:
        return f"❌ Cột '{column}' không tồn tại trong dữ liệu."
    
    # Analyze column
    col_data = df[column]
    missing_count = col_data.isnull().sum()
    missing_pct = (missing_count / len(df) * 100).round(2)
    dtype = col_data.dtype
    unique_count = col_data.nunique()
    
    # Sample values
    sample_values = col_data.dropna().head(10).tolist()
    
    context = f"""
    Bạn là chuyên gia data cleaning cho VNPT HRDC. Phân tích cột '{column}':
    
    - Kiểu dữ liệu: {dtype}
    - Số giá trị thiếu: {missing_count} ({missing_pct}%)
    - Số giá trị unique: {unique_count}
    - Mẫu dữ liệu: {sample_values}
    
    Hãy gợi ý:
    1. Chiến lược làm sạch tốt nhất (Keep NULL, Mode, Forward Fill, hay Custom Value)
    2. Lý do tại sao chọn chiến lược đó
    3. Cảnh báo nếu có (ví dụ: mất dữ liệu, bias...)
    4. Giá trị cụ thể nên điền (nếu chọn Custom Value)
    
    Trả lời ngắn gọn, cụ thể, bằng tiếng Việt.
    """
    
    try:
        response = model.generate_content(context)
        return response.text
    except Exception as e:
        return f"❌ Lỗi: {str(e)}"

def generate_business_insights(stats: Dict[str, Any], lang='vi') -> str:
    """
    Tạo business insights từ kết quả phân tích thống kê
    
    Args:
        stats: Dictionary chứa kết quả thống kê
        lang: Ngôn ngữ
    
    Returns:
        str: Business insights chi tiết
    """
    if model is None:
        return "⚠️ Gemini AI chưa được khởi tạo."
    
    context = f"""
    Bạn là Business Analyst cho VNPT HRDC. Phân tích kết quả thống kê sau và đưa ra insights kinh doanh:
    
    {stats}
    
    Hãy cung cấp:
    1. **Top 3 Insights Quan Trọng Nhất** (với số liệu cụ thể)
    2. **Xu Hướng Đáng Chú Ý** (tăng/giảm, pattern...)
    3. **Cơ Hội Kinh Doanh** (3-5 cơ hội cụ thể)
    4. **Rủi Ro Cần Lưu Ý** (2-3 rủi ro)
    5. **Khuyến Nghị Hành Động** (ưu tiên P0/P1/P2)
    
    Format: Markdown với emoji, bullet points, dễ đọc.
    Ngôn ngữ: Tiếng Việt, ngắn gọn, actionable.
    """
    
    try:
        response = model.generate_content(context)
        return response.text
    except Exception as e:
        return f"❌ Lỗi: {str(e)}"

def interpret_chart(chart_type: str, data_summary: Dict[str, Any], lang='vi') -> str:
    """
    Giải thích ý nghĩa của biểu đồ bằng ngôn ngữ kinh doanh
    
    Args:
        chart_type: Loại biểu đồ (bar, line, scatter...)
        data_summary: Tóm tắt dữ liệu trong biểu đồ
        lang: Ngôn ngữ
    
    Returns:
        str: Giải thích biểu đồ
    """
    if model is None:
        return "⚠️ Gemini AI chưa được khởi tạo."
    
    context = f"""
    Bạn là Data Visualization Expert cho VNPT HRDC. Giải thích biểu đồ {chart_type} sau:
    
    Dữ liệu: {data_summary}
    
    Hãy cung cấp:
    1. **Ý Nghĩa Chính** của biểu đồ (1-2 câu)
    2. **Pattern/Xu Hướng** quan sát được
    3. **Outliers/Điểm Bất Thường** (nếu có)
    4. **Business Implication** (ý nghĩa với kinh doanh)
    5. **Next Steps** (nên làm gì tiếp theo)
    
    Giải thích cho người không chuyên hiểu được.
    Tiếng Việt, ngắn gọn, có ví dụ cụ thể.
    """
    
    try:
        response = model.generate_content(context)
        return response.text
    except Exception as e:
        return f"❌ Lỗi: {str(e)}"

def analyze_churn_results(predictions_df: pd.DataFrame, accuracy: float, lang='vi') -> str:
    """
    Phân tích sâu kết quả dự báo churn và đưa ra chiến lược giữ chân
    
    Args:
        predictions_df: DataFrame chứa kết quả dự đoán
        accuracy: Độ chính xác của model
        lang: Ngôn ngữ
    
    Returns:
        str: Phân tích churn chi tiết
    """
    if model is None:
        return "⚠️ Gemini AI chưa được khởi tạo."
    
    # Analyze predictions
    total_customers = len(predictions_df)
    high_risk = len(predictions_df[predictions_df['churn_probability'] > 0.7])
    medium_risk = len(predictions_df[(predictions_df['churn_probability'] > 0.3) & (predictions_df['churn_probability'] <= 0.7)])
    
    # Top features if available
    top_features = predictions_df.columns.tolist()[:5]
    
    context = f"""
    Bạn là Churn Prevention Expert cho VNPT HRDC. Phân tích kết quả dự báo rời mạng:
    
    - Tổng số khách hàng: {total_customers:,}
    - Độ chính xác model: {accuracy:.1%}
    - Nguy cơ cao (>70%): {high_risk:,} khách hàng
    - Nguy cơ trung bình (30-70%): {medium_risk:,} khách hàng
    - Các yếu tố quan trọng: {top_features}
    
    Hãy cung cấp:
    
    ## 🎯 Phân Tích Chuyên Sâu
    1. **Root Causes** - Nguyên nhân gốc rễ khiến khách hàng rời đi
    2. **Customer Segments** - Phân nhóm khách hàng nguy cơ cao
    3. **Warning Signs** - Dấu hiệu cảnh báo sớm
    
    ## 💡 Chiến Lược Giữ Chân
    1. **Immediate Actions (7 ngày)** - Cho nhóm nguy cơ cao
    2. **Short-term (30 ngày)** - Cho nhóm nguy cơ trung bình
    3. **Long-term (90 ngày)** - Chiến lược dài hạn
    
    ## 📊 Expected Results
    - Tỷ lệ giữ chân dự kiến
    - ROI ước tính
    - KPIs cần theo dõi
    
    Format: Markdown, có emoji, bullet points, số liệu cụ thể.
    Tiếng Việt, actionable, dễ triển khai.
    """
    
    try:
        response = model.generate_content(context)
        return response.text
    except Exception as e:
        return f"❌ Lỗi: {str(e)}"

def create_segmentation_strategy(segments_df: pd.DataFrame, lang='vi') -> str:
    """
    Tạo chiến lược marketing chi tiết cho từng segment
    
    Args:
        segments_df: DataFrame chứa thông tin segments
        lang: Ngôn ngữ
    
    Returns:
        str: Chiến lược marketing chi tiết
    """
    if model is None:
        return "⚠️ Gemini AI chưa được khởi tạo."
    
    # Analyze segments
    segment_summary = segments_df.groupby('segment').agg({
        'TKC': ['mean', 'count'],
        'ACCOUNT_AGE': 'mean'
    }).round(0)
    
    context = f"""
    Bạn là Marketing Strategy Expert cho VNPT HRDC. Tạo chiến lược cho các segments:
    
    {segment_summary.to_string()}
    
    Cho MỖI SEGMENT, hãy cung cấp:
    
    ## 🎯 Segment [Tên]
    
    ### Đặc Điểm
    - Profile khách hàng
    - Hành vi tiêu dùng
    - Pain points
    
    ### Chiến Lược Marketing
    1. **Value Proposition** - Lợi ích chính
    2. **Channels** - Kênh tiếp cận (SMS, Email, Call...)
    3. **Offers** - Ưu đãi phù hợp
    4. **Messaging** - Nội dung truyền thông
    
    ### Budget Allocation
    - % ngân sách khuyến nghị
    - Expected ROI
    
    ### KPIs
    - Conversion rate mục tiêu
    - Retention rate mục tiêu
    
    Format: Markdown, có emoji, tables nếu cần.
    Tiếng Việt, cụ thể, có ví dụ campaigns.
    """
    
    try:
        response = model.generate_content(context)
        return response.text
    except Exception as e:
        return f"❌ Lỗi: {str(e)}"

def get_ai_response(question: str, context: Dict[str, Any] = None, lang='vi') -> str:
    """
    Trả lời câu hỏi của người dùng dựa trên context
    
    Args:
        question: Câu hỏi của người dùng
        context: Context về dữ liệu hiện tại
        lang: Ngôn ngữ
    
    Returns:
        str: Câu trả lời từ AI
    """
    if model is None:
        return "⚠️ Gemini AI chưa được khởi tạo."
    
    context_str = f"\nContext: {context}" if context else ""
    
    prompt = f"""
    Bạn là AI Assistant cho VNPT HRDC Data Analysis Platform.
    
    Câu hỏi: {question}
    {context_str}
    
    Hãy trả lời:
    - Ngắn gọn, súc tích
    - Có ví dụ cụ thể nếu cần
    - Actionable (có thể hành động được)
    - Tiếng Việt
    
    Nếu câu hỏi liên quan đến dữ liệu, hãy đưa ra insights và khuyến nghị cụ thể.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Lỗi: {str(e)}"
