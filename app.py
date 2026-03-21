import streamlit as st
import pandas as pd
from styles import inject_custom_css
from data_core import load_data, get_latest_movie, get_kpis, fetch_poster_url
import streamlit.components.v1 as components

# 1. PAGE SETTINGS
st.set_page_config(page_title="Letterboxd Analytics", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS INJECTION (Diğer dosyadan çekiliyor)
inject_custom_css()

# ==========================================
# QUOTE + HERO
# ==========================================
import base64 as _b64, os as _os

_img_path = _os.path.join(_os.path.dirname(__file__), "another.jpeg")
with open(_img_path, "rb") as _f:
    _hero_b64 = _b64.b64encode(_f.read()).decode()

st.markdown("""
<div style="padding:28px 0 8px 0;">
    <p style="color:rgba(255,255,255,0.22)!important;font-size:1.05rem;font-weight:400;letter-spacing:0.12em;font-family:Georgia,serif;font-style:italic;margin:0;line-height:1;">
        some masks come off, some don&rsquo;t
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 0. HERO BANNER (THE FACE OF ANOTHER)
# ==========================================
st.markdown(f"""
<style>
    /* --- DESKTOP (PC) GÖRÜNÜMÜ --- */
    #hero-banner {{
        position: relative;
        width: 100%;
        height: 430px;
        margin-bottom: 40px;
        margin-top: 10px;
        border-radius: 12px;
        overflow: hidden;
        background-color: #0a0c0f;
        border: 1px solid rgba(255,255,255,0.04);
        box-shadow: 0 15px 40px rgba(0,0,0,0.6);
    }}
    .hero-img {{
        position: absolute;
        left: 0;
        top: 0;
        width: 65%;
        height: 100%;
        background-image: url('data:image/jpeg;base64,{_hero_b64}');
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center center;
        mask-image: linear-gradient(to right, rgba(0,0,0,1) 50%, rgba(0,0,0,0) 100%);
        -webkit-mask-image: linear-gradient(to right, rgba(0,0,0,1) 50%, rgba(0,0,0,0) 100%);
        filter: grayscale(20%) contrast(110%);
    }}
    .hero-gradient {{
        position: absolute;
        inset: 0;
        background: linear-gradient(to bottom, rgba(10,12,15,0.8) 0%, transparent 15%, transparent 85%, rgba(10,12,15,0.8) 100%);
        pointer-events: none;
    }}
    .hero-content {{
        position: absolute;
        right: 0;
        top: 0;
        width: 45%;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding: 40px 50px 40px 20px;
        z-index: 10;
    }}
    .hero-manifesto {{
        color: rgba(200,212,222,0.85) !important;
        font-size: 0.95rem !important;
        font-weight: 400 !important;
        line-height: 1.8 !important;
        margin: 0 0 20px 0 !important;
        font-family: Georgia, serif !important; /* FONT KURTARILDI */
    }}
    .hero-signature {{
        color: rgba(200,212,222,0.85) !important;
        font-size: 0.65rem !important;
        font-weight: 700 !important;
        letter-spacing: 3px !important;
        text-transform: uppercase !important;
        margin: 0 !important;
        font-family: Georgia, serif !important; /* FONT KURTARILDI */
        font-style: italic !important;
    }}

    /* --- MOBİL (TELEFON) GÖRÜNÜMÜ --- */
    @media (max-width: 768px) {{
        #hero-banner {{
            height: auto; 
        }}
        .hero-img {{
            width: 100%; 
            height: 250px; 
            mask-image: linear-gradient(to bottom, rgba(0,0,0,1) 40%, rgba(0,0,0,0) 100%);
            -webkit-mask-image: linear-gradient(to bottom, rgba(0,0,0,1) 40%, rgba(0,0,0,0) 100%);
        }}
        .hero-content {{
            position: relative; 
            width: 100%;
            height: auto;
            padding: 200px 20px 30px 20px; 
        }}
        .hero-manifesto {{
            font-size: 0.85rem !important;
            text-align: justify !important;
        }}
        .hero-signature {{
            text-align: right !important;
        }}
    }}
</style>

<div id="hero-banner">
    <div class="hero-img"></div>
    <div class="hero-gradient"></div>
    <div class="hero-content">
        <p class="hero-manifesto">
            This project was born from a mix of pure boredom and absolute freedom. I built this system as a direct response to the absurdity of Letterboxd processing my own data just to sell it back to me. Now, fueled by a 24/7 GitHub automation, I construct my archive exactly how I want it, visualizing and tracking my cinematic history strictly on my own terms, in a way no paid subscription ever could.
        </p>
        <p class="hero-signature">created by burak</p>
    </div>
</div>
""", unsafe_allow_html=True)





# 3. DATA PREPARATION (Veriler diğer dosyadan yüklenip hazırlanıyor)
df = load_data()
df_all = df.copy()
df_dates = df_all.dropna(subset=['Watched Date']).copy()
df_dates['DateOnly'] = df_dates['Watched Date'].dt.date 
df_rated = df_all[df_all['Rating'] > 0].copy()

last_name, last_dir, last_runtime, raw_rating, poster_url, last_url = get_latest_movie()
total_films, total_hours, best_dir_name, best_dir_avg, best_genre_name, best_genre_avg, best_genre_count = get_kpis(df_all, df_rated)

# ==========================================
# HEADER & TOP KPI ŞERİDİ
# ==========================================
# app.py içindeki HEADER & TOP KPI ŞERİDİ kısmını bu blokla tamamen değiştir:

dir_slug = best_dir_name.lower().replace(' ', '-')
dir_url = f"https://letterboxd.com/director/{dir_slug}/"


st.markdown(f"""
<div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 25px; margin-top: -20px;">
    <div>
        <a href="https://letterboxd.com/burakxly/" target="_blank" class="custom-link" style="font-size: 0.85rem; font-weight: 600; letter-spacing: 1px;">@burakxly on Letterboxd ↗</a>
    </div>
</div>

<div class="kpi-container" style="display: flex; width: 100%; align-items: center; justify-content: space-between; padding: 20px 10px; margin-bottom: 35px; border-top: 1px solid rgba(255,255,255,0.04); border-bottom: 1px solid rgba(255,255,255,0.04); background: radial-gradient(circle at 50% 50%, rgba(255,255,255,0.015) 0%, transparent 100%);">
    <div class="kpi-item" style="flex: 1; padding: 0 15px; border-right: 1px solid rgba(255,255,255,0.05);">
        <p style="color: #7a8b99; font-size: 0.7rem; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase; margin: 0 0 5px 0;">Total Films</p>
        <p style="color: #e0e6ed; font-size: 2.2rem; font-weight: 700; line-height: 1; margin: 0;">{total_films}</p>
    </div>
    <div class="kpi-item" style="flex: 1; padding: 0 15px; border-right: 1px solid rgba(255,255,255,0.05);">
        <p style="color: #7a8b99; font-size: 0.7rem; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase; margin: 0 0 5px 0;">Total Hours</p>
        <p style="color: #e0e6ed; font-size: 2.2rem; font-weight: 700; line-height: 1; margin: 0;">{total_hours:,.0f} <span style="font-size: 1rem; color: #5a6b7c; font-weight: 500;">hrs</span></p>
    </div>
    <div class="kpi-item" style="flex: 1.8; padding: 0 25px; border-right: 1px solid rgba(255,255,255,0.05);">
        <p style="color: #7a8b99; font-size: 0.7rem; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase; margin: 0 0 5px 0;">Top Director <span style="color: #445566; font-weight: 400;">(Min 5)</span></p>
        <p style="color: #c5a059; font-size: 1.4rem; ..."><a href="{dir_url}" target="_blank" class="custom-link" style="color: #c5a059 !important;">{best_dir_name}</a></p>
        <p style="color: #a0b0c0; font-size: 0.8rem; font-weight: 400; margin: 3px 0 0 0; font-style: italic;">{best_dir_avg:.2f} Avg Rating</p>
    </div>
    <div class="kpi-item" style="flex: 1.8; padding: 0 0 0 25px;">
        <p style="color: #7a8b99; font-size: 0.7rem; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase; margin: 0 0 5px 0;">Top Genre <span style="color: #445566; font-weight: 400;">(Weighted)</span></p>
        <p style="color: #c5a059; font-size: 1.4rem; font-weight: 700; line-height: 1.2; margin: 0; letter-spacing: 0px;">{best_genre_name}</p>
        <p style="color: #a0b0c0; font-size: 0.8rem; font-weight: 400; margin: 3px 0 0 0; font-style: italic;">{best_genre_avg:.2f} Avg • {best_genre_count} Films</p>
    </div>
</div>
""", unsafe_allow_html=True)



# ==========================================
# ROW 2A: ANNUAL GOAL (full width)
# ==========================================

# --------------------------------------------------
# 1. BORDERLESS TRUE APPLE TYPOGRAPHY GOAL
# --------------------------------------------------
current_year = pd.Timestamp.now().year
df_this_year = df_dates[df_dates['Watched_Date_Log'].dt.year == current_year]
yearly_count = len(df_this_year)
goal = 200
progress_pct = min(100, int((yearly_count / goal) * 100))

html_goal = (
    f"<div style='margin-bottom:50px;width:100%;padding-top:10px;'>"
    f"<div style='display:flex;justify-content:space-between;align-items:flex-end;margin-bottom:15px;'>"
    f"<div style=\"font-family:-apple-system,BlinkMacSystemFont,'SF Pro Display','Segoe UI',Roboto,sans-serif;\">"
    f"<div style='color:#8E8E93;font-size:0.75rem;font-weight:600;letter-spacing:0.15em;text-transform:uppercase;margin-bottom:8px;'>{current_year} Campaign</div>"
    f"<div style='color:#F2F2F7;font-size:1.8rem;font-weight:700;letter-spacing:-0.04em;line-height:1;'>Annual Goal</div>"
    f"</div>"
    f"<div style=\"font-family:-apple-system,BlinkMacSystemFont,'SF Pro Display','Segoe UI',Roboto,sans-serif;display:flex;align-items:baseline;gap:6px;\">"
    f"<span style='color:#FFFFFF;font-size:4rem;font-weight:200;letter-spacing:-0.05em;line-height:0.8;'>{yearly_count}</span>"
    f"<span style='color:#636366;font-size:1.2rem;font-weight:500;'>/ {goal}</span>"
    f"</div>"
    f"</div>"
    f"<div style='position:relative;width:100%;height:4px;background-color:rgba(255,255,255,0.06);border-radius:4px;margin-top:25px;'>"
    f"<div style='position:absolute;top:0;left:0;width:{progress_pct}%;height:100%;background:linear-gradient(90deg,#D4AF37,#FDE08B);border-radius:4px;box-shadow:0 0 12px rgba(253,224,139,0.5);transition:width 1.5s cubic-bezier(0.2,0.8,0.2,1);'></div>"
    f"<div style='position:absolute;top:50%;left:{progress_pct}%;transform:translate(-50%,-50%);width:10px;height:10px;background-color:#FFFFFF;border-radius:50%;box-shadow:0 0 8px rgba(255,255,255,0.8);'></div>"
    f"</div>"
    f"</div>"
)
st.markdown(html_goal, unsafe_allow_html=True)


# ==========================================
# ROW 2B: THIS WEEK + MOST RECENT WATCH
# ==========================================
col1, col2 = st.columns([1.2, 0.8], gap="medium")

with col1:
    st.markdown("<h4 style='color: #a0b0c0; margin-bottom: 15px; font-size: 0.9rem; letter-spacing: 1px;'>THIS WEEK'S ACTIVITY</h4>", unsafe_allow_html=True)

    st.markdown("<h4 style='color: #a0b0c0; margin-bottom: 15px; font-size: 0.9rem; letter-spacing: 1px;'>THIS WEEK'S ACTIVITY</h4>", unsafe_allow_html=True)
    if not df_dates.empty:
        max_date = df_dates['Watched_Date_Log'].max()
        start_of_week = max_date - pd.Timedelta(days=max_date.weekday()) 
        end_of_week = start_of_week + pd.Timedelta(days=6)
        df_week = df_dates[(df_dates['Watched_Date_Log'] >= start_of_week) & (df_dates['Watched_Date_Log'] <= end_of_week)]
        week_count = len(df_week)
        week_avg = df_week[df_week['Rating'] > 0]['Rating'].mean() if week_count > 0 else 0.0
        week_runtime = int(df_week['Runtime'].sum()) 
    
        df_week_sorted = df_week.sort_index(ascending=False)
        movie_list_html = '<div style="margin-top: 25px; flex-grow: 1; overflow-y: auto;">'
    
        for idx, row in df_week_sorted.head(8).iterrows():
            m_name, m_year, m_link = str(row['Name']), int(row['Year']), str(row['Letterboxd URI'])
            if len(m_name) > 30: m_name = m_name[:27] + "..."
            year_str = f"({m_year})" if m_year > 0 else ""
            movie_list_html += f'<p style="margin: 0 0 6px 0; font-size: 0.8rem; font-weight: 500; letter-spacing: 0.5px;">▪ <a href="{m_link}" target="_blank" class="custom-link">{m_name} <span style="color: #5a6b7c; font-size: 0.75rem;">{year_str}</span></a></p>'
    
        if len(df_week_sorted) > 8: movie_list_html += f'<p style="margin: 0; font-size: 0.7rem; color: #5a6b7c; font-style: italic;">+ {len(df_week_sorted)-8} more films...</p>'
        movie_list_html += '</div>'
    
        st.markdown(f"""
        <div class="ins-week">
            <div class="week-top">
                <p class="week-title"><span class="pulse-dot"></span> RECORDING</p>
            </div>
            <div class="week-stats">
                <div class="w-stat-item"><p class="w-stat-label">Films</p><p class="w-stat-val">{week_count}</p></div>
                <div class="w-stat-item"><p class="w-stat-label">Rating</p><p class="w-stat-val">{week_avg:.2f}</p></div>
            </div>
            {movie_list_html}
            <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-top: auto; padding-top: 15px; border-top: 1px dashed rgba(255,255,255,0.05);">
                <p style="color: #7a8b99; font-size: 0.8rem; letter-spacing: 1px; font-weight: 600; margin: 0; text-transform: uppercase;">Total: <span style="color: #c5a059;">{week_runtime} mins</span></p>
                <p class="week-date" style="margin: 0;">[{start_of_week.strftime('%b %d')} - {end_of_week.strftime('%b %d')}]</p>
            </div>
        </div>
        """, unsafe_allow_html=True)


with col2:

    st.markdown("<h4 style='color: #a0b0c0; margin-bottom: 15px; font-size: 0.9rem; letter-spacing: 1px;'>MOST RECENT WATCH</h4>", unsafe_allow_html=True)
    full_stars = int(raw_rating)
    has_half_star = (raw_rating % 1 != 0)
    stars = "★" * full_stars + ("½" if has_half_star else "") + "☆" * (5 - full_stars - int(has_half_star)) if raw_rating > 0 else "No Rating"

    st.markdown(f"""
    <a href="{last_url}" target="_blank" class="hover-poster-link">
        <div class="ins-poster-card">
            <div class="poster-bg" style="background-image: url('{poster_url}');"></div>
            <div class="poster-content">
                <div>
                    <p style="color: #a0b0c0 !important; font-size: 0.75rem; letter-spacing: 1.5px; margin-bottom: 10px; text-transform: uppercase; text-shadow: 1px 1px 3px rgba(0,0,0,0.9);">Latest Entry</p>
                    <h2 style="font-size: 1.1rem; color: #f0f0f0 !important; margin: 0 0 2px 0; line-height: 1.4; font-weight: 800; text-transform: uppercase; text-shadow: 1px 1px 3px rgba(0,0,0,0.9);">{last_name}</h2>
                    <p style="color: #ccd6dd !important; font-size: 0.8rem; font-weight: 400; font-style: italic; margin: 0 0 15px 0; letter-spacing: 0.5px; text-shadow: 1px 1px 3px rgba(0,0,0,0.9);">{last_dir} • {last_runtime} mins</p>
                </div>
                <div>
                    <div style="color: #c5a059 !important; font-size: 1.3rem; letter-spacing: 3px; margin-bottom: 10px; text-shadow: 1px 1px 3px rgba(0,0,0,0.9);">{stars}</div>
                    <p style="color: #e0e6ed !important; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1px; margin: 0; text-shadow: 1px 1px 3px rgba(0,0,0,0.9);">Auto-synced via Bot</p>
                </div>
            </div>
        </div>
    </a>
    """, unsafe_allow_html=True)


# ==========================================
# ROW 2C: HALL OF FAME (full width)
# ==========================================
st.markdown("<div style='margin-top:40px;'></div>", unsafe_allow_html=True)

# --------------------------------------------------
# 2. WALL OF MASTERPIECES (SON 8 TANE 5 YILDIZ)
# --------------------------------------------------
df_5star = df_dates[(df_dates['Rating'] == 5.0) & (df_dates['Runtime'] >= 35)].sort_values('Watched_Date_Log', ascending=False)

posters_html = ""
for _, row in df_5star.iterrows():
    p_url = str(row.get('Poster_URL', '')) or "https://s.ltrbxd.com/static/img/empty-poster-1000.v3.jpg"
    m_name = str(row['Name']).replace("'", "&#39;")
    posters_html += f"<a href='{row['Letterboxd URI']}' target='_blank' title='{m_name}'><div class='master-poster' style=\"background-image:url('{p_url}');\"></div></a>"

html_wall = (
    f"<div style='background:linear-gradient(180deg,#181c20 0%,#111315 100%);border-radius:8px;padding:22px 0 22px 25px;border:1px solid rgba(255,255,255,0.05);box-shadow:0 10px 30px rgba(0,0,0,0.5);position:relative;height:260px;display:flex;flex-direction:column;justify-content:center;'>"
    f"<h4 style='color:#a0b0c0;font-size:0.8rem;letter-spacing:2px;font-weight:800;margin:0 0 15px 0;text-transform:uppercase;display:flex;align-items:center;gap:8px;'>"
    f"HALL OF FAME <span style='color:#5a6b7c;font-weight:500;font-size:0.7rem;'>(MASTERPIECES)</span>"
    f"</h4>"
    f"<div class='marquee-wrapper'>"
    f"<div class='marquee-content'>{posters_html}{posters_html}</div>"
    f"</div>"
    f"</div>"
)
st.markdown(html_wall, unsafe_allow_html=True)


# ==========================================
# ROW 3: DEEP INSIGHTS (full width, 2 cols)
# ==========================================
st.markdown("<div style='margin-top:50px;'></div>", unsafe_allow_html=True)
st.markdown("<h4 style='color: #a0b0c0; margin-bottom: 25px; font-size: 0.9rem; letter-spacing: 1px;'>DEEP INSIGHTS</h4>", unsafe_allow_html=True)
di_col1, di_col2 = st.columns([1, 1], gap='large')

with di_col1:

    # --- MARATHON + TIME WASTED: One big cinematic card ---
    marathon_stats = df_dates.groupby('DateOnly').agg(Film_Count=('Name', 'count'), Total_Runtime=('Runtime', 'sum')).reset_index()
    valid_marathons = marathon_stats[marathon_stats['Film_Count'] <= 8]

    wasted_df = df[(df['Rating'] > 0) & (df['Rating'] < 2.0)]
    wasted_runtime = int(wasted_df['Runtime'].sum())
    wasted_films = wasted_df.sort_values('Rating').head(5)
    wasted_links_html = ''.join([
        '<a href="' + str(r['Letterboxd URI']) + '" target="_blank" style="display:flex;justify-content:space-between;align-items:center;color:#7a5555;font-size:0.75rem;text-decoration:none;padding:4px 0;border-bottom:1px solid rgba(139,42,42,0.12);" '
        'onmouseover="this.style.color='#cc4444'" onmouseout="this.style.color='#7a5555'">'
        '<span>' + (str(r['Name'])[:36] + ('…' if len(str(r['Name'])) > 36 else '')) + '</span>'
        '<span style="font-weight:700;margin-left:8px;color:#a53838;">' + str(r['Rating']) + '★</span></a>'
        for _, r in wasted_films.iterrows()
    ])
    wasted_footer = (
        '<div style="margin-top:24px;padding-top:20px;border-top:1px solid rgba(139,42,42,0.2);">'
        '<p style="color:#6a3333!important;font-size:0.6rem;letter-spacing:3px;font-weight:800;text-transform:uppercase;margin:0 0 4px 0;">"Time Wasted" Index</p>'
        '<p style="font-size:1.8rem;font-weight:800;color:#a53838;margin:0 0 4px 0;font-family:Courier New,monospace;letter-spacing:-1px;line-height:1;">' + str(wasted_runtime // 60) + 'h ' + str(wasted_runtime % 60) + 'm</p>'
        '<p style="color:#4a3333!important;font-size:0.68rem;margin:0 0 10px 0;">on films rated below 2.0 stars</p>'
        '<div>' + wasted_links_html + '</div>'
        '</div>'
    )

    if not valid_marathons.empty:
        best_marathon = valid_marathons.sort_values(by=['Film_Count', 'Total_Runtime'], ascending=[False, False]).iloc[0]
        marathon_films = df_dates[df_dates['DateOnly'] == best_marathon['DateOnly']].sort_values('Watched_Date_Log')
        film_links_html = ''.join([
            '<a href="' + str(r['Letterboxd URI']) + '" target="_blank" style="display:flex;justify-content:space-between;align-items:center;color:#8090a0;font-size:0.82rem;text-decoration:none;padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.05);" '
            'onmouseover="this.style.color='#c5a059'" onmouseout="this.style.color='#8090a0'">'
            '<span>' + (str(r['Name'])[:45] + ('…' if len(str(r['Name'])) > 45 else '')) + '</span>'
            '<span style="color:#5a6b7c;font-size:0.7rem;">' + (str(int(r['Runtime'])) + ' min' if r['Runtime'] > 0 else '') + '</span>'
            '</a>'
            for _, r in marathon_films.iterrows()
        ])
        # Use first marathon film's poster as bg
        bg_poster = ''
        for _, rf in marathon_films.iterrows():
            p = str(rf.get('Poster_URL', ''))
            if p and p != 'nan' and p != '':
                bg_poster = p
                break

        bg_layer = (
            '<div style="position:absolute;inset:0;background-image:url(\'' + bg_poster + '\');background-size:cover;background-position:center;filter:blur(55px) brightness(0.12);z-index:0;"></div>'
            if bg_poster else ''
        )

        combined_html = (
            '<div style="background:#0d0f11;border:1px solid rgba(255,255,255,0.06);border-left:3px solid #e0e6ed;border-radius:8px;padding:32px;overflow:hidden;position:relative;">'
            + bg_layer +
            '<div style="position:relative;z-index:1;">'
            '<div style="position:absolute;top:-30px;right:-10px;font-size:13rem;font-weight:900;color:rgba(255,255,255,0.04);line-height:1;pointer-events:none;font-family:Georgia,serif;">'
            + str(int(best_marathon['Film_Count'])) +
            '</div>'
            '<p style="color:#5a6b7c!important;font-size:0.65rem;letter-spacing:3px;font-weight:800;text-transform:uppercase;margin:0 0 20px 0;">Longest Marathon</p>'
            '<div style="display:flex;align-items:flex-end;gap:24px;margin-bottom:8px;">'
            '<div>'
            '<span style="font-size:7rem;font-weight:900;color:#f0f0f0;line-height:1;letter-spacing:-5px;text-shadow:0 0 40px rgba(255,255,255,0.1);">' + str(int(best_marathon['Film_Count'])) + '</span>'
            '<span style="font-size:1.4rem;color:#7a8b99;font-weight:400;margin-left:8px;">films</span>'
            '</div>'
            '<div style="padding-bottom:12px;">'
            '<p style="font-size:2.4rem;font-weight:700;color:#c5a059;margin:0;line-height:1;text-shadow:0 0 20px rgba(197,160,89,0.3);">' + str(int(best_marathon['Total_Runtime'] // 60)) + 'H ' + str(int(best_marathon['Total_Runtime'] % 60)) + 'M</p>'
            '<p style="color:#445566!important;font-size:0.7rem;letter-spacing:1px;margin:4px 0 0 0;text-transform:uppercase;">total runtime</p>'
            '</div>'
            '</div>'
            '<p style="color:#556677!important;font-size:0.82rem;margin:0 0 28px 0;font-family:monospace;">' + best_marathon['DateOnly'].strftime('%B %d, %Y') + '</p>'
            '<div style="border-top:1px solid rgba(255,255,255,0.07);padding-top:16px;">'
            '<p style="color:#445566!important;font-size:0.65rem;letter-spacing:2px;text-transform:uppercase;margin:0 0 8px 0;">Films watched</p>'
            + film_links_html +
            '</div>'
            + wasted_footer +
            '</div>'
            '</div>'
        )
        st.markdown(combined_html, unsafe_allow_html=True)

with di_col2:

    # --- PEAK MONTH ---
    df_rated_months = df[(df['Rating'] > 0) & (df['Watched_Date_Log'].notna())].copy()
    df_rated_months['YearMonth'] = df_rated_months['Watched_Date_Log'].dt.to_period('M')
    month_stats = df_rated_months.groupby('YearMonth').agg(Film_Count=('Name', 'count'), Avg_Rating=('Rating', 'mean')).reset_index()
    valid_months = month_stats[month_stats['Film_Count'] >= 10]
    if not valid_months.empty:
        best_month = valid_months.loc[valid_months['Avg_Rating'].idxmax()]
        peak_films = df_rated_months[df_rated_months['YearMonth'] == best_month['YearMonth']].sort_values('Rating', ascending=False).head(5)
        peak_links_html = ''.join([
            '<a href="' + str(r['Letterboxd URI']) + '" target="_blank" style="display:block;color:#7a6a30;font-size:0.78rem;text-decoration:none;padding:5px 0;border-bottom:1px solid rgba(197,160,89,0.1);" '
            'onmouseover="this.style.color=\'#c5a059\'" onmouseout="this.style.color=\'#7a6a30\'">'
            + (str(r['Name'])[:45] + ('…' if len(str(r['Name'])) > 45 else '')) + '</a>'
            for _, r in peak_films.iterrows()
        ])
        peak_bg = str(peak_films.iloc[0].get('Poster_URL', '')) if not peak_films.empty else ''
        peak_bg = peak_bg if peak_bg and peak_bg != 'nan' else ''
        peak_bg_layer = ('<div style="position:absolute;inset:0;background-image:url(\'' + peak_bg + '\');background-size:cover;background-position:center;filter:blur(50px) brightness(0.08);z-index:0;"></div>' if peak_bg else '')
        peak_html = (
            '<div style="background:#0e0c08;border:1px solid rgba(197,160,89,0.2);border-bottom:2px solid #c5a059;border-radius:6px;padding:20px;margin-bottom:16px;text-align:center;position:relative;overflow:hidden;">'
            + peak_bg_layer +
            '<div style="position:relative;z-index:1;">'
            '<p style="color:#5a4a20!important;font-size:0.65rem;letter-spacing:3px;font-weight:800;text-transform:uppercase;margin:0 0 4px 0;">Peak Cinema Month</p>'
            '<p style="color:#4a3a18!important;font-size:0.78rem;font-style:italic;margin:0 0 4px 0;font-family:Georgia,serif;">The month you were most in tune with cinema</p>'
            '<p style="color:#3a2e12!important;font-size:0.62rem;letter-spacing:1px;text-transform:uppercase;margin:0 0 10px 0;">Highest avg rating · min. 10 films</p>'
            '<p style="font-size:2rem;font-weight:800;color:#e8d090;margin:0;line-height:1.1;">' + best_month['YearMonth'].strftime('%B') + '</p>'
            '<p style="font-size:1rem;font-weight:500;color:#7a6a30;margin:0 0 8px 0;">' + best_month['YearMonth'].strftime('%Y') + '</p>'
            '<span style="background:rgba(197,160,89,0.12);border:1px solid rgba(197,160,89,0.3);color:#c5a059;padding:3px 12px;border-radius:20px;font-weight:800;font-size:0.9rem;">'
            + f"{best_month['Avg_Rating']:.2f} AVG · {int(best_month['Film_Count'])} films" +
            '</span>'
            '<div style="border-top:1px solid rgba(197,160,89,0.12);padding-top:12px;margin-top:14px;text-align:left;">'
            + peak_links_html +
            '</div></div></div>'
        )
        st.markdown(peak_html, unsafe_allow_html=True)

    # --- MOST GENEROUS ERA ---
    df_generous = df[(df['Year'] > 1800) & (df['Rating'] > 0)].copy()
    df_generous['Decade'] = (df_generous['Year'] // 10) * 10
    decade_stats = df_generous.groupby('Decade').agg(Avg_Rating=('Rating', 'mean'), Film_Count=('Name', 'count')).reset_index()
    valid_decades = decade_stats[decade_stats['Film_Count'] >= 10]
    if not valid_decades.empty:
        best_decade = valid_decades.loc[valid_decades['Avg_Rating'].idxmax()]
        decade_val = int(best_decade['Decade'])
        decade_films = df_generous[df_generous['Decade'] == decade_val].sort_values('Rating', ascending=False).drop_duplicates('Name').head(5)
        era_links_html = ''.join([
            '<a href="' + str(r['Letterboxd URI']) + '" target="_blank" style="display:flex;justify-content:space-between;align-items:baseline;padding:7px 0;border-bottom:1px solid rgba(255,255,255,0.04);text-decoration:none;" '
            'onmouseover="this.style.opacity=\'0.65\'" onmouseout="this.style.opacity=\'1\'">'
            '<span style="color:#c8d4dc;font-size:0.82rem;font-family:Georgia,serif;font-style:italic;">' + (str(r['Name'])[:42] + ('…' if len(str(r['Name'])) > 42 else '')) + '</span>'
            '<span style="color:#c5a059;font-size:0.75rem;font-weight:700;margin-left:10px;white-space:nowrap;">' + str(int(r['Year'])) + '</span>'
            '</a>'
            for _, r in decade_films.iterrows()
        ])
        era_bg = str(decade_films.iloc[0].get('Poster_URL', '')) if not decade_films.empty else ''
        era_bg = era_bg if era_bg and era_bg != 'nan' else ''
        era_bg_layer = ('<div style="position:absolute;inset:0;background-image:url(\'' + era_bg + '\');background-size:cover;background-position:center;filter:blur(50px) brightness(0.1);z-index:0;"></div>' if era_bg else '')
        era_html = (
            '<div style="background:#0d0f11;border:1px solid rgba(255,255,255,0.06);border-radius:8px;padding:24px;margin-bottom:16px;position:relative;overflow:hidden;">'
            + era_bg_layer +
            '<div style="position:relative;z-index:1;">'
            '<div style="position:absolute;top:0;right:0;width:1px;height:100%;background:linear-gradient(to bottom,transparent,rgba(255,255,255,0.08),transparent);"></div>'
            '<p style="color:#5a6b7c!important;font-size:0.65rem;letter-spacing:3px;font-weight:800;text-transform:uppercase;margin:0 0 12px 0;">Most Generous Era</p>'
            '<div style="display:flex;align-items:baseline;gap:16px;margin-bottom:16px;padding-bottom:16px;border-bottom:1px solid rgba(255,255,255,0.07);">'
            '<p style="font-size:4.5rem;font-weight:900;color:#e0e6ed;line-height:1;margin:0;letter-spacing:-3px;font-family:Georgia,serif;">' + str(decade_val) + 's</p>'
            '<div>'
            '<p style="font-size:1.2rem;font-weight:700;color:#c5a059;margin:0;line-height:1;">' + f"{best_decade['Avg_Rating']:.2f}" + '</p>'
            '<p style="font-size:0.7rem;color:#5a6b7c!important;margin:2px 0 0 0;letter-spacing:1px;text-transform:uppercase;">avg rating</p>'
            '<p style="font-size:0.7rem;color:#5a6b7c!important;margin:2px 0 0 0;letter-spacing:1px;text-transform:uppercase;">' + str(int(best_decade['Film_Count'])) + ' films watched</p>'
            '</div></div>'
            '<p style="color:#445566!important;font-size:0.65rem;letter-spacing:2px;text-transform:uppercase;margin:0 0 4px 0;">Top Films</p>'
            + era_links_html +
            '</div>'
            '</div>'
            '</div>'
        )
        st.markdown(era_html, unsafe_allow_html=True)

    # --- FAVORITE DAY ---
    max_date = df_dates['Watched_Date_Log'].max()
    three_months_ago = max_date - pd.DateOffset(months=3)
    recent_df = df_dates[df_dates['Watched_Date_Log'] >= three_months_ago].copy()
    if not recent_df.empty:
        best_dow = recent_df['Watched_Date_Log'].dt.day_name().value_counts().idxmax()
        st.markdown(f"""<div class="ins-habit"><p class="h-title">FAVORITE RECENT DAY:</p><p class="h-val">{best_dow}s</p></div>""", unsafe_allow_html=True)


# ROW 4: DECADES OF CINEMA (full width)
# ==========================================
st.markdown("<div style='margin-top:50px;'></div>", unsafe_allow_html=True)

# ==================================================
# 7. ZAMAN TÜNELİ SLIDER - REACT DOM BUG FIXED (KUSURSUZ)
# ==================================================
df_decades = df_rated[(df_rated['Year'] >= 1900) & (df_rated['Runtime'] >= 35)].copy()
df_decades['Decade'] = (df_decades['Year'] // 10 * 10).astype(int)

top_per_decade = df_decades.sort_values(['Rating', 'Watched_Date_Log'], ascending=[False, False]).groupby('Decade').first().reset_index()
top_per_decade = top_per_decade.sort_values('Decade', ascending=False)

if not top_per_decade.empty:
    inputs_html = ""
    bg_html = ""
    slides_html = ""
    nav_items_html = ""
    
    css_rules = (
        f".tm-bg-0 {{ opacity: 1; transform: scale(1.05); z-index: 2; }}"
        f".tm-slide-0 {{ opacity: 1; transform: translateX(0); pointer-events: auto; z-index: 10; }}"
        f".tm-nav-track {{ transform: translateX(-40px); }}"
        f".tm-nav-wrapper .tm-nav-track [for='rd-dec-0'] {{ color: #F2F2F7; font-weight: 800; opacity: 1; transform: scale(1.15); }}"
        f".tm-nav-wrapper .tm-nav-track [for='rd-dec-0']::after {{ opacity: 1; transform: scaleX(1); }}"
    )
    
    for i, (_, row) in enumerate(top_per_decade.iterrows()):
        p_url = str(row.get('Poster_URL', '')) or "https://s.ltrbxd.com/static/img/empty-poster-1000.v3.jpg"
        m_name = str(row['Name']).replace("'", "&#39;")
        m_rating = row['Rating']
        decade_val = int(row['Decade'])
        decade_str = f"'{str(decade_val)[-2:]}s"
        m_link = str(row['Letterboxd URI'])
        
        inputs_html += f"<input type='radio' id='rd-dec-{i}' name='dec-slider'>"
        bg_html += f"<div class='tm-bg tm-bg-{i}' style=\"background-image:url('{p_url}');\"></div>"
        poster_attr = f"style=\"background-image:url('{p_url}');\"" if i == 0 else f"data-bg='{p_url}'"
        slides_html += (
            f"<div class='tm-slide tm-slide-{i}'>"
            f"<a href='{m_link}' target='_blank' style='text-decoration:none;flex-shrink:0;'>"
            f"<div class='tm-poster' {poster_attr}></div>"
            f"</a>"
            f"<div class='tm-info'>"
            f"<div class='tm-date'>THE {decade_val}s</div>"
            f"<a href='{m_link}' target='_blank' style='text-decoration:none;'><div class='tm-title'>{m_name}</div></a>"
            f"<p style='color:#fff;font-size:1.5rem;font-weight:300;margin:0;'><span style='color:#c5a059;'>★</span> {m_rating} / 5.0 <span class='rated-badge'>RATED BY BURAK</span></p>"
            f"</div>"
            f"</div>"
        )
        nav_items_html += f"<label for='rd-dec-{i}' class='tm-nav-item'>{decade_str}</label>"
        
        shift_px = (i * 80) + 40
        
        css_rules += f"#rd-dec-{i}:checked ~ .tm-bg-container .tm-bg-{i} {{ opacity: 1; transform: scale(1.05); z-index: 2; }}"
        css_rules += f"#rd-dec-{i}:checked ~ .tm-slides-container .tm-slide-{i} {{ opacity: 1; transform: translateX(0); pointer-events: auto; z-index: 10; transition: all 0.7s cubic-bezier(0.2, 0.8, 0.2, 1); }}"
        css_rules += f"#rd-dec-{i}:checked ~ .tm-nav-wrapper .tm-nav-track [for='rd-dec-{i}'] {{ color: #F2F2F7; font-weight: 800; opacity: 1; transform: scale(1.15); }}"
        css_rules += f"#rd-dec-{i}:checked ~ .tm-nav-wrapper .tm-nav-track [for='rd-dec-{i}']::after {{ opacity: 1; transform: scaleX(1); }}"
        css_rules += f"#rd-dec-{i}:checked ~ .tm-nav-wrapper .tm-nav-track {{ transform: translateX(-{shift_px}px); }}"
        
        for j in range(len(top_per_decade)):
            if j != i:
                css_rules += f"#rd-dec-{i}:checked ~ .tm-bg-container .tm-bg-{j} {{ opacity: 0 !important; transform: scale(1) !important; z-index: 1 !important; }}"
                css_rules += f"#rd-dec-{i}:checked ~ .tm-slides-container .tm-slide-{j} {{ opacity: 0 !important; transform: translateX(40px) !important; pointer-events: none !important; z-index: 1 !important; }}"
                css_rules += f"#rd-dec-{i}:checked ~ .tm-nav-wrapper .tm-nav-track [for='rd-dec-{j}'] {{ color: #5a6b7c !important; font-weight: 600 !important; opacity: 0.5 !important; transform: scale(1) !important; }}"
                css_rules += f"#rd-dec-{i}:checked ~ .tm-nav-wrapper .tm-nav-track [for='rd-dec-{j}']::after {{ opacity: 0 !important; transform: scaleX(0) !important; }}"




    tm_css = """
    <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { background: transparent; }
    .tm-container { position: relative; width: 100%; height: 480px; border-radius: 16px; overflow: hidden; background: #0a0c0f; border: 1px solid rgba(255,255,255,0.04); box-shadow: 0 25px 50px rgba(0,0,0,0.7); font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif; }
    .tm-container input[type='radio'] { display: none; }
    .tm-bg-container { position: absolute; inset: 0; z-index: 1; overflow: hidden; }
    .tm-bg { position: absolute; inset: -30px; background-size: cover; background-position: center; filter: blur(40px) brightness(0.2); opacity: 0; transition: opacity 0.6s ease; }
    .tm-slides-container { position: absolute; inset: 0; z-index: 2; padding-bottom: 70px; }
    .tm-slide { position: absolute; inset: 0; display: flex; align-items: center; justify-content: flex-start; padding: 0 50px; opacity: 0; transform: translateX(40px); transition: opacity 0.4s ease, transform 0s 0.4s; pointer-events: none; gap: 40px; }
    .tm-poster { width: 220px; height: 330px; border-radius: 8px; background-size: cover; background-position: center; box-shadow: 0 15px 35px rgba(0,0,0,0.9), 0 0 0 1px rgba(255,255,255,0.08); flex-shrink: 0; transition: transform 0.3s ease; }
    .tm-poster:hover { transform: scale(1.03); }
    .tm-title:hover { color: #c5a059 !important; }
    .tm-info { display: flex; flex-direction: column; justify-content: center; max-width: 60%; }
    .tm-date { color: #7a8b99; font-size: 0.85rem; font-weight: 700; letter-spacing: 0.2em; margin-bottom: 12px; }
    .tm-title { color: #F2F2F7; font-size: 2.6rem; font-weight: 800; line-height: 1.1; margin-bottom: 12px; letter-spacing: -0.02em; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; text-shadow: 0 4px 20px rgba(0,0,0,0.5); }
    .tm-rating { color: #FFFFFF; font-size: 1.8rem; font-weight: 300; letter-spacing: 0.05em; display: flex; align-items: center; }
    .tm-nav-wrapper { position: absolute; bottom: 0; left: 0; right: 0; height: 75px; z-index: 999; background: linear-gradient(0deg, rgba(10,12,15,0.95) 0%, rgba(10,12,15,0) 100%); border-top: 1px solid rgba(255,255,255,0.03); overflow: hidden; mask-image: linear-gradient(to right, transparent, black 15%, black 85%, transparent); -webkit-mask-image: linear-gradient(to right, transparent, black 15%, black 85%, transparent); }
    .tm-nav-track { display: flex; position: absolute; height: 100%; align-items: center; transition: transform 0.6s cubic-bezier(0.2, 0.8, 0.2, 1); left: 50%; }
    .tm-nav-item { width: 80px; text-align: center; color: #5a6b7c; font-size: 1.2rem; font-weight: 600; cursor: pointer; transition: all 0.4s ease; position: relative; user-select: none; opacity: 0.5; padding: 15px 0; flex-shrink: 0; }
    .tm-nav-item:hover { opacity: 0.9; color: #a0b0c0; }
    .tm-nav-item::after { content: ''; position: absolute; bottom: 10px; left: 50%; width: 4px; height: 4px; border-radius: 50%; background: #c5a059; transform: translateX(-50%) scaleX(0); transition: all 0.4s cubic-bezier(0.2, 0.8, 0.2, 1); opacity: 0; box-shadow: 0 0 10px rgba(197,160,89,0.8); }
    .rated-badge { font-size: 0.6rem; color: #6c757d; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; margin-left: 8px; border-left: 1px solid rgba(255,255,255,0.1); padding-left: 8px; vertical-align: middle; }
    .mobile .tm-slide { padding: 0 15px !important; gap: 10px !important; }
    .mobile .tm-poster { width: 80px !important; height: 120px !important; }
    .mobile .tm-title { font-size: 1.1rem !important; -webkit-line-clamp: 2 !important; }
    .mobile .tm-date { font-size: 0.7rem !important; }
    .mobile .tm-nav-item { width: 60px !important; font-size: 0.9rem !important; }
    .mobile .tm-nav-wrapper { mask-image: none !important; -webkit-mask-image: none !important; }
    .mobile .rated-badge { display: none !important; }
    </style>
    """

    tm_js = """
    <script>
    function isMobile() { return document.body.offsetWidth < 600; }

    function applyResponsive() {
        if (isMobile()) {
            document.body.classList.add('mobile');
        } else {
            document.body.classList.remove('mobile');
        }
    }

    function getNavItemWidth() { return isMobile() ? 60 : 80; }

    function updateNav(idx) {
        var w = getNavItemWidth();
        var shift = (idx * w) + (w / 2);
        var track = document.querySelector('.tm-nav-track');
        if (track) track.style.transform = 'translateX(-' + shift + 'px)';
    }

    document.addEventListener('change', function(e) {
        if (e.target && e.target.name === 'dec-slider') {
            var idx = parseInt(e.target.id.replace('rd-dec-', ''));
            updateNav(idx);
            var slide = document.querySelector('.tm-slide-' + idx);
            if (slide) {
                var lazyEl = slide.querySelector('[data-bg]');
                if (lazyEl) {
                    lazyEl.style.backgroundImage = "url('" + lazyEl.getAttribute('data-bg') + "')";
                    lazyEl.removeAttribute('data-bg');
                }
            }
        }
    });

    window.addEventListener('load', applyResponsive);
    window.addEventListener('resize', applyResponsive);
    </script>
    """

    final_html = (
        tm_css +
        tm_js +
        f"<div style='margin-bottom:15px; margin-top: 10px;'>"
        f"<h4 style='color:#a0b0c0;font-size:0.8rem;letter-spacing:2px;font-weight:800;margin:0 0 15px 0;text-transform:uppercase;'>DECADES OF CINEMA</h4>"
        f"</div>"
        f"<style>{css_rules}</style>"
        f"<div class='tm-container'>"
        f"{inputs_html}"
        f"<div class='tm-bg-container'>{bg_html}</div>"
        f"<div class='tm-slides-container'>{slides_html}</div>"
        f"<div class='tm-nav-wrapper'><div class='tm-nav-track'>{nav_items_html}</div></div>"
        f"</div>"
    )
    
    components.html(final_html, height=660, scrolling=False)