import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json
import re
import time

# ── 0. 페이지 설정 ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FRAMING ANALYZER — Elite Media Intelligence",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── 1. 글로벌 CSS (디자인 대폭 강화) ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=IBM+Plex+Mono:wght@400;600&family=Inter:wght@300;400;600;700&display=swap');

:root {
    --bg:       #0d1117;
    --surface:  #161b22;
    --border:   #30363d;
    --accent:   #ff4d4d;
    --accent-soft: rgba(255, 77, 77, 0.1);
    --accent2:  #ffb84d;
    --text:     #c9d1d9;
    --text-bright: #ffffff;
    --muted:    #8b949e;
}

html, body, [class*="css"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif;
}

/* 사이드바 스타일 */
[data-testid="stSidebar"] {
    background-color: var(--surface) !important;
    border-right: 1px solid var(--border);
}

/* 네오 브루탈리즘 카드 스타일 */
.custom-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 20px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.custom-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.3);
}

/* 섹션 타이틀 영문 병기 */
.section-header {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.15em;
    color: var(--muted);
    text-transform: uppercase;
    margin-bottom: 12px;
    display: flex;
    justify-content: space-between;
}

/* 버튼 디자인 업그레이드 */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #ff4d4d, #d70000) !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 700 !important;
    letter-spacing: 0.05em !important;
    height: 3.5rem !important;
}

/* IP 보호 문구 (글래스모피즘) */
.ip-notice {
    background: rgba(255, 184, 77, 0.05);
    border: 1px solid rgba(255, 184, 77, 0.2);
    border-radius: 10px;
    padding: 16px;
    font-size: 11px;
    color: var(--accent2);
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

# ── 2. 사이드바 (IP 보호 및 설정) ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="margin-bottom: 30px;">
        <div style="font-family:'IBM Plex Mono',monospace; font-size:10px; color:var(--muted); letter-spacing:0.2em;">SYSTEM V2.0 PRO</div>
        <div style="font-family:'DM Serif Display',serif; font-size:28px; color:var(--text-bright);">Intellectual<br>Framing Analyzer</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="ip-notice">
    ⚠️ <b>INTELLECTUAL PROPERTY NOTICE</b><br><br>
    본 시스템의 핵심 알고리즘 및 데이터 모델은 <b>특허 출원(공지예외주장)</b>에 의거하여 보호받는 고유 자산입니다.<br><br>
    © 2026. All Rights Reserved.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<br>', unsafe_allow_html=True)
    api_key = st.text_input("Claude API Key", type="password", placeholder="sk-ant-...")
    
    st.markdown("---")
    st.markdown("""
    <div style="font-size:11px; color:var(--muted); line-height:2;">
    ● Cognitive Bias Detection<br>
    ● Psychological Trigger Indexing<br>
    ● Loaded Language Filtering<br>
    ● Information Asymmetry Audit
    </div>
    """, unsafe_allow_html=True)

# ── 3. 메인 화면 헤더 ────────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding: 40px 0 30px;">
    <h1 style="font-family:'DM Serif Display',serif; font-size: 56px; color: var(--accent); margin-bottom: 0;">뉴스 심리 프레이밍 분석기</h1>
    <p style="font-family:'IBM Plex Mono',monospace; font-size: 18px; color: var(--muted); letter-spacing: 0.1em;">ADVANCED MEDIA PSYCHOLOGY ANALYTICS</p>
</div>
""", unsafe_allow_html=True)

# ── 4. 입력부 ───────────────────────────────────────────────────────────────────
input_text = st.text_area("기사 본문 입력 (News Content Input)", height=250, placeholder="분석할 기사를 붙여넣으세요...")
run = st.button("▶ EXECUTE DEEP ANALYSIS")

# ── 5. 분석 실행 및 결과 (디자인 강화 버전) ────────────────────────────────────────────────────
if run and input_text:
    with st.spinner("🔬 해부 중... (Dissecting Media Structure)"):
        # 실제 API 호출 로직 (생략, 기존 함수 사용)
        time.sleep(2) # 데모용 로딩 효과
        
        # 가상의 결과 데이터 (구조 확인용)
        data = {
            "main_frame": {"name": "공포 소구 (Fear Mongering)", "description": "불확실한 미래의 위협을 과장하여 독자의 이성적 판단을 마비시키고 특정 정책에 대한 지지를 유도함."},
            "biases": [{"name": "확증편향", "evidence": "'이미 예견된 결과였다'는 표현을 통해 독자의 기존 불신을 강화함."}],
            "triggers": {"anger": 85, "fear": 92, "disgust": 40, "crisis": 88, "bias": 75},
            "summary": "본 보도는 객관적 사실 보도보다 공포와 위기감을 극대화하여 독자의 감정적 대응을 선동하는 전형적인 프레이밍을 보입니다.",
            "asymmetry": {"over": "검증되지 않은 위기 시나리오", "under": "전문가들의 반론 및 완화 정책 설명"},
            "words": [{"word": "경악", "effect": "충격 및 공포", "alt": "우려"}, {"word": "혈세", "effect": "분노 유발", "alt": "예산"}]
        }

    # 레이아웃 구성
    col_left, col_right = st.columns([3, 2], gap="large")

    with col_left:
        # A. 프레이밍 진단
        st.markdown('<div class="section-header"><span>A. CORE FRAMING DIAGNOSIS</span><span>01</span></div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="custom-card" style="border-left: 4px solid var(--accent);">
            <h3 style="color:var(--accent); margin:0 0 10px 0;">{data['main_frame']['name']}</h3>
            <p style="font-size:15px; color:var(--text); line-height:1.6;">{data['main_frame']['description']}</p>
        </div>
        """, unsafe_allow_html=True)

        # B. 인지편향
        st.markdown('<div class="section-header"><span>B. COGNITIVE BIAS DETECTION</span><span>02</span></div>', unsafe_allow_html=True)
        for b in data['biases']:
            st.markdown(f"""
            <div class="custom-card" style="border-left: 4px solid var(--accent2);">
                <div style="font-family:'IBM Plex Mono',monospace; font-size:12px; color:var(--accent2); font-weight:600; margin-bottom:8px;">{b['name']}</div>
                <div style="font-size:14px; color:var(--muted); font-style:italic;">"{b['evidence']}"</div>
            </div>
            """, unsafe_allow_html=True)

        # D. 정보 불균형
        st.markdown('<div class="section-header"><span>D. INFORMATION ASYMMETRY AUDIT</span><span>04</span></div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="custom-card">
            <div style="color:var(--accent); font-weight:600; margin-bottom:8px;">▲ SALIENCE (과도하게 강조됨)</div>
            <div style="font-size:14px; margin-bottom:20px;">{data['asymmetry']['over']}</div>
            <div style="color:#3b82f6; font-weight:600; margin-bottom:8px;">▼ OMISSION (의도적 누락/축소)</div>
            <div style="font-size:14px;">{data['asymmetry']['under']}</div>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        # C. 심리 트리거 차트
        st.markdown('<div class="section-header"><span>C. PSYCHOLOGICAL TRIGGER INDEX</span><span>03</span></div>', unsafe_allow_html=True)
        # (기존 Plotly Radar Chart 코드 삽입 지점)
        st.info("📊 레이더 차트가 여기에 렌더링됩니다.")

        # 트리거 수치 바 (네온 스타일)
        for key, label in [('anger', 'ANGER'), ('fear', 'FEAR'), ('crisis', 'CRISIS')]:
            val = data['triggers'].get(key, 0)
            st.markdown(f"""
            <div style="margin-bottom:15px;">
                <div style="display:flex; justify-content:space-between; font-family:'IBM Plex Mono'; font-size:11px; margin-bottom:5px;">
                    <span>{label}</span><span>{val}%</span>
                </div>
                <div style="background:var(--border); height:6px; border-radius:3px;">
                    <div style="width:{val}%; height:100%; background:var(--accent); border-radius:3px; box-shadow: 0 0 10px var(--accent);"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # 데스크 총평 (Executive Summary)
        st.markdown('<div class="section-header" style="margin-top:30px;"><span>EXECUTIVE SUMMARY</span></div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background:var(--accent-soft); border:1px solid var(--accent); border-radius:12px; padding:20px;">
            <p style="font-size:14px; color:var(--text-bright); line-height:1.7; margin:0;">{data['summary']}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<p style="text-align:center; font-family:\'IBM Plex Mono\'; font-size:10px; color:var(--muted); margin-top:50px;">PROPRIETARY ALGORITHM © 2026 · PATENT PENDING · SECURED ENVIRONMENT</p>', unsafe_allow_html=True)
