"""
Conversational AI Assistant
Multi-turn conversations with context awareness and memory
"""

import streamlit as st
import pandas as pd
import google.generativeai as genai
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

class ConversationalAssistant:
    """
    AI Assistant có khả năng chat liên tục với memory và context awareness
    """
    
    def __init__(self, model):
        self.model = model
        self.conversation_history: List[Dict[str, str]] = []
        self.context: Dict[str, Any] = {}
        self.max_history = 10  # Giữ 10 messages gần nhất
    
    def set_context(self, page: str, data_summary: Dict[str, Any]):
        """
        Cập nhật context hiện tại (page nào, dữ liệu gì)
        
        Args:
            page: Tên page hiện tại
            data_summary: Tóm tắt dữ liệu hiện tại
        """
        self.context = {
            'page': page,
            'data_summary': data_summary,
            'timestamp': datetime.now().isoformat()
        }
    
    def chat(self, user_message: str, lang='vi') -> str:
        """
        Chat với AI, nhớ context và history
        
        Args:
            user_message: Tin nhắn từ người dùng
            lang: Ngôn ngữ
        
        Returns:
            str: Phản hồi từ AI
        """
        if not self.model:
            return "⚠️ Gemini AI chưa được khởi tạo."
        
        # Build conversation context
        history_text = self._format_history()
        context_text = self._format_context()
        
        # Create prompt
        system_prompt = f"""
Bạn là AI Data Analyst chuyên nghiệp cho VNPT HRDC.

**Vai trò của bạn**:
- Trả lời câu hỏi về dữ liệu một cách chính xác, dễ hiểu
- Chủ động gợi ý phân tích sâu hơn
- Đưa ra khuyến nghị actionable
- Giải thích bằng tiếng Việt, ngắn gọn, có ví dụ cụ thể

**Context hiện tại**:
{context_text}

**Lịch sử hội thoại**:
{history_text}

**Quy tắc trả lời**:
1. Ngắn gọn (2-3 đoạn văn)
2. Có số liệu cụ thể nếu có trong context
3. Kết thúc bằng câu hỏi follow-up hoặc gợi ý tiếp theo
4. Dùng emoji phù hợp (📊💡🎯⚠️✅)
5. Format markdown: **bold**, bullet points, numbers

**Người dùng hỏi**: {user_message}

**Trả lời**:
"""
        
        try:
            response = self.model.generate_content(system_prompt)
            ai_response = response.text
            
            # Save to history
            self._add_to_history(user_message, ai_response)
            
            return ai_response
            
        except Exception as e:
            return f"❌ Lỗi khi chat với AI: {str(e)}"
    
    def _format_history(self) -> str:
        """Format conversation history"""
        if not self.conversation_history:
            return "Chưa có lịch sử hội thoại"
        
        formatted = []
        for msg in self.conversation_history[-self.max_history:]:
            formatted.append(f"User: {msg['user']}")
            formatted.append(f"AI: {msg['assistant']}")
        
        return "\n".join(formatted)
    
    def _format_context(self) -> str:
        """Format current context"""
        if not self.context:
            return "Chưa có context"
        
        return f"""
Page: {self.context.get('page', 'Unknown')}
Data Summary: {json.dumps(self.context.get('data_summary', {}), ensure_ascii=False, indent=2)}
"""
    
    def _add_to_history(self, user_msg: str, ai_msg: str):
        """Add message pair to history"""
        self.conversation_history.append({
            'user': user_msg,
            'assistant': ai_msg,
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep only recent messages
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_conversation_summary(self) -> str:
        """Get summary of conversation"""
        if not self.conversation_history:
            return "Chưa có cuộc hội thoại nào"
        
        summary_prompt = f"""
Tóm tắt cuộc hội thoại sau thành 2-3 bullet points:

{self._format_history()}

Tóm tắt ngắn gọn những gì đã thảo luận.
"""
        
        try:
            response = self.model.generate_content(summary_prompt)
            return response.text
        except:
            return "Không thể tạo tóm tắt"


def create_ai_chat_widget(assistant: ConversationalAssistant, 
                          current_page: str,
                          data_summary: Dict[str, Any]):
    """
    Tạo chat widget cho sidebar
    
    Args:
        assistant: ConversationalAssistant instance
        current_page: Tên page hiện tại
        data_summary: Tóm tắt dữ liệu
    """
    # Update context
    assistant.set_context(current_page, data_summary)
    
    st.markdown("### 🤖 AI Assistant")
    st.markdown("Chat với AI về dữ liệu của bạn")
    
    # Show conversation history
    if assistant.conversation_history:
        with st.expander("📜 Lịch sử chat", expanded=False):
            for msg in assistant.conversation_history[-5:]:  # Show last 5
                st.markdown(f"**👤 Bạn**: {msg['user']}")
                st.markdown(f"**🤖 AI**: {msg['assistant']}")
                st.markdown("---")
    
    # Chat input
    user_input = st.text_input(
        "Hỏi AI về dữ liệu...",
        placeholder="VD: Tại sao có nhiều khách hàng rời mạng?",
        key=f"ai_chat_{current_page}"
    )
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if st.button("💬 Gửi", use_container_width=True, type="primary"):
            if user_input:
                with st.spinner("🤖 AI đang suy nghĩ..."):
                    response = assistant.chat(user_input)
                    st.session_state[f'last_ai_response_{current_page}'] = response
                    st.rerun()
    
    with col2:
        if st.button("🗑️ Xóa", use_container_width=True):
            assistant.clear_history()
            st.rerun()
    
    # Show last response
    if f'last_ai_response_{current_page}' in st.session_state:
        st.markdown("**💡 AI Response:**")
        st.info(st.session_state[f'last_ai_response_{current_page}'])
    
    # Quick suggestions
    st.markdown("**💭 Gợi ý câu hỏi:**")
    suggestions = get_smart_suggestions(current_page, data_summary)
    
    for suggestion in suggestions[:3]:
        if st.button(f"💡 {suggestion}", key=f"suggest_{hash(suggestion)}"):
            with st.spinner("🤖 AI đang suy nghĩ..."):
                response = assistant.chat(suggestion)
                st.session_state[f'last_ai_response_{current_page}'] = response
                st.rerun()


def get_smart_suggestions(page: str, data_summary: Dict[str, Any]) -> List[str]:
    """
    Tạo gợi ý câu hỏi thông minh dựa trên page và dữ liệu
    
    Args:
        page: Tên page hiện tại
        data_summary: Tóm tắt dữ liệu
    
    Returns:
        List[str]: Danh sách câu hỏi gợi ý
    """
    suggestions_map = {
        'Data Exploration': [
            "Chất lượng dữ liệu của tôi thế nào?",
            "Cột nào cần ưu tiên làm sạch?",
            "Có bất thường gì trong dữ liệu không?",
            "Dữ liệu này phù hợp để phân tích gì?"
        ],
        'Data Cleaning': [
            "Nên xử lý missing values như thế nào?",
            "Có nên xóa outliers không?",
            "Chiến lược làm sạch nào tốt nhất?",
            "Làm sao để chuẩn hóa dữ liệu?"
        ],
        'Statistical Analysis': [
            "Insights quan trọng nhất là gì?",
            "Xu hướng nào đáng chú ý?",
            "Có correlation nào bất ngờ không?",
            "Nên tập trung vào metric nào?"
        ],
        'Visualization': [
            "Biểu đồ nào phù hợp nhất?",
            "Làm sao để truyền đạt insight này?",
            "Story gì nên kể từ dữ liệu?",
            "Dashboard nên có gì?"
        ],
        'AI Analysis': [
            "Tại sao khách hàng rời mạng?",
            "Segment nào có giá trị nhất?",
            "Chiến lược giữ chân nào hiệu quả?",
            "ROI dự kiến là bao nhiêu?"
        ]
    }
    
    return suggestions_map.get(page, [
        "Phân tích dữ liệu này giúp tôi",
        "Insights quan trọng nhất là gì?",
        "Tôi nên làm gì tiếp theo?"
    ])


def initialize_conversational_assistant():
    """
    Initialize conversational assistant in session state
    """
    if 'conversational_assistant' not in st.session_state:
        from gemini_assistant import model
        st.session_state.conversational_assistant = ConversationalAssistant(model)
    
    return st.session_state.conversational_assistant
