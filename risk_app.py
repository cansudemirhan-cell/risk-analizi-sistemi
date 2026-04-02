import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Proses Risk Analizi Dashboard", layout="wide")

# --- VERİ YÜKLEME ---
@st.cache_data
def load_initial_data():
    return pd.read_csv('risk_analizi_temizlenmis.csv')

if 'df' not in st.session_state:
    st.session_state.df = load_initial_data()

# --- YENİ RİSK EKLEME FORMU (SIDEBAR) ---
st.sidebar.header("➕ Yeni Risk Kaydı")
with st.sidebar.form("risk_form"):
    new_dept = st.selectbox("Departman", ["KALİTE", "ÜRETİM", "SATİNALMA", "LOJİSTİK", "İK"])
    new_risk = st.text_input("Risk Tanımı")
    new_prob = st.slider("Olasılık (1-5)", 1, 5, 3)
    new_imp = st.slider("Etki/Şiddet (1-5)", 1, 5, 3)
    new_owner = st.text_input("Sorumlu")
    submit = st.form_submit_button("Sisteme Ekle")

    if submit:
        puan = new_prob * new_imp
        derece = "Kabul Edilemez" if puan >= 13 else ("Dikkate Değer" if puan >= 7 else "Kabul Edilebilir")
        new_data = pd.DataFrame([{
            "NO": len(st.session_state.df) + 1,
            "DEPARTMAN": new_dept,
            "RİSK": new_risk,
            "OLASILIK": new_prob,
            "ETKI_DEGERI": new_imp,
            "TOPLAM_RISK_PUANI": puan,
            "RISK_DERECESI": derece,
            "SORUMLU": new_owner,
            "SURE": "2026-12-31"
        }])
        st.session_state.df = pd.concat([st.session_state.df, new_data], ignore_index=True)
        st.success("Risk başarıyla eklendi!")

# --- DASHBOARD ÜST KISIM ---
st.title("🛡️ Proses Risk Analizi ve Isı Haritası")

col1, col2, col3 = st.columns(3)
col1.metric("Toplam Proses Riski", len(st.session_state.df))
col2.metric("Kritik (Kırmızı) Bölge", len(st.session_state.df[st.session_state.df['TOPLAM_RISK_PUANI'] >= 13]))
col3.metric("Ortalama Risk Skoru", round(st.session_state.df['TOPLAM_RISK_PUANI'].mean(), 1))

st.divider()

# --- ISI HARİTASI (GÖRSELDEKİ YAPI) ---
st.subheader("📍 Risk Matrisi (Heatmap)")

# Matris verisini hazırlama
z_data = [[1, 2, 3, 4, 5], [2, 4, 6, 8, 10], [3, 6, 9, 12, 15], [4, 8, 12, 16, 20], [5, 10, 15, 20, 25]]
fig_heat = ff = go.Figure(data=go.Heatmap(
    z=z_data,
    x=['1', '2', '3', '4', '5'],
    y=['1', '2', '3', '4', '5'],
    colorscale=[[0, 'green'], [0.3, 'yellow'], [0.6, 'orange'], [1, 'red']],
    showscale=False
))

# Mevcut riskleri matris üzerine nokta olarak ekleme
for i, row in st.session_state.df.iterrows():
    fig_heat.add_trace(go.Scatter(
        x=[str(int(row['OLASILIK']))], 
        y=[str(int(row['ETKI_DEGERI']))],
        mode='markers+text',
        marker=dict(color='black', size=12, line=dict(width=2, color='white')),
        text=[str(int(row['NO']))],
        textposition="top center",
        name=row['RİSK'],
        hovertext=f"Risk No: {row['NO']}<br>{row['RİSK']}"
    ))

fig_heat.update_layout(xaxis_title="OLASILIK", yaxis_title="ŞİDDET/ETKİ", height=500)
st.plotly_chart(fig_heat, use_container_width=True)

# --- DETAYLI TABLO ---
st.subheader("📋 Güncel Risk Kayıtları")
st.dataframe(st.session_state.df, use_container_width=True)

# --- VERİ İNDİRME ---
csv = st.session_state.df.to_csv(index=False).encode('utf-8')
st.download_button("Güncel Veriyi Excel/CSV Olarak İndir", data=csv, file_name="guncel_risk_analizi.csv", mime='text/csv')
