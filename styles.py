import streamlit as st

def inject_custom_css():
    st.markdown("""
    <style>
        .stApp { background-color: #111315; }
        h1, h2, h3, h4, h5, p { color: #e0e6ed !important; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
        
        a { text-decoration: none !important; }
        .custom-link { color: #a0b0c0 !important; text-decoration: none !important; transition: color 0.2s ease, text-shadow 0.2s ease; }
        .custom-link:hover { color: #c5a059 !important; text-shadow: 0 0 8px rgba(197, 160, 89, 0.4) !important; }
        
        .hover-poster-link { display: block; text-decoration: none !important; color: inherit !important; }
        .hover-poster-link:hover, .hover-poster-link:active, .hover-poster-link:visited { text-decoration: none !important; color: inherit !important; }
        .hover-poster-link * { text-decoration: none !important; color: inherit !important; } 
        
        .movie-card { background-color: #181c20; border-left: 3px solid #667788; padding: 12px 16px; margin-bottom: 10px; border-radius: 4px; transition: all 0.3s ease; }
        .movie-card:hover { background-color: #1e2429; border-left: 3px solid #c5a059; transform: translateX(5px); }
        .movie-title { font-size: 1.05rem; font-weight: 700; margin: 0 0 4px 0; letter-spacing: 0.5px; color: #f0f0f0 !important; }
        .movie-meta { color: #7a8b99 !important; font-size: 0.85rem; margin: 0; }
        .rating-badge { float: right; background-color: #111315; padding: 4px 8px; border-radius: 4px; color: #c5a059; font-weight: 700; font-size: 0.85rem; border: 1px solid rgba(197, 160, 89, 0.2); }
        
        [data-testid="stMetricValue"] { font-size: 1.8rem !important; font-weight: 700 !important; color: #e0e6ed !important; white-space: normal !important; line-height: 1.2 !important; }
        @media (max-width: 768px) { [data-testid="stMetricValue"] { font-size: 1.3rem !important; } }
        [data-testid="stMetricLabel"] { font-size: 0.9rem !important; color: #7a8b99 !important; text-transform: uppercase !important; letter-spacing: 1px !important; }

        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(204, 51, 51, 0.6); }
            70% { box-shadow: 0 0 0 8px rgba(204, 51, 51, 0); }
            100% { box-shadow: 0 0 0 0 rgba(204, 51, 51, 0); }
        }
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

        .ins-poster-card { border-radius: 8px; border: 1px solid rgba(255, 255, 255, 0.05); height: 420px; position: relative; overflow: hidden; display: flex; flex-direction: column; justify-content: flex-end; box-shadow: 0 10px 30px rgba(0,0,0,0.8); transition: 0.3s; }
        .ins-poster-card:hover { border-color: rgba(255, 255, 255, 0.25); transform: translateY(-3px); }
        .poster-bg { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-size: cover; background-position: center; filter: blur(2px) brightness(0.4); z-index: 1; transition: filter 0.3s ease; }
        .ins-poster-card:hover .poster-bg { filter: blur(0px) brightness(0.5); }
        .poster-content { position: relative; z-index: 2; padding: 30px; height: 100%; display: flex; flex-direction: column; justify-content: space-between; }

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
        
        @media (max-width: 768px) {
            .kpi-container {
                flex-direction: column !important;
                align-items: flex-start !important;
                gap: 20px !important;
                padding: 20px !important;
            }
            .kpi-item {
                border-right: none !important;
                border-left: 2px solid rgba(197, 160, 89, 0.3) !important;
                padding: 0 0 0 15px !important;
                width: 100% !important;
            }
            [data-testid="stMetricValue"] {
                font-size: 1.5rem !important;
            }
        }
    
    </style>
    """, unsafe_allow_html=True)