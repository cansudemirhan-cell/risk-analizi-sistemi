import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Lazzoni Entegre Risk Yönetimi", layout="wide")

# --- FONKSİYONLAR ---
def fine_kinney_derece(puan):
    if puan >= 400: return "Tolere Edilemez Risk", "red"
    elif puan >= 200: return "Çok Yüksek Risk", "orange"
    elif puan >= 70: return "Yüksek Risk", "yellow"
    elif puan >= 20: return "Önemli Risk", "blue"
    else: return "Düşük Risk", "green"

def matris_5x5_derece(puan):
    if puan >= 13: return "Kabul Edilemez Risk", "red"
    elif puan >= 7: return "Dikkate Değer Risk", "orange"
    else: return "Kabul Edilebilir Risk", "green"

# --- ANA BAŞLIK ---
st.title("🛡️ Lazzoni Entegre Risk & Boyut Analiz Paneli")
tab1, tab2, tab3 = st.tabs(["📊 Kalite (9001)", "🏥 İSG (45001 - Fine Kinney)", "🍃 Çevre (14001)"])

# --- TAB 1: KALİTE (5X5 MATRİS) ---
with tab1:
    st.header("Kalite Risk Değerlendirme (5x5)")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Yeni Risk Ekle")
        k_risk = st.text_input("Risk Tanımı (Kalite)")
        k_o = st.slider("Olasılık", 1, 5, 3, key="k_o")
        k_s = st.slider("Şiddet", 1, 5, 3, key="k_s")
        if st.button("Kalite Riski Kaydet"):
            st.success(f"Risk Puanı: {k_o * k_s}")
    
    with col2:
        # Isı Haritası (Daha önce kurduğumuz yapı)
        z_data = [[1, 2, 3, 4, 5], [2, 4, 6, 8, 10], [3, 6, 9, 12, 15], [4, 8, 12, 16, 20], [5, 10, 15, 20, 25]]
        fig = px.imshow(z_data, labels=dict(x="Olasılık", y="Şiddet", color="Puan"),
                        x=['1', '2', '3', '4', '5'], y=['1', '2', '3', '4', '5'],
                        color_continuous_scale='RdYlGn_r')
        st.plotly_chart(fig, use_container_width=True)

# --- TAB 2: İSG (FINE-KINNEY) ---
with tab2:
    st.header("İSG Risk Analizi (Fine-Kinney)")
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        olasılık = st.selectbox("Olasılık (O)", [0.1, 0.2, 0.5, 1, 3, 6, 10], help="0.1: Hemen hemen imkansız - 10: Beklenir")
    with c2:
        frekans = st.selectbox("Frekans (F)", [0.5, 1, 2, 3, 6, 10], help="0.5: Çok nadir - 10: Sürekli")
    with c3:
        siddet = st.selectbox("Şiddet (S)", [1, 3, 7, 15, 40, 100], help="1: Küçük hasar - 100: Çoklu ölüm")
    
    fk_puan = olasılık * frekans * siddet
    derece, renk = fine_kinney_derece(fk_puan)
    
    with c4:
        st.metric("Fine-Kinney Skoru", f"{fk_puan:.1f}")
        st.markdown(f"**Derece:** :{renk}[{derece}]")

    # Fine-Kinney Risk Dağılım Grafiği (Örnek Veriyle)
    st.info("Fine-Kinney metodunda risk, maruziyet sıklığı (Frekans) dahil edilerek hesaplanır.")

# --- TAB 3: ÇEVRE (BOYUT ANALİZİ) ---
with tab3:
    st.header("Çevre Boyut ve Etki Analizi")
    st.warning("Çevre boyutları yasal şartlar ve kirlilik potansiyeline göre değerlendirilir.")
    # Buraya yüklediğin Çevre CSV'sinden özet tablo ekleyebiliriz
    st.write("Mevcut Çevre Boyutları Sayısı: 22 (CSV Verisi)")
    
    # Çevre için basit bir bar chart
    env_data = pd.DataFrame({
        "Boyut": ["Atık Yağ", "Emisyon", "Gürültü", "Tehlikeli Atık"],
        "Etki Puanı": [12, 8, 15, 20]
    })
    fig_env = px.bar(env_data, x="Boyut", y="Etki Puanı", color="Etki Puanı", color_continuous_scale='Viridis')
    st.plotly_chart(fig_env, use_container_width=True)

# --- VERİ AKTARMA ---
st.sidebar.divider()
st.sidebar.download_button("Excel Raporu Al", data="test", file_name="EYS_Risk_Raporu.csv")
