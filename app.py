import re
import time

import streamlit as st

from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain
from pipeline import extract_text
from tools import scrape_url

# ---------------------------------------------------------------------------
# Branding — change these two lines to make it yours
# ---------------------------------------------------------------------------
APP_NAME = "ThinkTrail"
ACCENT = "#2dd4bf"  # teal

st.set_page_config(page_title=APP_NAME, page_icon="◆", layout="wide")

# ---------------------------------------------------------------------------
# Styling: deep navy + single teal accent, horizontal stepper layout
# ---------------------------------------------------------------------------
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

html, body, [class*="css"], .stApp { font-family: 'Inter', sans-serif; }

.stApp {
    background-color: #0b1020;
    background-image:
        linear-gradient(rgba(255,255,255,.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,.025) 1px, transparent 1px),
        radial-gradient(ellipse at 50% 0%, rgba(45,212,191,.12) 0%, transparent 55%);
    background-size: 42px 42px, 42px 42px, 100% 100%;
    color: #e6edf7;
}
header[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }
.block-container { padding-top: 2.2rem; max-width: 980px; }

/* Hero */
.logo {
    width: 46px; height: 46px; margin: 0 auto 1rem auto;
    border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.4rem; color: #06241f; font-weight: 700;
    background: __ACCENT__;
    box-shadow: 0 0 30px rgba(45,212,191,.45);
}
.title {
    text-align: center;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 3.1rem;
    letter-spacing: -0.03em;
    color: #f4f8ff;
    margin: 0;
}
.title span { color: __ACCENT__; }
.subtitle {
    text-align: center;
    max-width: 520px;
    margin: .7rem auto 1.8rem auto;
    color: #8c9ab3;
    line-height: 1.6;
}

/* Search bar */
.stTextInput label { display: none; }
.stTextInput input {
    height: 3.2rem;
    background: #111a30 !important;
    color: #f4f8ff !important;
    border: 1px solid rgba(255,255,255,.12) !important;
    border-radius: 14px !important;
    padding: 0 1.1rem !important;
    font-size: 1rem !important;
}
.stTextInput input:focus {
    border-color: __ACCENT__ !important;
    box-shadow: 0 0 0 3px rgba(45,212,191,.18) !important;
}
.stTextInput input::placeholder { color: #5f6f8c !important; }

.stButton > button[kind="primary"] {
    height: 3.2rem;
    background: __ACCENT__;
    color: #06241f;
    border: none;
    border-radius: 14px;
    font-weight: 700;
    transition: all .2s ease;
}
.stButton > button[kind="primary"]:hover {
    filter: brightness(1.1);
    box-shadow: 0 6px 24px rgba(45,212,191,.35);
}
.stButton > button[kind="primary"]:disabled { opacity: .35; }

/* Example chips */
.stButton > button[kind="secondary"] {
    background: transparent;
    color: #8c9ab3;
    border: 1px dashed rgba(255,255,255,.18);
    border-radius: 999px;
    font-size: .78rem;
    padding: .2rem .5rem;
    min-height: 0;
    transition: all .2s ease;
}
.stButton > button[kind="secondary"]:hover {
    color: __ACCENT__;
    border-color: __ACCENT__;
    border-style: solid;
}

/* Horizontal stepper */
.stepper { display: flex; margin: 2.2rem 0 1.2rem 0; }
.stp { flex: 1; text-align: center; position: relative; }
.stp::after {
    content: ""; position: absolute; top: 19px; left: 50%;
    width: 100%; height: 2px; background: rgba(255,255,255,.1);
}
.stp:last-child::after { display: none; }
.stp.done::after { background: __ACCENT__; }
.dot {
    position: relative; z-index: 2;
    width: 38px; height: 38px; margin: 0 auto;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-family: 'IBM Plex Mono', monospace; font-size: .85rem;
    background: #0b1020;
    border: 2px solid rgba(255,255,255,.14);
    color: #5f6f8c;
}
.stp.running .dot {
    border-color: __ACCENT__; color: __ACCENT__;
    animation: ring 1.4s ease-in-out infinite;
}
.stp.done .dot { background: __ACCENT__; border-color: __ACCENT__; color: #06241f; font-weight: 700; }
@keyframes ring {
    0%, 100% { box-shadow: 0 0 0 0 rgba(45,212,191,.5); }
    50%      { box-shadow: 0 0 0 9px rgba(45,212,191,0); }
}
.lbl { margin-top: .6rem; font-family: 'Space Grotesk', sans-serif; font-weight: 600; color: #8c9ab3; }
.stp.running .lbl, .stp.done .lbl { color: #f4f8ff; }
.sub { font-size: .74rem; color: #5f6f8c; margin-top: .15rem; }

/* Results */
.rhead {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600; font-size: 1.5rem; color: #f4f8ff;
    margin: 1.4rem 0 .5rem 0; line-height: 1.3;
}
.pills { margin-bottom: 1rem; }
.pill {
    display: inline-block; margin-right: .5rem;
    padding: .2rem .7rem; border-radius: 999px;
    font-family: 'IBM Plex Mono', monospace; font-size: .72rem;
    color: __ACCENT__; background: rgba(45,212,191,.1);
    border: 1px solid rgba(45,212,191,.25);
}
.stTabs [data-baseweb="tab-list"] { gap: 4px; border-bottom: 1px solid rgba(255,255,255,.08); }
.stTabs [data-baseweb="tab"] { background: transparent; color: #8c9ab3; padding: .5rem 1rem; }
.stTabs [aria-selected="true"] { color: __ACCENT__ !important; }
.stTabs [data-baseweb="tab-highlight"] { background-color: __ACCENT__ !important; }
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #0f1730;
    border: 1px solid rgba(255,255,255,.08) !important;
    border-radius: 14px !important;
}
.stDownloadButton > button {
    background: transparent !important;
    color: __ACCENT__ !important;
    border: 1px solid __ACCENT__ !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
}
.stDownloadButton > button:hover { background: rgba(45,212,191,.1) !important; }
a { color: __ACCENT__ !important; }

.foot {
    text-align: center; margin-top: 3rem;
    font-family: 'IBM Plex Mono', monospace; font-size: .68rem; color: #4d5b78;
}
h1, h2, h3, h4 { color: #f4f8ff !important; }
</style>
"""
st.markdown(CSS.replace("__ACCENT__", ACCENT), unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
STEPS = [
    ("Search", "Finds sources"),
    ("Read", "Scrapes content"),
    ("Write", "Drafts report"),
    ("Critique", "Reviews quality"),
]


def render_stepper(placeholder, current: int):
    """current: index of running step, 4 = all done, -1 = idle."""
    html = '<div class="stepper">'
    for i, (name, sub) in enumerate(STEPS):
        if i < current:
            cls, mark = "done", "✓"
        elif i == current:
            cls, mark = "running", str(i + 1)
        else:
            cls, mark = "", str(i + 1)
        html += (
            f'<div class="stp {cls}"><div class="dot">{mark}</div>'
            f'<div class="lbl">{name}</div><div class="sub">{sub}</div></div>'
        )
    html += "</div>"
    placeholder.markdown(html, unsafe_allow_html=True)


def set_topic(value: str):
    st.session_state["topic_input"] = value


def tool_outputs(response) -> str:
    """Raw text returned by tools during an agent run (not the LLM's summary)."""
    parts = []
    for msg in response.get("messages", []):
        if getattr(msg, "type", "") == "tool":
            content = msg.content
            if isinstance(content, list):
                content = "\n".join(c.get("text", "") for c in content if isinstance(c, dict))
            parts.append(str(content))
    return "\n".join(parts)


def extract_urls(text: str) -> list:
    """Unique http(s) links from text, in order of appearance."""
    found = re.findall(r"https?://[^\s\)\]\}>\"'<]+", text or "")
    urls, seen = [], set()
    for u in found:
        u = u.rstrip(".,;:!?*")
        if u not in seen:
            seen.add(u)
            urls.append(u)
    return urls


def scrape_ok(text: str) -> bool:
    return bool(text) and "Could not scrape" not in text and len(text.strip()) > 300


def run_pipeline(topic: str, step_ph) -> dict:
    state = {}
    t0 = time.time()

    # ---- Step 1: search -------------------------------------------------
    render_stepper(step_ph, 0)
    search_agent = build_search_agent()
    search_result = search_agent.invoke(
        {
            "messages": [
                (
                    "user",
                    f"Find recent, reliable and detailed information about: {topic}. "
                    f"Use the web_search tool.",
                )
            ]
        }
    )
    raw_search = tool_outputs(search_result)
    summary = extract_text(search_result)
    state["search_results"] = raw_search or summary
    state["urls"] = extract_urls(raw_search + "\n" + summary)

    # ---- Step 2: read / scrape ------------------------------------------
    render_stepper(step_ph, 1)
    url_list = "\n".join(state["urls"][:5]) or "(none)"
    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke(
        {
            "messages": [
                (
                    "user",
                    f"Research topic: '{topic}'.\n"
                    f"Pick the most relevant URL from this list and scrape it with the "
                    f"scrape_url tool. Use the URL exactly as written.\n\n{url_list}",
                )
            ]
        }
    )
    scraped = tool_outputs(reader_result)
    state["scraped_url"] = next(
        (u for u in state["urls"] if u in str(reader_result.get("messages", ""))), None
    )

    if not scrape_ok(scraped):
        for u in state["urls"][:5]:
            text = scrape_url.invoke({"url": u})
            if scrape_ok(text):
                scraped, state["scraped_url"] = text, u
                break

    state["scraped_content"] = scraped or extract_text(reader_result)

    # ---- Step 3: write --------------------------------------------------
    render_stepper(step_ph, 2)
    research_combined = (
        f"SEARCH RESULTS : \n {state['search_results']} \n\n"
        f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
    )
    state["report"] = writer_chain.invoke({"topic": topic, "research": research_combined})

    # ---- Step 4: critique -----------------------------------------------
    render_stepper(step_ph, 3)
    state["feedback"] = critic_chain.invoke({"report": state["report"]})

    render_stepper(step_ph, 4)
    state["elapsed"] = time.time() - t0
    return state


# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------
st.markdown(
    f"""
    <div class="logo">◆</div>
    <div class="title">{APP_NAME}<span>.</span></div>
    <div class="subtitle">
        Ask anything. Four AI agents search, read, write and critique —
        and hand you a sourced research report.
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Search bar (input + button on one line) and example chips
# ---------------------------------------------------------------------------
c_input, c_btn = st.columns([5, 1.4], gap="small")
with c_input:
    topic = st.text_input(
        "Research topic",
        key="topic_input",
        placeholder="What do you want to research?",
        label_visibility="collapsed",
    )
with c_btn:
    run = st.button("Research →", type="primary", use_container_width=True, disabled=not topic.strip())

examples = ["LLM agents 2026", "CRISPR gene editing", "Fusion energy progress", "AI jobs for freshers"]
chip_cols = st.columns(len(examples), gap="small")
for col, ex in zip(chip_cols, examples):
    col.button(ex, key=f"ex_{ex}", on_click=set_topic, args=(ex,), use_container_width=True)

step_ph = st.empty()
if run:
    pass
elif "state" in st.session_state:
    render_stepper(step_ph, 4)
else:
    render_stepper(step_ph, -1)

if run:
    try:
        st.session_state["topic"] = topic.strip()
        st.session_state["state"] = run_pipeline(topic.strip(), step_ph)
    except Exception as e:
        st.error(f"Something went wrong while running the pipeline: {e}")

# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------
state = st.session_state.get("state")
if state:
    report_text = str(state["report"])
    feedback_text = str(state["feedback"])

    st.markdown(
        f'<div class="rhead">{st.session_state.get("topic", "")}</div>'
        f'<div class="pills">'
        f'<span class="pill">{state["elapsed"]:.0f}s</span>'
        f'<span class="pill">{len(report_text.split())} words</span>'
        f'<span class="pill">{len(state.get("urls", []))} sources</span>'
        f"</div>",
        unsafe_allow_html=True,
    )

    tab_report, tab_feedback, tab_sources, tab_search, tab_scraped = st.tabs(
        ["Report", "Critic Feedback", "Sources", "Search Results", "Scraped Content"]
    )

    with tab_report:
        with st.container(border=True):
            st.markdown(report_text)
        st.download_button(
            "Download report (.md)",
            data=report_text,
            file_name="research_report.md",
            mime="text/markdown",
        )

    with tab_feedback:
        with st.container(border=True):
            st.markdown(feedback_text)

    with tab_sources:
        with st.container(border=True):
            urls = state.get("urls", [])
            if urls:
                scraped_from = state.get("scraped_url")
                for i, u in enumerate(urls, 1):
                    tag = "  ← scraped" if u == scraped_from else ""
                    st.markdown(f"{i}. [{u}]({u}){tag}")
            else:
                st.warning("No links found. Check your TAVILY_API_KEY in .env.")

    with tab_search:
        with st.container(border=True):
            st.markdown(state["search_results"])

    with tab_scraped:
        with st.container(border=True):
            st.markdown(state["scraped_content"])

st.markdown(f'<div class="foot">{APP_NAME} · LangChain multi-agent pipeline · Streamlit</div>', unsafe_allow_html=True)