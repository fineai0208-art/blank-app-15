import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json
import re
import time

# ── 0. 페이지 설정 ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FRAMING ANALYZER — 뉴스 심리 프레이밍 분석기",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── 1. 글로벌 CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=IBM+Plex+Mono:wght@400;600&family=Noto+Sans+KR:wght@300;400;700&display=swap');

:root {
    --bg:       #0a0c10;
    --surface:  #111318;
    --border:   #1e2330;
    --accent:   #e84040;
    --accent2:  #f5a623;
    --text:     #e8eaf0;
    --muted:    #6b7280;
    --safe:     #22c55e;
}

html, body, [class*="css"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Noto Sans KR', sans-serif;
}

/* 사이드바 */
[data-testid="stSidebar"] {
    background-color: var(--surface) !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

/* 입력창 */
textarea, input[type="text"], input[type="password"] {
    background-color: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 6px !important;
    font-family: 'Noto Sans KR', sans-serif !important;
}
textarea:focus, input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(232,64,64,0.2) !important;
}

/* 버튼 */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, var(--accent), #c02020) !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    letter-spacing: 0.08em !important;
    padding: 0.75rem 1.5rem !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(232,64,64,0.4) !important;
}

/* Streamlit 기본 컴포넌트 dark 처리 */
.stSelectbox > div > div,
.stSlider { background: transparent !important; }
[data-baseweb="select"] > div {
    background-color: var(--surface) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
}

/* 스피너 */
.stSpinner > div { border-top-color: var(--accent) !important; }

/* 숨기기 */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem !important; }

/* 커스텀 카드들 */
.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(28px, 4vw, 48px);
    letter-spacing: -0.02em;
    line-height: 1.1;
    color: #fff;
    margin-bottom: 4px;
}
.hero-sub {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.18em;
    color: var(--muted);
    text-transform: uppercase;
    margin-bottom: 32px;
}
.frame-banner {
    background: linear-gradient(135deg, rgba(232,64,64,0.12), rgba(232,64,64,0.03));
    border: 1px solid rgba(232,64,64,0.4);
    border-left: 4px solid var(--accent);
    border-radius: 8px;
    padding: 18px 22px;
    margin-bottom: 16px;
}
.frame-banner .label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.2em;
    color: var(--accent);
    text-transform: uppercase;
    margin-bottom: 6px;
}
.frame-banner .value {
    font-family: 'DM Serif Display', serif;
    font-size: 22px;
    color: #fff;
    margin-bottom: 6px;
}
.frame-banner .desc {
    font-size: 13px;
    color: var(--muted);
    line-height: 1.6;
}
.bias-card {
    background-color: var(--surface);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent2);
    border-radius: 8px;
    padding: 14px 18px;
    margin-bottom: 10px;
}
.bias-card .bias-name {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    font-weight: 600;
    color: var(--accent2);
    margin-bottom: 6px;
    letter-spacing: 0.05em;
}
.bias-card .bias-ev {
    font-size: 13px;
    color: #c0c8d8;
    line-height: 1.6;
    border-left: 2px solid var(--border);
    padding-left: 10px;
    font-style: italic;
}
.summary-box {
    background: linear-gradient(135deg, rgba(245,166,35,0.08), rgba(245,166,35,0.02));
    border: 1px solid rgba(245,166,35,0.3);
    border-radius: 8px;
    padding: 20px 24px;
    margin-top: 16px;
}
.summary-box .s-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.2em;
    color: var(--accent2);
    text-transform: uppercase;
    margin-bottom: 10px;
}
.summary-box .s-text {
    font-size: 14px;
    color: var(--text);
    line-height: 1.8;
}
.asym-box {
    background-color: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px 20px;
    margin-bottom: 12px;
}
.asym-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.ip-notice {
    background: rgba(245,166,35,0.06);
    border: 1px solid rgba(245,166,35,0.2);
    border-radius: 6px;
    padding: 12px 14px;
    font-size: 11px;
    color: #b0860a;
    line-height: 1.6;
    margin-bottom: 20px;
}
.metric-row {
    display: flex;
    gap: 12px;
    margin-bottom: 20px;
}
.metric-item {
    flex: 1;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 12px 14px;
    text-align: center;
}
.metric-num {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 28px;
    font-weight: 600;
    color: var(--accent);
    line-height: 1;
    margin-bottom: 4px;
}
.metric-lbl {
    font-size: 11px;
    color: var(--muted);
}
.section-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 14px;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--border);
}
.divider { border: none; border-top: 1px solid var(--border); margin: 28px 0; }
.status-dot {
    display: inline-block;
    width: 8px; height: 8px;
    border-radius: 50%;
    background: var(--safe);
    margin-right: 6px;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

/* 데이터프레임 다크 테마 */
[data-testid="stDataFrame"] { background: var(--surface) !important; }
.stDataFrame { border: 1px solid var(--border) !important; border-radius: 8px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)


# ── 2. Claude API 분석 함수 ────────────────────────────────────────────────────
def analyze_article(text: str, api_key: str) -> tuple[dict | None, str | None]:
    """Claude API로 기사 심리 프레이밍 분석. (dict, None) or (None, error_str) 반환."""
    try:
        import anthropic

        client = anthropic.Anthropic(api_key=api_key.strip())

        prompt = f"""당신은 30년 경력의 미디어 심리학자이자 전직 보도국 데스크입니다.
아래 뉴스 기사가 독자의 심리를 어떻게 조작하고 어떤 프레임을 씌웠는지 냉정하게 분석하세요.

반드시 아래 JSON 형식으로만 응답하세요.
- 마크다운(```json 등) 절대 사용 금지
- 순수 JSON만 출력
- 모든 설명은 한국어로

{{
  "main_frame": {{
    "name": "주요 프레임명 (예: 공포 소구, 희생양 찾기, 갈등 조장 등)",
    "description": "이 프레임이 기사에서 어떻게 작동하는지 2문장 설명"
  }},
  "biases": [
    {{
      "name": "편향명 (예: 확증편향, 흑백논리, 성급한 일반화 등)",
      "evidence": "기사에서 이 편향을 보여주는 구체적 문구 또는 서술 방식"
    }}
  ],
  "triggers": {{
    "anger": 0,
    "fear": 0,
    "disgust": 0,
    "crisis": 0,
    "bias": 0
  }},
  "words": [
    {{
      "word": "자극적 어휘",
      "effect": "유발하는 심리 반응",
      "alt": "객관적 대체어"
    }}
  ],
  "asymmetry": {{
    "over": "과도하게 강조된 내용",
    "under": "의도적으로 누락되거나 축소된 반론/사실"
  }},
  "summary": "보도국 데스크 관점의 최종 총평. 이 기사의 감정 조작 수위와 저널리즘 품질을 2문장으로 평가."
}}

biases는 최대 3개, words는 3~5개 추출하세요. triggers 값은 0~100 정수입니다.

기사 본문:
{text}"""

        # 404 에러 방지를 위해 모델 리스트를 순차적으로 시도 (Fallback 로직)
        # 1순위: Sonnet 3.5 최신, 2순위: Sonnet 3.5 초기 버전, 3순위: Sonnet 3.5 식별자
        target_models = ["claude-3-5-sonnet-latest", "claude-3-5-sonnet-20240620", "claude-3-5-sonnet-20241022"]
        
        last_exception = None
        for model_id in target_models:
            try:
                message = client.messages.create(
                    model=model_id,
                    max_tokens=1500,
                    messages=[{"role": "user", "content": prompt}]
                )
                raw = message.content[0].text.strip()
                json_match = re.search(r'\{[\s\S]*\}', raw)
                if json_match:
                    return json.loads(json_match.group()), None
            except Exception as e:
                last_exception = e
                # 404 에러인 경우에만 다음 모델로 시도
                if "404" in str(e):
                    continue
                else:
                    break
        
        # 모든 시도가 실패한 경우 마지막 예외 반환
        return None, f"엔진 호출 실패 (모델 404): {str(last_exception)}"

    except json.JSONDecodeError as e:
        return None, f"JSON 파싱 오류: {e}"
    except ImportError:
        return None, "anthropic 패키지가 설치되지 않았습니다.\n터미널에서: pip install anthropic"
    except Exception as e:
        err = str(e)
        if "authentication" in err.lower() or "invalid" in err.lower() or "401" in err:
            return None, "API 키가 유효하지 않습니다. console.anthropic.com에서 키를 확인해주세요."
        if "credit" in err.lower() or "billing" in err.lower() or "402" in err:
            return None, "크레딧이 부족합니다. console.anthropic.com에서 충전해주세요."
        if "rate" in err.lower() or "429" in err:
            return None, "요청이 너무 많습니다. 잠시 후 다시 시도해주세요."
        return None, f"오류: {err}"


# ── 3. 사이드바 ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 8px 0 20px;">
        <div style="font-family:'IBM Plex Mono',monospace; font-size:10px; letter-spacing:0.2em;
                    color:#6b7280; text-transform:uppercase; margin-bottom:4px;">System v1.0</div>
        <div style="font-family:'DM Serif Display',serif; font-size:20px; color:#fff;">
            Framing<br>Analyzer
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="ip-notice">
    ⚠️ <b>지식재산권 보호 고지</b><br><br>
    본 시스템의 핵심 심리 분석 알고리즘 및 프레이밍 평가 로직은
    <b>특허 출원 완료(공지예외주장)</b>된 개발자 고유의 지식재산입니다.<br><br>
    본 페이지는 MBC AI 저널리즘 교육과정 시연 목적으로만 제한 배포됩니다.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">API 설정</div>', unsafe_allow_html=True)

    # secrets 안전 처리: 없으면 빈 문자열
    try:
        default_key = st.secrets.get("ANTHROPIC_API_KEY", "")
    except Exception:
        default_key = ""

    api_key = st.text_input(
        "Claude API Key",
        type="password",
        value=default_key,
        placeholder="sk-ant-...",
        help="console.anthropic.com 에서 발급"
    )

    st.markdown('<hr class="divider" style="margin:16px 0;">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">분석 정보</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:12px; color:#6b7280; line-height:1.8;">
    🔬 심리 트리거 5종 수치화<br>
    🚩 인지편향 최대 3종 감지<br>
    🗣️ 자극 어휘 3~5개 추출<br>
    ⚖️ 정보 불균형 분석<br>
    📋 데스크 총평 생성
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="divider" style="margin:16px 0;">', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-size:11px; color:#6b7280;">
    <span class="status-dot"></span>Claude Sonnet<br>
    <span style="margin-left:14px;">분석 최적화 모드</span>
    </div>
    """, unsafe_allow_html=True)


# ── 4. 메인 헤더 ────────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding: 32px 0 24px;">
    <div style="font-family:'DM Serif Display',serif; font-size:clamp(36px,5vw,64px);
                color:#e84040; line-height:1.05; letter-spacing:-0.02em;">
        뉴스 심리 프레이밍 분석기
    </div>
    <div style="font-family:'DM Serif Display',serif; font-size:clamp(18px,2.5vw,32px);
                color:#6b7280; line-height:1.2; letter-spacing:-0.01em; margin-top:8px;">
        News Psychological Framing Analyzer
    </div>
    <div style="width:60px; height:3px; background:#e84040;
                border-radius:2px; margin-top:20px;"></div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="background:var(--surface); border:1px solid var(--border); border-radius:8px;
            padding:14px 18px; margin-bottom:28px; font-size:13px; color:#9ca3af; line-height:1.7;">
기사 본문을 입력하면 AI 미디어 심리학자가 <b style="color:#e8eaf0;">숨겨진 프레임, 인지편향, 감정 트리거, 선동 어휘</b>를
실시간으로 해부합니다. 단순 긍/부정 감성분석이 아닌 <b style="color:#e8eaf0;">심리 조작 구조</b>를 뜯어냅니다.
</div>
""", unsafe_allow_html=True)

# ── 5. 입력부 ───────────────────────────────────────────────────────────────────
input_text = st.text_area(
    "분석할 뉴스 기사 본문",
    height=220,
    placeholder="여기에 분석할 기사의 전체 텍스트를 복사해서 붙여넣으세요...\n\n최소 80자 이상 입력해야 분석이 시작됩니다.",
    label_visibility="collapsed"
)

char_count = len(input_text)
col_info, col_btn = st.columns([3, 1])
with col_info:
    color = "#22c55e" if char_count >= 80 else "#e84040"
    st.markdown(f"""
    <div style="font-family:'IBM Plex Mono',monospace; font-size:11px; color:{color};
                margin-top:6px; padding: 4px 0;">
    {char_count}자 입력됨 {"✓ 분석 가능" if char_count >= 80 else f"— {80-char_count}자 더 필요"}
    </div>
    """, unsafe_allow_html=True)

with col_btn:
    run = st.button("▶ 분석 실행", disabled=(char_count < 80))

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ── 6. 분석 결과 & 결과 출력 ────────────────────────────────────────────────────
if run:
    if not api_key:
        st.error("⚠️ 사이드바에서 Claude API Key를 입력해주세요.")
        st.stop()

    with st.spinner("🔬 AI 미디어 심리학자가 기사 구조를 해부 중입니다..."):
        data, error = analyze_article(input_text, api_key)

    if error:
        st.error(f"**분석 실패**\n\n{error}")
        st.stop()

    # ── 결과 헤더
    st.markdown("""
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:24px;">
        <div style="font-family:'DM Serif Display',serif; font-size:24px; color:#fff;">심층 분석 리포트</div>
        <div style="font-family:'IBM Plex Mono',monospace; font-size:10px; color:#6b7280;
                    background:var(--surface); border:1px solid var(--border);
                    padding:3px 10px; border-radius:20px; letter-spacing:0.15em;">COMPLETE</div>
    </div>
    """, unsafe_allow_html=True)

    triggers = data.get("triggers", {})
    total_score = round(sum(triggers.values()) / max(len(triggers), 1))
    max_trigger = max(triggers, key=triggers.get) if triggers else "—"
    trigger_labels = {"anger": "분노", "fear": "공포", "disgust": "혐오", "crisis": "위기감", "bias": "확증편향"}
    max_label = trigger_labels.get(max_trigger, max_trigger)

    # ── 요약 메트릭
    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-item">
            <div class="metric-num">{total_score}</div>
            <div class="metric-lbl">감정조작 종합지수</div>
        </div>
        <div class="metric-item">
            <div class="metric-num" style="color:var(--accent2);">{triggers.get(max_trigger, 0)}</div>
            <div class="metric-lbl">최고 트리거 ({max_label})</div>
        </div>
        <div class="metric-item">
            <div class="metric-num" style="font-size:20px;">{len(data.get('biases', []))}</div>
            <div class="metric-lbl">감지된 인지편향</div>
        </div>
        <div class="metric-item">
            <div class="metric-num" style="font-size:20px;">{len(data.get('words', []))}</div>
            <div class="metric-lbl">선동 어휘 수</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── 메인 레이아웃
    left, right = st.columns([3, 2], gap="large")

    with left:
        # 섹션 A: 핵심 프레임
        st.markdown('<div class="section-title">A. 핵심 프레이밍 진단</div>', unsafe_allow_html=True)
        frame = data.get("main_frame", {})
        st.markdown(f"""
        <div class="frame-banner">
            <div class="label">Primary Frame Detected</div>
            <div class="value">{frame.get('name', 'N/A')}</div>
            <div class="desc">{frame.get('description', '')}</div>
        </div>
        """, unsafe_allow_html=True)

        # 섹션 B: 인지편향
        st.markdown('<div class="section-title" style="margin-top:24px;">B. 인지편향 감지</div>', unsafe_allow_html=True)
        biases = data.get("biases", [])
        if biases:
            for b in biases:
                st.markdown(f"""
                <div class="bias-card">
                    <div class="bias-name">[ {b.get('name', '')} ]</div>
                    <div class="bias-ev">{b.get('evidence', '')}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<div style="color:var(--muted); font-size:13px;">감지된 주요 편향 없음</div>', unsafe_allow_html=True)

        # 섹션 D: 정보 불균형
        st.markdown('<div class="section-title" style="margin-top:24px;">D. 정보 불균형 분석</div>', unsafe_allow_html=True)
        asym = data.get("asymmetry", {})
        st.markdown(f"""
        <div class="asym-box" style="border-left:3px solid var(--accent);">
            <div class="asym-label" style="color:var(--accent);">▲ 과도하게 강조됨</div>
            <div style="font-size:13px; color:#c0c8d8; line-height:1.7;">{asym.get('over', 'N/A')}</div>
        </div>
        <div class="asym-box" style="border-left:3px solid #3b82f6;">
            <div class="asym-label" style="color:#3b82f6;">▼ 누락·축소됨</div>
            <div style="font-size:13px; color:#c0c8d8; line-height:1.7;">{asym.get('under', 'N/A')}</div>
        </div>
        """, unsafe_allow_html=True)

        # 섹션 E: 선동 어휘 필터 (D 바로 아래)
        st.markdown('<div class="section-title" style="margin-top:24px;">E. 선동 어휘 필터</div>', unsafe_allow_html=True)
        words = data.get("words", [])
        if words:
            df = pd.DataFrame(words)
            df.columns = ['자극 어휘', '심리 효과', '대체어'] if len(df.columns) == 3 else df.columns
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                height=250,
                column_config={
                    "자극 어휘": st.column_config.TextColumn(width="small"),
                    "심리 효과": st.column_config.TextColumn(width="medium"),
                    "대체어": st.column_config.TextColumn(width="small"),
                }
            )
        else:
            st.markdown('<div style="color:var(--muted); font-size:13px;">추출된 선동 어휘 없음</div>', unsafe_allow_html=True)

    with right:
        # 섹션 C: 방사형 차트 (Elite Pro 시각화 적용)
        st.markdown('<div class="section-title">C. 심리 트리거 지수</div>', unsafe_allow_html=True)

        cats = ['분노\n(Anger)', '공포\n(Fear)', '혐오\n(Disgust)', '위기감\n(Crisis)', '확증편향\n(Bias)']
        vals = [
            triggers.get('anger', 0),
            triggers.get('fear', 0),
            triggers.get('disgust', 0),
            triggers.get('crisis', 0),
            triggers.get('bias', 0),
        ]
        vals_closed = vals + [vals[0]]
        cats_closed = cats + [cats[0]]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=vals_closed,
            theta=cats_closed,
            fill='toself',
            fillcolor='rgba(232, 64, 64, 0.2)', # Neon Fill
            line=dict(color='#e84040', width=4), # Thicker Neon Line
            marker=dict(size=10, color='#fff', line=dict(color='#e84040', width=2)), # Visible Markers
            name='Trigger Index',
            hovertemplate='%{theta}: <b>%{r}</b><extra></extra>'
        ))
        fig.update_layout(
            polar=dict(
                bgcolor='rgba(17,19,24,0)',
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickfont=dict(size=10, color='#6b7280', family='IBM Plex Mono'),
                    gridcolor='#1e2330',
                    linecolor='#1e2330',
                    tickvals=[25, 50, 75, 100]
                ),
                angularaxis=dict(
                    tickfont=dict(size=11, color='#9ca3af', family='Noto Sans KR'),
                    gridcolor='#1e2330',
                    linecolor='#1e2330',
                )
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            margin=dict(l=70, r=70, t=70, b=70), # Elite Spacing
            height=450 # Enhanced Impact
        )
        st.plotly_chart(fig, use_container_width=True)

        # 트리거 수치 상세 바
        st.markdown('<div class="section-title" style="margin-top:8px;">트리거 수치 상세</div>', unsafe_allow_html=True)
        trigger_colors = {
            'anger': '#e84040', 'fear': '#f97316',
            'disgust': '#a855f7', 'crisis': '#f59e0b', 'bias': '#3b82f6'
        }
        trigger_names = {'anger': '분노', 'fear': '공포', 'disgust': '혐오', 'crisis': '위기감', 'bias': '확증편향'}

        for key in ['anger', 'fear', 'disgust', 'crisis', 'bias']:
            v = triggers.get(key, 0)
            c = trigger_colors[key]
            label = trigger_names[key]
            st.markdown(f"""
            <div style="margin-bottom:10px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                    <span style="font-size:12px; color:#9ca3af;">{label}</span>
                    <span style="font-family:'IBM Plex Mono',monospace; font-size:12px;
                                 font-weight:600; color:{c};">{v}</span>
                </div>
                <div style="background:var(--border); border-radius:3px; height:4px; overflow:hidden;">
                    <div style="width:{v}%; height:100%; background:{c};
                                border-radius:3px; transition:width 0.5s ease;
                                box-shadow: 0 0 8px {c}44;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # 데스크 총평 (오른쪽 하단)
        st.markdown(f"""
        <div class="summary-box" style="margin-top:20px;">
            <div class="s-label">💡 데스크 총평</div>
            <div class="s-text">{data.get('summary', '')}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── 하단 주석
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-family:'IBM Plex Mono',monospace; font-size:10px; color:#374151;
                text-align:center; letter-spacing:0.15em;">
    본 분석 결과는 AI 보조 도구의 출력물이며 최종 판단은 저널리스트의 전문 검토를 거쳐야 합니다.
    CORE ALGORITHM © 2025 · PATENT PENDING · ALL RIGHTS RESERVED
    </div>
    """, unsafe_allow_html=True)

else:
    # ── 초기 안내 화면
    c1, c2, c3 = st.columns(3)
    cards = [
        ("01", "기사 입력", "분석할 뉴스 기사 본문을 위 입력창에 붙여넣으세요."),
        ("02", "AI 해부", "Claude가 미디어 심리학 관점에서 기사 구조를 분해합니다."),
        ("03", "리포트 확인", "프레임·편향·트리거·어휘·정보불균형을 시각화로 확인하세요."),
    ]
    for col, (num, title, desc) in zip([c1, c2, c3], cards):
        with col:
            st.markdown(f"""
            <div style="background:var(--surface); border:1px solid var(--border);
                        border-radius:10px; padding:24px 20px; height:140px;">
                <div style="font-family:'IBM Plex Mono',monospace; font-size:28px;
                             font-weight:600; color:var(--border); margin-bottom:10px;">{num}</div>
                <div style="font-weight:700; font-size:14px; margin-bottom:8px; color:#fff;">{title}</div>
                <div style="font-size:12px; color:var(--muted); line-height:1.6;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
