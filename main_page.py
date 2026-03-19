from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field
from typing import List
import io
import base64
import re

load_dotenv()
# ── 페이지 설정 ──────────────────────────────────────────────
st.set_page_config(
    page_title="부야오 샹차이",
    page_icon="🌿",
    layout="centered"
)

# ── 커스텀 CSS ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&family=Noto+Sans+SC:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}

/* 배경 */
.stApp {
    background: linear-gradient(160deg, #f5f0e8 0%, #eee8d8 50%, #f5f0e8 100%);
}

/* 로고 영역 */
.logo-area {
    text-align: center;
    padding: 2rem 0 0.5rem 0;
}
.logo-sub {
    font-size: 1rem;
    color: #4a7c59;
    margin-top: 0.5rem;
    letter-spacing: 0.15em;
    font-weight: 500;
}

/* 구분선 */
.divider {
    border: none;
    height: 2px;
    background: linear-gradient(to right, transparent, #4a7c59, transparent);
    margin: 1.5rem 0;
}

/* 채팅 메시지 */
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding: 1rem 0;
}
.msg-user {
    align-self: flex-end;
    background: #d6eadb;
    border: 1px solid #4a7c5944;
    color: #1e3a28;
    padding: 0.75rem 1.1rem;
    border-radius: 1.2rem 1.2rem 0.2rem 1.2rem;
    max-width: 100%;
    font-size: 0.95rem;
}
.msg-assistant {
    align-self: flex-start;
    background: #ffffff;
    border: 1px solid #4a7c5933;
    color: #2c2c2c;
    padding: 0.75rem 1.1rem;
    border-radius: 1.2rem 1.2rem 1.2rem 0.2rem;
    max-width: 100%;
    font-size: 0.95rem;
    line-height: 1.7;
}
.msg-label {
    font-size: 0.72rem;
    color: #4a7c59;
    margin-bottom: 0.3rem;
    letter-spacing: 0.08em;
}

/* 버튼 */
.stButton > button {
    background: #4a7c59;
    color: #ffffff;
    border: none;
    font-weight: 700;
    font-family: 'Noto Sans KR', sans-serif;
    border-radius: 1.5rem;
    padding: 0.5rem 1.5rem;
    transition: all 0.2s ease;
}
.stButton > button:hover {
    background: #3a6347;
    transform: translateY(-1px);
    box-shadow: 0 4px 20px rgba(74,124,89,0.3);
}

/* audio_input 라벨 */
[data-testid="stAudioInput"] label,
[data-testid="stAudioInput"] p {
    color: #4a7c59 !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}

/* audio_input 컴팩트하게 */
[data-testid="stAudioInput"] {
    border: 1.5px solid #4a7c5966;
    border-radius: 1rem;
    background: #ffffff;
    padding: 0.2rem 0.5rem;
}

/* 마이크 버튼 영역 */
[data-testid="stAudioInput"] > div {
    min-height: unset !important;
}
            
/* 오디오 플레이어 너비 제한 */
[data-testid="stAudioInput"] ~ div .stAudio,
.stAudio {
    max-width: 100%px;
}

/* 샹차이 이펙트 */
.xiangcai-overlay {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none;
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
    animation: fadeInOut 3s ease forwards;
}
.xiangcai-img {
    width: 400px;
    animation: zoomBounce 3s ease forwards;
}
@keyframes fadeInOut {
    0%   { opacity: 0; }
    20%  { opacity: 1; }
    70%  { opacity: 1; }
    100% { opacity: 0; }
}
@keyframes zoomBounce {
    0%   { transform: scale(0.2) rotate(-10deg); }
    30%  { transform: scale(1.1) rotate(3deg); }
    50%  { transform: scale(0.95) rotate(-2deg); }
    70%  { transform: scale(1.0) rotate(0deg); }
    100% { transform: scale(1.3) rotate(5deg); }
}

/* 섹션 헤더 */
.section-label {
    color: #4a7c59;
    font-size: 0.8rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# ── LangChain 설정 ───────────────────────────────────────────
@st.cache_resource
def get_chain():
    prompt = ChatPromptTemplate.from_messages([
        ('system', '''
# RULE
-ROLE: 중화권 여행 중인 사용자에게 통역의 도움을 주는 Assistant
-GOAL: 중화권(보통화, 광둥어, 중국 사투리 등)의 언어를 통역
# TASK
- {speech_prompt}를 인식 → 상황에 맞는 답변
-기본적으로 한국어를 포함해 응답
## SITUATION
-사용자가 한국어로 말하는 경우: 여행 중 중국인과 소통이 어려움 → 사용자의 요청을 이해하고 사용자가 말하고자 하는 바를 중국어로 출력
-사용자가 중국어로 말하는 경우: 상대방이 사용자와의 소통을 위해 말함 → 사용자를 위해 중국어를 한국어로 번역/전달
# CONSTRAINTS
-각 언어로 번역 시, 원문을 훼손하지 않는 범위에서 의미 중심의 의역을 활용
-자연스러운 구어체 활용
-비속어 인식 시: '나쁜 말이에요. 번역할 수 없어요.' 중국어/한국어 모두 출력
-심한 사투리, 알아들을 수 없는 말 인식 시: '조금 더 천천히 말해 주세요.' 중국어/한국어 모두 출력
'''),
        MessagesPlaceholder(variable_name='history'),
        ('human', '{speech_prompt}')
    ])
    llm = init_chat_model('openai:gpt-4.1-mini')
    output_parser = StrOutputParser()
    return prompt | llm | output_parser

# ── 메모리 설정 ──────────────────────────────────────────────
class InMemoryHistory(BaseChatMessageHistory, BaseModel):
    messages: List[BaseMessage] = Field(default_factory=list)
    def add_messages(self, messages: List[BaseMessage]) -> None:
        self.messages.extend(messages)
    def clear(self) -> None:
        self.messages = []

if 'store' not in st.session_state:
    st.session_state.store = {}
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'show_xiangcai' not in st.session_state:
    st.session_state.show_xiangcai = False
if 'last_audio_id' not in st.session_state:
    st.session_state.last_audio_id = None

def get_by_session_id(session_id: str) -> BaseChatMessageHistory:
    if session_id not in st.session_state.store:
        st.session_state.store[session_id] = InMemoryHistory()
    return st.session_state.store[session_id]

def get_chain_with_memory():
    chain = get_chain()
    return RunnableWithMessageHistory(
        chain,
        get_by_session_id,
        input_messages_key='speech_prompt',
        history_messages_key='history'
    )

# ── 샹차이 감지 ──────────────────────────────────────────────
XIANGCAI_PATTERNS = [
    r'부야오\s*샹차이', r'不要\s*香菜', r'bù\s*yào\s*xiāng\s*cài',
    r'고수\s*빼', r'고수\s*없이', r'향채', r'芫荽'
]

def detect_xiangcai(text: str) -> bool:
    for pattern in XIANGCAI_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

# ── 로고 ─────────────────────────────────────────────────────
with open('./image/logo.png', 'rb') as f:
    logo_b64 = base64.b64encode(f.read()).decode()

st.markdown(f"""
<div class="logo-area">
    <img src="data:image/png;base64,{logo_b64}" style="max-width:400px; width:100%; object-fit:contain; margin-bottom:0.5rem;">
    <div class="logo-sub">중화권 여행 통역 어시스턴트</div>
</div>
""", unsafe_allow_html=True)

# 초기화 버튼
col1, col2, col3 = st.columns([3, 2, 3])
with col2:
    if st.button("🗑 대화 초기화", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.store = {}
        st.session_state.show_xiangcai = False
        st.rerun()

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── 샹차이 이펙트 ─────────────────────────────────────────────
if st.session_state.show_xiangcai:
    with open('./image/shangchai.png', 'rb') as f:
        xc_b64 = base64.b64encode(f.read()).decode()
    st.markdown(f"""
    <div class="xiangcai-overlay">
        <img class="xiangcai-img" src="data:image/png;base64,{xc_b64}">
    </div>
    """, unsafe_allow_html=True)
    st.session_state.show_xiangcai = False

# ── 대화 히스토리 ─────────────────────────────────────────────
if st.session_state.chat_history:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for msg in st.session_state.chat_history:
        if msg['role'] == 'user':
            st.markdown(f"""
            <div class="msg-user">
                <div class="msg-label">🎙 나</div>
                {msg['text']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="msg-assistant">
                <div class="msg-label">🌿 통역</div>
                {msg['text']}
            </div>
            """, unsafe_allow_html=True)
            if msg.get('audio'):
                st.audio(msg['audio'], format='audio/mp3')
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── 음성 입력 ─────────────────────────────────────────────────
audio_input = st.audio_input("  🎙 마이크를 눌러 말씀하세요.")

if audio_input is not None:
    audio_id = hash(audio_input.read())
    audio_input.seek(0)
    if audio_id == st.session_state.last_audio_id:
        st.stop()
    st.session_state.last_audio_id = audio_id

    client = OpenAI()

    with st.spinner("🗣️ 음성 인식 중..."):
        audio_bytes = audio_input.read()
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=("audio.wav", io.BytesIO(audio_bytes), "audio/wav"),
            language=None
        )
        user_text = transcript.text

    if not user_text.strip():
        st.warning("🥲 음성을 인식하지 못했어요. 다시 시도해 주세요.")
    else:
        if detect_xiangcai(user_text):
            st.session_state.show_xiangcai = True

        with st.spinner("🔃 번역 중..."):
            chain_with_memory = get_chain_with_memory()
            response_text = chain_with_memory.invoke(
                {'speech_prompt': user_text},
                config={'configurable': {'session_id': 'user_session'}}
            )

        with st.spinner("🦜 음성 생성 중..."):
            tts_response = client.audio.speech.create(
                model='tts-1',
                voice='alloy',
                input=response_text
            )
            audio_data = tts_response.content

        st.session_state.chat_history.append({'role': 'user', 'text': user_text})
        st.session_state.chat_history.append({'role': 'assistant', 'text': response_text, 'audio': audio_data})

        st.rerun()
