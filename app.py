import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from styles import inject_custom_css
from data_core import load_data, get_latest_movie, get_kpis

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
    st.markdown("<h4 style='color: #a0b0c0; margin-bottom: 15px; font-size: 0.9rem; letter-spacing: 1px;'>RUNTIME FLOW</h4>", unsafe_allow_html=True)
    df_runtime = df[(df['Runtime'] >= 10) & (df['Runtime'] <= 220)]
    hist_data = df_runtime['Runtime'].value_counts(bins=30).sort_index()
    fig_runtime = go.Figure(go.Scatter(
        x=[m.mid for m in hist_data.index], y=hist_data.values, mode='lines', fill='tozeroy',
        line=dict(color='#5a6b7c', width=2.5, shape='spline'), fillcolor='rgba(90, 107, 124, 0.15)',
        hovertemplate="<b>%{x:.0f} mins</b><br>Films: %{y}<extra></extra>"
    ))
    fig_runtime.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=420, margin=dict(l=0, r=0, t=10, b=0), dragmode=False,
        xaxis=dict(gridcolor='rgba(255, 255, 255, 0.03)', tickfont=dict(color='#7a8b99'), fixedrange=True),
        yaxis=dict(gridcolor='rgba(255, 255, 255, 0.03)', tickfont=dict(color='#7a8b99'), fixedrange=True),
        hoverlabel=dict(bgcolor="#181c20", font_size=14, font_color="#e0e6ed")
    )
    st.plotly_chart(fig_runtime, use_container_width=True, theme=None, config={'displayModeBar': False})

st.markdown("<hr style='border: 1px solid #2c3440; margin-bottom: 20px;'>", unsafe_allow_html=True)

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
    st.markdown("<h4 style='color: #a0b0c0; margin-bottom: 15px; font-size: 0.9rem; letter-spacing: 1px;'>TOP 10 ACTIVE MONTHS' FAVORITES</h4>", unsafe_allow_html=True)
    top_10_months_series = df_rated_months['YearMonth'].dt.strftime('%Y-%m').value_counts().head(10).index
    df_rated_months['YearMonthStr'] = df_rated_months['YearMonth'].dt.strftime('%Y-%m')
    df_top10 = df_rated_months[df_rated_months['YearMonthStr'].isin(top_10_months_series)]
    
    if not df_top10.empty:
        monthly_top_busiest = df_top10.loc[df_top10.groupby('YearMonthStr')['Rating'].idxmax()].sort_values('YearMonthStr', ascending=False)
        for i, (_, row) in enumerate(monthly_top_busiest.iterrows()):
            st.markdown(f"""
            <div class="movie-card" style="position: relative; overflow: hidden; z-index: 1;">
                <div style="position: absolute; right: 10px; bottom: -15px; font-size: 4.5rem; font-weight: 900; color: rgba(255,255,255,0.02); z-index: -1; line-height: 1; font-family: 'Courier New', Courier, monospace;">{i+1:02d}</div>
                <div class="rating-badge">{row['Rating']} / 5.0</div>
                <p class="movie-title"><a href="{row['Letterboxd URI']}" target="_blank" class="custom-link" style="color: #f0f0f0 !important;">{row['Name']}</a> <span style='color: #5a6b7c; font-weight: 400; font-size:0.9rem;'>({int(row['Year'])})</span></p>
                <p class="movie-meta">Period: <b style="color: #a0b0c0;">{row['YearMonthStr']}</b> &nbsp;|&nbsp; Dir: {str(row['Director']).split(',')[0]}</p>
            </div>
            """, unsafe_allow_html=True)