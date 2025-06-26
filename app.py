import streamlit as st
import pandas as pd
from datetime import datetime, time
import base64

# Configuração da página
st.set_page_config(
    page_title="SClínico - Simulação",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizado para melhorar a aparência
st.markdown("""
<style>
    .main-header {
        background-color: #2E86AB;
        color: white;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 20px;
        text-align: center;
    }
    
    .consultation-row {
        background-color: #f0f2f6;
        padding: 8px;
        margin: 2px 0;
        border-radius: 3px;
        border-left: 4px solid #2E86AB;
    }
    
    .consultation-selected {
        background-color: #E3F2FD;
        border-left: 4px solid #1976D2;
    }
    
    .calendar-widget {
        background-color: white;
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
    }
    
    .section-header {
        background-color: #37474F;
        color: white;
        padding: 5px 10px;
        margin: 10px 0 5px 0;
        border-radius: 3px;
        font-size: 14px;
        font-weight: bold;
    }
    
    .soap-section {
        border: 1px solid #ddd;
        margin: 10px 0;
        border-radius: 5px;
    }
    
    .soap-header {
        background-color: #455A64;
        color: white;
        padding: 10px;
        margin: 0;
        font-weight: bold;
        font-size: 18px;
        text-align: center;
    }
    
    .soap-content {
        padding: 20px;
        min-height: 150px;
        background-color: #fafafa;
    }
    
    .button-container {
        text-align: center;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar estado da sessão
if 'current_screen' not in st.session_state:
    st.session_state.current_screen = 'agenda'
if 'selected_patient' not in st.session_state:
    st.session_state.selected_patient = None

# Dados de exemplo das consultas
consultas_data = [
    {"hora": "09:00", "estado": "Agendado", "nome": "Maria Silva Santos", "tipo": "Adultos", "obs": "Consulta de rotina"},
    {"hora": "09:30", "estado": "Agendado", "nome": "João Pedro Costa", "tipo": "Adultos", "obs": "Seguimento"},
    {"hora": "10:15", "estado": "Agendado", "nome": "Ana Rodrigues", "tipo": "Adultos", "obs": "Primeira consulta"},
    {"hora": "11:00", "estado": "Agendado", "nome": "Carlos Manuel", "tipo": "Adultos", "obs": "Renovação receitas"},
    {"hora": "11:30", "estado": "Agendado", "nome": "Isabel Santos", "tipo": "Adultos", "obs": "Consulta de enfermagem"},
    {"hora": "13:00", "estado": "Em Espera", "nome": "José António Santos", "tipo": "Adultos", "obs": "Consulta urgente"},
    {"hora": "14:00", "estado": "Agendado", "nome": "Teresa Ferreira", "tipo": "Adultos", "obs": "Seguimento"},
    {"hora": "14:30", "estado": "Agendado", "nome": "António Costa", "tipo": "Adultos", "obs": "Consulta de rotina"},
    {"hora": "15:00", "estado": "Agendado", "nome": "Fernanda Lima", "tipo": "Adultos", "obs": "Primeira consulta"},
    {"hora": "15:30", "estado": "Agendado", "nome": "Manuel Oliveira", "tipo": "Adultos", "obs": "Seguimento"},
]

def show_agenda_screen():
    """Mostra o ecrã principal com a agenda do dia"""
    
    # Header principal
    st.markdown('<div class="main-header"><h2>SClínico - Dr(a) Bessa Cardoso - UCSP Breiner Porto</h2></div>', unsafe_allow_html=True)
    
    # Layout em colunas
    col1, col2, col3 = st.columns([2, 4, 2])
    
    with col1:
        # Calendário
        st.markdown('<div class="section-header">Calendário</div>', unsafe_allow_html=True)
        data_atual = datetime.now()
        st.date_input("Data:", value=data_atual.date(), key="date_picker")
        
        # Notas/Tarefas
        st.markdown('<div class="section-header">Notas/Tarefas do Dia</div>', unsafe_allow_html=True)
        st.text_area("", height=100, placeholder="Adicionar nota...", key="notes")
        
        # Mensagens internas
        st.markdown('<div class="section-header">Mensagens Internas</div>', unsafe_allow_html=True)
        st.selectbox("", ["Selecionar..."], key="messages")
    
    with col2:
        # Botão principal para abrir consulta
        st.markdown('<div class="button-container">', unsafe_allow_html=True)
        if st.button("📋 Nova Consulta", key="new_consultation", type="primary"):
            st.session_state.current_screen = 'consulta'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Lista de consultas
        st.markdown('<div class="section-header">Consultas do Dia - 05.07.2018</div>', unsafe_allow_html=True)
        
        # Header da tabela
        header_cols = st.columns([1, 1, 3, 2, 2])
        with header_cols[0]:
            st.write("**Hora**")
        with header_cols[1]:
            st.write("**Estado**")
        with header_cols[2]:
            st.write("**Nome do Utente**")
        with header_cols[3]:
            st.write("**Tipo**")
        with header_cols[4]:
            st.write("**Observações**")
        
        st.divider()
        
        # Lista de consultas
        for i, consulta in enumerate(consultas_data):
            cols = st.columns([1, 1, 3, 2, 2])
            
            # Destacar consulta "Em Espera"
            css_class = "consultation-selected" if consulta["estado"] == "Em Espera" else "consultation-row"
            
            with cols[0]:
                st.write(consulta["hora"])
            with cols[1]:
                if consulta["estado"] == "Em Espera":
                    st.markdown(f"🔵 **{consulta['estado']}**")
                else:
                    st.write(consulta["estado"])
            with cols[2]:
                if st.button(consulta["nome"], key=f"patient_{i}"):
                    st.session_state.selected_patient = consulta
                    st.session_state.current_screen = 'consulta'
                    st.rerun()
            with cols[3]:
                st.write(consulta["tipo"])
            with cols[4]:
                st.write(consulta["obs"])
            
            if i < len(consultas_data) - 1:
                st.markdown("<hr style='margin: 5px 0; border: 0.5px solid #ddd;'>", unsafe_allow_html=True)
    
    with col3:
        # Médico e informações
        st.markdown('<div class="section-header">Médico</div>', unsafe_allow_html=True)
        st.write("**Dr(a) Bessa Cardoso**")
        st.write("UCSP Breiner Porto")
        
        # Últimas consultas
        st.markdown('<div class="section-header">Últimas Consultas</div>', unsafe_allow_html=True)
        ultimas_consultas = [
            "02/07/2018 - Consulta de Enfermagem",
            "02/07/2018 - Consulta",
            "02/07/2018 - Consulta"
        ]
        for consulta in ultimas_consultas:
            st.write(f"• {consulta}")

def show_consultation_screen():
    """Mostra o ecrã de consulta (SOAP)"""
    
    # Header
    patient_name = st.session_state.selected_patient["nome"] if st.session_state.selected_patient else "Paciente Selecionado"
    st.markdown(f'<div class="main-header"><h2>Registo Clínico da Consulta - {patient_name}</h2></div>', unsafe_allow_html=True)
    
    # Botões de ação
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 2])
    
    with col1:
        if st.button("💾 Guardar", type="primary"):
            st.success("Consulta guardada com sucesso!")
    
    with col2:
        if st.button("🖨️ Imprimir"):
            st.info("Função de impressão ativada")
    
    with col3:
        if st.button("📧 Enviar"):
            st.info("Documento enviado")
    
    with col4:
        if st.button("📁 Arquivo"):
            st.info("Documento arquivado")
    
    with col5:
        if st.button("🚪 Sair", key="exit_consultation"):
            st.session_state.current_screen = 'agenda'
            st.session_state.selected_patient = None
            st.rerun()
    
    st.divider()
    
    # Seções SOAP
    soap_sections = [
        ("S", "Subjetivo", "Queixas do paciente, história clínica..."),
        ("O", "Objetivo", "Sinais vitais, exame físico, resultados de exames..."),
        ("A", "Avaliação", "Diagnóstico, impressão clínica..."),
        ("P", "Plano", "Tratamento, medicação, seguimento...")
    ]
    
    for letter, title, placeholder in soap_sections:
        st.markdown(f'<div class="soap-section">', unsafe_allow_html=True)
        st.markdown(f'<div class="soap-header">{letter}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="soap-content">', unsafe_allow_html=True)
        st.text_area(
            f"**{title}**",
            height=150,
            placeholder=placeholder,
            key=f"soap_{letter.lower()}",
            label_visibility="visible"
        )
        st.markdown('</div></div>', unsafe_allow_html=True)
    
    # Informações adicionais
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Informações do Paciente:**")
        if st.session_state.selected_patient:
            st.write(f"• **Nome:** {st.session_state.selected_patient['nome']}")
            st.write(f"• **Hora da consulta:** {st.session_state.selected_patient['hora']}")
            st.write(f"• **Tipo:** {st.session_state.selected_patient['tipo']}")
    
    with col2:
        st.markdown("**Ações rápidas:**")
        if st.button("📋 Receitar medicação"):
            st.info("Módulo de prescrição aberto")
        if st.button("📊 Ver histórico"):
            st.info("Histórico clínico carregado")
        if st.button("📅 Agendar retorno"):
            st.info("Agendamento iniciado")

# Controle principal da aplicação
def main():
    if st.session_state.current_screen == 'agenda':
        show_agenda_screen()
    elif st.session_state.current_screen == 'consulta':
        show_consultation_screen()

if __name__ == "__main__":
    main()
