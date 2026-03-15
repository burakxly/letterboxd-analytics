import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go

# 1. PAGE SETTINGS
st.set_page_config(page_title="Letterboxd Analytics", layout="wide", initial_sidebar_state="collapsed")

# 2. ADVANCED CSS INJECTION (Premium Muted Palette)
st.markdown("""
<style>
    .stApp { background-color: #111315; } /* Daha derin ve karanlık bir siyah */
    h1, h2, h3, h4, h5, p { color: #e0e6ed !important; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
    
    /* Sağ Taraf - Film Kartları (Mat ve Asil) */
    .movie-card { background-color: #181c20; border-left: 3px solid #667788; padding: 12px 16px; margin-bottom: 10px; border-radius: 4px; transition: all 0.3s ease; }
    .movie-card:hover { background-color: #1e2429; border-left: 3px solid #c5a059; transform: translateX(5px); }
    .movie-title { font-size: 1.05rem; font-weight: 700; margin: 0 0 4px 0; letter-spacing: 0.5px; color: #f0f0f0 !important; }
    .movie-meta { color: #7a8b99 !important; font-size: 0.85rem; margin: 0; }
    .rating-badge { float: right; background-color: #111315; padding: 4px 8px; border-radius: 4px; color: #c5a059; font-weight: 700; font-size: 0.85rem; border: 1px solid rgba(197, 160, 89, 0.2); }
    
    [data-testid="stMetricValue"] { font-size: 1.8rem !important; font-weight: 700 !important; color: #e0e6ed !important; white-space: normal !important; line-height: 1.2 !important; }
    @media (max-width: 768px) { [data-testid="stMetricValue"] { font-size: 1.3rem !important; } }
    [data-testid="stMetricLabel"] { font-size: 0.9rem !important; color: #7a8b99 !important; text-transform: uppercase !important; letter-spacing: 1px !important; }

    /* ========================================================= */
    /* THIS WEEK'S ACTIVITY: CANLI TAKİP PANELİ (Kamera Işığı) */
    /* ========================================================= */
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(204, 51, 51, 0.6); }
        70% { box-shadow: 0 0 0 8px rgba(204, 51, 51, 0); }
        100% { box-shadow: 0 0 0 0 rgba(204, 51, 51, 0); }
    }
    
    .ins-week { background: linear-gradient(180deg, #181c20 0%, #111315 100%); border-radius: 8px; padding: 25px; height: 260px; display: flex; flex-direction: column; justify-content: space-between; position: relative; border: 1px solid rgba(255, 255, 255, 0.05); box-shadow: 0 10px 30px rgba(0,0,0,0.8); transition: 0.3s; }
    .ins-week:hover { border-color: rgba(255, 255, 255, 0.15); }
    .week-top { display: flex; justify-content: space-between; align-items: center; }
    .week-title { color: #e0e6ed; font-size: 0.85rem; font-weight: 800; letter-spacing: 2px; margin: 0; display: flex; align-items: center; gap: 10px; text-transform: uppercase; }
    .pulse-dot { width: 8px; height: 8px; background-color: #cc3333; border-radius: 50%; animation: pulse 2s infinite; }
    .week-stats { display: flex; gap: 15px; margin-top: 15px; }
    .w-stat-item { flex: 1; background: rgba(0,0,0,0.3); padding: 20px 15px; border-radius: 6px; border-left: 2px solid #5a6b7c; display: flex; flex-direction: column; justify-content: center; }
    .w-stat-label { color: #7a8b99; font-size: 0.75rem; letter-spacing: 1px; font-weight: 700; margin-bottom: 8px; text-transform: uppercase; }
    .w-stat-val { color: #f0f0f0; font-size: 2.8rem; font-weight: 900; line-height: 1; margin: 0; }
    .week-date { color: #556677; font-size: 0.85rem; font-family: monospace; text-align: right; margin: 0; letter-spacing: 0.5px; }

    /* ========================================================= */
    /* DEEP INSIGHTS: PREMIUM YETİŞKİN TASARIMLARI */
    /* ========================================================= */
    
    /* 1. Marathon: Çelik Grisi ve Mat Beyaz */
    .ins-marathon { display: flex; justify-content: space-between; align-items: center; background: linear-gradient(90deg, #181c20 0%, #111315 100%); border-left: 3px solid #e0e6ed; padding: 20px; border-radius: 6px; margin-bottom: 16px; box-shadow: inset 0 0 20px rgba(0,0,0,0.5); transition: 0.3s; }
    .ins-marathon:hover { transform: scale(1.01); }
    .m-title { color: #e0e6ed !important; font-size: 0.75rem; letter-spacing: 2px; font-weight: 800; margin-bottom: 5px; }
    .m-val { font-size: 2.2rem; font-weight: 900; line-height: 1; margin: 0; color: #f0f0f0; }
    .m-sub { color: #7a8b99 !important; font-size: 0.9rem; margin: 5px 0 0 0; }
    .m-right { text-align: right; border-left: 1px solid rgba(255,255,255,0.05); padding-left: 20px; }
    .m-time { font-size: 1.5rem; font-weight: 700; color: #c5a059; margin: 0; }
    .m-date { color: #667788 !important; font-size: 0.8rem; text-transform: uppercase; margin: 0; }

    /* 2. Time Wasted: Derin ve Ciddi Bordo */
    .ins-wasted { background-color: #111315; border: 1px solid rgba(139, 42, 42, 0.4); border-radius: 6px; padding: 15px 20px; margin-bottom: 16px; position: relative; overflow: hidden; }
    .ins-wasted::before { content: ''; position: absolute; top: 0; right: 0; width: 150px; height: 100%; background: radial-gradient(circle, rgba(139, 42, 42, 0.1) 0%, rgba(0,0,0,0) 70%); }
    .w-title { color: #7a8b99 !important; font-size: 0.8rem; letter-spacing: 1px; font-weight: 600; text-transform: uppercase; margin: 0; }
    .w-val { font-size: 2rem; font-weight: 800; color: #a53838; margin: 5px 0; font-family: 'Courier New', Courier, monospace; letter-spacing: -1px; }
    .w-sub { color: #667788 !important; font-size: 0.85rem; margin: 0; }

    /* 3. Peak Month: Mat Altın (Premium) Rozet */
    .ins-peak { background-color: #181c20; border-bottom: 2px solid #c5a059; border-radius: 6px; padding: 20px; margin-bottom: 16px; text-align: center; }
    .p-title { color: #7a8b99 !important; font-size: 0.8rem; letter-spacing: 1.5px; font-weight: 700; margin-bottom: 10px; }
    .p-flex { display: flex; justify-content: center; align-items: center; gap: 15px; }
    .p-val { font-size: 1.8rem; font-weight: 800; color: #f0f0f0; margin: 0; }
    .p-badge { background: rgba(197, 160, 89, 0.1); border: 1px solid rgba(197, 160, 89, 0.3); color: #c5a059; padding: 4px 12px; border-radius: 20px; font-weight: 800; font-size: 1.1rem; }

    /* 4. Generous Era: Arduvaz Mavisi */
    .ins-era { display: flex; justify-content: flex-end; align-items: center; gap: 20px; background: linear-gradient(135deg, #15181b 0%, #1a1e23 100%); border-right: 3px solid #5a6b7c; border-radius: 6px; padding: 20px; margin-bottom: 16px; text-align: right; }
    .e-left { text-align: right; }
    .e-title { color: #5a6b7c !important; font-size: 0.75rem; letter-spacing: 2px; font-weight: 800; margin-bottom: 5px; }
    .e-sub { color: #7a8b99 !important; font-size: 0.9rem; margin: 0; }
    .e-val { font-size: 2.8rem; font-weight: 900; color: #e0e6ed; line-height: 1; margin: 0; opacity: 0.9; }

    /* 5. Recent Habit: Koyu Füme Hap */
    .ins-habit { display: flex; align-items: center; gap: 15px; background-color: #111315; border: 1px dashed rgba(122, 139, 153, 0.4); border-radius: 50px; padding: 10px 25px; width: fit-content; margin-top: 5px; }
    .h-title { color: #667788 !important; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin: 0; }
    .h-val { font-size: 1.2rem; font-weight: 800; color: #a0b0c0; margin: 0; text-transform: uppercase; }

</style>
""", unsafe_allow_html=True)

# 3. DATA LOADING & PROCESSING
@st.cache_data
def load_data():
    conn = sqlite3.connect("letterboxd_master.db")
    df = pd.read_sql("SELECT * FROM movies", conn)
    conn.close()
    
    # --- YENİ EKLENEN KORUMA KALKANI ---
    # Eğer veritabanı sıfırlanmışsa ve sütunlar yoksa, programın çökmesini engeller
    if 'Runtime' not in df.columns: df['Runtime'] = 0
    if 'Year' not in df.columns: df['Year'] = 0
    if 'Rating' not in df.columns: df['Rating'] = 0
    if 'Director' not in df.columns: df['Director'] = "Unknown"
    if 'Genre' not in df.columns: df['Genre'] = "Unknown"
    # -----------------------------------

    # Her iki tarihi de sisteme tanıtıyoruz
    if 'Watched_Date_Log' in df.columns:
        df['Watched_Date_Log'] = pd.to_datetime(df['Watched_Date_Log'], errors='coerce')
    if 'Watched Date' in df.columns:
        df['Watched Date'] = pd.to_datetime(df['Watched Date'], errors='coerce') 
        
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce').fillna(0)
    df['Runtime'] = pd.to_numeric(df['Runtime'], errors='coerce').fillna(0)
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce').fillna(0)
    
    return df

df = load_data()

# DÜNYA 1: Toplam veriler (Her şey dahil)
df_all = df.copy()

# DÜNYA 2: Sadece Günlük (Diary) Verileri
# "Watched Date" (Günlük) sütunu boş olmayanları alıyoruz
df_diary = df_all.dropna(subset=['Watched Date']).copy()

# Aşağıdaki analizlerin bozulmaması için isimleri Diary'ye güncelliyoruz
df_dates = df_diary.copy()
# DİKKAT: Artık DateOnly için gerçek günlüğü ('Watched Date') baz alıyoruz!
df_dates['DateOnly'] = df_dates['Watched Date'].dt.date 

# Puanlı filmler her iki dünyadan da gelebilir (Tür hesaplamaları için)
df_rated = df_all[df_all['Rating'] > 0].copy()

# --- EN SON IZLENEN FILM VERISI ---
# --- EN SON IZLENEN FILM VERISI ---
conn = sqlite3.connect("letterboxd_master.db")

# ÖNEMLİ DEĞİŞİKLİK: Sadece Watched Date değil, rowid'yi de işin içine katarak 
# veritabanına "en son eklenen" satırı garantiliyoruz.
last_movie_query = """
    SELECT Name, Rating FROM movies 
    WHERE "Watched Date" IS NOT NULL AND "Watched Date" != ''
    ORDER BY "Watched Date" DESC, rowid DESC 
    LIMIT 1
"""
last_movie_df = pd.read_sql(last_movie_query, conn)
conn.close()

if not last_movie_df.empty:
    last_name = str(last_movie_df['Name'].iloc[0]).upper()
    raw_rating = last_movie_df['Rating'].iloc[0]
    try:
        last_rating_val = int(float(raw_rating))
    except:
        last_rating_val = 0
else:
    last_name = "VERI YOK"
    last_rating_val = 0
# ----------------------------------



# ==========================================
# HEADER
# ==========================================
st.markdown("<h2 style='letter-spacing: 2px; text-transform: uppercase; margin-top: -20px; color: #f0f0f0;'>Deep Profile Analysis</h2>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid #2c3440; margin-bottom: 20px;'>", unsafe_allow_html=True)

# ==========================================
# ROW 1: TOP KPI METRICS
# ==========================================
# Sadece isim değil, isim ve yönetmen kombinasyonu eşsiz olanları sayar
total_films = len(df_all.drop_duplicates(subset=['Name', 'Director']))
total_hours = int(df_all['Runtime'].sum()) / 60 # Tüm izlenenlerin süresini toplar

df_dir = df_rated.assign(Director=df_rated['Director'].str.split(', ')).explode('Director')
df_dir = df_dir[~df_dir['Director'].isin(['Unknown', '', None])]
dir_stats = df_dir.groupby('Director').agg(Film_Count=('Name', 'count'), Avg_Rating=('Rating', 'mean'))
valid_dirs = dir_stats[dir_stats['Film_Count'] >= 5]
best_dir_str = f"{valid_dirs.sort_values(by='Avg_Rating', ascending=False).iloc[0].name} ({valid_dirs.sort_values(by='Avg_Rating', ascending=False).iloc[0]['Avg_Rating']:.2f} Avg)" if not valid_dirs.empty else "N/A"

df_genre = df_rated.assign(Genre=df_rated['Genre'].str.split(', ')).explode('Genre')
df_genre = df_genre[~df_genre['Genre'].isin(['Unknown', '', None])]
genre_stats = df_genre.groupby('Genre').agg(Film_Count=('Name', 'count'), Avg_Rating=('Rating', 'mean'))
valid_genres = genre_stats[genre_stats['Film_Count'] >= 10].copy()

if not valid_genres.empty:
    max_c, min_c = valid_genres['Film_Count'].max(), valid_genres['Film_Count'].min()
    max_r, min_r = valid_genres['Avg_Rating'].max(), valid_genres['Avg_Rating'].min()
    range_c = max_c - min_c if max_c > min_c else 1
    range_r = max_r - min_r if max_r > min_r else 1
    valid_genres['Combined_Score'] = ((valid_genres['Film_Count'] - min_c) / range_c) + ((valid_genres['Avg_Rating'] - min_r) / range_r)
    best_genre = valid_genres.sort_values(by='Combined_Score', ascending=False).iloc[0]
    best_genre_str = f"{best_genre.name} ({best_genre['Avg_Rating']:.2f} Avg | {int(best_genre['Film_Count'])} Films)"
else: best_genre_str = "N/A"

m1, m2, m3, m4 = st.columns([1, 1, 3, 4])
m1.metric("Total Films", f"{total_films}")
m2.metric("Total Hours", f"{total_hours:,.0f}")
m3.metric("Top Director (Min 5)", best_dir_str)
m4.metric("Top Genre (Weighted)", best_genre_str)

st.markdown("<hr style='border: 1px solid #2c3440; margin: 20px 0 30px 0;'>", unsafe_allow_html=True)

# ==========================================
# ROW 2: TRIPLE PANEL (ACTIVITY - RECENT - FLOW)
# ==========================================
# Kolon genişliklerini [Aktivite, Son İzlenen, Grafik] olarak ayarlıyoruz
col1, col2, col3 = st.columns([1, 1, 1.3])

with col1:
    st.markdown("<h4 style='color: #a0b0c0; margin-bottom: 15px; font-size: 0.9rem; letter-spacing: 1px;'>CURRENT ACTIVITY</h4>", unsafe_allow_html=True)
    if not df_dates.empty:
        max_date = df_dates['Watched_Date_Log'].max()
        start_of_week = max_date - pd.Timedelta(days=max_date.weekday()) 
        end_of_week = start_of_week + pd.Timedelta(days=6)
        df_week = df_dates[(df_dates['Watched_Date_Log'] >= start_of_week) & (df_dates['Watched_Date_Log'] <= end_of_week)]
        week_count = len(df_week)
        week_avg = df_week[df_week['Rating'] > 0]['Rating'].mean() if week_count > 0 else 0.0
        
        st.markdown(f"""
        <div class="ins-week">
            <div class="week-top">
                <p class="week-title"><span class="pulse-dot"></span> RECORDING</p>
            </div>
            <div class="week-stats">
                <div class="w-stat-item">
                    <p class="w-stat-label">Films</p>
                    <p class="w-stat-val" style="font-size: 2.2rem;">{week_count}</p>
                </div>
                <div class="w-stat-item">
                    <p class="w-stat-label">Rating</p>
                    <p class="w-stat-val" style="font-size: 2.2rem;">{week_avg:.2f}</p>
                </div>
            </div>
            <p class="week-date">[{start_of_week.strftime('%b %d')} - {end_of_week.strftime('%b %d')}]</p>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("<h4 style='color: #a0b0c0; margin-bottom: 15px; font-size: 0.9rem; letter-spacing: 1px;'>MOST RECENT WATCH</h4>", unsafe_allow_html=True)
    # Emoji yok, saf Unicode karakter yıldızlar:
    stars = "★" * last_rating_val + "☆" * (5 - last_rating_val)
    st.markdown(f"""
    <div class="ins-week" style="border-left: 2px solid #c5a059;">
        <div>
            <p style="color: #7a8b99; font-size: 0.75rem; letter-spacing: 1.5px; margin-bottom: 15px; text-transform: uppercase;">Latest Entry</p>
            <h2 style="font-size: 1.1rem; color: #f0f0f0; margin: 5px 0; line-height: 1.4; font-weight: 800;">{last_name}</h2>
        </div>
        <div>
            <div style="color: #c5a059; font-size: 1.3rem; letter-spacing: 3px; margin-bottom: 10px;">{stars}</div>
            <p style="color: #445566; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1px;">Auto-synced via Bot</p>
        </div>
    </div>
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
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=260,
        margin=dict(l=0, r=0, t=10, b=0), dragmode=False,
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
    
    # 1. LONGEST MARATHON
    marathon_stats = df_dates.groupby('DateOnly').agg(Film_Count=('Name', 'count'), Total_Runtime=('Runtime', 'sum')).reset_index()
    valid_marathons = marathon_stats[marathon_stats['Film_Count'] <= 8]
    if not valid_marathons.empty:
        best_marathon = valid_marathons.sort_values(by=['Film_Count', 'Total_Runtime'], ascending=[False, False]).iloc[0]
        st.markdown(f"""
        <div class="ins-marathon">
            <div>
                <p class="m-title">LONGEST MARATHON</p>
                <p class="m-val">{int(best_marathon['Film_Count'])} FILMS</p>
                <p class="m-sub">in a single day</p>
            </div>
            <div class="m-right">
                <p class="m-time">{int(best_marathon['Total_Runtime'] // 60)}H {int(best_marathon['Total_Runtime'] % 60)}M</p>
                <p class="m-date">{best_marathon['DateOnly'].strftime('%B %d, %Y')}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 2. TIME WASTED
    wasted_df = df[(df['Rating'] > 0) & (df['Rating'] < 2.0)]
    wasted_runtime = int(wasted_df['Runtime'].sum())
    st.markdown(f"""
    <div class="ins-wasted">
        <p class="w-title">"TIME WASTED" INDEX</p>
        <p class="w-val">{wasted_runtime // 60}h {wasted_runtime % 60}m</p>
        <p class="w-sub">Total time spent watching films rated below 2.0.</p>
    </div>
    """, unsafe_allow_html=True)

    # 3. PEAK CINEMA MONTH
    df_rated_months = df[(df['Rating'] > 0) & (df['Watched_Date_Log'].notna())].copy()
    df_rated_months['YearMonth'] = df_rated_months['Watched_Date_Log'].dt.to_period('M')
    month_stats = df_rated_months.groupby('YearMonth').agg(Film_Count=('Name', 'count'), Avg_Rating=('Rating', 'mean')).reset_index()
    valid_months = month_stats[month_stats['Film_Count'] >= 10]
    if not valid_months.empty:
        best_month = valid_months.loc[valid_months['Avg_Rating'].idxmax()]
        st.markdown(f"""
        <div class="ins-peak">
            <p class="p-title">PEAK CINEMA MONTH (MIN. 10 FILMS)</p>
            <div class="p-flex">
                <p class="p-val">{best_month['YearMonth'].strftime('%B %Y')}</p>
                <span class="p-badge">{best_month['Avg_Rating']:.2f} AVG</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 4. MOST GENEROUS DECADE
    df_generous = df[(df['Year'] > 1800) & (df['Rating'] > 0)].copy()
    df_generous['Decade'] = (df_generous['Year'] // 10) * 10
    decade_stats = df_generous.groupby('Decade').agg(Avg_Rating=('Rating', 'mean'), Film_Count=('Name', 'count')).reset_index()
    valid_decades = decade_stats[decade_stats['Film_Count'] >= 10]
    if not valid_decades.empty:
        best_decade = valid_decades.loc[valid_decades['Avg_Rating'].idxmax()]
        st.markdown(f"""
        <div class="ins-era">
            <div class="e-left">
                <p class="e-title">MOST GENEROUS ERA</p>
                <p class="e-sub">{best_decade['Avg_Rating']:.2f} Avg Rating</p>
            </div>
            <p class="e-val">{int(best_decade['Decade'])}s</p>
        </div>
        """, unsafe_allow_html=True)

    # 5. RECENT HABIT
    max_date = df_dates['Watched_Date_Log'].max()
    three_months_ago = max_date - pd.DateOffset(months=3)
    recent_df = df_dates[df_dates['Watched_Date_Log'] >= three_months_ago].copy()
    if not recent_df.empty:
        best_dow = recent_df['Watched_Date_Log'].dt.day_name().value_counts().idxmax()
        st.markdown(f"""
        <div class="ins-habit">
            <p class="h-title">FAVORITE RECENT DAY:</p>
            <p class="h-val">{best_dow}s</p>
        </div>
        """, unsafe_allow_html=True)

with col_right:
    st.markdown("<h4 style='color: #a0b0c0; margin-bottom: 15px; font-size: 0.9rem; letter-spacing: 1px;'>TOP 10 ACTIVE MONTHS' FAVORITES</h4>", unsafe_allow_html=True)
    top_10_months_series = df_rated_months['YearMonth'].dt.strftime('%Y-%m').value_counts().head(10).index
    df_rated_months['YearMonthStr'] = df_rated_months['YearMonth'].dt.strftime('%Y-%m')
    df_top10 = df_rated_months[df_rated_months['YearMonthStr'].isin(top_10_months_series)]
    
    if not df_top10.empty:
        monthly_top_busiest = df_top10.loc[df_top10.groupby('YearMonthStr')['Rating'].idxmax()].sort_values('YearMonthStr', ascending=False)
        
        # Renk döngüsü söküldü, asil ve tek tonlu mat tasarıma geçildi
        for i, (_, row) in enumerate(monthly_top_busiest.iterrows()):
            rank_num = f"{i+1:02d}" 
            
            st.markdown(f"""
            <div class="movie-card" style="position: relative; overflow: hidden; z-index: 1;">
                <div style="position: absolute; right: 10px; bottom: -15px; font-size: 4.5rem; font-weight: 900; color: rgba(255,255,255,0.02); z-index: -1; line-height: 1; font-family: 'Courier New', Courier, monospace;">
                    {rank_num}
                </div>
                <div class="rating-badge">{row['Rating']} / 5.0</div>
                <p class="movie-title">{row['Name']} <span style='color: #5a6b7c; font-weight: 400; font-size:0.9rem;'>({int(row['Year'])})</span></p>
                <p class="movie-meta">Period: <b style="color: #a0b0c0;">{row['YearMonthStr']}</b> &nbsp;|&nbsp; Dir: {str(row['Director']).split(',')[0]}</p>
            </div>
            """, unsafe_allow_html=True)