"""
Smart Column Dictionary
Tự động phát hiện và quản lý ý nghĩa các cột với AI
"""

import pandas as pd
import google.generativeai as genai
from typing import Dict, Any, Optional
import json
import streamlit as st

class ColumnDictionary:
    """
    Quản lý ý nghĩa các cột với AI inference và user editing
    """
    
    def __init__(self, df: pd.DataFrame, model):
        """
        Initialize Column Dictionary
        
        Args:
            df: DataFrame cần phân tích
            model: Gemini model instance
        """
        self.df = df
        self.model = model
        self.dictionary = {}  # {column_name: column_info}
    
    def auto_detect_meanings(self) -> Dict[str, Dict[str, Any]]:
        """
        Sử dụng Gemini AI để tự động đoán ý nghĩa tất cả các cột
        OPTIMIZED: Batch processing - phân tích tất cả cột trong 1 lần gọi API
        
        Returns:
            Dict[column_name, column_info]
        """
        if not self.model:
            # Fallback: basic inference without AI
            return self._basic_inference()
        
        try:
            # Batch inference - all columns at once
            self.dictionary = self._batch_infer_all_columns()
        except Exception as e:
            print(f"Batch inference failed: {e}, falling back to basic inference")
            self.dictionary = self._basic_inference()
        
        return self.dictionary
    
    def _batch_infer_all_columns(self) -> Dict[str, Dict[str, Any]]:
        """
        Phân tích TẤT CẢ các cột trong 1 lần gọi API (nhanh hơn nhiều)
        
        Returns:
            Dict[column_name, column_info]
        """
        # Prepare summary for all columns
        columns_data = []
        
        for col in self.df.columns:
            col_data = self.df[col]
            sample_values = col_data.dropna().head(3).tolist()
            
            col_summary = {
                'name': col,
                'dtype': str(col_data.dtype),
                'unique': int(col_data.nunique()),
                'missing': int(col_data.isnull().sum()),
                'sample': sample_values
            }
            
            # Add stats for numeric
            if col_data.dtype in ['int64', 'float64']:
                col_summary['stats'] = {
                    'min': float(col_data.min()) if not pd.isna(col_data.min()) else None,
                    'max': float(col_data.max()) if not pd.isna(col_data.max()) else None,
                    'mean': float(col_data.mean()) if not pd.isna(col_data.mean()) else None
                }
            
            columns_data.append(col_summary)
        
        # Build batch prompt
        prompt = f"""
Bạn là chuyên gia phân tích dữ liệu VNPT Viễn thông. Phân tích TẤT CẢ các cột dữ liệu sau:

**Danh sách cột**:
{json.dumps(columns_data, ensure_ascii=False, indent=2)}

**YÊU CẦU QUAN TRỌNG**:
Cho MỖI cột, bạn PHẢI:

1. **Phân tích tên cột**: 
   - Nếu là viết tắt → giải thích đầy đủ (VD: "Domvi" có thể là "Doanh thu vi tính" hoặc "Domain VI")
   - Nếu là tiếng Anh → dịch sang tiếng Việt
   - Nếu là tiếng Việt → giải thích rõ ràng

2. **Phân tích dữ liệu mẫu**:
   - Xem sample values để hiểu cột chứa gì
   - Xem dtype, min/max, unique để xác định loại dữ liệu

3. **Đưa ra ý nghĩa CỤ THỂ**:
   - KHÔNG được chỉ lặp lại tên cột
   - PHẢI giải thích cột này chứa thông tin gì
   - VD: Thay vì "Domvi" → "Doanh thu vi tính" hoặc "Tổng doanh thu từ dịch vụ data"

**DOMAIN KNOWLEDGE - VNPT Viễn thông**:
- **TKC** = Tài Khoản Chính (số dư tài khoản, KHÔNG phải "Tiền khuyến cáo")
- **Total_TKC** = Tổng số tiền trong tài khoản chính
- **PHONE/SDT** = Số điện thoại khách hàng (identifier)
- **TINH/PROVINCE** = Tỉnh/Thành phố
- **NGAY_KICH_HOAT/DATE_ENTER_ACTIVE** = Ngày kích hoạt dịch vụ
- **ACCOUNT_AGE** = Tuổi tài khoản (số ngày từ khi kích hoạt)
- **SERVICE** = Loại dịch vụ (Data, Voice, SMS, VAS...)
- **ARPU** = Average Revenue Per User (Doanh thu trung bình/user)
- **STAFF_CODE** = Mã nhân viên quản lý
- **CHURN** = Rời mạng (khách hàng ngừng sử dụng dịch vụ)
- **Domvi** = Có thể là "Doanh thu vi tính" hoặc domain-specific term

**CATEGORY**:
- financial: Tiền, doanh thu, chi phí, TKC...
- demographic: Tuổi, giới tính, địa chỉ, tỉnh...
- behavioral: Hành vi sử dụng, service, churn...
- temporal: Ngày tháng, thời gian
- identifier: ID, phone, mã KH...
- other: Không thuộc các loại trên

**CONFIDENCE**:
- 1.0: Chắc chắn 100% (hardcoded terms hoặc rõ ràng)
- 0.8-0.9: Rất chắc (tên cột + sample values khớp)
- 0.6-0.7: Khá chắc (tên cột gợi ý, sample values hợp lý)
- 0.4-0.5: Không chắc (tên cột mơ hồ, sample values không rõ)
- <0.4: Đoán mò (không đủ thông tin)

**REASONING**:
Giải thích TẠI SAO bạn đoán như vậy:
- Dựa vào tên cột (viết tắt gì, nghĩa gì)
- Dựa vào sample values (giá trị như thế nào)
- Dựa vào dtype, stats (số, text, date...)
- Dựa vào domain knowledge VNPT

**VÍ DỤ TỐT**:
{{
    "Domvi": {{
        "meaning_vi": "Doanh thu vi tính (doanh thu từ dịch vụ data/internet)",
        "meaning_en": "Data service revenue",
        "category": "financial",
        "confidence": 0.75,
        "reasoning": "Tên cột 'Domvi' có thể là viết tắt của 'Doanh thu vi tính'. Sample values là số, dtype là float64, có giá trị min/max/mean → khả năng cao là doanh thu. Trong ngành viễn thông, 'vi tính' thường chỉ dịch vụ data/internet."
    }}
}}

**VÍ DỤ XẤU** (KHÔNG được làm như này):
{{
    "Domvi": {{
        "meaning_vi": "Domvi",  ← SAI! Chỉ lặp lại tên cột
        "meaning_en": "Domvi",  ← SAI! Không giải thích
        "category": "other",
        "confidence": 0.5,
        "reasoning": "Unknown"  ← SAI! Không phân tích
    }}
}}

**Trả về JSON** (object với key là tên cột):
{{
    "COLUMN_NAME_1": {{
        "meaning_vi": "Ý nghĩa CỤ THỂ, KHÔNG lặp lại tên cột",
        "meaning_en": "Specific English meaning",
        "category": "financial|demographic|behavioral|temporal|identifier|other",
        "confidence": 0.0-1.0,
        "reasoning": "Giải thích chi tiết dựa trên tên cột, sample values, dtype, domain knowledge"
    }},
    ...
}}

**JSON**:
"""
        
        try:
            response = self.model.generate_content(prompt)
            
            # Extract JSON
            json_text = self._extract_json(response.text)
            results = json.loads(json_text)
            
            # Post-process: Fix common VNPT terms (hardcoded rules)
            results = self._apply_vnpt_corrections(results)
            
            # Add metadata
            for col, info in results.items():
                info['user_edited'] = False
                info['original_ai_meaning'] = info.get('meaning_vi', col)
            
            return results
            
        except Exception as e:
            print(f"Error in batch inference: {e}")
            raise
    
    def _apply_vnpt_corrections(self, results: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """
        Áp dụng corrections cho các thuật ngữ VNPT phổ biến
        Override AI nếu sai
        """
        VNPT_CORRECTIONS = {
            'TKC': {
                'meaning_vi': 'Tài khoản chính',
                'meaning_en': 'Main account balance',
                'category': 'financial',
                'confidence': 1.0,
                'reasoning': 'Hardcoded VNPT term'
            },
            'TOTAL_TKC': {
                'meaning_vi': 'Tổng số tiền trong tài khoản chính',
                'meaning_en': 'Total amount in main account',
                'category': 'financial',
                'confidence': 1.0,
                'reasoning': 'Hardcoded VNPT term'
            },
            'PHONE': {
                'meaning_vi': 'Số điện thoại khách hàng',
                'meaning_en': 'Customer phone number',
                'category': 'identifier',
                'confidence': 1.0,
                'reasoning': 'Hardcoded VNPT term'
            },
            'SDT': {
                'meaning_vi': 'Số điện thoại',
                'meaning_en': 'Phone number',
                'category': 'identifier',
                'confidence': 1.0,
                'reasoning': 'Hardcoded VNPT term'
            }
        }
        
        # Apply corrections
        for col_name, correction in VNPT_CORRECTIONS.items():
            # Check exact match or contains
            for col in results.keys():
                if col.upper() == col_name or col_name in col.upper():
                    # Override AI inference
                    results[col] = correction.copy()
                    print(f"Applied VNPT correction for {col}: {correction['meaning_vi']}")
        
        return results
    
    def _infer_single_column(self, column: str) -> Dict[str, Any]:
        """
        Đoán ý nghĩa một cột bằng Gemini AI
        
        Args:
            column: Tên cột
        
        Returns:
            Dict chứa meaning, category, confidence, reasoning
        """
        # Prepare column analysis data
        col_data = self.df[column]
        dtype = str(col_data.dtype)
        sample_values = col_data.dropna().head(5).tolist()
        unique_count = col_data.nunique()
        missing_count = col_data.isnull().sum()
        
        # Statistics for numeric columns
        stats = {}
        if col_data.dtype in ['int64', 'float64']:
            stats = {
                'min': float(col_data.min()) if not pd.isna(col_data.min()) else None,
                'max': float(col_data.max()) if not pd.isna(col_data.max()) else None,
                'mean': float(col_data.mean()) if not pd.isna(col_data.mean()) else None
            }
        
        # Build prompt for Gemini
        prompt = f"""
Phân tích cột dữ liệu và đoán ý nghĩa:

**Thông tin cột**:
- Tên cột: {column}
- Kiểu dữ liệu: {dtype}
- Số giá trị unique: {unique_count}
- Số giá trị missing: {missing_count}
- Mẫu dữ liệu: {sample_values}
{f"- Thống kê: {stats}" if stats else ""}

**Yêu cầu**:
Dựa trên tên cột (có thể viết tắt), kiểu dữ liệu, và giá trị mẫu, hãy đoán:
1. Ý nghĩa của cột (tiếng Việt, ngắn gọn, dễ hiểu)
2. Ý nghĩa tiếng Anh
3. Danh mục dữ liệu (financial/demographic/behavioral/temporal/identifier/other)
4. Độ tin cậy (0.0-1.0)
5. Lý do đoán như vậy

**Lưu ý**:
- TKC = Tài Khoản Chính (phổ biến trong viễn thông VN)
- PHONE = Số điện thoại
- TINH = Tỉnh/Thành phố
- Nếu không chắc, confidence thấp hơn

**Trả về JSON**:
{{
    "meaning_vi": "Ý nghĩa tiếng Việt",
    "meaning_en": "English meaning",
    "category": "financial|demographic|behavioral|temporal|identifier|other",
    "confidence": 0.95,
    "reasoning": "Lý do ngắn gọn"
}}

**JSON**:
"""
        
        try:
            response = self.model.generate_content(prompt)
            
            # Extract JSON from response
            json_text = self._extract_json(response.text)
            result = json.loads(json_text)
            
            # Add metadata
            result['user_edited'] = False
            result['original_ai_meaning'] = result['meaning_vi']
            
            return result
            
        except Exception as e:
            print(f"Error inferring column {column}: {e}")
            return self._basic_column_info(column)
    
    def _basic_inference(self) -> Dict[str, Dict[str, Any]]:
        """Fallback inference without AI"""
        result = {}
        for col in self.df.columns:
            result[col] = self._basic_column_info(col)
        return result
    
    def _basic_column_info(self, column: str) -> Dict[str, Any]:
        """Basic column info without AI"""
        col_data = self.df[column]
        
        # Simple category detection
        category = 'other'
        if 'phone' in column.lower() or 'tel' in column.lower():
            category = 'identifier'
        elif 'date' in column.lower() or 'time' in column.lower():
            category = 'temporal'
        elif 'price' in column.lower() or 'amount' in column.lower() or 'tkc' in column.lower():
            category = 'financial'
        elif 'name' in column.lower() or 'address' in column.lower():
            category = 'demographic'
        
        return {
            'meaning_vi': column.replace('_', ' ').title(),
            'meaning_en': column.replace('_', ' ').title(),
            'category': category,
            'confidence': 0.5,
            'reasoning': 'Fallback inference (AI not available)',
            'user_edited': False,
            'original_ai_meaning': column
        }
    
    def _extract_json(self, text: str) -> str:
        """Extract JSON from markdown or text"""
        import re
        
        # Try to find JSON in code blocks
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
        if json_match:
            return json_match.group(1)
        
        # Try to find JSON directly
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            return json_match.group(0)
        
        raise ValueError("No JSON found in response")
    
    def update_meaning(self, column: str, meaning_vi: str, meaning_en: str = None):
        """
        Cập nhật ý nghĩa do user sửa
        
        Args:
            column: Tên cột
            meaning_vi: Ý nghĩa tiếng Việt
            meaning_en: Ý nghĩa tiếng Anh (optional)
        """
        if column in self.dictionary:
            self.dictionary[column]['meaning_vi'] = meaning_vi
            if meaning_en:
                self.dictionary[column]['meaning_en'] = meaning_en
            self.dictionary[column]['user_edited'] = True
        else:
            # Create new entry
            self.dictionary[column] = {
                'meaning_vi': meaning_vi,
                'meaning_en': meaning_en or meaning_vi,
                'category': 'other',
                'confidence': 1.0,
                'reasoning': 'User defined',
                'user_edited': True,
                'original_ai_meaning': ''
            }
    
    def get_meaning(self, column: str, lang='vi') -> str:
        """
        Lấy ý nghĩa của một cột
        
        Args:
            column: Tên cột
            lang: Ngôn ngữ ('vi' hoặc 'en')
        
        Returns:
            str: Ý nghĩa của cột
        """
        if column not in self.dictionary:
            return column
        
        key = 'meaning_vi' if lang == 'vi' else 'meaning_en'
        return self.dictionary[column].get(key, column)
    
    def get_confidence(self, column: str) -> float:
        """Lấy độ tin cậy của AI inference"""
        if column not in self.dictionary:
            return 0.0
        return self.dictionary[column].get('confidence', 0.0)
    
    def get_category(self, column: str) -> str:
        """Lấy category của cột"""
        if column not in self.dictionary:
            return 'other'
        return self.dictionary[column].get('category', 'other')
    
    def to_context_string(self) -> str:
        """
        Chuyển dictionary thành string để dùng làm context cho AI
        
        Returns:
            str: Formatted string với ý nghĩa các cột
        """
        lines = ["Column Dictionary:"]
        for col, info in self.dictionary.items():
            lines.append(f"- {col}: {info['meaning_vi']} ({info['category']})")
        return "\n".join(lines)
    
    def save_to_session(self):
        """Lưu vào Streamlit session state"""
        st.session_state.column_dictionary = self.dictionary
    
    def load_from_session(self):
        """Load từ Streamlit session state"""
        if 'column_dictionary' in st.session_state:
            self.dictionary = st.session_state.column_dictionary
    
    def export_to_json(self) -> str:
        """
        Export dictionary ra JSON string
        
        Returns:
            str: JSON string
        """
        return json.dumps(self.dictionary, ensure_ascii=False, indent=2)
    
    def import_from_json(self, json_str: str):
        """
        Import dictionary từ JSON string
        
        Args:
            json_str: JSON string
        """
        self.dictionary = json.loads(json_str)
    
    @classmethod
    def from_json(cls, json_str: str, df: pd.DataFrame, model):
        """
        Tạo ColumnDictionary từ JSON string
        
        Args:
            json_str: JSON string
            df: DataFrame
            model: Gemini model
        
        Returns:
            ColumnDictionary instance
        """
        instance = cls(df, model)
        instance.import_from_json(json_str)
        return instance
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """Lấy thống kê tổng quan về dictionary"""
        total_columns = len(self.dictionary)
        user_edited = sum(1 for info in self.dictionary.values() if info.get('user_edited', False))
        avg_confidence = sum(info.get('confidence', 0) for info in self.dictionary.values()) / total_columns if total_columns > 0 else 0
        
        categories = {}
        for info in self.dictionary.values():
            cat = info.get('category', 'other')
            categories[cat] = categories.get(cat, 0) + 1
        
        return {
            'total_columns': total_columns,
            'user_edited': user_edited,
            'ai_inferred': total_columns - user_edited,
            'avg_confidence': round(avg_confidence, 2),
            'categories': categories
        }


def initialize_column_dictionary(df: pd.DataFrame) -> ColumnDictionary:
    """
    Initialize hoặc load Column Dictionary từ session state
    
    Args:
        df: DataFrame
    
    Returns:
        ColumnDictionary instance
    """
    from gemini_assistant import model
    
    # Check if already exists in session
    if 'column_dict_obj' in st.session_state:
        col_dict = st.session_state.column_dict_obj
        # Update df if changed
        col_dict.df = df
        return col_dict
    
    # Create new instance
    col_dict = ColumnDictionary(df, model)
    
    # Try to load from session state
    col_dict.load_from_session()
    
    # If empty, run auto-detection
    if not col_dict.dictionary:
        with st.spinner("🤖 AI đang phân tích ý nghĩa các cột..."):
            col_dict.auto_detect_meanings()
            col_dict.save_to_session()
    
    # Save object to session
    st.session_state.column_dict_obj = col_dict
    
    return col_dict
