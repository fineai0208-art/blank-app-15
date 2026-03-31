import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json
import re
import time
import os

# ── 0. 페이지 설정 (Elite Dashboard Config) ───────────────────────────────────────────────────
st.set_page_config(
    page_title="FRAMING ANALYZER — Elite Media Intelligence",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── 1. 익스트림 고도화 CSS (Elite Pro Visual Identity) ──────────────────────────────────────────
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
    --glass:    rgba(255, 255, 255, 0.02);
    --card-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
}

/* 글로벌 베이스 */
html, body, [class*="css"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Noto Sans KR', sans-serif;
    letter-spacing: -0.02em;
}

/* 사이드바 커스텀 */
[data-testid="stSidebar"] {
    background-color: var(--surface) !important;
    border-right: 1px solid var(--border);
    padding-top: 2rem;
}

/* 텍스트 입력창 고도화 */
textarea {
    background-color: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 16px !important;
    font-size: 16px !important;
    line-height: 1.8 !important;
    padding: 2rem !important;
    transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1) !important;
    box-shadow: inset 0 2px 20px rgba(0,0,0,0.3) !important;
}
textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 4px var(--accent-glow) !important;
    transform: translateY(-2px);
}

/* 버튼 네오-브루탈리즘 & 네온 스타일 */
.stButton > button {
    width: 100%;
    background: linear-gradient(145deg, var(--accent), #a01010) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    letter-spacing: 0.18em !important;
    padding: 1.5rem !important;
    text-transform: uppercase;
    box-shadow: 0 8px 25px rgba(232, 64, 64, 0.3) !important;
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
}
.stButton > button:hover {
    transform: translateY(-4px) scale(1.01) !important;
    box-shadow: 0 12px 40px rgba(232, 64, 64, 0.5) !important;
}

/* 섹션 타이틀 헤더 */
.section-header {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    letter-spacing: 0.35em;
    text-transform: uppercase;
    color: var(--muted);
    margin: 50px 0 25px 0;
    padding-bottom: 15px;
    border-bottom: 2px solid var(--border);
    display: flex;
    justify-content: space-between;
}

/* 리포트 카드 디자인 */
.frame-hero {
    background: linear-gradient(135deg, rgba(232, 64, 64, 0.2), rgba(232, 64, 64, 0.04));
    border: 1px solid rgba(232, 64, 64, 0.4);
    border-left: 10px solid var(--accent);
    padding: 45px;
    border-radius: 20px;
    margin-bottom: 35px;
    box-shadow: var(--card-shadow);
}

.asym-box {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 30px;
    margin-bottom: 20px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

.bias-tag {
    background: rgba(245, 166, 35, 0.05);
    border: 1px solid rgba(245, 166, 35, 0.15);
    border-left: 5px solid var(--accent2);
    padding: 22px 28px;
    margin-bottom: 18px;
    border-radius: 12px;
}

/* IP 보호 고지 */
.ip-notice {
    background: rgba(245, 166, 35, 0.04);
    border: 1px solid rgba(245, 166, 35, 0.15);
    border-radius: 14px;
    padding: 24px;
    margin-bottom: 40px;
}

/* 메트릭 박스 */
.metric-box {
    background: var(--glass);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
}

/* 애니메이션 */
@keyframes revealUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}
.reveal { animation: revealUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards; }
</style>
""", unsafe_allow_html=True)

# ── 2. Claude API 분석 로직 (기존 로직 100% 보존) ──────────────────────────────
def perform_deep_analysis(text: str, key: str):
    """Claude Sonnet 3.5 엔진을 활용한 고차원 미디어 심리 해부"""
    if not key or not key.strip().startswith("sk-"):
        return None, "유효한 Claude API 키가 아닙니다."

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=key.strip())
        
        system_prompt = """당신은 30년 경력의 미디어 심리학자이자 전직 보도국 데스크입니다. 
뉴스의 표면적 팩트가 아니라, 독자의 뇌를 어떻게 해킹(Hacking)하는지 분석하세요. 
반드시 JSON 형식으로만 응답하며, 모든 설명은 한국어로 작성합니다."""

        user_prompt = f"""아래 기사를 분석하여 JSON 응답을 생성하세요.
[ARTICLE]:
{text}

[JSON STRUCTURE]:
{{
  "main_frame": {{"name": "프레임명", "description": "분석 내용(2문장)"}},
  "biases": [{{"name": "편향명", "evidence": "구체적 증거 문구"}}],
  "triggers": {{"anger": 0, "fear": 0, "disgust": 0, "crisis": 0, "bias": 0}},
  "words": [{{"word": "단어", "effect": "심리적 영향", "alt": "중립 대체어"}}],
  "asymmetry": {{"over": "과도하게 강조된 포인트", "under": "의도적 누락/축소 포인트"}},
  "summary": "데스크 관점의 냉철한 최종 총평 (2문장)"
}}
각 트리거 수치는 0-100 정수, biases는 3개, words는 5개 추출하세요."""

        # 기존 안정적인 폴백 리스트 유지
        model_candidates = ["claude-3-5-sonnet-20240620", "claude-3-5-sonnet-latest", "claude-3-sonnet-20240229"]
        
        last_err = ""
        for model_id in model_candidates:
            try:
                message = client.messages.create(
                    model=model_id,
                    max_tokens=2500,
                    messages=[{"role": "user", "content": user_prompt}],
                    system=system_prompt
                )
                raw_res = message.content[0].text.strip()
                json_match = re.search(r'\{[\s\S]*\}', raw_res)
                return json.loads(json_match.group()), None
            except Exception as e:
                last_err = str(e)
                if "404" in last_err: continue 
                else: break 
        
        return None, f"엔진 호출 실패: {last_err}"
    except Exception as e:
        return None, str(e)

# ── 3. 사이드바 (IP 보호 및 전문가용 UI) ───────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 10px 0 40px;">
        <div style="font-family:'IBM Plex Mono',monospace; font-size:11px; color:var(--muted); letter-spacing:0.4em; margin-bottom:12px;">SYSTEM V2.9 ELITE</div>
        <div style="font-family:'DM Serif Display',serif; font-size:42px; color:#fff; line-height:0.9;">Framing<br>Analyzer Pro</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="ip-notice">
        <div style="font-family:'IBM Plex Mono'; font-size:10px; font-weight:700; color:var(--accent2); letter-spacing:0.15em; margin-bottom:12px;">⚠️ INTELLECTUAL PROPERTY NOTICE</div>
        <div style="font-size:11px; color:#b0860a; line-height:1.8;">
            본 시스템의 핵심 알고리즘 및 분석 프레임워크는 <b>특허법 제30조(공지예외주장)</b>에 의거 보호받는 고유 자산입니다.<br><br>
            © 2026. Proprietary Media Intelligence.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header"><span>API AUTHENTICATION</span></div>', unsafe_allow_html=True)
    
    if 'stored_key' not in st.session_state: st.session_state['stored_key'] = ""
    
    with st.form("login_form"):
        st.markdown('<div style="font-size:11px; color:var(--muted); margin-bottom:8px;">Claude API Access Token</div>', unsafe_allow_html=True)
        key_input = st.text_input(
            "API Key", 
            type="password", 
            value=st.session_state['stored_key'],
            placeholder="sk-ant-...",
            label_visibility="collapsed",
            autocomplete="current-password"
        )
        save_btn = st.form_submit_button("CONNECT & SECURE")
        if save_btn:
            st.session_state['stored_key'] = key_input.strip()
            st.success("인증 정보가 동기화되었습니다.")

    st.markdown('<div class="section-header"><span>CAPABILITIES</span></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:12px; color:var(--muted); line-height:2.5;">
    🔬 5-Factor Psychological Indexing<br>
    🚩 Cognitive Bias Audit Matrix<br>
    ⚖️ Information Asymmetry Audit<br>
    🗣️ Loaded Word & Agitation Filter
    </div>
    """, unsafe_allow_html=True)

# ── 4. 메인 헤더 및 입력부 ────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding: 40px 0 50px;" class="reveal">
    <h1 style="font-family:'DM Serif Display',serif; font-size: 86px; color: var(--accent); margin-bottom: 10px; line-height:0.85;">뉴스 심리 프레이밍 분석기</h1>
    <p style="font-family:'IBM Plex Mono',monospace; font-size: 18px; color: var(--muted); letter-spacing: 0.35em; text-transform:uppercase;">
        Strategic Media Intelligence & Psychological Dissection
    </p>
    <div style="width: 120px; height: 6px; background: var(--accent); border-radius: 3px; margin-top: 40px;"></div>
</div>
""", unsafe_allow_html=True)

article_text = st.text_area("기사 본문 입력", height=420, placeholder="분석할 뉴스 기사를 입력하세요. AI 미디어 심리학자가 즉시 구조를 해부합니다.", label_visibility="collapsed")

col_left, col_right = st.columns([4, 1])
with col_right:
    run_analysis = st.button("▶ EXECUTE DEEP SCAN", disabled=(len(article_text) < 100))

st.markdown('<div style="margin: 50px 0;"></div>', unsafe_allow_html=True)

# ── 5. 분석 결과 리포팅 (디자인 강화 섹션) ────────────────────────────────────────────────
if run_analysis:
    active_key = st.session_state['stored_key'] if st.session_state['stored_key'] else key_input
    
    if not active_key:
        st.error("⚠️ 사이드바에서 API 키를 입력하고 CONNECT를 눌러주세요.")
    else:
        with st.spinner("🔬 Claude 3.5 Pro가 기사의 심리 구조를 해부 중입니다..."):
            res, err = perform_deep_analysis(article_text, active_key)
            
        if err:
            st.error(f"**CRITICAL ENGINE ERROR**: {err}")
        else:
            st.markdown('<div class="section-header"><span>DEEP ANALYSIS REPORT</span><span>GENERATED BY ELITE ENGINE</span></div>', unsafe_allow_html=True)
            
            main_pane, side_pane = st.columns([3, 2], gap="large")
            
            with main_pane:
                # A. 프레이밍
                st.markdown('<div class="section-header" style="border:none; margin-top:0;"><span>A. Core Framing Diagnosis</span></div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="frame-hero reveal">
                    <div style="font-family:'IBM Plex Mono'; font-size:11px; color:var(--accent); letter-spacing:0.3em; margin-bottom:15px;">PRIMARY FRAME DETECTED</div>
                    <div style="font-family:'DM Serif Display'; font-size:42px; color:#fff; margin-bottom:20px; line-height:1.1;">{res['main_frame']['name']}</div>
                    <div style="font-size:17px; color:var(--text); line-height:1.9;">{res['main_frame']['description']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # B. 인지 편향
                st.markdown('<div class="section-header" style="border:none;"><span>B. Cognitive Bias Matrix</span></div>', unsafe_allow_html=True)
                for b in res['biases']:
                    st.markdown(f"""
                    <div class="bias-tag reveal">
                        <div style="font-family:'IBM Plex Mono'; font-size:13px; color:var(--accent2); font-weight:700; margin-bottom:12px;">[ {b['name']} ]</div>
                        <div style="font-size:15px; font-style:italic; color:#c0c8d8; line-height:1.7;">"{b['evidence']}"</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # D. 정보 불균형 (잡스가 원한 D 섹션)
                st.markdown('<div class="section-header" style="border:none;"><span>D. Information Asymmetry Audit</span></div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="asym-box reveal" style="border-left: 6px solid var(--accent);">
                    <div style="font-family:'IBM Plex Mono'; font-size:11px; color:var(--accent); letter-spacing:0.2em; margin-bottom:15px;">▲ SALIENCE (OVER-EMPHASIZED)</div>
                    <div style="font-size:16px; line-height:1.8; color:var(--text);">{res['asymmetry']['over']}</div>
                </div>
                <div class="asym-box reveal" style="border-left: 6px solid #3b82f6;">
                    <div style="font-family:'IBM Plex Mono'; font-size:11px; color:#3b82f6; letter-spacing:0.2em; margin-bottom:15px;">▼ OMISSION (MINIMIZED OR GAPS)</div>
                    <div style="font-size:16px; line-height:1.8; color:var(--text);">{res['asymmetry']['under']}</div>
                </div>
                """, unsafe_allow_html=True)

                # E. 어휘 필터 (잡스가 원한 E 섹션)
                st.markdown('<div class="section-header" style="border:none;"><span>E. Loaded Words & Agitation Filter</span></div>', unsafe_allow_html=True)
                word_df = pd.DataFrame(res['words'], columns=['word', 'effect', 'alt'])
                word_df.columns = ['자극적 어휘', '심리적 효과', '중립 대체어']
                st.dataframe(word_df, use_container_width=True, hide_index=True)

            with side_pane:
                # C. 그래프
                st.markdown('<div class="section-header" style="border:none; margin-top:0;"><span>C. Psychological Trigger Indexing</span></div>', unsafe_allow_html=True)
                trig = res['triggers']
                cats = ['분노(Anger)', '공포(Fear)', '혐오(Disgust)', '위기감(Crisis)', '확증편향(Bias)']
                vals = [trig['anger'], trig['fear'], trig['disgust'], trig['crisis'], trig['bias']]
                
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                    r=vals + [vals[0]],
                    theta=cats + [cats[0]],
                    fill='toself',
                    fillcolor='rgba(232, 64, 64, 0.2)',
                    line=dict(color='#e84040', width=4),
                    marker=dict(size=10, color='#fff', line=dict(color='#e84040', width=2))
                ))
                fig.update_layout(
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
                st.plotly_chart(fig, use_container_width=True)

                # 트리거 상세 바
                m_map = {'anger': '분노', 'fear': '공포', 'disgust': '혐오', 'crisis': '위기감', 'bias': '확증편향'}
                for m_key, m_val in trig.items():
                    st.markdown(f"""
                    <div style="margin-bottom:18px;" class="reveal">
                        <div style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:8px;">
                            <span style="color:#9ca3af;">{m_map[m_key]}</span>
                            <span style="font-family:'IBM Plex Mono'; color:var(--accent); font-weight:800;">{m_val}%</span>
                        </div>
                        <div style="background:var(--border); height:6px; border-radius:3px;">
                            <div style="width:{m_val}%; height:100%; background:var(--accent); border-radius:3px; box-shadow: 0 0 15px var(--accent-glow);"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # 데스크 총평
                st.markdown('<div style="margin-top:60px;"></div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div style="background:rgba(245, 166, 35, 0.08); border:1px solid rgba(245, 166, 35, 0.2); border-radius:16px; padding:35px;" class="reveal">
                    <div style="font-family:'IBM Plex Mono'; font-size:11px; color:var(--accent2); letter-spacing:0.3em; margin-bottom:18px;">💡 EXECUTIVE EDITOR'S FINAL ASSESSMENT</div>
                    <div style="font-size:17px; line-height:2.0; color:#fff; font-weight:400;">{res['summary']}</div>
                </div>
                """, unsafe_allow_html=True)

            # 푸터
            st.markdown('<hr style="border:none; border-top:2px solid var(--border); margin:80px 0;">', unsafe_allow_html=True)
            st.markdown("""
            <div style="font-family:'IBM Plex Mono',monospace; font-size:11px; color:#374151; text-align:center; letter-spacing:0.4em;">
                ELITE COGNITIVE ANALYSIS ARCHITECTURE © 2026 · ALL RIGHTS RESERVED
            </div>
            """, unsafe_allow_html=True)

# ── 6. 초기 가이드 ─────────────────────────────────────────────────────────────
else:
    st.markdown('<div style="margin-top:40px;"></div>', unsafe_allow_html=True)
    g_c1, g_c2, g_c3 = st.columns(3)
    g_info = [
        ("01", "PASTE", "분석을 원하는 뉴스 기사 본문을 입력창에 붙여넣으세요. 시스템이 텍스트의 심리적 결을 추적할 준비를 합니다."),
        ("02", "SCAN", "Claude 3.5 Pro 엔진이 기사 이면의 심리적 아키텍처와 교묘하게 설계된 인지 편향을 정밀 해부합니다."),
        ("03", "REPORT", "수치화된 감정 트리거 지수와 선동 어휘 리포트를 통해 보도의 객관성을 즉각 검증하세요.")
    ]
    for g_col, (g_num, g_title, g_desc) in zip([g_c1, g_c2, g_c3], g_info):
        with g_col:
            st.markdown(f"""
            <div style="background:var(--surface); border:1px solid var(--border); border-radius:20px; padding:45px; height:260px;" class="reveal">
                <div style="font-family:'IBM Plex Mono'; font-size:64px; font-weight:600; color:rgba(232, 64, 64, 0.05); margin-bottom:20px; line-height:1;">{g_num}</div>
                <div style="font-weight:700; font-size:18px; margin-bottom:15px; color:#fff; letter-spacing:0.15em;">{g_title}</div>
                <div style="font-size:15px; color:var(--muted); line-height:1.8;">{g_desc}</div>
            </div>
            """, unsafe_allow_html=True)
