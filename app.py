import streamlit as st
import pandas as pd
from styles import inject_custom_css
from data_core import load_data, get_latest_movie, get_kpis, fetch_poster_url
import streamlit.components.v1 as components

# 1. PAGE SETTINGS
st.set_page_config(page_title="Letterboxd Analytics", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS INJECTION (Diğer dosyadan çekiliyor)
inject_custom_css()

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
        <h2 style="margin: 0; color: #e0e6ed; font-size: 1.5rem; letter-spacing: 1px; font-weight: 700; text-transform: uppercase;">Cinema Log</h2>
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
# ROW 2: TRIPLE PANEL
# ==========================================
col1, col2, col3 = st.columns([1.15, 0.75, 1.6], gap="medium") 

with col1:
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

with col3:
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

    # --------------------------------------------------
    # 2. WALL OF MASTERPIECES (SON 8 TANE 5 YILDIZ)
    # --------------------------------------------------
    df_5star = df_dates[(df_dates['Rating'] == 5.0) & (df_dates['Runtime'] >= 35)].sort_values('Watched_Date_Log', ascending=False).head(8)
    
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
# ROW 3: DEEP INSIGHTS & TOP 10 MONTHS
# ==========================================
col_left, col_right = st.columns([1.1, 0.9])

with col_left:
    st.markdown("<h4 style='color: #a0b0c0; margin-bottom: 15px; font-size: 0.9rem; letter-spacing: 1px;'>DEEP INSIGHTS</h4>", unsafe_allow_html=True)
    marathon_stats = df_dates.groupby('DateOnly').agg(Film_Count=('Name', 'count'), Total_Runtime=('Runtime', 'sum')).reset_index()
    valid_marathons = marathon_stats[marathon_stats['Film_Count'] <= 8]
    if not valid_marathons.empty:
        best_marathon = valid_marathons.sort_values(by=['Film_Count', 'Total_Runtime'], ascending=[False, False]).iloc[0]
        st.markdown(f"""
        <div class="ins-marathon">
            <div><p class="m-title">LONGEST MARATHON</p><p class="m-val">{int(best_marathon['Film_Count'])} FILMS</p><p class="m-sub">in a single day</p></div>
            <div class="m-right"><p class="m-time">{int(best_marathon['Total_Runtime'] // 60)}H {int(best_marathon['Total_Runtime'] % 60)}M</p><p class="m-date">{best_marathon['DateOnly'].strftime('%B %d, %Y')}</p></div>
        </div>
        """, unsafe_allow_html=True)

    wasted_df = df[(df['Rating'] > 0) & (df['Rating'] < 2.0)]
    wasted_runtime = int(wasted_df['Runtime'].sum())
    st.markdown(f"""<div class="ins-wasted"><p class="w-title">"TIME WASTED" INDEX</p><p class="w-val">{wasted_runtime // 60}h {wasted_runtime % 60}m</p><p class="w-sub">Total time spent watching films rated below 2.0.</p></div>""", unsafe_allow_html=True)

    df_rated_months = df[(df['Rating'] > 0) & (df['Watched_Date_Log'].notna())].copy()
    df_rated_months['YearMonth'] = df_rated_months['Watched_Date_Log'].dt.to_period('M')
    month_stats = df_rated_months.groupby('YearMonth').agg(Film_Count=('Name', 'count'), Avg_Rating=('Rating', 'mean')).reset_index()
    valid_months = month_stats[month_stats['Film_Count'] >= 10]
    if not valid_months.empty:
        best_month = valid_months.loc[valid_months['Avg_Rating'].idxmax()]
        st.markdown(f"""<div class="ins-peak"><p class="p-title">PEAK CINEMA MONTH (MIN. 10 FILMS)</p><div class="p-flex"><p class="p-val">{best_month['YearMonth'].strftime('%B %Y')}</p><span class="p-badge">{best_month['Avg_Rating']:.2f} AVG</span></div></div>""", unsafe_allow_html=True)

    df_generous = df[(df['Year'] > 1800) & (df['Rating'] > 0)].copy()
    df_generous['Decade'] = (df_generous['Year'] // 10) * 10
    decade_stats = df_generous.groupby('Decade').agg(Avg_Rating=('Rating', 'mean'), Film_Count=('Name', 'count')).reset_index()
    valid_decades = decade_stats[decade_stats['Film_Count'] >= 10]
    if not valid_decades.empty:
        best_decade = valid_decades.loc[valid_decades['Avg_Rating'].idxmax()]
        st.markdown(f"""<div class="ins-era"><div class="e-left"><p class="e-title">MOST GENEROUS ERA</p><p class="e-sub">{best_decade['Avg_Rating']:.2f} Avg Rating</p></div><p class="e-val">{int(best_decade['Decade'])}s</p></div>""", unsafe_allow_html=True)

    max_date = df_dates['Watched_Date_Log'].max()
    three_months_ago = max_date - pd.DateOffset(months=3)
    recent_df = df_dates[df_dates['Watched_Date_Log'] >= three_months_ago].copy()
    if not recent_df.empty:
        best_dow = recent_df['Watched_Date_Log'].dt.day_name().value_counts().idxmax()
        st.markdown(f"""<div class="ins-habit"><p class="h-title">FAVORITE RECENT DAY:</p><p class="h-val">{best_dow}s</p></div>""", unsafe_allow_html=True)

with col_right:
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
            
            inputs_html += f"<input type='radio' id='rd-dec-{i}' name='dec-slider'>"
            bg_html += f"<div class='tm-bg tm-bg-{i}'></div>"
            poster_attr = f"style=\"background-image:url('{p_url}');\"" if i == 0 else f"data-bg='{p_url}'"
            slides_html += (
                f"<div class='tm-slide tm-slide-{i}'>"
                f"<div class='tm-poster' {poster_attr}></div>"
                f"<div class='tm-info'>"
                f"<div class='tm-date'>THE {decade_val}s</div>"
                f"<div class='tm-title'>{m_name}</div>"
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
        .tm-container { position: relative; width: 100%; height: 420px; border-radius: 16px; overflow: hidden; background: #0a0c0f; border: 1px solid rgba(255,255,255,0.04); box-shadow: 0 25px 50px rgba(0,0,0,0.7); font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif; }
        .tm-container input[type='radio'] { display: none; }
        .tm-bg-container { position: absolute; inset: 0; z-index: 1; overflow: hidden; }
        .tm-bg { position: absolute; inset: -30px; background-size: cover; background-position: center; filter: blur(40px) brightness(0.2); opacity: 0; transition: opacity 0.6s ease; }
        .tm-slides-container { position: absolute; inset: 0; z-index: 2; padding-bottom: 70px; }
        .tm-slide { position: absolute; inset: 0; display: flex; align-items: center; justify-content: flex-start; padding: 0 50px; opacity: 0; transform: translateX(40px); transition: opacity 0.4s ease, transform 0s 0.4s; pointer-events: none; gap: 40px; }
        .tm-poster { width: 170px; height: 255px; border-radius: 8px; background-size: cover; background-position: center; box-shadow: 0 15px 35px rgba(0,0,0,0.9), 0 0 0 1px rgba(255,255,255,0.08); flex-shrink: 0; }
        .tm-info { display: flex; flex-direction: column; justify-content: center; max-width: 60%; }
        .tm-date { color: #7a8b99; font-size: 0.85rem; font-weight: 700; letter-spacing: 0.2em; margin-bottom: 12px; }
        .tm-title { color: #F2F2F7; font-size: 2.6rem; font-weight: 800; line-height: 1.1; margin-bottom: 12px; letter-spacing: -0.02em; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; text-shadow: 0 4px 20px rgba(0,0,0,0.5); }
        .tm-rating { color: #FFFFFF; font-size: 1.8rem; font-weight: 300; letter-spacing: 0.05em; display: flex; align-items: center; }
        .tm-nav-wrapper { position: absolute; bottom: 0; left: 0; right: 0; height: 75px; z-index: 999; background: linear-gradient(0deg, rgba(10,12,15,0.95) 0%, rgba(10,12,15,0) 100%); border-top: 1px solid rgba(255,255,255,0.03); overflow: hidden; mask-image: linear-gradient(to right, transparent, black 15%, black 85%, transparent); -webkit-mask-image: linear-gradient(to right, transparent, black 15%, black 85%, transparent); }
        .tm-nav-track { display: flex; position: absolute; height: 100%; align-items: center; transition: transform 0.6s cubic-bezier(0.2, 0.8, 0.2, 1); left: 50%; }
        .tm-nav-item { width: 80px; text-align: center; color: #5a6b7c; font-size: 1.2rem; font-weight: 600; cursor: pointer; transition: all 0.4s ease; position: relative; user-select: none; opacity: 0.5; padding: 15px 0; flex-shrink: 0; }
        .tm-nav-item:hover { opacity: 0.9; color: #a0b0c0; }
        .tm-nav-item::after { content: ''; position: absolute; bottom: 10px; left: 50%; width: 4px; height: 4px; border-radius: 50%; background: #c5a059; transform: translateX(-50%) scaleX(0); transition: all 0.4s cubic-bezier(0.2, 0.8, 0.2, 1); opacity: 0; box-shadow: 0 0 10px rgba(197,160,89,0.8); }
        @media (max-width: 768px) {
            .tm-slide { padding: 0 20px; gap: 15px; }
            .tm-poster { width: 110px; height: 165px; }
            .tm-title { font-size: 1.5rem; }
            .tm-rating { font-size: 1.2rem; }
            .tm-date { font-size: 0.75rem; }
            .tm-nav-item { width: 60px; font-size: 1rem; }
            .tm-nav-wrapper { mask-image: none; -webkit-mask-image: none; }
            .rated-badge { display: none; }
        }
        .rated-badge { font-size: 0.6rem; color: #6c757d; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; margin-left: 8px; border-left: 1px solid rgba(255,255,255,0.1); padding-left: 8px; vertical-align: middle; }
        </style>
        """

        tm_js = """
        <script>
        document.addEventListener('change', function(e) {
            if (e.target && e.target.name === 'dec-slider') {
                var idx = e.target.id.replace('rd-dec-', '');
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
        
        components.html(final_html, height=600, scrolling=False)