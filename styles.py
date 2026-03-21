import streamlit as st

def inject_custom_css():
    st.markdown("""
    <style>
        /* --- TEMEL AYARLAR VE LİNKLER --- */
        .stApp { background-color: #111315; }
        h1, h2, h3, h4, h5, p { color: #e0e6ed !important; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
        
        a { text-decoration: none !important; }
        .custom-link { color: #a0b0c0 !important; text-decoration: none !important; transition: color 0.2s ease, text-shadow 0.2s ease; }
        .custom-link:hover { color: #c5a059 !important; text-shadow: 0 0 8px rgba(197, 160, 89, 0.4) !important; }
        
        .hover-poster-link { display: block; text-decoration: none !important; color: inherit !important; }
        .hover-poster-link:hover, .hover-poster-link:active, .hover-poster-link:visited { text-decoration: none !important; color: inherit !important; }
        .hover-poster-link * { text-decoration: none !important; color: inherit !important; } 

        /* --- STREAMLIT METRIC (ESKİ KPI'lar İÇİN) --- */
        [data-testid="stMetricValue"] { font-size: 1.8rem !important; font-weight: 700 !important; color: #e0e6ed !important; white-space: normal !important; line-height: 1.2 !important; }
        @media (max-width: 768px) { [data-testid="stMetricValue"] { font-size: 1.3rem !important; } }
        [data-testid="stMetricLabel"] { font-size: 0.9rem !important; color: #7a8b99 !important; text-transform: uppercase !important; letter-spacing: 1px !important; }
        
        /* --- 1. YENİ KPI (HEADER) ŞERİDİ CSS --- */
        .kpi-container { display: flex; justify-content: space-between; align-items: center; background: linear-gradient(180deg, #181c20 0%, #111315 100%); padding: 25px 35px; border-radius: 12px; margin-bottom: 30px; border: 1px solid rgba(255, 255, 255, 0.05); box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        .kpi-item { text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center; }
        .kpi-title { color: #7a8b99 !important; font-size: 0.75rem; letter-spacing: 2px; font-weight: 800; text-transform: uppercase; margin-bottom: 8px; }
        .kpi-value { font-size: 2.2rem; font-weight: 900; color: #f5f5f7; line-height: 1; text-shadow: 0 2px 10px rgba(0,0,0,0.5); }
        .kpi-sub { color: #5a6b7c !important; font-size: 0.85rem; font-weight: 600; margin-top: 5px; }
        .kpi-divider { width: 1px; height: 60px; background: linear-gradient(180deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.1) 50%, rgba(255,255,255,0) 100%); }

        /* --- 2. THIS WEEK'S ACTIVITY (ISI HARİTASI & ÖZET) CSS --- */
        @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(204, 51, 51, 0.6); } 70% { box-shadow: 0 0 0 8px rgba(204, 51, 51, 0); } 100% { box-shadow: 0 0 0 0 rgba(204, 51, 51, 0); } }
        .ins-week { background: linear-gradient(180deg, #181c20 0%, #111315 100%); border-radius: 8px; padding: 30px; height: 420px; display: flex; flex-direction: column; justify-content: space-between; position: relative; border: 1px solid rgba(255, 255, 255, 0.05); box-shadow: 0 10px 30px rgba(0,0,0,0.8); transition: 0.3s; }
        .ins-week:hover { border-color: rgba(255, 255, 255, 0.15); }
        .week-top { display: flex; justify-content: space-between; align-items: center; }
        .week-title { color: #e0e6ed; font-size: 0.85rem; font-weight: 800; letter-spacing: 2px; margin: 0; display: flex; align-items: center; gap: 10px; text-transform: uppercase; }
        .pulse-dot { width: 8px; height: 8px; background-color: #cc3333; border-radius: 50%; animation: pulse 2s infinite; }
        .week-stats { display: flex; gap: 15px; margin-top: 15px; }
        .w-stat-item { flex: 1; background: rgba(0,0,0,0.3); padding: 25px 15px; border-radius: 6px; border-left: 2px solid #5a6b7c; display: flex; flex-direction: column; justify-content: center; }
        .w-stat-label { color: #7a8b99; font-size: 0.75rem; letter-spacing: 1px; font-weight: 700; margin-bottom: 8px; text-transform: uppercase; }
        .w-stat-val { color: #f0f0f0; font-size: 3.2rem; font-weight: 900; line-height: 1; margin: 0; }
        .week-date { color: #556677; font-size: 0.85rem; font-family: monospace; text-align: right; margin: 0; letter-spacing: 0.5px; }

        /* --- 3. MOST RECENT WATCH (AFİŞ KARTI) CSS --- */
        .ins-poster-card { border-radius: 8px; border: 1px solid rgba(255, 255, 255, 0.05); height: 420px; width: 280px; margin: 0 auto; position: relative; overflow: hidden; display: flex; flex-direction: column; justify-content: flex-end; box-shadow: 0 10px 30px rgba(0,0,0,0.8); transition: 0.3s; }
        .ins-poster-card:hover { border-color: rgba(255, 255, 255, 0.25); transform: translateY(-3px); }
        .poster-bg { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-size: cover; background-position: center; filter: blur(2px) brightness(0.4); z-index: 1; transition: filter 0.3s ease; }
        .ins-poster-card:hover .poster-bg { filter: blur(0px) brightness(0.5); }
        .poster-content { position: relative; z-index: 2; padding: 30px; height: 100%; display: flex; flex-direction: column; justify-content: space-between; }

        /* --- 4. DEEP INSIGHTS KARTLARI (Marathon, Wasted vs) CSS --- */
        .ins-marathon { display: flex; justify-content: space-between; align-items: center; background: linear-gradient(90deg, #181c20 0%, #111315 100%); border-left: 3px solid #e0e6ed; padding: 20px; border-radius: 6px; margin-bottom: 16px; box-shadow: inset 0 0 20px rgba(0,0,0,0.5); transition: 0.3s; }
        .ins-marathon:hover { transform: scale(1.01); }
        .m-title { color: #e0e6ed !important; font-size: 0.75rem; letter-spacing: 2px; font-weight: 800; margin-bottom: 5px; }
        .m-val { font-size: 2.2rem; font-weight: 900; line-height: 1; margin: 0; color: #f0f0f0; }
        .m-sub { color: #7a8b99 !important; font-size: 0.9rem; margin: 5px 0 0 0; }
        .m-right { text-align: right; border-left: 1px solid rgba(255,255,255,0.05); padding-left: 20px; }
        .m-time { font-size: 1.5rem; font-weight: 700; color: #c5a059; margin: 0; }
        .m-date { color: #667788 !important; font-size: 0.8rem; text-transform: uppercase; margin: 0; }
        
        .ins-wasted { background-color: #111315; border: 1px solid rgba(139, 42, 42, 0.4); border-radius: 6px; padding: 15px 20px; margin-bottom: 16px; position: relative; overflow: hidden; }
        .ins-wasted::before { content: ''; position: absolute; top: 0; right: 0; width: 150px; height: 100%; background: radial-gradient(circle, rgba(139, 42, 42, 0.1) 0%, rgba(0,0,0,0) 70%); }
        .w-title { color: #7a8b99 !important; font-size: 0.8rem; letter-spacing: 1px; font-weight: 600; text-transform: uppercase; margin: 0; }
        .w-val { font-size: 2rem; font-weight: 800; color: #a53838; margin: 5px 0; font-family: 'Courier New', Courier, monospace; letter-spacing: -1px; }
        .w-sub { color: #667788 !important; font-size: 0.85rem; margin: 0; }
        
        .ins-peak { background-color: #181c20; border-bottom: 2px solid #c5a059; border-radius: 6px; padding: 20px; margin-bottom: 16px; text-align: center; }
        .p-title { color: #7a8b99 !important; font-size: 0.8rem; letter-spacing: 1.5px; font-weight: 700; margin-bottom: 10px; }
        .p-flex { display: flex; justify-content: center; align-items: center; gap: 15px; }
        .p-val { font-size: 1.8rem; font-weight: 800; color: #f0f0f0; margin: 0; }
        .p-badge { background: rgba(197, 160, 89, 0.1); border: 1px solid rgba(197, 160, 89, 0.3); color: #c5a059; padding: 4px 12px; border-radius: 20px; font-weight: 800; font-size: 1.1rem; }
        
        .ins-era { display: flex; justify-content: flex-end; align-items: center; gap: 20px; background: linear-gradient(135deg, #15181b 0%, #1a1e23 100%); border-right: 3px solid #5a6b7c; border-radius: 6px; padding: 20px; margin-bottom: 16px; text-align: right; }
        .e-left { text-align: right; }
        .e-title { color: #5a6b7c !important; font-size: 0.75rem; letter-spacing: 2px; font-weight: 800; margin-bottom: 5px; }
        .e-sub { color: #7a8b99 !important; font-size: 0.9rem; margin: 0; }
        .e-val { font-size: 2.8rem; font-weight: 900; color: #e0e6ed; line-height: 1; margin: 0; opacity: 0.9; }
        
        .ins-habit { display: flex; align-items: center; gap: 15px; background-color: #111315; border: 1px dashed rgba(122, 139, 153, 0.4); border-radius: 50px; padding: 10px 25px; width: fit-content; margin-top: 5px; }
        .h-title { color: #667788 !important; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin: 0; }
        .h-val { font-size: 1.2rem; font-weight: 800; color: #a0b0c0; margin: 0; text-transform: uppercase; }

        /* --- 5. HALL OF FAME (MASTERPIECES) CSS --- */
        @keyframes scrollMarquee { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }
        .marquee-wrapper { display: flex; overflow: hidden; width: 100%; mask-image: linear-gradient(to right, transparent, black 5%, black 95%, transparent); -webkit-mask-image: linear-gradient(to right, transparent, black 5%, black 95%, transparent); }
        .marquee-content { display: flex; gap: 15px; padding-right: 15px; animation: scrollMarquee 30s linear infinite; }
        .marquee-wrapper:hover .marquee-content { animation-play-state: paused; }
        .master-poster { width: 110px; height: 165px; border-radius: 6px; background-size: cover; background-position: center; box-shadow: 0 8px 20px rgba(0,0,0,0.8); transition: all 0.3s ease; border: 1px solid rgba(255,255,255,0.05); flex-shrink: 0; filter: grayscale(20%) contrast(110%); }
        .master-poster:hover { transform: translateY(-8px) scale(1.05); border-color: #c5a059; box-shadow: 0 12px 25px rgba(197, 160, 89, 0.4); filter: grayscale(0%) brightness(1.1); z-index: 10; }

        /* --- 6. DECADES OF CINEMA (TIMELINE SLIDER) CSS --- */
        .tm-container { position: relative; width: 100%; height: 420px; border-radius: 16px; overflow: hidden; background: #0a0c0f; border: 1px solid rgba(255,255,255,0.04); box-shadow: 0 25px 50px rgba(0,0,0,0.7); font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif; }
        .tm-container input[type='radio'] { display: none; }
        .tm-bg-container { position: absolute; inset: 0; z-index: 1; overflow: hidden; }
        .tm-bg { position: absolute; inset: -30px; background-size: cover; background-position: center; filter: blur(40px) brightness(0.2); opacity: 0; transition: opacity 0.6s ease; transform: scale(1); }
        .tm-slides-container { position: absolute; inset: 0; z-index: 2; padding-bottom: 70px; }
        .tm-slide { position: absolute; inset: 0; display: flex; align-items: center; justify-content: flex-start; padding: 0 50px; opacity: 0; transform: translateX(40px); transition: opacity 0.4s ease, transform 0s 0.4s; pointer-events: none; gap: 40px; }
        .tm-poster { width: 170px; height: 255px; border-radius: 8px; background-size: cover; background-position: center; box-shadow: 0 15px 35px rgba(0,0,0,0.9), 0 0 0 1px rgba(255,255,255,0.08); flex-shrink: 0; }
        .tm-info { display: flex; flex-direction: column; justify-content: center; max-width: 60%; }
        .tm-date { color: #7a8b99; font-size: 0.85rem; font-weight: 700; letter-spacing: 0.2em; margin-bottom: 12px; }
        .tm-title { color: #F2F2F7; font-size: 2.6rem; font-weight: 800; line-height: 1.1; margin-bottom: 12px; letter-spacing: -0.02em; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; text-overflow: ellipsis; text-shadow: 0 4px 20px rgba(0,0,0,0.5); }
        .tm-rating { color: #FFFFFF; font-size: 1.8rem; font-weight: 300; letter-spacing: 0.05em; display: flex; align-items: center; }
        .tm-nav-wrapper { position: absolute; bottom: 0; left: 0; right: 0; height: 75px; z-index: 999; background: linear-gradient(0deg, rgba(10,12,15,0.95) 0%, rgba(10,12,15,0) 100%); border-top: 1px solid rgba(255,255,255,0.03); overflow: hidden; mask-image: linear-gradient(to right, transparent, black 15%, black 85%, transparent); -webkit-mask-image: linear-gradient(to right, transparent, black 15%, black 85%, transparent); }
        .tm-nav-track { display: flex; position: absolute; height: 100%; align-items: center; transition: transform 0.6s cubic-bezier(0.2, 0.8, 0.2, 1); pointer-events: auto; left: 50%; }
        .tm-nav-item { width: 80px; text-align: center; color: #5a6b7c; font-size: 1.2rem; font-weight: 600; cursor: pointer; transition: all 0.4s ease; position: relative; user-select: none; opacity: 0.5; padding: 15px 0; flex-shrink: 0; }
        .tm-nav-item:hover { opacity: 0.9; color: #a0b0c0; }
        .tm-nav-item::after { content: ''; position: absolute; bottom: 10px; left: 50%; width: 4px; height: 4px; border-radius: 50%; background: #c5a059; transform: translateX(-50%) scaleX(0); transition: all 0.4s cubic-bezier(0.2, 0.8, 0.2, 1); opacity: 0; box-shadow: 0 0 10px rgba(197,160,89,0.8); }
        
        /* --- MOBİL UYUM (RESPONSIVE) --- */
        @media (max-width: 768px) {
            .kpi-container { flex-direction: column !important; align-items: flex-start !important; gap: 20px !important; padding: 20px !important; }
            .kpi-item { border-right: none !important; border-left: 2px solid rgba(197, 160, 89, 0.3) !important; padding: 0 0 0 15px !important; width: 100% !important; }
            [data-testid="stPlotlyChart"] { pointer-events: none; }
        }

    </style>
    """, unsafe_allow_html=True)