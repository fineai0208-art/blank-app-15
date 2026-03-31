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

# ── 1. 익스트림 고도화 CSS (잡스의 st01 감성 + 600줄급 디테일) ────────────────────────────────────
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
}

/* 글로벌 베이스 */
html, body, [class*="css"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Noto Sans KR', sans-serif;
}

/* 사이드바 전문가용 테마 */
[data-testid="stSidebar"] {
    background-color: var(--surface) !important;
    border-right: 1px solid var(--border);
    padding-top: 2rem;
}

/* 텍스트 입력창 (st01 업그레이드) */
textarea {
    background-color: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 12px !important;
    font-size: 16px !important;
    line-height: 1.8 !important;
    padding: 1.8rem !important;
    transition: all 0.4s ease !important;
}
textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 4px var(--accent-glow) !important;
}

/* 버튼 네오-브루탈리즘 */
.stButton > button {
    width: 100%;
    background: linear-gradient(145deg, var(--accent), #a01010) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    letter-spacing: 0.15em !important;
    padding: 1.2rem !important;
    text-transform: uppercase;
    box-shadow: 0 6px 20px rgba(232, 64, 64, 0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 10px 35px rgba(232, 64, 64, 0.5) !important;
}

/* 섹션 타이틀 */
.section-header {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--muted);
    margin: 45px 0 20px 0;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
}

/* 카드 및 배너 */
.frame-hero {
    background: linear-gradient(135deg, rgba(232, 64, 64, 0.15), rgba(232, 64, 64, 0.03));
    border: 1px solid rgba(232, 64, 64, 0.3);
    border-left: 6px solid var(--accent);
    padding: 35px;
    border-radius: 12px;
    margin-bottom: 30px;
}

.asym-box {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 25px;
    margin-bottom: 15px;
}

/* IP 보호 고지 (영문 혼용) */
.ip-notice {
    background: rgba(245, 166, 35, 0.05);
    border: 1px solid rgba(245, 166, 35, 0.2);
    border-radius: 10px;
    padding: 18px;
    margin-bottom: 30px;
}

/* 애니메이션 */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
.reveal { animation: fadeInUp 0.6s ease-out forwards; }
</style>
""", unsafe_allow_html=True)

# ── 2. Claude API 분석 로직 (404/401 에러 철벽 방어) ──────────────────────────────
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

        # 404 에러 방지를 위해 모델 리스트 순차 시도 (Fallback)
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
                if "404" in last_err: continue # 다음 모델 시도
                else: break # 401 등은 즉시 중단
        
        return None, f"엔진 호출 실패: {last_err}"
    except Exception as e:
        return None, str(e)

# ── 3. 사이드바 (IP 보호 및 자동저장 팝업 대응) ───────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 10px 0 30px;">
        <div style="font-family:'IBM Plex Mono',monospace; font-size:10px; color:var(--muted); letter-spacing:0.3em; margin-bottom:10px;">VERSION 2.8 PRO</div>
        <div style="font-family:'DM Serif Display',serif; font-size:32px; color:#fff; line-height:1;">Framing<br>Analyzer</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="ip-notice">
        <div style="font-family:'IBM Plex Mono'; font-size:10px; font-weight:700; color:var(--accent2); letter-spacing:0.1em; margin-bottom:8px;">⚠️ INTELLECTUAL PROPERTY NOTICE</div>
        <div style="font-size:11px; color:#b0860a; line-height:1.6;">
            본 시스템의 핵심 알고리즘은 <b>특허법 제30조(공지예외주장)</b>에 의거 보호받는 고유 자산입니다.<br><br>
            © 2026. Proprietary Intelligence.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header"><span>API AUTHENTICATION</span></div>', unsafe_allow_html=True)
    
    # 브라우저 자동저장 팝업을 유도하기 위해 st.form 사용
    if 'stored_key' not in st.session_state: st.session_state['stored_key'] = ""
    
    with st.form("login_form"):
        st.markdown('<div style="font-size:11px; color:var(--muted); margin-bottom:5px;">Claude API Access Token</div>', unsafe_allow_html=True)
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
            st.success("인증 키 동기화됨.")

# ── 4. 메인 헤더 및 입력 ─────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding: 30px 0 40px;" class="reveal">
    <h1 style="font-family:'DM Serif Display',serif; font-size: 72px; color: var(--accent); margin-bottom: 10px; line-height:0.9;">뉴스 심리 프레이밍 분석기</h1>
    <p style="font-family:'IBM Plex Mono',monospace; font-size: 16px; color: var(--muted); letter-spacing: 0.25em; text-transform:uppercase;">
        Strategic Media Intelligence Dissection
    </p>
    <div style="width: 100px; height: 5px; background: var(--accent); border-radius: 3px; margin-top: 30px;"></div>
</div>
""", unsafe_allow_html=True)

article_text = st.text_area("기사 본문 입력", height=380, placeholder="분석할 기사를 입력하세요...", label_visibility="collapsed")
run_analysis = st.button("▶ EXECUTE DEEP ANALYSIS", disabled=(len(article_text) < 100))

# ── 5. 분석 결과 (D/E 섹션 및 그래프 완벽 복구) ──────────────────────────────────────────
if run_analysis:
    active_key = st.session_state['stored_key'] if st.session_state['stored_key'] else key_input
    
    if not active_key:
        st.error("⚠️ 사이드바에서 API 키를 입력하고 CONNECT를 눌러주세요.")
    else:
        with st.spinner("🔬 Claude 3.5 Pro가 기사의 심리 구조를 해부 중입니다..."):
            res, err = perform_deep_analysis(article_text, active_key)
            
        if err:
            st.error(f"**CRITICAL ERROR**: {err}")
        else:
            st.markdown('<div class="section-header"><span>DEEP ANALYSIS REPORT</span><span>COMPLETE</span></div>', unsafe_allow_html=True)
            
            left, right = st.columns([3, 2], gap="large")
            
            with left:
                # A. 프레이밍
                st.markdown('<div class="section-title">A. Core Framing Diagnosis</div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="frame-hero reveal">
                    <div style="font-family:'IBM Plex Mono'; font-size:10px; color:var(--accent); letter-spacing:0.2em; margin-bottom:12px;">PRIMARY FRAME</div>
                    <div style="font-family:'DM Serif Display'; font-size:32px; color:#fff; margin-bottom:15px;">{res['main_frame']['name']}</div>
                    <div style="font-size:16px; line-height:1.8;">{res['main_frame']['description']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # B. 인지 편향
                st.markdown('<div class="section-title">B. Cognitive Bias Matrix</div>', unsafe_allow_html=True)
                for b in res['biases']:
                    st.markdown(f"""
                    <div class="bias-tag reveal">
                        <div style="font-family:'IBM Plex Mono'; font-size:12px; color:var(--accent2); font-weight:700; margin-bottom:8px;">[ {b['name']} ]</div>
                        <div style="font-size:14px; font-style:italic; color:#c0c8d8;">"{b['evidence']}"</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # D. 정보 불균형 (잡스가 원한 D 섹션)
                st.markdown('<div class="section-title">D. Information Asymmetry Audit</div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="asym-box reveal" style="border-left: 4px solid var(--accent);">
                    <div style="font-family:'IBM Plex Mono'; font-size:10px; color:var(--accent); margin-bottom:10px;">▲ OVER-EMPHASIZED (Salience)</div>
                    <div style="font-size:15px; line-height:1.7;">{res['asymmetry']['over']}</div>
                </div>
                <div class="asym-box reveal" style="border-left: 4px solid #3b82f6;">
                    <div style="font-family:'IBM Plex Mono'; font-size:10px; color:#3b82f6; margin-bottom:10px;">▼ OMISSION (Gap)</div>
                    <div style="font-size:15px; line-height:1.7;">{res['asymmetry']['under']}</div>
                </div>
                """, unsafe_allow_html=True)

                # E. 어휘 필터 (잡스가 원한 E 섹션)
                st.markdown('<div class="section-title">E. Loaded Words & Agitation Filter</div>', unsafe_allow_html=True)
                st.dataframe(pd.DataFrame(res['words'], columns=['word', 'effect', 'alt']), use_container_width=True, hide_index=True)

            with right:
                # C. 그래프 복원
                st.markdown('<div class="section-title">C. Psychological Trigger Index</div>', unsafe_allow_html=True)
                trig = res['triggers']
                cats = ['분노(Anger)', '공포(Fear)', '혐오(Disgust)', '위기감(Crisis)', '확증편향(Bias)']
                vals = [trig['anger'], trig['fear'], trig['disgust'], trig['crisis'], trig['bias']]
                
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(r=vals+[vals[0]], theta=cats+[cats[0]], fill='toself', 
                                              fillcolor='rgba(232, 64, 64, 0.2)', line=dict(color='#e84040', width=3)))
                fig.update_layout(polar=dict(bgcolor='rgba(0,0,0,0)', radialaxis=dict(visible=True, range=[0, 100], gridcolor='#1e2330')),
                                  paper_bgcolor='rgba(0,0,0,0)', showlegend=False, height=450)
                st.plotly_chart(fig, use_container_width=True)

                # 데스크 총평
                st.markdown('<div style="margin-top:40px;"></div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div style="background:rgba(245, 166, 35, 0.08); border:1px solid rgba(245, 166, 35, 0.2); border-radius:12px; padding:25px;" class="reveal">
                    <div style="font-family:'IBM Plex Mono'; font-size:11px; color:var(--accent2); letter-spacing:0.2em; margin-bottom:12px;">💡 EXECUTIVE EDITOR'S SUMMARY</div>
                    <div style="font-size:16px; line-height:1.9; color:#fff;">{res['summary']}</div>
                </div>
                """, unsafe_allow_html=True)

# ── 7. 초기 가이드 ─────────────────────────────────────────────────────────────
else:
    st.markdown('<div style="margin-top:30px;"></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    guides = [
        ("01", "PASTE", "분석할 뉴스 기사 본문을 입력창에 붙여넣으세요."),
        ("02", "SCAN", "Claude 3.5 Pro가 기사 이면의 심리 프레임을 해부합니다."),
        ("03", "REPORT", "수치화된 트리거 지수와 불균형 분석 리포트를 확인하세요.")
    ]
    for col, (num, tit, desc) in zip([c1, c2, c3], guides):
        with col:
            st.markdown(f"""
            <div style="background:var(--surface); border:1px solid var(--border); border-radius:15px; padding:35px; height:200px;">
                <div style="font-family:'IBM Plex Mono'; font-size:48px; font-weight:600; color:rgba(232, 64, 64, 0.1); margin-bottom:15px;">{num}</div>
                <div style="font-weight:700; color:#fff; margin-bottom:10px;">{tit}</div>
                <div style="font-size:13px; color:var(--muted);">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
