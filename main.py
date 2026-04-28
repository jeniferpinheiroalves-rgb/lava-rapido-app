import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import urllib.parse
from datetime import datetime

# --- CONFIGURAÇÃO DO FIREBASE ---
if not firebase_admin._apps:

    firebase_admin.initialize_app(cred)

db = firestore.client()

# --- INTERFACE ---
st.set_page_config(page_title="Lava Rápido do Fabinho", page_icon="🚗")

# Estilo personalizado (Terracota)
st.markdown("""
    <style>
    .stButton>button { background-color: #B2522E; color: white; border-radius: 10px; }
    .stTextInput>div>div>input { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚗 Lava Rápido do Fabinho")
menu = ["Agendar Serviço", "Planos Mensais", "Nossa Localização"]
escolha = st.sidebar.selectbox("Menu", menu)

# --- TELA 1: AGENDAMENTO ---
if escolha == "Agendar Serviço":
    st.header("Agende seu Horário")
    
    with st.form("agendamento"):
        nome = st.text_input("Seu Nome")
        telefone = st.text_input("WhatsApp (com DDD)")
        veiculo = st.text_input("Modelo do Veículo (Ex: Honda Civic)")
        cor = st.text_input("Cor")
        placa = st.text_input("Placa").upper()
        
        servico = st.selectbox("Escolha o Serviço", 
                               ["Lavagem Simples - R$ 40", 
                                "Lavagem Completa - R$ 60", 
                                "Higienização Interna - R$ 150",
                                "Polimento - R$ 200"])
        
        data = st.date_input("Data")
        hora = st.time_input("Horário")
        leva_traz = st.radio("Precisa de Leva e Traz?", ("Não", "Sim"))
        
        submit = st.form_submit_button("Confirmar Agendamento")

    if submit:
        if nome and placa:
            # Dados para o Banco
            dados = {
                "cliente": nome,
                "telefone": telefone,
                "veiculo": f"{veiculo} ({cor})",
                "placa": placa,
                "servico": servico,
                "data": str(data),
                "hora": str(hora),
                "leva_traz": leva_traz,
                "status": "Pendente"
            }
            
            # Salva no Firestore
            db.collection('agendamentos').add(dados)
            st.success(f"✅ Agendamento realizado para {data} às {hora}!")

            # Lógica do WhatsApp para Leva e Traz
            if leva_traz == "Sim":
                seu_whatsapp = "5511999999999" # COLOQUE O SEU NÚMERO AQUI
                texto_msg = (
                    f"🚗 NOVO AGENDAMENTO (LEVA E TRAZ)\n\n"
                    f"👤 Cliente: {nome}\n"
                    f"🚘 Veículo: {veiculo} ({cor})\n"
                    f"🔢 Placa: {placa}\n"
                    f"🛠️ Serviço: {servico}\n"
                    f"📅 Data: {data} às {hora}\n\n"
                    f"📍 Por favor, envie sua localização agora."
                )
                texto_url = urllib.parse.quote(texto_msg)
                link = f"https://wa.me/{seu_whatsapp}?text={texto_url}"
                st.link_button("🚀 Enviar Localização no WhatsApp", link)
        else:
            st.error("Por favor, preencha o nome e a placa.")

# --- TELA 2: PLANOS ---
elif escolha == "Planos Mensais":
    st.header("Planos de Fidelidade")
    st.write("Economize com nossos pacotes mensais.")
    
    planos = [
        {"nome": "Prata", "preco": "R$ 80", "lavagens": 2, "obs": "Bucha + Pretinho"},
        {"nome": "Ouro", "preco": "R$ 150", "lavagens": 4, "obs": "Completa + Cera"},
        {"nome": "Black", "preco": "R$ 280", "lavagens": 8, "obs": "Tudo incluso + Motor"}
    ]
    
    for p in planos:
        with st.expander(f"🏆 Planos {p['nome']} - {p['preco']}"):
            st.write(f"Benefícios: {p['obs']}")
            st.write(f"Quantidade: {p['lavagens']} lavagens por mês")
            st.button(f"Assinar Plano {p['nome']}")

# --- TELA 3: LOCALIZAÇÃO ---
elif escolha == "Nossa Localização":
    st.header("Venha nos visitar!")
    st.write("📍 Rua do Automóvel, 500 - Centro")
    st.info("Atendimento de Segunda a Sábado, das 08:00 às 18:00")

# --- ÁREA DO ADMINISTRADOR ---
st.sidebar.divider()
if st.sidebar.checkbox("Acesso Administrativo"):
    senha = st.sidebar.text_input("Senha", type="password")
    if senha == "1234":
        st.header("👨‍🔧 Painel do Fabinho")
        
        tab1, tab2 = st.tabs(["Novos Clientes", "Ver Agendamentos"])
        
        with tab1:
            st.subheader("Cadastrar Cliente no Plano")
            c_nome = st.text_input("Nome do Cliente")
            c_placa = st.text_input("Placa")
            c_saldo = st.number_input("Saldo de Lavagens", min_value=0)
            if st.button("Salvar Cliente"):
                db.collection('clientes').add({
                    'nome': c_nome,
                    'placa': c_placa.upper(),
                    'saldo': c_saldo
                })
                st.success("Cliente cadastrado!")
        
        with tab2:
            st.subheader("Agenda do Dia")
            agendas = db.collection('agendamentos').stream()
            for ag in agendas:
                item = ag.to_dict()
                st.write(f"📅 {item['data']} - {item['placa']} ({item['servico']})"
                         import json

firebase_config = dict(st.secrets["firebase"])
firebase_config["private_key"] = firebase_config["private_key"].replace("\\n", "\n")

cred = credentials.Certificate(firebase_config)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

