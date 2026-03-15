import streamlit as st
import streamlit.components.v1 as components
from config import PIPELINE_STEPS
from modules.data_handler    import DataHandler
from modules.session_manager import SessionManager


HERO_CSS = """
<style>
/* INTRO OVERLAY */
#intro-overlay {
    position: fixed; inset: 0;
    background: #0b0f1a;
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
    pointer-events: none;
    animation: overlayFade 2s cubic-bezier(.77,0,.18,1) .2s both;
}
@keyframes overlayFade {
    0%  { opacity: 1; }
    65% { opacity: 1; }
    100%{ opacity: 0; }
}
#intro-lines {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: .7rem;
}
.intro-line {
    height: 2px;
    background: linear-gradient(90deg, transparent, #00e5c0, transparent);
    border-radius: 2px;
    transform: scaleX(0);
    transform-origin: center;
}

/* HERO SECTION */
.hero-section {
    text-align: center;
    padding: 4rem 1rem 1.5rem;
    opacity: 0;
    animation: heroReveal .9s cubic-bezier(.4,0,.2,1) 1.7s both;
}
.hero-section.retrigger {
    animation: none;
    opacity: 0;
    transform: translateY(20px);
    transition: opacity .8s cubic-bezier(.4,0,.2,1), transform .8s cubic-bezier(.4,0,.2,1);
}
.hero-section.retrigger.in-view {
    opacity: 1;
    transform: translateY(0);
}
@keyframes heroReveal {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}
.hero-eyebrow {
    font-family: 'Space Mono', monospace;
    font-size: .7rem;
    letter-spacing: .2em;
    color: #00e5c0;
    text-transform: uppercase;
    margin: 0 0 1rem;
    opacity: .75;
}
.hero-title {
    font-family: 'DM Sans', sans-serif;
    font-size: clamp(2rem, 5vw, 3.2rem);
    font-weight: 700;
    color: #e8edf8;
    line-height: 1.15;
    letter-spacing: -.02em;
    margin: 0 0 .9rem;
}
.hero-pre {
    font-size: clamp(1.3rem, 3.2vw, 2.1rem);
    color: #e8edf8;
    font-weight: 600;
    display: block;
    margin-bottom: .05rem;
    letter-spacing: -.01em;
    line-height: 1.15;
}
.hero-accent {
    color: #00e5c0;
    position: relative;
    display: inline-block;
}
.hero-accent::after {
    content: '';
    position: absolute;
    bottom: -3px; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #00e5c0, #3b82f6);
    transform: scaleX(0);
    transform-origin: left;
    animation: underlineIn .6s cubic-bezier(.4,0,.2,1) 2.3s both;
    transition: transform .55s cubic-bezier(.4,0,.2,1) .3s;
}
@keyframes underlineIn { to { transform: scaleX(1); } }
.hero-section.retrigger .hero-accent::after {
    animation: none;
    transform: scaleX(0);
}
.hero-section.retrigger.in-view .hero-accent::after {
    transform: scaleX(1);
}
.hero-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 1.05rem;
    color: #6b7fa3;
    margin: 0 0 2.5rem;
    font-weight: 300;
    letter-spacing: .01em;
}
.hero-divider {
    width: 60px; height: 1px;
    background: linear-gradient(90deg, transparent, #1f2d45, transparent);
    margin: 2.5rem auto 1.8rem;
}

/* GROUP LABEL */
.group-label {
    font-family: 'Space Mono', monospace;
    font-size: .72rem;
    letter-spacing: .16em;
    color: #00e5c0;
    text-transform: uppercase;
    margin: 1.8rem 0 .8rem;
    padding-left: .2rem;
    opacity: .85;
}
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
</style>
"""


GROUPS = [
    ("📥 Chargement",           PIPELINE_STEPS[0:4]),
    ("🔍 Inspection",            PIPELINE_STEPS[4:6]),
    ("⚙️ Feature Engineering", PIPELINE_STEPS[6:10]),
    ("🤖 Modélisation",     PIPELINE_STEPS[10:15]),
]


class HomeView:

    @staticmethod
    def render_hero():
        """Full hero + grouped pipeline cards + upload gate."""

        st.markdown(HERO_CSS, unsafe_allow_html=True)
        st.markdown('<div id="intro-overlay"><div id="intro-lines"></div></div>',
                    unsafe_allow_html=True)

        # Hero text
        st.markdown("""
        <div class="hero-section">
          <p class="hero-eyebrow">
            Universite Abdelmalek Essaadi &nbsp;&middot;&nbsp; A.U. 2025/2026
          </p>
          <h1 class="hero-title">
            <span class="hero-pre">Prediction du</span>
            <span class="hero-accent">Profit d'Entreprise</span>
          </h1>
          <p class="hero-sub">
            Regression Lineaire Multiple &nbsp;&mdash;&nbsp;
            Preparation des donnees &amp; Prediction
          </p>
        </div>
        """, unsafe_allow_html=True)

        # Upload
        import pathlib, base64
        csv_path = pathlib.Path(__file__).parent.parent / "profitentr.csv"

        st.subheader("1. 📂 Chargement du Jeu de Données")
        fichier = st.file_uploader(
            "Importer le fichier « profitentr » (CSV) depuis votre PC",
            type=["csv"]
        )

        # Download row below uploader
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:.8rem;margin-top:.5rem;">
          <span style="font-family:'DM Sans',sans-serif;font-size:.88rem;color:#6b7fa3;">
            Vous n'avez pas le fichier&nbsp;?
          </span>
          <a href="data:text/csv;base64,UiZEIFNwZW5kLEFkbWluaXN0cmF0aW9uLE1hcmtldGluZyBTcGVuZCxTdGF0ZSxQcm9maXQNCjE2NTM0OS4yLDEzNjg5Ny44LDQ3MTc4NC4xLE5ldyBZb3JrLDE5MjI2MS44Mw0KMTYyNTk3LjcsMTUxMzc3LjU5LDQ0Mzg5OC41MyxDYWxpZm9ybmlhLDE5MTc5Mi4wNg0KMTUzNDQxLjUxLDEwMTE0NS41NSw0MDc5MzQuNTQsQ2FsaWZvcm5pYSwxOTEwNTAuMzkNCjE0NDM3Mi40MSwxMTg2NzEuODUsMzgzMTk5LjYyLE5ldyBZb3JrLDE4MjkwMS45OQ0KMTQyMTA3LjM0LDkxMzkxLjc3LDM2NjE2OC40MixDYWxpZm9ybmlhLDE2NjE4Ny45NA0KMTMxODc2LjksOTk4MTQuNzEsMzYyODYxLjM2LE5ldyBZb3JrLDE1Njk5MS4xMg0KMTM0NjE1LjQ2LDE0NzE5OC44NywxMjc3MTYuODIsQ2FsaWZvcm5pYSwxNTYxMjIuNTENCjEzMDI5OC4xMywxNDU1MzAuMDYsMzIzODc2LjY4LE5ldyBZb3JrLDE1NTc1Mi42DQoxMjA1NDIuNTIsMTQ4NzE4Ljk1LDMxMTYxMy4yOSxOZXcgWW9yaywxNTIyMTEuNzcNCjEyMzMzNC44OCwxMDg2NzkuMTcsMzA0OTgxLjYyLENhbGlmb3JuaWEsMTQ5NzU5Ljk2DQoxMDE5MTMuMDgsMTEwNTk0LjExLDIyOTE2MC45NSxDYWxpZm9ybmlhLDE0NjEyMS45NQ0KMTAwNjcxLjk2LDkxNzkwLjYxLDI0OTc0NC41NSxDYWxpZm9ybmlhLDE0NDI1OS40DQo5Mzg2My43NSwxMjczMjAuMzgsMjQ5ODM5LjQ0LENhbGlmb3JuaWEsMTQxNTg1LjUyDQo5MTk5Mi4zOSwxMzU0OTUuMDcsLENhbGlmb3JuaWEsMTM0MzA3LjM1DQoxMTk5NDMuMjQsMTU2NTQ3LjQyLDI1NjUxMi45MixOZXcgWW9yaywxMzI2MDIuNjUNCjExNDUyMy42MSwxMjI2MTYuODQsMjYxNzc2LjIzLE5ldyBZb3JrLDEyOTkxNy4wNA0KNzgwMTMuMTEsMTIxNTk3LjU1LDI2NDM0Ni4wNixDYWxpZm9ybmlhLDEyNjk5Mi45Mw0KOTQ2NTcuMTYsMTQ1MDc3LjU4LDI4MjU3NC4zMSxOZXcgWW9yaywxMjUzNzAuMzcNCjkxNzQ5LjE2LDExNDE3NS43OSwyOTQ5MTkuNTcsTmV3IFlvcmssMTI0MjY2LjkNCjg2NDE5LjcsMTUzNTE0LjExLDAsTmV3IFlvcmssMTIyNzc2Ljg2DQo3NjI1My44NiwxMTM4NjcuMywyOTg2NjQuNDcsQ2FsaWZvcm5pYSwxMTg0NzQuMDMNCjc4Mzg5LjQ3LDE1Mzc3My40MywyOTk3MzcuMjksTmV3IFlvcmssMTExMzEzLjAyDQo3Mzk5NC41NiwxMjI3ODIuNzUsMzAzMzE5LjI2LENhbGlmb3JuaWEsMTEwMzUyLjI1DQo2NzUzMi41MywxMDU3NTEuMDMsMzA0NzY4LjczLENhbGlmb3JuaWEsMTA4NzMzLjk5DQo3NzA0NC4wMSw5OTI4MS4zNCwxNDA1NzQuODEsTmV3IFlvcmssMTA4NTUyLjA0DQo2NDY2NC43MSwxMzk1NTMuMTYsMTM3OTYyLjYyLENhbGlmb3JuaWEsMTA3NDA0LjM0DQo3NTMyOC44NywxNDQxMzUuOTgsLE5ldyBZb3JrLDEwNTczMy41NA0KNzIxMDcuNiwxMjc4NjQuNTUsMzUzMTgzLjgxLE5ldyBZb3JrLDEwNTAwOC4zMQ0KNzgzODkuNDcsLDI5OTczNy4yOSxOZXcgWW9yaywxMTEzMTMuMDINCjY2MDUxLjUyLDE4MjY0NS41NiwxMTgxNDguMixOZXcgWW9yaywxMDMyODIuMzgNCjY1NjA1LjQ4LDE1MzAzMi4wNiwxMDcxMzguMzgsTmV3IFlvcmssMTAxMDA0LjY0DQo2MTk5NC40OCwxMTU2NDEuMjgsOTExMzEuMjQsTmV3IFlvcmssOTk5MzcuNTkNCjYxMTM2LjM4LDE1MjcwMS45Miw4ODIxOC4yMyxOZXcgWW9yayw5NzQ4My41Ng0KNjM0MDguODYsMTI5MjE5LjYxLDQ2MDg1LjI1LENhbGlmb3JuaWEsOTc0MjcuODQNCjU1NDkzLjk1LDEwMzA1Ny40OSwyMTQ2MzQuODEsTmV3IFlvcmssOTY3NzguOTINCjQ2NDI2LjA3LDE1NzY5My45MiwyMTA3OTcuNjcsQ2FsaWZvcm5pYSw5NjcxMi44DQo5MTc0OS4xNiwxMTQxNzUuNzksLE5ldyBZb3JrLDEyNDI2Ni45DQo0NjAxNC4wMiw4NTA0Ny40NCwyMDU1MTcuNjQsTmV3IFlvcmssOTY0NzkuNTENCjI4NjYzLjc2LDEyNzA1Ni4yMSwyMDExMjYuODIsTmV3IFlvcmssOTA3MDguMTkNCjQ0MDY5Ljk1LDUxMjgzLjE0LDE5NzAyOS40MixDYWxpZm9ybmlhLDg5OTQ5LjE0DQoyMDIyOS41OSw2NTk0Ny45MywxODUyNjUuMSxOZXcgWW9yayw4MTIyOS4wNg0KMzg1NTguNTEsODI5ODIuMDksMTc0OTk5LjMsQ2FsaWZvcm5pYSw4MTAwNS43Ng0KMjg3NTQuMzMsMTE4NTQ2LjA1LDE3Mjc5NS42NyxDYWxpZm9ybmlhLDc4MjM5LjkxDQoyNzg5Mi45Miw4NDcxMC43NywxNjQ0NzAuNzEsQ2FsaWZvcm5pYSw3Nzc5OC44Mw0KMjM2NDAuOTMsOTYxODkuNjMsMTQ4MDAxLjExLENhbGlmb3JuaWEsNzE0OTguNDkNCjE1NTA1LjczLCwzNTUzNC4xNyxOZXcgWW9yayw2OTc1OC45OA0KMjIxNzcuNzQsMTU0ODA2LjE0LDI4MzM0LjcyLENhbGlmb3JuaWEsNjUyMDAuMzMNCjEwMDAuMjMsMTI0MTUzLjA0LDE5MDMuOTMsTmV3IFlvcmssNjQ5MjYuMDgNCjEzMTUuNDYsMTE1ODE2LjIxLDI5NzExNC40NixDYWxpZm9ybmlhLDQ5NDkwLjc1DQowLDEzNTQyNi45MiwwLENhbGlmb3JuaWEsNDI1NTkuNzMNCjU0Mi4wNSw1MTc0My4xNSwwLE5ldyBZb3JrLDM1NjczLjQxDQowLDExNjk4My44LDQ1MTczLjA2LENhbGlmb3JuaWEsMTQ2ODEuNA0K"
             download="profitentr.csv"
             style="display:inline-block;background:#00e5c0;color:#0b0f1a;
                    font-family:'Space Mono',monospace;font-size:.76rem;font-weight:700;
                    letter-spacing:.05em;padding:.35rem .9rem;border-radius:6px;
                    text-decoration:none;">
            Télécharger ici
          </a>
        </div>
        """, unsafe_allow_html=True)



        # Scroll watcher — lives in its own iframe, reaches parent DOM freely
        components.html("""
<script>
(function(){
    // This runs inside an iframe. window.parent is the Streamlit main page.
    var par = window.parent;

    function triggerHero(){
        var h = par.document.querySelector('.hero-section');
        if(!h) return;
        h.classList.add('retrigger');
        h.classList.remove('in-view');
        void h.offsetWidth;
        setTimeout(function(){ h.classList.add('in-view'); }, 20);
    }

    function resetHero(){
        var h = par.document.querySelector('.hero-section');
        if(!h) return;
        h.classList.add('retrigger');
        h.classList.remove('in-view');
    }

    // Find the scrolling container in the parent document
    function findScroller(){
        var doc = par.document;
        var els = [
            doc.querySelector('[data-testid="stAppViewContainer"]'),
            doc.querySelector('[data-testid="stMain"]'),
            doc.documentElement,
            doc.body
        ];
        for(var i=0;i<els.length;i++){
            if(!els[i]) continue;
            var st = par.getComputedStyle(els[i]);
            if(st.overflowY==='auto'||st.overflowY==='scroll') return els[i];
        }
        return doc.documentElement;
    }

    function init(){
        var h = par.document.querySelector('.hero-section');
        if(!h){ setTimeout(init, 100); return; }

        var scroller = findScroller();
        var lastScrollTop = 0;

        scroller.addEventListener('scroll', function(){
            var st = scroller.scrollTop;
            var hero = par.document.querySelector('.hero-section');
            if(!hero) return;

            // Hero rect relative to the scroller
            var heroTop = hero.offsetTop;
            var heroBot = heroTop + hero.offsetHeight;
            var vpH     = scroller.clientHeight;
            var visible = heroBot > st + 60 && heroTop < st + vpH - 60;

            if(visible && st < lastScrollTop){
                // Scrolling UP and hero is visible -> trigger animation
                triggerHero();
            } else if(!visible){
                resetHero();
            }
            lastScrollTop = st;
        }, {passive:true});
    }

    // Start after first-load animation finishes
    setTimeout(init, 2600);
})();
</script>
        """, height=0, scrolling=False)

        if fichier is None:
            st.markdown('<div class="hero-divider"></div>', unsafe_allow_html=True)
            HomeView._render_grouped_cards()
            st.markdown("<div style='margin-top:1.5rem'></div>", unsafe_allow_html=True)
            st.caption(
                "Université Abdelmalek Essaâdi · "
                "Module : Intelligence Artificielle · A.U. 2025/2026"
            )
            return None, None

        handler = DataHandler(fichier)
        SessionManager.set("data_handler", handler)
        st.divider()
        return fichier, handler

    @staticmethod
    def _render_grouped_cards():
        for group_title, steps in GROUPS:
            st.markdown(f'<p class="group-label">{group_title}</p>',
                        unsafe_allow_html=True)
            cols = st.columns(3)
            for i, (icon, title, sub) in enumerate(steps):
                step_num = PIPELINE_STEPS.index((icon, title, sub)) + 1
                with cols[i % 3]:
                    st.markdown(f"""
                    <div class="pipeline-card">
                      <div class="pipeline-icon">{icon}</div>
                      <div>
                        <p class="pipeline-title">
                          <span class="step-badge">{step_num:02d}</span>{title}
                        </p>
                        <p class="pipeline-sub">{sub}</p>
                      </div>
                    </div>""", unsafe_allow_html=True)
            st.markdown("<div style='margin:.6rem 0'></div>", unsafe_allow_html=True)

    @staticmethod
    def render():
        HomeView._render_grouped_cards()