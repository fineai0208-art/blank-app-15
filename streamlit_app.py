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

# ── 1. 글로벌 고도화 CSS (기존 st01.txt 스타일 완벽 계승 + 심미성 극대화) ─────────────────────────────────
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

/* 베이스 레이아웃 */
html, body, [class*="css"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Noto Sans KR', sans-serif;
}

/* 사이드바 전문가용 다크 테마 */
[data-testid="stSidebar"] {
    background-color: var(--surface) !important;
    border-right: 1px solid var(--border);
}

/* 텍스트 영역 고도화 (st01 감성 유지) */
textarea {
    background-color: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 12px !important;
    font-size: 15px !important;
    line-height: 1.7 !important;
    padding: 1.5rem !important;
    transition: all 0.3s ease !important;
}
textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-glow) !important;
}

/* 버튼 네오-브루탈리즘 & 네온 스타일 */
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
    padding: 1.2rem !important;
    text-transform: uppercase;
    box-shadow: 0 4px 20px rgba(232, 64, 64, 0.25) !important;
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
}
.stButton > button:hover {
    transform: translateY(-3px) scale(1.01) !important;
    box-shadow: 0 10px 40px rgba(232, 64, 64, 0.45) !important;
}

/* 섹션 헤더 디자인 */
.section-header {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--muted);
    margin: 40px 0 20px 0;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
}

/* 카드 및 배너 시스템 */
.glass-card {
    background: var(--glass);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 28px;
    margin-bottom: 25px;
    backdrop-filter: blur(10px);
}

.frame-hero {
    background: linear-gradient(135deg, rgba(232, 64, 64, 0.15), rgba(232, 64, 64, 0.03));
    border: 1px solid rgba(232, 64, 64, 0.35);
    border-left: 6px solid var(--accent);
    padding: 35px;
    border-radius: 12px;
    margin-bottom: 30px;
}

.bias-tag {
    background: rgba(245, 166, 35, 0.08);
    border: 1px solid rgba(245, 166, 35, 0.25);
    border-left: 4px solid var(--accent2);
    padding: 18px 22px;
    margin-bottom: 15px;
    border-radius: 10px;
}

/* IP 보호 고지 박스 (영문 혼용 철벽 방어) */
.ip-protection-notice {
    background: rgba(245, 166, 35, 0.05);
    border: 1px solid rgba(245, 166, 35, 0.2);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 35px;
}
.ip-title-en {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    font-weight: 600;
    color: var(--accent2);
    letter-spacing: 0.1em;
    margin-bottom: 10px;
}

/* 메트릭 카드 */
.metric-container {
    display: flex;
    gap: 15px;
    margin-bottom: 35px;
}
.metric-box {
    flex: 1;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
}
.metric-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 32px;
    font-weight: 600;
    color: var(--accent);
    line-height: 1;
}

/* 스크롤바 커스텀 */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: var(--muted); }

/* 애니메이션 효과 */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
.fade-in-up { animation: fadeInUp 0.7s ease-out forwards; }
</style>
""", unsafe_allow_html=True)

# ── 2. Claude API 고도화 분석 로직 (에러 수정 및 모델 최신화) ──────────────────────────────────
def perform_deep_analysis(text: str, key: str):
    """Claude Sonnet 3.5 엔진을 활용한 고차원 미디어 심리 해부"""
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=key)
        
        system_prompt = """당신은 30년 경력의 미디어 심리학자이자 전직 보도국 데스크입니다. 
뉴스의 표면적 팩트가 아니라, 독자의 뇌를 어떻게 해킹(Hacking)하는지 분석하세요. 
반드시 JSON 형식으로만 응답하며, 모든 설명은 한국어로 작성합니다.
마크다운 태그를 포함하지 마세요."""

        user_prompt = f"""아래 기사를 분석하여 JSON 응답을 생성하세요.
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

        # 404 에러를 방지하기 위해 가장 안정적인 모델 ID 사용
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2500,
            temperature=0.3,
            messages=[{"role": "user", "content": user_prompt}],
            system=system_prompt
        )
        
        response_text = message.content[0].text.strip()
        match = re.search(r'\{[\s\S]*\}', response_text)
        if match:
            return json.loads(match.group()), None
        return None, "JSON 파싱 오류가 발생했습니다."
    except Exception as e:
        return None, str(e)

# ── 3. 사이드바 (IP 보호 및 관제 타워) ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 10px 0 35px;">
        <div style="font-family:'IBM Plex Mono',monospace; font-size:10px; color:var(--muted); letter-spacing:0.3em; margin-bottom:10px;">VERSION 2.5 ELITE</div>
        <div style="font-family:'DM Serif Display',serif; font-size:36px; color:#fff; line-height:1;">Framing<br>Analyzer</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="ip-protection-notice">
        <div class="ip-title-en">⚠️ INTELLECTUAL PROPERTY NOTICE</div>
        <div style="font-size:11px; color:#b0860a; line-height:1.7;">
            본 시스템의 핵심 분석 알고리즘 및 지표화 로직은 <b>대한민국 특허법 제30조(공지예외주장)</b>에 의거하여 보호받는 개발자 고유의 지식재산권(IP)입니다.<br><br>
            Any unauthorized use or reproduction of this framework is strictly prohibited and protected under global IP laws.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header"><span>API CONFIGURATION</span></div>', unsafe_allow_html=True)
    user_api_key = st.text_input("Claude API Key", type="password", placeholder="sk-ant-...", help="Anthropic에서 발급받은 키를 입력하세요.")

    st.markdown('<div class="section-header"><span>SYSTEM CAPABILITIES</span></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:12px; color:var(--muted); line-height:2.4;">
    🔬 5-Factor Psychological Indexing<br>
    🚩 Multi-layered Cognitive Bias Audit<br>
    🗣️ Loaded Word & Agitation Filtering<br>
    ⚖️ Information Asymmetry Analysis<br>
    📋 Senior Executive Editor Insight
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"""
    <div style="font-size:11px; color:var(--muted);">
    <span style="display:inline-block; width:8px; height:8px; background:var(--safe); border-radius:50%; margin-right:8px;"></span>
    Engine: Claude 3.5 Sonnet<br>
    Status: Analysis Optimized
    </div>
    """, unsafe_allow_html=True)

# ── 4. 메인 대시보드 헤더 ─────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding: 40px 0 35px;" class="fade-in-up">
    <h1 style="font-family:'DM Serif Display',serif; font-size: 72px; color: var(--accent); margin-bottom: 10px; line-height:0.9;">뉴스 심리 프레이밍 분석기</h1>
    <p style="font-family:'IBM Plex Mono',monospace; font-size: 16px; color: var(--muted); letter-spacing: 0.25em; text-transform:uppercase;">
        Advanced Media Intelligence & Psychological Structural Analysis
    </p>
    <div style="width: 100px; height: 5px; background: var(--accent); border-radius: 3px; margin-top: 30px;"></div>
</div>
""", unsafe_allow_html=True)

# ── 5. 기사 입력부 (디자인 보존) ───────────────────────────────────────────────────────
input_container = st.container()
with input_container:
    article_text = st.text_area(
        "분석할 뉴스 기사 본문",
        height=320,
        placeholder="분석하고자 하는 뉴스 기사의 전체 텍스트를 입력하세요. AI 미디어 심리학자가 즉시 구조를 해부합니다.",
        label_visibility="collapsed"
    )
    
    col_s, col_a = st.columns([4, 1])
    with col_s:
        text_len = len(article_text)
        s_color = "#22c55e" if text_len >= 100 else "#e84040"
        st.markdown(f"""
        <div style="font-family:'IBM Plex Mono',monospace; font-size:12px; color:{s_color}; margin-top:12px;">
            {text_len} CHARS LOADED — {"READY FOR DISSECTION" if text_len >= 100 else f"MINIMUM 100 CHARS REQUIRED (NEED {100-text_len} MORE)"}
        </div>
        """, unsafe_allow_html=True)
        
    with col_a:
        trigger_analysis = st.button("▶ EXECUTE ANALYSIS", disabled=(text_len < 100))

st.markdown('<div style="margin: 45px 0;"></div>', unsafe_allow_html=True)

# ── 6. 분석 결과 렌더링 (잡스가 원한 모든 섹션 완벽 구현) ─────────────────────────────────────
if trigger_analysis:
    if not user_api_key:
        st.error("⚠️ 사이드바에서 Claude API Key를 입력해주시기 바랍니다.")
    else:
        with st.spinner("🔬 기사의 심리적 아키텍처를 해부하는 중입니다... 잠시만 기다려주세요."):
            analysis, err = perform_deep_analysis(article_text, user_api_key)
            
        if err:
            st.error(f"**ANALYSIS FAILED**: {err}")
            if "404" in err:
                st.info("💡 모델 식별자 에러 발생 시, API 계정이 Claude 3.5 Sonnet 모델을 지원하는지 확인해주세요.")
        else:
            # 리포트 헤더
            st.markdown('<div class="section-header"><span>DEEP ANALYSIS REPORT</span><span>GENERATED BY CLAUDE 3.5</span></div>', unsafe_allow_html=True)
            
            # 레이아웃 분할 (3:2)
            left_pane, right_pane = st.columns([3, 2], gap="large")
            
            with left_pane:
                # 섹션 A: 핵심 프레이밍
                st.markdown('<div class="section-title">A. Core Psychological Framing Diagnosis</div>', unsafe_allow_html=True)
                frame_data = analysis['main_frame']
                st.markdown(f"""
                <div class="frame-hero fade-in-up">
                    <div style="font-family:'IBM Plex Mono',monospace; font-size:10px; color:var(--accent); letter-spacing:0.2em; margin-bottom:12px;">PRIMARY FRAME DETECTED</div>
                    <div style="font-family:'DM Serif Display',serif; font-size:32px; color:#fff; margin-bottom:15px;">{frame_data['name']}</div>
                    <div style="font-size:16px; color:var(--text); line-height:1.8;">{frame_data['description']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # 섹션 B: 인지 편향
                st.markdown('<div class="section-title">B. Cognitive Bias Detection Matrix</div>', unsafe_allow_html=True)
                for b_item in analysis['biases']:
                    st.markdown(f"""
                    <div class="bias-tag fade-in-up">
                        <div style="font-family:'IBM Plex Mono',monospace; font-size:13px; font-weight:600; color:var(--accent2); margin-bottom:10px;">[ {b_item['name']} ]</div>
                        <div style="font-size:15px; color:#c0c8d8; font-style:italic; line-height:1.7;">"{b_item['evidence']}"</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # 섹션 D: 정보 불균형 (잡스가 원한 영역)
                st.markdown('<div class="section-title">D. Information Asymmetry Audit</div>', unsafe_allow_html=True)
                asymmetry_data = analysis['asymmetry']
                st.markdown(f"""
                <div class="glass-card fade-in-up" style="border-left: 5px solid var(--accent); padding: 30px;">
                    <div style="font-family:'IBM Plex Mono'; font-size:10px; color:var(--accent); letter-spacing:0.2em; margin-bottom:12px;">▲ SALIENCE (OVER-EMPHASIZED)</div>
                    <div style="font-size:15px; color:var(--text); line-height:1.8;">{asymmetry_data['over']}</div>
                    <div style="margin: 25px 0; border-top: 1px solid var(--border);"></div>
                    <div style="font-family:'IBM Plex Mono'; font-size:10px; color:#3b82f6; letter-spacing:0.2em; margin-bottom:12px;">▼ OMISSION (MINIMIZED OR GAPS)</div>
                    <div style="font-size:15px; color:var(--text); line-height:1.8;">{asymmetry_data['under']}</div>
                </div>
                """, unsafe_allow_html=True)

                # 섹션 E: 선동 어휘 필터
                st.markdown('<div class="section-title">E. Loaded Words & Emotional Agitation Filter</div>', unsafe_allow_html=True)
                word_df = pd.DataFrame(analysis['words'])
                word_df.columns = ['자극적 어휘', '심리적 효과', '중립 대체어']
                st.dataframe(word_df, use_container_width=True, hide_index=True)

            with right_pane:
                # 섹션 C: 방사형 차트 (Radar Chart 복원)
                st.markdown('<div class="section-title">C. Psychological Trigger Indexing</div>', unsafe_allow_html=True)
                
                trig_scores = analysis['triggers']
                cats_radar = ['분노(Anger)', '공포(Fear)', '혐오(Disgust)', '위기감(Crisis)', '확증편향(Bias)']
                vals_radar = [trig_scores['anger'], trig_scores['fear'], trig_scores['disgust'], trig_scores['crisis'], trig_scores['bias']]
                
                radar_fig = go.Figure()
                radar_fig.add_trace(go.Scatterpolar(
                    r=vals_radar + [vals_radar[0]],
                    theta=cats_radar + [cats_radar[0]],
                    fill='toself',
                    fillcolor='rgba(232, 64, 64, 0.18)',
                    line=dict(color='#e84040', width=3.5),
                    marker=dict(size=8, color='#fff'),
                    name='Index'
                ))
                radar_fig.update_layout(
                    polar=dict(
                        bgcolor='rgba(0,0,0,0)',
                        radialaxis=dict(visible=True, range=[0, 100], gridcolor='#1e2330', tickfont=dict(size=9, color='#6b7280', family='IBM Plex Mono')),
                        angularaxis=dict(gridcolor='#1e2330', tickfont=dict(size=11, color='#9ca3af', family='Noto Sans KR'))
                    ),
                    paper_bgcolor='rgba(0,0,0,0)',
                    showlegend=False,
                    height=450,
                    margin=dict(l=60, r=60, t=60, b=60)
                )
                st.plotly_chart(radar_fig, use_container_width=True)

                # 트리거 상세 바 시각화
                trig_map = {'anger': '분노', 'fear': '공포', 'disgust': '혐오', 'crisis': '위기감', 'bias': '확증편향'}
                for t_key, t_val in trig_scores.items():
                    st.markdown(f"""
                    <div style="margin-bottom:15px;" class="fade-in-up">
                        <div style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:6px;">
                            <span style="color:#9ca3af;">{trig_map[t_key]}</span>
                            <span style="font-family:'IBM Plex Mono'; color:var(--accent); font-weight:700;">{t_val}%</span>
                        </div>
                        <div style="background:var(--border); height:5px; border-radius:3px;">
                            <div style="width:{t_val}%; height:100%; background:var(--accent); border-radius:3px; box-shadow: 0 0 10px var(--accent-glow);"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # 최종 요약 (데스크 총평)
                st.markdown('<div style="margin-top:50px;"></div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="summary-box fade-in-up">
                    <div style="font-family:'IBM Plex Mono'; font-size:11px; color:var(--accent2); letter-spacing:0.25em; margin-bottom:15px;">💡 EXECUTIVE EDITOR'S FINAL ASSESSMENT</div>
                    <div style="font-size:16px; line-height:1.9; color:#fff; font-weight:400;">{analysis['summary']}</div>
                </div>
                """, unsafe_allow_html=True)

            # 푸터 주석
            st.markdown('<hr style="border:none; border-top:1px solid var(--border); margin:60px 0;">', unsafe_allow_html=True)
            st.markdown("""
            <div style="font-family:'IBM Plex Mono',monospace; font-size:10px; color:#374151; text-align:center; letter-spacing:0.25em;">
                CORE COGNITIVE ANALYSIS ENGINE © 2026 · PROPRIETARY INFRASTRUCTURE · ALL RIGHTS RESERVED
            </div>
            """, unsafe_allow_html=True)

# ── 7. 초기 화면 안내 가이드 (잡스의 초기 디자인 복원) ───────────────────────────────────────────
else:
    st.markdown('<div style="margin-top:30px;"></div>', unsafe_allow_html=True)
    guide_c1, guide_c2, guide_c3 = st.columns(3)
    guide_data = [
        ("01", "PASTE ARTICLE", "분석을 원하는 뉴스 기사 본문을 위 입력창에 붙여넣으세요. 최소 100자 이상의 텍스트가 정밀 분석을 위해 필요합니다."),
        ("02", "CORE DISSECTION", "Claude 3.5 Sonnet 엔진이 기사 이면의 심리적 아키텍처와 교묘하게 설계된 인지 편향을 해부합니다."),
        ("03", "VISUAL REPORT", "수치화된 감정 트리거 지수와 선동 어휘 리스트를 통해 보도의 객관성과 선동성을 즉각 확인하세요.")
    ]
    for g_col, (g_num, g_title, g_desc) in zip([guide_c1, guide_c2, guide_c3], guide_data):
        with g_col:
            st.markdown(f"""
            <div style="background:var(--surface); border:1px solid var(--border); border-radius:16px; padding:35px; height:200px;" class="fade-in-up">
                <div style="font-family:'IBM Plex Mono'; font-size:48px; font-weight:600; color:rgba(232, 64, 64, 0.08); margin-bottom:15px; line-height:1;">{g_num}</div>
                <div style="font-weight:700; font-size:16px; margin-bottom:12px; color:#fff; letter-spacing:0.1em;">{g_title}</div>
                <div style="font-size:14px; color:var(--muted); line-height:1.7;">{g_desc}</div>
            </div>
            """, unsafe_allow_html=True)
