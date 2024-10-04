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
min_date = pd.to_datetime(day_df['dteday']).dt.date.min()
max_date = pd.to_datetime(day_df['dteday']).dt.date.max()


 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://png.pngtree.com/png-clipart/20230807/original/pngtree-vector-illustration-of-a-bicycle-rental-logo-on-a-white-background-vector-picture-image_10130399.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]

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


st.subheader("persentase penyewaan yang berasal dari pengguna terdaftar dibandingkan dengan pengguna kasual")
# Menghitung jumlah pendaftar Kasual dan Terdaftar
casual_counts = sum(day_df['casual'])
registered_counts = sum(day_df['registered'])

# Definisikan data untuk pie chart
data = [casual_counts, registered_counts]
labels = ["Casual", "Registered"]

# Membuat Pie Chart menggunakan Matplotlib
fig, ax = plt.subplots()
ax.pie(data, labels=labels, autopct='%1.1f%%')

# Menampilkan grafik di Streamlit
st.pyplot(fig)
st.text("Berdasarkan gaambar di atas, Penyewaan yang berasal dari penyewa terdaftar adalah 81,2% dan penyewa casual adalah 18,8%")

st.subheader("Jam Penyewaan sepeda paling tinggi")

# Menghitung total penyewaan berdasarkan jam
hour_counts = hour_df.groupby('hr')['cnt'].sum()

# Membuat barplot menggunakan Seaborn
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x=hour_counts.index, y=hour_counts.values, ax=ax)
ax.set_title('Total Penyewaan berdasarkan Jam')
ax.set_xlabel('Jam dalam Sehari')
ax.set_ylabel('Total Penyewaan')
ax.set_xticks(range(len(hour_counts.index)))
ax.set_xticklabels(hour_counts.index, rotation=0)

# Menampilkan plot di Streamlit
st.pyplot(fig)
st.text("Berdasarkan gambar di atas, Penyewaan sepeda paling tinggi yaitu pada jam 17.00 dan paling sedikit pada jam 04.00")

st.header("pengaruh season terhadap penyewaan sepeda baik penyewa registered ataupun penyewa casual")

# Mengelompokkan data berdasarkan season dan registered/casual
seasonal = day_df.groupby("season")[["registered", "casual"]].sum().reset_index()

# Membuat bar plot
fig, ax = plt.subplots(figsize=(10, 5))

# Bar plot untuk "Registered"
ax.bar(
    seasonal["season"],
    seasonal["registered"],
    label="Registered",
    color="tab:orange"
)

# Bar plot untuk "Casual"
ax.bar(
    seasonal["season"],
    seasonal["casual"],
    label="Casual",
    color="tab:blue"
)

# Menambahkan judul dan label
ax.set_title('Total Penyewaan berdasarkan Musim')
ax.set_xlabel('Season')
ax.set_ylabel('Total Penyewaan')
ax.legend()

# Menampilkan plot di Streamlit
st.pyplot(fig)
st.text("Berdasarkan gambar di atas, terlihat bahwa season berpengaruh terhadap jumlah penyewa. Penyewa paling banyak yaitu pada musim gugur(fall), lalu pada musim panas(summer), musim dingin (winter), dan paling sedikit pada musim semi (spring)")

#Caption
st.caption('Copyright (c) Arfah Hamidah 2024')