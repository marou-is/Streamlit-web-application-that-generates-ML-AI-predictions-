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

        # Upload + download side by side
        st.subheader("1. 📂 Chargement du Jeu de Données")
        col_dl, col_up = st.columns([1, 2])
        with col_dl:
            import pathlib
            csv_path = pathlib.Path(__file__).parent.parent / "profitentr.csv"
            if csv_path.exists():
                st.download_button(
                    label="📥 Télécharger profitentr.csv",
                    data=csv_path.read_bytes(),
                    file_name="profitentr.csv",
                    mime="text/csv",
                    use_container_width=True,
                )
                st.caption("Pas encore le fichier ? Téléchargez-le ici.")
        with col_up:
            fichier = st.file_uploader(
                "Importer le fichier « profitentr » (CSV) depuis votre PC",
                type=["csv"]
            )


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