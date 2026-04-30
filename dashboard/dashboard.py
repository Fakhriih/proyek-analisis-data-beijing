import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from datetime import datetime

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Beijing Air Quality Dashboard",
    page_icon="🏥",
    layout="wide"
)

# --- STYLE CSS (Untuk Mempercantik Tampilan) ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOAD DATA ---
import os # Pastikan sudah ada import os di bagian paling atas

@st.cache_data
def load_data():
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "main_data.csv")
    df = pd.read_csv(file_path)

    # Memaksa konversi ke datetime dan menangani data kosong
    df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
    df = df.dropna(subset=['datetime'])
    
    # Memastikan index adalah datetime agar resample lebih stabil
    df = df.set_index('datetime')
    return df

# Saat memanggil data:
main_df = load_data()

# Gunakan resample langsung pada index (lebih stabil)
monthly_co = main_df['CO'].resample('M').mean().reset_index()

df = load_data()

# --- SIDEBAR (Filter) ---
with st.sidebar:
    st.image("https://ui-avatars.com/api/?name=Air+Quality&background=0D8ABC&color=fff", width=100)
    st.title("Pusat Kendali Data")
    st.markdown("---")
    
    # 1. Filter Rentang Waktu
    min_date = df["datetime"].min()
    max_date = df["datetime"].max()
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu Analisis',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

    # 2. Filter Stasiun
    stasiun_pilihan = st.multiselect(
        "Pilih Stasiun Pemantauan:",
        options=df["station"].unique(),
        default=df["station"].unique()[:3] # Default pilih 3 stasiun pertama
    )
    
    st.markdown("---")
    st.caption("Proyek Analisis Data - Fakhri (MedTech)")

# --- FILTERING LOGIC ---
main_df = df[(df["datetime"] >= pd.to_datetime(start_date)) & 
             (df["datetime"] <= pd.to_datetime(end_date)) &
             (df["station"].isin(stasiun_pilihan))]

# --- HEADER ---
st.title("Beijing Air Quality Health Dashboard")
st.markdown(f"Menampilkan data dari **{start_date}** sampai **{end_date}**")

# --- KARTU METRIK ---
col1, col2, col3 = st.columns(3)
with col1:
    avg_pm25 = main_df["PM2.5"].mean()
    st.metric("Rata-rata PM2.5", f"{avg_pm25:.2f} µg/m³")
with col2:
    avg_co = main_df["CO"].mean()
    st.metric("Rata-rata CO", f"{avg_co:.2f} µg/m³")
with col3:
    max_temp = main_df["TEMP"].max()
    st.metric("Suhu Tertinggi", f"{max_temp:.1f} °C")

st.markdown("---")

# --- VISUALISASI UTAMA ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Polusi PM2.5 Berdasarkan Wilayah")
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Agregasi data
    station_pm = main_df.groupby("station")["PM2.5"].mean().sort_values(ascending=False).reset_index()
    
    sns.barplot(
        x="PM2.5", 
        y="station", 
        data=station_pm, 
        palette="Reds_r", 
        ax=ax
    )
    ax.set_xlabel("Konsentrasi PM2.5 (µg/m³)")
    ax.set_ylabel(None)
    st.pyplot(fig)

with col_right:
    st.subheader("Tren Bulanan Kadar CO")
    # Agregasi bulanan
    monthly_co = main_df.resample(rule='M', on='datetime').agg({"CO": "mean"}).reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(
        monthly_co["datetime"], 
        monthly_co["CO"], 
        marker='o', 
        linewidth=2, 
        color="#3498db"
    )
    ax.fill_between(monthly_co["datetime"], monthly_co["CO"], color="#3498db", alpha=0.1)
    ax.set_xlabel(None)
    ax.set_ylabel("Kadar CO (µg/m³)")
    st.pyplot(fig)

# --- ANALISIS TAMBAHAN ---
st.markdown("---")
with st.expander("Lihat Insight Analisis"):
    st.write(f"""
        - Wilayah dengan polusi tertinggi saat ini adalah **{station_pm.iloc[0]['station']}**.
        - Rata-rata polusi udara di rentang waktu terpilih menunjukkan angka **{avg_pm25:.2f} µg/m³**, 
          yang masuk dalam kategori kualitas udara tertentu berdasarkan standar kesehatan.
        - Grafik tren menunjukkan adanya fluktuasi polusi yang dipengaruhi oleh perubahan musim.
    """)

st.caption("© 2026 Dashboard Kualitas Udara Beijing | Dikembangkan oleh Fakhri")