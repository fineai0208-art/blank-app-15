import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json
import re
import time

# ── 0. 페이지 설정 (Elite Dashboard Config) ───────────────────────────────────────────────────
st.set_page_config(
    page_title="FRAMING ANALYZER — Elite Intelligence System",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── 1. 익스트림 고도화 CSS (브랜드 아이덴티티 및 UX 최적화) ──────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=IBM+Plex+Mono:wght@300;400;600&family=Noto+Sans+KR:wght@300;400;700&display=swap');

:root {
    --bg:       #0a0c10;
    --surface:  #111318;
    --border:   #1e2330;
    --accent:   #e84040;
    --accent-glow: rgba(232, 64, 64, 0.4);
    --accent2:  #f5a623;
    --text:     #e8eaf0;
    --muted:    #6b7280;
    --safe:     #22c55e;
    --glass:    rgba(255, 255, 255, 0.03);
    --shadow:   0 10px 40px rgba(0,0,0,0.5);
}

/* 글로벌 베이스 */
html, body, [class*="css"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Noto Sans KR', sans-serif;
}

/* 사이드바 전문가용 다크 테마 */
[data-testid="stSidebar"] {
    background-color: var(--surface) !important;
    border-right: 1px solid var(--border);
    padding-top: 2rem;
}

/* 입력 영역 디자인 (긴 기사 대응) */
textarea {
    background-color: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 12px !important;
    font-size: 16px !important;
    line-height: 1.8 !important;
    padding: 1.8rem !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: inset 0 2px 10px rgba(0,0,0,0.2) !important;
}
textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 4px var(--accent-glow) !important;
}

/* 버튼 네오-브루탈리즘 스타일 */
.stButton > button {
    width: 100%;
    background: linear-gradient(145deg, var(--accent), #a01010) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    letter-spacing: 0.15em !important;
    padding: 1.4rem !important;
    text-transform: uppercase;
    box-shadow: 0 6px 25px rgba(232, 64, 64, 0.3) !important;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
}
.stButton > button:hover {
    transform: translateY(-4px) scale(1.02) !important;
    box-shadow: 0 12px 45px rgba(232, 64, 64, 0.5) !important;
}

/* 섹션 헤더 디자인 */
.section-header {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: var(--muted);
    margin: 50px 0 25px 0;
    padding-bottom: 15px;
    border-bottom: 2px solid var(--border);
    display: flex;
    justify-content: space-between;
}

/* 카드 시스템 고도화 */
.glass-card {
    background: var(--glass);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 35px;
    margin-bottom: 30px;
    backdrop-filter: blur(15px);
    box-shadow: var(--shadow);
}

.frame-hero {
    background: linear-gradient(135deg, rgba(232, 64, 64, 0.2), rgba(232, 64, 64, 0.05));
    border: 1px solid rgba(232, 64, 64, 0.4);
    border-left: 8px solid var(--accent);
    padding: 45px;
    border-radius: 15px;
    margin-bottom: 40px;
}

.bias-tag {
    background: rgba(245, 166, 35, 0.06);
    border: 1px solid rgba(245, 166, 35, 0.2);
    border-left: 5px solid var(--accent2);
    padding: 22px 28px;
    margin-bottom: 20px;
    border-radius: 12px;
}

/* IP 보호 고지 (영문 혼용 철벽 방어) */
.ip-protection-notice {
    background: rgba(245, 166, 35, 0.03);
    border: 1px solid rgba(245, 166, 35, 0.12);
    border-radius: 14px;
    padding: 22px;
    margin-bottom: 40px;
}
.ip-title-en {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    font-weight: 700;
    color: var(--accent2);
    letter-spacing: 0.15em;
    margin-bottom: 12px;
}

/* 애니메이션 */
@keyframes slideUpFade {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}
.reveal { animation: slideUpFade 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards; }
</style>
""", unsafe_allow_html=True)

# ── 2. Claude API 고도화 로직 (긴 기사 대응 및 모델 최신화) ──────────────────────────────
def perform_deep_analysis(text: str, key: str):
    """Claude Sonnet 3.5 최신 엔진을 활용한 고차원 미디어 심리 구조 해체"""
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=key)
        
        system_prompt = """당신은 30년 경력의 미디어 심리학자이자 전직 보도국 데스크입니다. 
뉴스의 표면적 팩트가 아니라, 독자의 뇌를 어떻게 해킹(Hacking)하는지 분석하세요. 
반드시 JSON 형식으로만 응답하며, 모든 설명은 한국어로 작성합니다.
응답에 마크다운 태그(```json 등)를 포함하지 마세요."""

        user_prompt = f"""아래 기사를 분석하여 JSON 응답을 생성하세요. 
기사가 길더라도 전체 맥락을 관통하는 핵심 프레임을 찾아내야 합니다.

[ARTICLE]:
{text}

[JSON STRUCTURE]:
{{
  "main_frame": {{"name": "주요 프레임명", "description": "이 프레임이 작동하는 방식 (2문장)"}},
  "biases": [{{"name": "편향명", "evidence": "구체적 증거 문구"}}],
  "triggers": {{"anger": 0, "fear": 0, "disgust": 0, "crisis": 0, "bias": 0}},
  "words": [{{"word": "자극적 단어", "effect": "심리적 영향", "alt": "중립 대체어"}}],
  "asymmetry": {{"over": "과도하게 강조된 포인트", "under": "의도적 누락/축소 포인트"}},
  "summary": "데스크 관점의 최종 총평 (2문장)"
}}
각 트리거 수치는 0-100 정수, biases는 3개, words는 5개 추출하세요."""

        # 404 에러 완벽 차단을 위해 검증된 모델 ID 사용 (Sonnet 3.5)
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=3000, # 긴 분석 대응을 위해 토큰 상향
            temperature=0.2,
            messages=[{"role": "user", "content": user_prompt}],
            system=system_prompt
        )
        
        response_text = message.content[0].text.strip()
        match = re.search(r'\{[\s\S]*\}', response_text)
        if match:
            return json.loads(match.group()), None
        return None, "JSON 응답 파싱 실패. 다시 시도해 주십시오."
    except Exception as e:
        return None, str(e)

# ── 3. 사이드바 (IP 보호 및 API 자동저장 트리거 대응) ──────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 10px 0 40px;">
        <div style="font-family:'IBM Plex Mono',monospace; font-size:11px; color:var(--muted); letter-spacing:0.4em; margin-bottom:12px;">SYSTEM V2.6 ELITE</div>
        <div style="font-family:'DM Serif Display',serif; font-size:40px; color:#fff; line-height:0.9;">Framing<br>Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="ip-protection-notice">
        <div class="ip-title-en">⚠️ INTELLECTUAL PROPERTY NOTICE</div>
        <div style="font-size:11px; color:#b0860a; line-height:1.8;">
            본 시스템의 핵심 분석 알고리즘 및 지표화 아키텍처는 <b>대한민국 특허법 제30조(공지예외주장)</b>에 의거하여 보호받는 개발자 고유 자산입니다.<br><br>
            © 2026. All Rights Reserved. Proprietary Framework.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header"><span>API CONFIGURATION</span></div>', unsafe_allow_html=True)
    
    # 브라우저 자동저장 팝업을 유도하기 위해 st.form을 활용
    with st.form("api_access_form"):
        st.markdown('<div style="font-size:11px; color:var(--muted); margin-bottom:5px;">System Access Key (Claude API)</div>', unsafe_allow_html=True)
        # 패스워드 타입으로 지정하여 브라우저가 중요 정보로 인식하게 유도
        user_api_key = st.text_input(
            "Access Token", 
            type="password", 
            placeholder="sk-ant-...",
            label_visibility="collapsed"
        )
        submit_key = st.form_submit_button("SAVE & AUTHENTICATE")
        if submit_key:
            st.session_state['api_key_stored'] = user_api_key
            st.success("Access Token Synchronized.")

    st.markdown('<div class="section-header"><span>ANALYTICS CAPABILITIES</span></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:12px; color:var(--muted); line-height:2.6;">
    🔬 5-Factor Psychological Indexing<br>
    🚩 Cognitive Bias Audit Matrix<br>
    🗣️ Loaded Word & Agitation Filter<br>
    ⚖️ Information Asymmetry Audit<br>
    📋 Executive Editor's Assessment
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"""
    <div style="font-size:11px; color:var(--muted);">
    <span style="display:inline-block; width:8px; height:8px; background:var(--safe); border-radius:50%; margin-right:8px;"></span>
    Engine: Claude 3.5 Sonnet (Pro)<br>
    Status: Analysis Optimized
    </div>
    """, unsafe_allow_html=True)

# ── 4. 메인 대시보드 헤더 ─────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding: 40px 0 45px;" class="reveal">
    <h1 style="font-family:'DM Serif Display',serif; font-size: 82px; color: var(--accent); margin-bottom: 15px; line-height:0.85;">뉴스 심리 프레이밍 분석기</h1>
    <p style="font-family:'IBM Plex Mono',monospace; font-size: 18px; color: var(--muted); letter-spacing: 0.3em; text-transform:uppercase;">
        Strategic Media Intelligence & Psychological Structural Analysis
    </p>
    <div style="width: 120px; height: 6px; background: var(--accent); border-radius: 3px; margin-top: 35px;"></div>
</div>
""", unsafe_allow_html=True)

# ── 5. 기사 입력부 (긴 기사 입력에 최적화) ───────────────────────────────────────────────────
with st.container():
    article_input = st.text_area(
        "분석할 뉴스 기사 본문",
        height=400, # 긴 기사를 위해 높이 상향
        placeholder="분석하고자 하는 뉴스 기사의 전체 텍스트를 입력하세요. 시스템이 즉시 심리적 아키텍처를 추적합니다.",
        label_visibility="collapsed"
    )
    
    stat_col, action_col = st.columns([4, 1])
    with stat_col:
        input_len = len(article_input)
        valid_color = "#22c55e" if input_len >= 120 else "#e84040"
        st.markdown(f"""
        <div style="font-family:'IBM Plex Mono',monospace; font-size:12px; color:{valid_color}; margin-top:15px;">
            {input_len} CHARACTERS LOADED — {"SYSTEM READY FOR DEEP SCAN" if input_len >= 120 else f"MINIMUM 120 CHARS REQUIRED (NEED {120-input_len} MORE)"}
        </div>
        """, unsafe_allow_html=True)
        
    with action_col:
        # 버튼을 누르면 분석 실행
        execute_analysis = st.button("▶ EXECUTE DEEP SCAN", disabled=(input_len < 120))

st.markdown('<div style="margin: 50px 0;"></div>', unsafe_allow_html=True)

# ── 6. 분석 결과 리포트 (Elite Layout) ──────────────────────────────────────────────────
if execute_analysis:
    key_to_use = st.session_state.get('api_key_stored', user_api_key)
    if not key_to_use:
        st.error("⚠️ ACCESS DENIED: API Key is required. Please check the sidebar.")
    else:
        with st.spinner("🔬 Dissecting Media Architecture using Claude 3.5 Pro..."):
            res, error_log = perform_deep_analysis(article_input, key_to_use)
            
        if error_log:
            st.error(f"**CRITICAL ENGINE ERROR**: {error_log}")
            if "404" in error_log:
                st.info("💡 모델 식별자를 다시 확인해 주세요. 현재 시스템은 claude-3-5-sonnet-20241022 버전을 사용 중입니다.")
        else:
            st.markdown('<div class="section-header"><span>DEEP ANALYSIS REPORT</span><span>GENERATED BY PRO ENGINE</span></div>', unsafe_allow_html=True)
            
            main_pane, side_pane = st.columns([3, 2], gap="large")
            
            with main_pane:
                # 섹션 A: 핵심 프레이밍
                st.markdown('<div class="section-title">A. Core Psychological Framing Diagnosis</div>', unsafe_allow_html=True)
                frame_res = res['main_frame']
                st.markdown(f"""
                <div class="frame-hero reveal">
                    <div style="font-family:'IBM Plex Mono',monospace; font-size:11px; color:var(--accent); letter-spacing:0.25em; margin-bottom:15px;">PRIMARY FRAME DETECTED</div>
                    <div style="font-family:'DM Serif Display',serif; font-size:36px; color:#fff; margin-bottom:20px; line-height:1.1;">{frame_res['name']}</div>
                    <div style="font-size:17px; color:var(--text); line-height:1.9;">{frame_res['description']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # 섹션 B: 인지 편향 Matrix
                st.markdown('<div class="section-title">B. Cognitive Bias Audit Matrix</div>', unsafe_allow_html=True)
                for b_unit in res['biases']:
                    st.markdown(f"""
                    <div class="bias-tag reveal">
                        <div style="font-family:'IBM Plex Mono',monospace; font-size:13px; font-weight:700; color:var(--accent2); margin-bottom:12px;">[ {b_unit['name']} ]</div>
                        <div style="font-size:16px; color:#c0c8d8; font-style:italic; line-height:1.8;">"{b_unit['evidence']}"</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # 섹션 D: 정보 불균형 Audit
                st.markdown('<div class="section-title">D. Information Asymmetry Audit</div>', unsafe_allow_html=True)
                asym_res = res['asymmetry']
                st.markdown(f"""
                <div class="glass-card reveal" style="border-left: 6px solid var(--accent); padding: 40px;">
                    <div style="font-family:'IBM Plex Mono'; font-size:11px; color:var(--accent); letter-spacing:0.25em; margin-bottom:15px;">▲ SALIENCE (OVER-EMPHASIZED)</div>
                    <div style="font-size:16px; color:var(--text); line-height:1.9;">{asym_res['over']}</div>
                    <div style="margin: 30px 0; border-top: 1px solid var(--border);"></div>
                    <div style="font-family:'IBM Plex Mono'; font-size:11px; color:#3b82f6; letter-spacing:0.25em; margin-bottom:15px;">▼ OMISSION (MINIMIZED OR GAPS)</div>
                    <div style="font-size:16px; color:var(--text); line-height:1.9;">{asym_res['under']}</div>
                </div>
                """, unsafe_allow_html=True)

                # 섹션 E: 선동 어휘 필터
                st.markdown('<div class="section-title">E. Loaded Words & Emotional Agitation Filter</div>', unsafe_allow_html=True)
                word_report = pd.DataFrame(res['words'])
                word_report.columns = ['자극적 어휘', '심리적 효과', '중립 대체어']
                st.dataframe(word_report, use_container_width=True, hide_index=True)

            with side_pane:
                # 섹션 C: 방사형 차트 (Radar Chart)
                st.markdown('<div class="section-title">C. Psychological Trigger Indexing</div>', unsafe_allow_html=True)
                
                s_trig = res['triggers']
                c_radar = ['분노(Anger)', '공포(Fear)', '혐오(Disgust)', '위기감(Crisis)', '확증편향(Bias)']
                v_radar = [s_trig['anger'], s_trig['fear'], s_trig['disgust'], s_trig['crisis'], s_trig['bias']]
                
                r_fig = go.Figure()
                r_fig.add_trace(go.Scatterpolar(
                    r=v_radar + [v_radar[0]],
                    theta=c_radar + [c_radar[0]],
                    fill='toself',
                    fillcolor='rgba(232, 64, 64, 0.2)',
                    line=dict(color='#e84040', width=4),
                    marker=dict(size=10, color='#fff', line=dict(color='#e84040', width=2)),
                    name='Index'
                ))
                r_fig.update_layout(
                    polar=dict(
                        bgcolor='rgba(0,0,0,0)',
                        radialaxis=dict(visible=True, range=[0, 100], gridcolor='#1e2330', tickfont=dict(size=10, color='#6b7280', family='IBM Plex Mono')),
                        angularaxis=dict(gridcolor='#1e2330', tickfont=dict(size=12, color='#9ca3af', family='Noto Sans KR'))
                    ),
                    paper_bgcolor='rgba(0,0,0,0)',
                    showlegend=False,
                    height=500,
                    margin=dict(l=70, r=70, t=70, b=70)
                )
                st.plotly_chart(r_fig, use_container_width=True)

                # 상세 수치 바 (Visual Feedback)
                m_map = {'anger': '분노', 'fear': '공포', 'disgust': '혐오', 'crisis': '위기감', 'bias': '확증편향'}
                for m_key, m_val in s_trig.items():
                    st.markdown(f"""
                    <div style="margin-bottom:18px;" class="reveal">
                        <div style="display:flex; justify-content:space-between; font-size:14px; margin-bottom:8px;">
                            <span style="color:#9ca3af;">{m_map[m_key]}</span>
                            <span style="font-family:'IBM Plex Mono'; color:var(--accent); font-weight:800;">{m_val}%</span>
                        </div>
                        <div style="background:var(--border); height:6px; border-radius:3px;">
                            <div style="width:{m_val}%; height:100%; background:var(--accent); border-radius:3px; box-shadow: 0 0 12px var(--accent-glow);"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # 최종 요약 (데스크 총평)
                st.markdown('<div style="margin-top:60px;"></div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="summary-box reveal">
                    <div style="font-family:'IBM Plex Mono'; font-size:12px; color:var(--accent2); letter-spacing:0.3em; margin-bottom:18px;">💡 EXECUTIVE EDITOR'S FINAL ASSESSMENT</div>
                    <div style="font-size:17px; line-height:2.0; color:#fff; font-weight:400;">{res['summary']}</div>
                </div>
                """, unsafe_allow_html=True)

            # 푸터
            st.markdown('<hr style="border:none; border-top:2px solid var(--border); margin:70px 0;">', unsafe_allow_html=True)
            st.markdown("""
            <div style="font-family:'IBM Plex Mono',monospace; font-size:11px; color:#374151; text-align:center; letter-spacing:0.3em;">
                CORE COGNITIVE ANALYSIS ENGINE © 2026 · PRIVATE INFRASTRUCTURE · ALL RIGHTS RESERVED
            </div>
            """, unsafe_allow_html=True)

# ── 7. 초기 화면 가이드 ──────────────────────────────────────────────────────────────
else:
    st.markdown('<div style="margin-top:40px;"></div>', unsafe_allow_html=True)
    g_c1, g_c2, g_c3 = st.columns(3)
    g_info = [
        ("01", "PASTE ARTICLE", "분석을 원하는 뉴스 기사 본문을 입력창에 붙여넣으세요. 기사가 길수록 AI가 더 깊은 맥락을 파헤칩니다."),
        ("02", "CORE DISSECTION", "Claude 3.5 Sonnet Pro 엔진이 기사 이면의 심리적 아키텍처와 인지 편향을 정밀 해부합니다."),
        ("03", "VISUAL REPORT", "수치화된 감정 트리거 지수와 선동 어휘 리포트를 통해 보도의 객관성을 즉각 검증하세요.")
    ]
    for g_col, (g_num, g_title, g_desc) in zip([g_c1, g_c2, g_c3], g_info):
        with g_col:
            st.markdown(f"""
            <div style="background:var(--surface); border:1px solid var(--border); border-radius:20px; padding:45px; height:240px;" class="reveal">
                <div style="font-family:'IBM Plex Mono'; font-size:56px; font-weight:600; color:rgba(232, 64, 64, 0.06); margin-bottom:20px; line-height:1;">{g_num}</div>
                <div style="font-weight:700; font-size:18px; margin-bottom:15px; color:#fff; letter-spacing:0.15em;">{g_title}</div>
                <div style="font-size:15px; color:var(--muted); line-height:1.8;">{g_desc}</div>
            </div>
            """, unsafe_allow_html=True)
