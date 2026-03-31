import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json
import re
import time

# ── 0. 페이지 설정 (Wide Layout & State Management) ──────────────────────────────────────────────
st.set_page_config(
    page_title="FRAMING ANALYZER — Elite Media Intelligence",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── 1. 글로벌 고도화 CSS (브랜드 아이덴티티 및 UI/UX) ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=IBM+Plex+Mono:wght@300;400;600&family=Noto+Sans+KR:wght@300;400;700&display=swap');

:root {
    --bg:       #0a0c10;
    --surface:  #111318;
    --border:   #1e2330;
    --accent:   #e84040;
    --accent-glow: rgba(232, 64, 64, 0.3);
    --accent2:  #f5a623;
    --text:     #e8eaf0;
    --muted:    #6b7280;
    --safe:     #22c55e;
    --glass:    rgba(255, 255, 255, 0.03);
}

/* 베이스 스타일 */
html, body, [class*="css"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Noto Sans KR', sans-serif;
}

/* 사이드바 커스텀 */
[data-testid="stSidebar"] {
    background-color: var(--surface) !important;
    border-right: 1px solid var(--border);
}

/* 입력창 고도화 */
textarea {
    background-color: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 12px !important;
    font-size: 15px !important;
    line-height: 1.6 !important;
    padding: 1.5rem !important;
    transition: all 0.3s ease !important;
}
textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-glow) !important;
}

/* 버튼 네오-브루탈리즘 스타일 */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, var(--accent), #b01a1a) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    letter-spacing: 0.12em !important;
    padding: 1rem !important;
    text-transform: uppercase;
    box-shadow: 0 4px 20px rgba(232, 64, 64, 0.25) !important;
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) scale(1.01) !important;
    box-shadow: 0 8px 30px rgba(232, 64, 64, 0.4) !important;
}

/* 섹션 타이틀 헤더 */
.section-header {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--muted);
    margin: 40px 0 20px 0;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
}

/* 커스텀 카드 디자인 */
.glass-card {
    background: var(--glass);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    backdrop-filter: blur(10px);
}

.frame-hero {
    background: linear-gradient(135deg, rgba(232, 64, 64, 0.15), rgba(232, 64, 64, 0.03));
    border: 1px solid rgba(232, 64, 64, 0.35);
    border-left: 5px solid var(--accent);
    padding: 30px;
    border-radius: 12px;
}

.bias-tag {
    background: rgba(245, 166, 35, 0.08);
    border: 1px solid rgba(245, 166, 35, 0.25);
    border-left: 3px solid var(--accent2);
    padding: 15px 20px;
    margin-bottom: 12px;
    border-radius: 8px;
}

/* IP 보호 고지 박스 (사이드바) */
.ip-protection-notice {
    background: rgba(245, 166, 35, 0.04);
    border: 1px solid rgba(245, 166, 35, 0.15);
    border-radius: 12px;
    padding: 18px;
    margin-bottom: 30px;
}
.ip-title-en {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    font-weight: 600;
    color: var(--accent2);
    letter-spacing: 0.1em;
    margin-bottom: 8px;
}

/* 스크롤바 커스텀 */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: var(--muted); }

/* 애니메이션 */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
.fade-in { animation: fadeIn 0.6s ease-out forwards; }
</style>
""", unsafe_allow_html=True)

# ── 2. Claude API 고도화 분석 로직 ───────────────────────────────────────────────────
def perform_deep_analysis(text: str, key: str):
    """Claude Sonnet 최신 엔진을 활용한 미디어 심리 구조 해부"""
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=key)
        
        system_prompt = """당신은 30년 경력의 미디어 심리학자이자 전직 보도국 데스크입니다. 
뉴스의 표면적 팩트가 아니라, 독자의 뇌를 어떻게 해킹(Hacking)하는지 분석하세요. 
반드시 JSON 형식으로만 응답하며, 모든 설명은 한국어로 작성합니다."""

        user_prompt = f"""아래 기사를 분석하여 JSON 응답을 생성하세요.
[분석 대상 기사]:
{text}

[JSON 구조]:
{{
  "main_frame": {{"name": "프레임명", "description": "분석 내용(2문장)"}},
  "biases": [{{"name": "편향명", "evidence": "구체적 증거 문구"}}],
  "triggers": {{"anger": 0, "fear": 0, "disgust": 0, "crisis": 0, "bias": 0}},
  "words": [{{"word": "단어", "effect": "심리적 영향", "alt": "중립 대체어"}}],
  "asymmetry": {{"over": "과도하게 강조된 포인트", "under": "의도적 누락/축소 포인트"}},
  "summary": "데스크 관점의 냉철한 최종 총평 (2문장)"
}}
각 트리거 수치는 0-100 사이 정수이며, biases는 최대 3개, words는 5개 추출하세요."""

        # 404 에러 해결을 위해 명확한 최신 모델 ID인 claude-3-5-sonnet-20241022를 사용
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            messages=[{"role": "user", "content": user_prompt}]
        )
        
        response_text = message.content[0].text.strip()
        match = re.search(r'\{[\s\S]*\}', response_text)
        if match:
            return json.loads(match.group()), None
        return None, "결과 파싱 중 오류가 발생했습니다."
    except Exception as e:
        return None, str(e)

# ── 3. 사이드바 (IP 철벽 방어 및 시스템 설정) ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 15px 0 35px;">
        <div style="font-family:'IBM Plex Mono',monospace; font-size:10px; color:var(--muted); letter-spacing:0.3em; margin-bottom:8px;">VERSION 2.5 ELITE</div>
        <div style="font-family:'DM Serif Display',serif; font-size:32px; color:#fff; line-height:1;">Framing<br>Analyzer</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="ip-protection-notice">
        <div class="ip-title-en">⚠️ INTELLECTUAL PROPERTY NOTICE</div>
        <div style="font-size:11px; color:#b0860a; line-height:1.7;">
            본 시스템의 핵심 분석 알고리즘 및 지표화 로직은 <b>대한민국 특허법 제30조(공지예외주장)</b>에 의거하여 보호받는 개발자 고유의 자산입니다.<br><br>
            All analytical frameworks are proprietary and protected under IP laws.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header"><span>API CONFIGURATION</span></div>', unsafe_allow_html=True)
    user_api_key = st.text_input("Claude API Key", type="password", placeholder="sk-ant-...")

    st.markdown('<div class="section-header"><span>SYSTEM CAPABILITIES</span></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:12px; color:var(--muted); line-height:2.2;">
    ● 5-Factor Psychological Indexing<br>
    ● Cognitive Bias Extraction (Max 3)<br>
    ● Loaded Word Filtering (Max 5)<br>
    ● Information Asymmetry Audit<br>
    ● Executive Editor Summary
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"""
    <div style="font-size:11px; color:var(--muted);">
    <span style="display:inline-block; width:8px; height:8px; background:var(--safe); border-radius:50%; margin-right:8px;"></span>
    Engine: Claude 3.5 Sonnet (New)<br>
    Status: Analysis Optimized
    </div>
    """, unsafe_allow_html=True)

# ── 4. 메인 대시보드 헤더 ─────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding: 40px 0 30px;" class="fade-in">
    <h1 style="font-family:'DM Serif Display',serif; font-size: 64px; color: var(--accent); margin-bottom: 5px; line-height:1;">뉴스 심리 프레이밍 분석기</h1>
    <p style="font-family:'IBM Plex Mono',monospace; font-size: 16px; color: var(--muted); letter-spacing: 0.2em; text-transform:uppercase;">
        Advanced Media Intelligence & Psychological Dissection
    </p>
    <div style="width: 80px; height: 4px; background: var(--accent); border-radius: 2px; margin-top: 25px;"></div>
</div>
""", unsafe_allow_html=True)

# ── 5. 기사 입력부 ─────────────────────────────────────────────────────────────────
input_area = st.container()
with input_area:
    article_text = st.text_area(
        "분석할 뉴스 기사 본문 (Full Article Text)",
        height=280,
        placeholder="분석하고자 하는 뉴스 기사의 전체 텍스트를 이곳에 붙여넣으세요. AI 미디어 심리학자가 즉시 분석을 시작합니다.",
        label_visibility="collapsed"
    )
    
    col_stat, col_action = st.columns([4, 1])
    with col_stat:
        char_len = len(article_text)
        status_color = "#22c55e" if char_len > 100 else "#e84040"
        st.markdown(f"""
        <div style="font-family:'IBM Plex Mono',monospace; font-size:11px; color:{status_color}; margin-top:10px;">
            {char_len} CHARACTERS LOADED — {"READY TO ANALYZE" if char_len > 100 else "MINIMUM 100 CHARS REQUIRED"}
        </div>
        """, unsafe_allow_html=True)
        
    with col_action:
        analyze_btn = st.button("▶ EXECUTE ANALYSIS", disabled=(char_len < 100))

st.markdown('<div style="margin: 40px 0;"></div>', unsafe_allow_html=True)

# ── 6. 분석 결과 렌더링 (Deep Report) ────────────────────────────────────────────────
if analyze_btn:
    if not user_api_key:
        st.error("⚠️ 사이드바에서 Claude API Key를 입력해주시기 바랍니다.")
    else:
        with st.spinner("🔬 AI 미디어 심리학자가 기사의 심리적 아키텍처를 해부하는 중입니다..."):
            result, error = perform_deep_analysis(article_text, user_api_key)
            
        if error:
            st.error(f"**ANALYSIS FAILED**: {error}")
            if "404" in error:
                st.info("💡 모델 식별자를 다시 조정했습니다. 최신 Sonnet 3.5 모델에 접근 가능한지 확인 부탁드립니다.")
        else:
            # 리포트 헤더
            st.markdown('<div class="section-header"><span>DEEP ANALYSIS REPORT</span><span>COMPLETE</span></div>', unsafe_allow_html=True)
            
            # 레이아웃 분할
            left_pane, right_pane = st.columns([3, 2], gap="large")
            
            with left_pane:
                # 섹션 A: 핵심 프레이밍
                st.markdown('<div class="section-title">A. Core Psychological Framing</div>', unsafe_allow_html=True)
                frame = result['main_frame']
                st.markdown(f"""
                <div class="frame-hero fade-in">
                    <div style="font-family:'IBM Plex Mono',monospace; font-size:10px; color:var(--accent); letter-spacing:0.2em; margin-bottom:10px;">PRIMARY FRAME DETECTED</div>
                    <div style="font-family:'DM Serif Display',serif; font-size:28px; color:#fff; margin-bottom:12px;">{frame['name']}</div>
                    <div style="font-size:15px; color:var(--text); line-height:1.7;">{frame['description']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # 섹션 B: 인지 편향
                st.markdown('<div class="section-title">B. Cognitive Bias Detection</div>', unsafe_allow_html=True)
                for b in result['biases']:
                    st.markdown(f"""
                    <div class="bias-tag fade-in">
                        <div style="font-family:'IBM Plex Mono',monospace; font-size:12px; font-weight:600; color:var(--accent2); margin-bottom:8px;">[ {b['name']} ]</div>
                        <div style="font-size:14px; color:#c0c8d8; font-style:italic; line-height:1.6;">"{b['evidence']}"</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # 섹션 D: 정보 불균형
                st.markdown('<div class="section-title">D. Information Asymmetry Audit</div>', unsafe_allow_html=True)
                asym = result['asymmetry']
                st.markdown(f"""
                <div class="glass-card fade-in" style="border-left: 4px solid var(--accent);">
                    <div style="font-family:'IBM Plex Mono'; font-size:10px; color:var(--accent); letter-spacing:0.15em; margin-bottom:8px;">▲ OVER-EMPHASIZED (Salience)</div>
                    <div style="font-size:14px; color:var(--text); line-height:1.7;">{asym['over']}</div>
                </div>
                <div class="glass-card fade-in" style="border-left: 4px solid #3b82f6;">
                    <div style="font-family:'IBM Plex Mono'; font-size:10px; color:#3b82f6; letter-spacing:0.15em; margin-bottom:8px;">▼ OMITTED OR MINIMIZED (Gap)</div>
                    <div style="font-size:14px; color:var(--text); line-height:1.7;">{asym['under']}</div>
                </div>
                """, unsafe_allow_html=True)

                # 섹션 E: 선동 어휘 필터
                st.markdown('<div class="section-title">E. Loaded Words & Agitation Filter</div>', unsafe_allow_html=True)
                df_words = pd.DataFrame(result['words'])
                df_words.columns = ['자극적 어휘', '심리적 효과', '중립 대체어']
                st.dataframe(df_words, use_container_width=True, hide_index=True)

            with right_pane:
                # 섹션 C: 방사형 차트
                st.markdown('<div class="section-title">C. Psychological Trigger Index</div>', unsafe_allow_html=True)
                
                triggers = result['triggers']
                categories = ['분노(Anger)', '공포(Fear)', '혐오(Disgust)', '위기감(Crisis)', '확증편향(Bias)']
                values = [triggers['anger'], triggers['fear'], triggers['disgust'], triggers['crisis'], triggers['bias']]
                
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                    r=values + [values[0]],
                    theta=categories + [categories[0]],
                    fill='toself',
                    fillcolor='rgba(232, 64, 64, 0.15)',
                    line=dict(color='#e84040', width=3),
                    name='Index'
                ))
                fig.update_layout(
                    polar=dict(
                        bgcolor='rgba(0,0,0,0)',
                        radialaxis=dict(visible=True, range=[0, 100], gridcolor='#1e2330', tickfont=dict(size=9, color='#6b7280')),
                        angularaxis=dict(gridcolor='#1e2330', tickfont=dict(size=10, color='#9ca3af', family='Noto Sans KR'))
                    ),
                    paper_bgcolor='rgba(0,0,0,0)',
                    showlegend=False,
                    height=400,
                    margin=dict(l=50, r=50, t=50, b=50)
                )
                st.plotly_chart(fig, use_container_width=True)

                # 상세 수치 바 (Visual Feedback)
                trigger_map = {'anger': '분노', 'fear': '공포', 'disgust': '혐오', 'crisis': '위기감', 'bias': '확증편향'}
                for key, val in triggers.items():
                    st.markdown(f"""
                    <div style="margin-bottom:12px;" class="fade-in">
                        <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:5px;">
                            <span style="color:#9ca3af;">{trigger_map[key]}</span>
                            <span style="font-family:'IBM Plex Mono'; color:var(--accent); font-weight:600;">{val}%</span>
                        </div>
                        <div style="background:var(--border); height:4px; border-radius:2px;">
                            <div style="width:{val}%; height:100%; background:var(--accent); border-radius:2px; box-shadow: 0 0 8px var(--accent-glow);"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # 최종 요약 (데스크 총평)
                st.markdown('<div style="margin-top:40px;"></div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="summary-box fade-in">
                    <div style="font-family:'IBM Plex Mono'; font-size:10px; color:var(--accent2); letter-spacing:0.2em; margin-bottom:12px;">💡 EXECUTIVE EDITOR'S SUMMARY</div>
                    <div style="font-size:15px; line-height:1.8; color:#fff; font-weight:400;">{result['summary']}</div>
                </div>
                """, unsafe_allow_html=True)

            # 푸터 주석
            st.markdown('<hr style="border:none; border-top:1px solid var(--border); margin:50px 0;">', unsafe_allow_html=True)
            st.markdown("""
            <div style="font-family:'IBM Plex Mono',monospace; font-size:10px; color:#374151; text-align:center; letter-spacing:0.2em;">
                CORE ANALYSIS ENGINE © 2026 · PRIVATE INFRASTRUCTURE · ALL RIGHTS RESERVED
            </div>
            """, unsafe_allow_html=True)

# ── 7. 초기 화면 가이드 (복원 및 강화) ────────────────────────────────────────────────────
else:
    st.markdown('<div style="margin-top:20px;"></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    steps = [
        ("01", "PASTE ARTICLE", "분석을 원하는 기사 본문을 입력창에 붙여넣으세요. 최소 100자 이상의 텍스트가 필요합니다."),
        ("02", "DEEP DISSECTION", "Claude 3.5 Sonnet 엔진이 기사 이면의 심리적 프레임과 인지 편향을 해부합니다."),
        ("03", "VISUAL INSIGHT", "수치화된 감정 지수와 선동 어휘 리스트를 통해 보도의 객관성을 즉각 확인하세요.")
    ]
    for col, (num, title, desc) in zip([c1, c2, c3], steps):
        with col:
            st.markdown(f"""
            <div style="background:var(--surface); border:1px solid var(--border); border-radius:16px; padding:30px; height:180px;" class="fade-in">
                <div style="font-family:'IBM Plex Mono'; font-size:36px; font-weight:600; color:rgba(232, 64, 64, 0.1); margin-bottom:15px; line-height:1;">{num}</div>
                <div style="font-weight:700; font-size:15px; margin-bottom:12px; color:#fff; letter-spacing:0.05em;">{title}</div>
                <div style="font-size:13px; color:var(--muted); line-height:1.7;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
