import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

day_df = pd.read_csv("dashboard/day_clean.csv")
hour_df = pd.read_csv("dashboard/hour_clean.csv")


def create_count_df(day_df):
    count_df = day_df.groupby(by='dteday').agg({
        'cnt': 'sum'
    }).reset_index()
    return count_df

def create_registered_df(day_df):
    registered_df = day_df.groupby(by='dteday').agg({
        'registered': 'sum'
    }).reset_index()
    return registered_df

def create_casual_df(day_df):
    casual_df = day_df.groupby(by='dteday').agg({
        'casual': 'sum'
    }).reset_index()
    return casual_df

def create_seasonal_df(day_df):
    seasonal_df=day_df.groupby("season")[["registered", "casual"]].sum().reset_index()
    return seasonal_df

# def create_hour_counts_df(hour_df):
#     hour_counts_df =  hour_df.groupby(by="hr").agg({"cnt": ["sum"]}).reset_index()
#     return hour_counts_df

# Membuat komponen filter
day_df["dteday"] = pd.to_datetime(day_df["dteday"])
min_date = day_df['dteday'].dt.date.min()
max_date = day_df['dteday'].dt.date.max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://png.pngtree.com/png-clipart/20230807/original/pngtree-vector-illustration-of-a-bicycle-rental-logo-on-a-white-background-vector-picture-image_10130399.png")
    
    # Mengambil start_date & end_date dari date_input
    selected_dates = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

try:
    # Cek apakah user memilih rentang tanggal yang valid
    if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
        start_date, end_date = selected_dates

        # Jika tanggal awal lebih besar dari tanggal akhir, tampilkan warning
        if start_date > end_date:
            raise ValueError("Tanggal awal tidak boleh lebih besar dari tanggal akhir!")

        # Filter data berdasarkan rentang waktu
        main_df = day_df[(day_df["dteday"].dt.date >= start_date) & 
                         (day_df["dteday"].dt.date <= end_date)]
    
    else:
        raise ValueError("Rentang tanggal tidak valid!")

except ValueError as e:
    # Jika terjadi error, tampilkan warning dan kembalikan ke data default
    st.warning(f"⚠️ {str(e)} Menampilkan data default.")
    start_date, end_date = min_date, max_date
    main_df = day_df

# Data farme
count_df = create_count_df(main_df)
registered_df = create_registered_df(main_df)
casual_df = create_casual_df(main_df)
seasonal_df = create_seasonal_df(main_df)
# hour_count_df=create_hour_counts_df(main_df)

st.header("Bike Rental Dashboard :sparkles:")

# Membuat tampilan jumlah penyewaan harian
st.subheader('Penyewaan Harian')
col1, col2, col3 = st.columns(3)

with col1:
    daily_casual = casual_df['casual'].sum()
    st.metric('Casual User', value= daily_casual)

with col2:
    daily_registered = registered_df['registered'].sum()
    st.metric('Registered User', value= daily_registered)
 
with col3:
    daily_total = count_df['cnt'].sum()
    st.metric('Total User', value= daily_total)


st.subheader("Persentase penyewaan yang berasal dari pengguna terdaftar dibandingkan dengan pengguna kasual")
# Menghitung jumlah pendaftar Kasual dan Terdaftar
casual_counts = sum(casual_df['casual'])
registered_counts = sum(registered_df['registered'])

# Definisikan data untuk pie chart
data = [casual_counts, registered_counts]
labels = ["Casual", "Registered"]
colors=['#ff6361', '#ffa600']

# Membuat Pie Chart menggunakan Matplotlib
fig, ax = plt.subplots()
ax.pie(data, labels=labels, autopct='%1.1f%%', colors=colors)
ax.set_title("Distribusi Penyewaan sepeda")
ax.legend(labels, loc="best")

# Menampilkan grafik di Streamlit
st.pyplot(fig)
percentages = [f"{(x / sum(data)) * 100:.1f}%" for x in data]
st.markdown(f"Berdasarkan gambar di atas, Penyewaan yang berasal dari penyewa terdaftar adalah **{percentages[1]}** dan penyewa casual adalah **{percentages[0]}**")

st.subheader("Jam Penyewaan sepeda paling tinggi")

# Menghitung total penyewaan berdasarkan jam
hour_counts = hour_df[hour_df["dteday"].between(str(start_date), str(end_date))].groupby('hr')['cnt'].sum()

# Membuat barplot menggunakan Seaborn
max_hour = hour_counts.idxmax()
min_hour = hour_counts.idxmin()
colors = ['#004c6d' if hour in [max_hour, min_hour] else '#c1e7ff' for hour in hour_counts.index] 
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x=hour_counts.index, y=hour_counts.values, ax=ax, palette=colors)
ax.set_title('Total Penyewaan berdasarkan Jam')
ax.set_xlabel('Jam dalam Sehari')
ax.set_ylabel('Total Penyewaan')
ax.set_xticks(range(len(hour_counts.index)))
ax.set_xticklabels(hour_counts.index, rotation=0)

# Menampilkan plot di Streamlit
st.pyplot(fig)
st.markdown("Berdasarkan gambar di atas, Penyewaan sepeda paling tinggi yaitu pada jam 17.00 dan paling sedikit pada jam 04.00")

st.header("pengaruh season terhadap penyewaan sepeda baik penyewa registered ataupun penyewa casual")

# Mengelompokkan data berdasarkan season dan registered/casual
seasonal = seasonal_df.groupby("season")[["registered", "casual"]].sum().reset_index()

# Membuat bar plot
fig, ax = plt.subplots(figsize=(10, 5))

# Bar plot untuk "Registered"
ax.bar(
    seasonal["season"],
    seasonal["registered"],
    label="Registered",
    color="#ffa600"
)

# Bar plot untuk "Casual"
ax.bar(
    seasonal["season"],
    seasonal["casual"],
    label="Casual",
    color="#ff6361"
)

# Menambahkan judul dan label
ax.set_title('Total Penyewaan berdasarkan Musim')
ax.set_xlabel('Season')
ax.set_ylabel('Total Penyewaan')
ax.legend()

# Menampilkan plot di Streamlit
st.pyplot(fig)
# st.markdown("Berdasarkan gambar di atas, terlihat bahwa season berpengaruh terhadap jumlah penyewa. Penyewa paling banyak yaitu pada musim gugur(fall), lalu pada musim panas(summer), musim dingin (winter), dan paling sedikit pada musim semi (spring)")
if not seasonal_df.empty:
    # Buat dictionary mapping season
    season_dict = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}

    if not seasonal.empty:
        max_season = seasonal.loc[(seasonal["registered"] + seasonal["casual"]).idxmax(), "season"]

        # Pastikan season ada di dictionary sebelum mengaksesnya
        max_season_name = season_dict.get(max_season)

        # Menampilkan hasil dalam Streamlit
        st.markdown(f"Berdasarkan gambar di atas, terlihat bahwa musim berpengaruh terhadap jumlah penyewa. "
                    f"Penyewaan terbanyak terjadi pada musim **{max_season_name}**.")
    else:
        st.warning("Data tidak tersedia untuk perhitungan seasonal setelah filtering.")
else:
    st.warning("Tidak ada data dalam rentang waktu yang dipilih.")

#Caption
st.caption('Copyright (c) Arfah Hamidah 2024')