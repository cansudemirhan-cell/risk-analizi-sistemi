import streamlit as st
import pandas as pd
import plotly.express as px

# Sayfa Ayarları
st.set_page_config(page_title="Risk Analizi Paneli", layout="wide")

# Veriyi Oku
try:
    df = pd.read_csv('risk_analizi_temizlenmis.csv')
    
    st.title("📊 Risk Fırsat Değerlendirme Programı")
    st.sidebar.header("Filtreleme Menüsü")
    
    # Filtreler
    dept = st.sidebar.multiselect("Departman", df['DEPARTMAN'].unique(), default=df['DEPARTMAN'].unique())
    df_filtered = df[df['DEPARTMAN'].isin(dept)]

    # Metrikler
    c1, c2, c3 = st.columns(3)
    c1.metric("Toplam Risk Sayısı", len(df_filtered))
    c2.metric("Ortalama Risk Puanı", round(df_filtered['TOPLAM_RISK_PUANI'].mean(), 2))
    c3.metric("Kritik Riskler (12+)", len(df_filtered[df_filtered['TOPLAM_RISK_PUANI'] >= 12]))

    # Grafik
    fig = px.bar(df_filtered, x="RİSK", y="TOPLAM_RISK_PUANI", color="RISK_DERECESI", title="Risk Puan Dağılımı")
    st.plotly_chart(fig, use_container_width=True)

    # Tablo
    st.subheader("📋 Detaylı Risk Listesi")
    st.dataframe(df_filtered[['NO', 'DEPARTMAN', 'RİSK', 'TOPLAM_RISK_PUANI', 'RISK_DERECESI', 'SURE']])

except FileNotFoundError:
    st.error("HATA: 'risk_analizi_temizlenmis.csv' dosyası bulunamadı! Lütfen aynı klasöre koyun.")