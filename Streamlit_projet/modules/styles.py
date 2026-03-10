"""
modules/styles.py — Dark Teal theme
"""
import streamlit as st
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
  --bg:    #0b0f1a;
  --bg2:   #111827;
  --bg3:   #1a2235;
  --rim:   #1f2d45;
  --teal:  #00e5c0;
  --white: #e8edf8;
  --muted: #6b7fa3;
  --r:     10px;
  --mono:  'Space Mono', monospace;
  --sans:  'DM Sans', sans-serif;
}

html,body,[data-testid="stApp"],[data-testid="stAppViewContainer"],
[data-testid="stMain"],.main,.block-container {
  background-color: var(--bg) !important;
  font-family: var(--sans) !important;
  color: var(--white) !important;
}
.block-container { max-width:1060px !important; padding-top:1.8rem !important; padding-bottom:4rem !important; }
[data-testid="stVerticalBlock"],[data-testid="stHorizontalBlock"],[data-testid="column"] { background:transparent !important; }

/* Header */
[data-testid="stHeader"] { 
  background:rgba(11,15,26,.92) !important; 
  backdrop-filter:blur(12px) !important; 
  border-bottom:1px solid var(--rim) !important; 
}

/* Show the three-dots menu */
[data-testid="stHeader"] [data-testid="stStatusWidget"] {
  display: flex !important;
  opacity: 1 !important;
  visibility: visible !important;
}

/* Remove cyan square from deploy button */
[data-testid="stHeader"] [data-testid="stStatusWidget"] [data-testid="baseButton-header"] {
  background: transparent !important;
  border: 1px solid var(--rim) !important;
  border-radius: 6px !important;
}

/* Style the three-dots icon */
[data-testid="stHeader"] [data-testid="stStatusWidget"] svg {
  fill: var(--white) !important;
  color: var(--white) !important;
}

/* Remove any cyan backgrounds */
[data-testid="stHeader"] [data-testid="stStatusWidget"] div[style*="background"] {
  background: transparent !important;
}

/* Keep hover effect clean */
[data-testid="stHeader"] [data-testid="stStatusWidget"] [data-testid="baseButton-header"]:hover {
  border-color: var(--teal) !important;
}

[data-testid="stHeader"] [data-testid="stStatusWidget"] [data-testid="baseButton-header"]:hover svg {
  fill: var(--teal) !important;
}

/* Typography */
p,span,li,[data-testid="stMarkdownContainer"] p,[data-testid="stMarkdownContainer"] li { color:var(--white) !important; font-family:var(--sans) !important; }
[data-testid="stCaptionContainer"] p { color:var(--muted) !important; font-size:.82rem !important; }

[data-testid="stAppViewContainer"] h2,
[data-testid="stAppViewContainer"] h3 {
  font-family:var(--mono) !important; font-weight:700 !important; font-size:.95rem !important;
  color:var(--teal) !important; letter-spacing:.06em !important; text-transform:uppercase !important;
  padding:.5rem 0 .5rem .85rem !important; margin-top:3rem !important; margin-bottom:1.1rem !important;
  border-left:3px solid var(--teal) !important; background:transparent !important; border-radius:0 !important;
}

hr { border:none !important; height:1px !important; background:linear-gradient(90deg,transparent,var(--teal),transparent) !important; margin:.8rem 0 1.4rem !important; opacity:.35 !important; }

/* Buttons */
.stButton > button { background:transparent !important; border:1.5px solid var(--teal) !important; color:var(--teal) !important; font-family:var(--mono) !important; font-size:.82rem !important; letter-spacing:.05em !important; border-radius:6px !important; padding:.45rem 1.5rem !important; transition:all .2s !important; }
.stButton > button:hover { background:var(--teal) !important; color:var(--bg) !important; box-shadow:0 0 18px rgba(0,229,192,.3) !important; }
.stButton > button p,.stButton > button span { color:inherit !important; font-family:var(--mono) !important; }

/* Labels */
[data-testid="stSelectbox"] > label,[data-testid="stRadio"] > label,[data-testid="stSlider"] > label,[data-testid="stNumberInput"] > label { color:var(--muted) !important; font-family:var(--mono) !important; font-size:.76rem !important; letter-spacing:.07em !important; text-transform:uppercase !important; }
[data-testid="stFileUploader"] > label { color:var(--muted) !important; font-family:var(--sans) !important; font-size:.88rem !important; text-transform:none !important; }

/* Selectbox */
[data-baseweb="select"] > div:first-child { background:var(--bg3) !important; border:1px solid var(--rim) !important; border-radius:8px !important; }
[data-baseweb="select"] > div:first-child:hover,[data-baseweb="select"] > div:first-child:focus-within { border-color:var(--teal) !important; }
[data-baseweb="select"] span,[data-baseweb="select"] div { color:var(--white) !important; background:transparent !important; }
[data-baseweb="select"] svg path { fill:var(--teal) !important; }
[data-baseweb="popover"]>div,[data-baseweb="menu"],[role="listbox"] { background:var(--bg2) !important; border:1px solid var(--rim) !important; border-radius:10px !important; box-shadow:0 16px 48px rgba(0,0,0,.6) !important; }
[data-baseweb="menu"] *,[role="listbox"] * { color:var(--white) !important; background:transparent !important; }
li[role="option"] { color:var(--white) !important; background:transparent !important; padding:9px 16px !important; transition:background .15s !important; }
li[role="option"]:hover { background:var(--bg3) !important; color:var(--teal) !important; }
li[aria-selected="true"] { background:var(--bg3) !important; color:var(--teal) !important; font-weight:600 !important; }

/* Inputs */
[data-baseweb="base-input"],[data-baseweb="input"]>div { background:var(--bg3) !important; border:1px solid var(--rim) !important; border-radius:8px !important; }
[data-baseweb="base-input"]:focus-within { border-color:var(--teal) !important; }
[data-baseweb="base-input"] input { color:var(--white) !important; font-family:var(--mono) !important; }
[data-testid="stNumberInput"] button { background:var(--bg3) !important; border:none !important; }
[data-testid="stNumberInput"] button svg path { fill:var(--teal) !important; }

/* Radio / Slider */
[data-testid="stRadio"] [data-testid="stMarkdownContainer"] p { color:var(--white) !important; }
[data-testid="stSlider"] span,[data-testid="stSlider"] [data-testid="stMarkdownContainer"] p { color:var(--white) !important; }
[data-baseweb="slider"] [role="slider"] { background:var(--teal) !important; }

/* File uploader */
[data-testid="stFileUploader"] section { background:var(--bg3) !important; border:1.5px dashed var(--rim) !important; border-radius:var(--r) !important; transition:border-color .2s !important; }
[data-testid="stFileUploader"] section:hover { border-color:var(--teal) !important; }
[data-testid="stFileUploaderDropzoneInstructions"] p,[data-testid="stFileUploaderDropzoneInstructions"] span { color:var(--muted) !important; }
[data-testid="stFileUploader"] button { background:var(--bg3) !important; color:var(--teal) !important; border:1px solid var(--rim) !important; border-radius:6px !important; font-family:var(--mono) !important; }

/* Metrics */
[data-testid="stMetric"] { background:var(--bg3) !important; border:1px solid var(--rim) !important; border-radius:var(--r) !important; padding:1.1rem !important; position:relative !important; overflow:hidden !important; }
[data-testid="stMetric"]::before { content:"" !important; position:absolute !important; top:0;left:0;right:0;height:2px !important; background:linear-gradient(90deg,var(--teal),#3b82f6) !important; }
[data-testid="stMetricLabel"] p { color:var(--muted) !important; font-family:var(--mono) !important; font-size:.72rem !important; text-transform:uppercase !important; letter-spacing:.08em !important; }
[data-testid="stMetricValue"] { color:var(--teal) !important; font-family:var(--mono) !important; font-weight:700 !important; }

/* Alerts */
[data-testid="stAlert"] { background:var(--bg3) !important; border:1px solid var(--rim) !important; border-radius:8px !important; padding:.75rem 1rem !important; margin:.5rem 0 !important; }
[data-testid="stAlert"] p,[data-testid="stAlert"] span { color:var(--white) !important; }

/* Expander */
[data-testid="stExpander"] { background:var(--bg3) !important; border:1px solid var(--rim) !important; border-radius:8px !important; margin:.5rem 0 .9rem !important; }
[data-testid="stExpander"] summary p,[data-testid="stExpander"] summary span { color:var(--teal) !important; font-family:var(--mono) !important; font-size:.8rem !important; }
[data-testid="stExpander"] svg { stroke:var(--teal) !important; }

/* Dataframe */
[data-testid="stDataFrame"] { border:1px solid var(--rim) !important; border-radius:var(--r) !important; overflow:hidden !important; margin:.6rem 0 !important; }
[data-testid="stDataFrame"] * { color:var(--white) !important; }
[data-testid="StyledDataFrameToolbar"] { background:var(--bg2) !important; border:1px solid var(--rim) !important; border-radius:8px !important; }
[data-testid="StyledDataFrameToolbar"] button { background:transparent !important; border:none !important; }
[data-testid="StyledDataFrameToolbar"] button:hover { background:var(--bg3) !important; border-radius:4px !important; }
[data-testid="StyledDataFrameToolbar"] svg path { fill:var(--teal) !important; }

/* Spacing */
.stButton { margin-top:.9rem !important; margin-bottom:.4rem !important; }
[data-testid="stSelectbox"],[data-testid="stSlider"],[data-testid="stRadio"],[data-testid="stNumberInput"] { margin-bottom:.8rem !important; }

/* Scrollbar */
::-webkit-scrollbar { width:5px; height:5px; }
::-webkit-scrollbar-track { background:var(--bg2); }
::-webkit-scrollbar-thumb { background:var(--rim); border-radius:3px; }
::-webkit-scrollbar-thumb:hover { background:var(--teal); }

/* Pipeline cards */
.pipeline-card {
  background:var(--bg3); border:1px solid var(--rim); border-radius:var(--r);
  padding:.95rem 1.1rem; margin:.35rem 0; display:flex; align-items:flex-start; gap:.8rem;
  box-shadow:0 2px 12px rgba(0,0,0,.35); transition:transform .18s,border-color .18s,box-shadow .18s;
  position:relative; overflow:hidden;
}
.pipeline-card::before { content:""; position:absolute; top:0;left:0;right:0;height:2px; background:linear-gradient(90deg,var(--teal),#3b82f6); opacity:0; transition:opacity .18s; }
.pipeline-card:hover { transform:translateY(-2px); border-color:var(--teal); box-shadow:0 6px 20px rgba(0,229,192,.12); }
.pipeline-card:hover::before { opacity:1; }
.pipeline-icon { font-size:1.4rem; line-height:1.3; min-width:2rem; text-align:center; }
.pipeline-title { font-size:.88rem; font-weight:700; color:var(--white); margin:0; font-family:var(--mono); }
.pipeline-sub { font-size:.74rem; color:var(--muted); margin:.15rem 0 0; }
.step-badge { font-size:.6rem; font-weight:700; color:var(--bg); background:var(--teal); border-radius:99px; padding:.1rem .45rem; margin-right:.4rem; vertical-align:middle; font-family:var(--mono); }
</style>
"""

JS = """
<script>
(function(){
  const BG2='#111827',BG3='#1a2235',T='#00e5c0',W='#e8edf8',RIM='#1f2d45';
  function patch(root){
    if(!root?.querySelectorAll)return;
    root.querySelectorAll('[data-baseweb="popover"]>div,[data-baseweb="menu"],[role="listbox"]').forEach(el=>{
      el.style.cssText+='background:'+BG2+'!important;border:1px solid '+RIM+'!important;border-radius:10px!important;box-shadow:0 16px 48px rgba(0,0,0,.6)!important;';
      el.querySelectorAll('span,p,div').forEach(c=>c.style.setProperty('color',W,'important'));
    });
    root.querySelectorAll('li[role="option"]').forEach(li=>{
      li.style.cssText+='background:transparent!important;color:'+W+'!important;';
      li.onmouseenter=()=>{li.style.setProperty('background',BG3,'important');li.style.setProperty('color',T,'important');};
      li.onmouseleave=()=>{li.style.setProperty('background','transparent','important');li.style.setProperty('color',W,'important');};
      if(li.getAttribute('aria-selected')=='true')li.style.setProperty('color',T,'important');
    });
    root.querySelectorAll('[data-testid="StyledDataFrameToolbar"] button').forEach(b=>{b.style.background='transparent';b.querySelectorAll('svg path').forEach(p=>p.style.fill=T);});
    root.querySelectorAll('[data-testid="stHeader"] svg path,[data-testid="stHeader"] svg rect').forEach(el=>el.style.setProperty('fill',T,'important'));
    root.querySelectorAll('[data-testid="stHeaderActionElements"] button > div,[data-testid="stHeaderActionElements"] button svg').forEach(el=>el.style.setProperty('display','none','important'));
  }
  new MutationObserver(ms=>ms.forEach(m=>m.addedNodes.forEach(n=>{if(n.nodeType===1){patch(n);patch(document.body);}}))).observe(document.body,{childList:true,subtree:true});
  [400,900,1800].forEach(t=>setTimeout(()=>patch(document.body),t));
})();
</script>
"""

def inject():
    st.markdown(CSS, unsafe_allow_html=True)
    st.markdown(JS,  unsafe_allow_html=True)
