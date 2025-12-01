"""
Natural Language Query Engine
Cho phép hỏi dữ liệu bằng tiếng Việt tự nhiên
"""

import pandas as pd
import google.generativeai as genai
from typing import Dict, Any, Tuple, Optional
import plotly.express as px
import plotly.graph_objects as go
import json
import re

class NaturalLanguageQuery:
    """
    Engine để xử lý câu hỏi tiếng Việt tự nhiên về dữ liệu
    """
    
    def __init__(self, model):
        self.model = model
    
    def query(self, question: str, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Xử lý câu hỏi tiếng Việt và trả về kết quả
        
        Args:
            question: Câu hỏi của người dùng
            df: DataFrame để query
        
        Returns:
            Dict chứa: result, code, chart, explanation
        """
        if not self.model:
            return {
                'success': False,
                'error': 'Gemini AI chưa được khởi tạo'
            }
        
        # Analyze question and generate pandas code
        intent_response = self._analyze_intent(question, df)
        
        if not intent_response['success']:
            return intent_response
        
        # Execute code safely
        result = self._safe_execute(intent_response['code'], df)
        
        if result['success']:
            # Create visualization if needed
            chart = None
            if intent_response.get('chart_type'):
                chart = self._create_chart(
                    result['data'],
                    intent_response['chart_type'],
                    intent_response.get('chart_config', {})
                )
            
            return {
                'success': True,
                'result': result['data'],
                'code': intent_response['code'],
                'chart': chart,
                'explanation': intent_response['explanation'],
                'chart_type': intent_response.get('chart_type')
            }
        else:
            return result
    
    def _analyze_intent(self, question: str, df: pd.DataFrame) -> Dict[str, Any]:
        """Phân tích câu hỏi và tạo pandas code"""
        
        # Get column info
        columns_info = {
            'columns': df.columns.tolist(),
            'dtypes': df.dtypes.astype(str).to_dict(),
            'sample': df.head(2).to_dict()
        }
        
        prompt = f"""
Bạn là Python/Pandas expert. Phân tích câu hỏi và tạo code để trả lời.

**Câu hỏi**: {question}

**Thông tin DataFrame**:
- Columns: {columns_info['columns']}
- Data types: {columns_info['dtypes']}
- Sample data: {json.dumps(columns_info['sample'], ensure_ascii=False)}

**Yêu cầu**:
1. Tạo pandas code để trả lời câu hỏi (dùng biến `df`)
2. Code phải an toàn, không có eval/exec
3. Chọn loại biểu đồ phù hợp (nếu cần)
4. Giải thích kết quả bằng tiếng Việt

**Trả về JSON**:
{{
    "intent": "count|filter|aggregate|group|sort|visualize",
    "code": "result = df[df['TKC'] > 10000].shape[0]",
    "chart_type": "bar|line|scatter|pie|histogram|null",
    "chart_config": {{
        "x": "column_name",
        "y": "column_name",
        "title": "Tiêu đề biểu đồ"
    }},
    "explanation": "Giải thích kết quả"
}}

**Lưu ý**:
- Code phải gán kết quả vào biến `result`
- Nếu không cần biểu đồ, chart_type = null
- Giải thích ngắn gọn, dễ hiểu

**JSON**:
"""
        
        try:
            response = self.model.generate_content(prompt)
            
            # Extract JSON from response
            json_text = self._extract_json(response.text)
            intent_data = json.loads(json_text)
            
            return {
                'success': True,
                **intent_data
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Không thể phân tích câu hỏi: {str(e)}'
            }
    
    def _extract_json(self, text: str) -> str:
        """Extract JSON from markdown code blocks or text"""
        # Try to find JSON in code blocks
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
        if json_match:
            return json_match.group(1)
        
        # Try to find JSON directly
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            return json_match.group(0)
        
        raise ValueError("No JSON found in response")
    
    def _safe_execute(self, code: str, df: pd.DataFrame) -> Dict[str, Any]:
        """Execute pandas code safely"""
        
        # Security check
        dangerous_keywords = ['eval', 'exec', 'import', '__', 'open', 'file']
        if any(keyword in code.lower() for keyword in dangerous_keywords):
            return {
                'success': False,
                'error': 'Code chứa từ khóa nguy hiểm'
            }
        
        try:
            # Create safe namespace
            namespace = {
                'df': df,
                'pd': pd,
                'result': None
            }
            
            # Execute code
            exec(code, namespace)
            
            result = namespace.get('result')
            
            if result is None:
                return {
                    'success': False,
                    'error': 'Code không trả về kết quả (thiếu biến result)'
                }
            
            return {
                'success': True,
                'data': result
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Lỗi khi thực thi code: {str(e)}'
            }
    
    def _create_chart(self, data: Any, chart_type: str, config: Dict[str, Any]) -> go.Figure:
        """Create plotly chart from data"""
        
        try:
            if chart_type == 'bar':
                if isinstance(data, pd.Series):
                    fig = px.bar(
                        x=data.index,
                        y=data.values,
                        title=config.get('title', 'Biểu đồ'),
                        labels={'x': config.get('x', 'X'), 'y': config.get('y', 'Y')}
                    )
                elif isinstance(data, pd.DataFrame):
                    fig = px.bar(
                        data,
                        x=config.get('x'),
                        y=config.get('y'),
                        title=config.get('title', 'Biểu đồ')
                    )
                else:
                    return None
            
            elif chart_type == 'line':
                if isinstance(data, pd.Series):
                    fig = px.line(
                        x=data.index,
                        y=data.values,
                        title=config.get('title', 'Biểu đồ')
                    )
                elif isinstance(data, pd.DataFrame):
                    fig = px.line(
                        data,
                        x=config.get('x'),
                        y=config.get('y'),
                        title=config.get('title', 'Biểu đồ')
                    )
                else:
                    return None
            
            elif chart_type == 'pie':
                if isinstance(data, pd.Series):
                    fig = px.pie(
                        values=data.values,
                        names=data.index,
                        title=config.get('title', 'Biểu đồ')
                    )
                else:
                    return None
            
            elif chart_type == 'histogram':
                if isinstance(data, pd.Series):
                    fig = px.histogram(
                        x=data.values,
                        title=config.get('title', 'Biểu đồ')
                    )
                elif isinstance(data, pd.DataFrame):
                    fig = px.histogram(
                        data,
                        x=config.get('x'),
                        title=config.get('title', 'Biểu đồ')
                    )
                else:
                    return None
            
            else:
                return None
            
            # Update layout
            fig.update_layout(
                template='plotly_white',
                font=dict(family='Inter, sans-serif')
            )
            
            return fig
            
        except Exception as e:
            print(f"Error creating chart: {e}")
            return None


def create_nl_query_widget(df: pd.DataFrame):
    """
    Tạo widget Natural Language Query
    
    Args:
        df: DataFrame để query
    """
    import streamlit as st
    from gemini_assistant import model
    
    st.markdown("### 🗣️ Hỏi Dữ Liệu Bằng Tiếng Việt")
    st.markdown("Đặt câu hỏi tự nhiên, AI sẽ tự động phân tích và trả lời")
    
    # Examples
    with st.expander("💡 Ví dụ câu hỏi"):
        st.markdown("""
        - Có bao nhiêu khách hàng có TKC > 10000?
        - Tỉnh nào có nhiều khách hàng nhất?
        - So sánh số lượng khách hàng theo dịch vụ
        - Tạo biểu đồ phân bố TKC
        - Top 10 khách hàng có TKC cao nhất
        - Tỷ lệ khách hàng có dịch vụ
        """)
    
    # Query input
    question = st.text_input(
        "Câu hỏi của bạn:",
        placeholder="VD: Có bao nhiêu khách hàng ở Hà Nội?",
        key="nl_query_input"
    )
    
    if st.button("🔍 Tìm Kiếm", type="primary"):
        if question:
            with st.spinner("🤖 AI đang phân tích câu hỏi..."):
                nl_engine = NaturalLanguageQuery(model)
                result = nl_engine.query(question, df)
                
                if result['success']:
                    # Show result
                    st.success("✅ Đã tìm thấy kết quả!")
                    
                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        st.markdown("**📊 Kết quả:**")
                        st.write(result['result'])
                        
                        st.markdown("**💡 Giải thích:**")
                        st.info(result['explanation'])
                    
                    with col2:
                        if result.get('chart'):
                            st.markdown("**📈 Biểu đồ:**")
                            st.plotly_chart(result['chart'], use_container_width=True)
                    
                    # Show code (expandable)
                    with st.expander("👨‍💻 Xem code đã chạy"):
                        st.code(result['code'], language='python')
                else:
                    st.error(f"❌ {result.get('error', 'Lỗi không xác định')}")
        else:
            st.warning("⚠️ Vui lòng nhập câu hỏi")
