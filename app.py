import streamlit as st
import pandas as pd
from datetime import datetime
import calendar

# Configuração da página
st.set_page_config(
    page_title="SClínico - Dr(a) Bessa Cardoso - UCSP Breiner Porto",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizado para replicar exatamente o SClínico
st.markdown("""
<style>
    /* Reset padrão do Streamlit */
    .main > div {
        padding: 0px;
    }
    
    /* Barra de título */
    .title-bar {
        background: linear-gradient(to bottom, #e8e8e8, #d0d0d0);
        border: 1px solid #999;
        padding: 3px 8px;
        font-size: 11px;
        font-family: "Segoe UI", Tahoma, Arial, sans-serif;
        color: #333;
        margin-bottom: 0px;
    }
    
    /* Barra de menu */
    .menu-bar {
        background: linear-gradient(to bottom, #f0f0f0, #e0e0e0);
        border: 1px solid #ccc;
        border-top: none;
        padding: 4px;
        font-size: 11px;
        font-family: "Segoe UI", Tahoma, Arial, sans-serif;
        margin-bottom: 2px;
    }
    
    /* Container principal */
    .main-container {
        background-color: #f0f0f0;
        border: 1px solid #999;
        font-family: "Segoe UI", Tahoma, Arial, sans-serif;
        font-size: 11px;
    }
    
    /* Painel esquerdo */
    .left-panel {
        background-color: #f8f8f8;
        border-right: 1px solid #ccc;
        padding: 8px;
        min-height: 600px;
    }
    
    /* Calendário */
    .calendar-section {
        background-color: white;
        border: 1px solid #ccc;
        margin-bottom: 10px;
        padding: 5px;
    }
    
    .calendar-header {
        background: linear-gradient(to bottom, #4a90e2, #357abd);
        color: white;
        text-align: center;
        padding: 3px;
        font-size: 11px;
        font-weight: bold;
        margin: -5px -5px 5px -5px;
    }
    
    .calendar-grid {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 1px;
        font-size: 10px;
    }
    
    .calendar-day {
        text-align: center;
        padding: 2px;
        cursor: pointer;
        background-color: white;
    }
    
    .calendar-day:hover {
        background-color: #e6f3ff;
    }
    
    .calendar-day.today {
        background-color: #4a90e2;
        color: white;
        font-weight: bold;
    }
    
    .calendar-day.selected {
        background-color: #357abd;
        color: white;
    }
    
    /* Seções */
    .section-title {
        background: linear-gradient(to bottom, #e0e0e0, #d0d0d0);
        border: 1px solid #999;
        padding: 2px 5px;
        font-size: 11px;
        font-weight: bold;
        margin: 8px 0 2px 0;
    }
    
    .section-content {
        background-color: white;
        border: 1px solid #ccc;
        border-top: none;
        padding: 5px;
        min-height: 80px;
    }
    
    /* Painel central - lista de consultas */
    .center-panel {
        background-color: white;
        padding: 0px;
    }
    
    .consultation-header {
        background: linear-gradient(to bottom, #4a90e2, #357abd);
        color: white;
        padding: 8px;
        font-size: 12px;
        font-weight: bold;
        border-bottom: 1px solid #ccc;
    }
    
    .consultation-controls {
        background-color: #f0f0f0;
        padding: 5px 8px;
        border-bottom: 1px solid #ccc;
        font-size: 11px;
    }
    
    .consultation-table {
        background-color: white;
    }
    
    .consultation-table-header {
        background: linear-gradient(to bottom, #e8e8e8, #d8d8d8);
        border-bottom: 1px solid #ccc;
        padding: 4px 8px;
        font-size: 11px;
        font-weight: bold;
        color: #333;
    }
    
    .consultation-row {
        border-bottom: 1px solid #e0e0e0;
        padding: 3px 8px;
        font-size: 11px;
        cursor: pointer;
        background-color: white;
    }
    
    .consultation-row:hover {
        background-color: #f0f8ff;
    }
    
    .consultation-row.selected {
        background-color: #4a90e2;
        color: white;
    }
    
    .consultation-row.waiting {
        background-color: #ffffe0;
    }
    
    /* Painel direito */
    .right-panel {
        background-color: #f8f8f8;
        border-left: 1px solid #ccc;
        padding: 8px;
        min-height: 600px;
    }
    
    /* Seções do painel direito */
    .right-section {
        margin-bottom: 15px;
    }
    
    .right-section-title {
        background: linear-gradient(to bottom, #e0e0e0, #d0d0d0);
        border: 1px solid #999;
        padding: 2px 5px;
        font-size: 10px;
        font-weight: bold;
        margin-bottom: 2px;
    }
    
    .right-section-content {
        background-color: white;
        border: 1px solid #ccc;
        border-top: none;
        padding: 5px;
        font-size: 10px;
        min-height: 60px;
    }
    
    /* Botões */
    .sclinico-button {
        background: linear-gradient(to bottom, #f0f0f0, #e0e0e0);
        border: 1px solid #999;
        padding: 2px 8px;
        font-size: 11px;
        font-family: "Segoe UI", Tahoma, Arial, sans-serif;
        cursor: pointer;
        margin: 2px;
    }
    
    .sclinico-button:hover {
        background: linear-gradient(to bottom, #e0e0e0, #d0d0d0);
    }
    
    .sclinico-button:active {
        background: linear-gradient(to bottom, #d0d0d0, #e0e0e0);
    }
    
    /* SOAP Interface */
    .soap-container {
        background-color: #f0f0f0;
        padding: 0px;
        font-family: "Segoe UI", Tahoma, Arial, sans-serif;
    }
    
    .soap-header {
        background: linear-gradient(to bottom, #4a90e2, #357abd);
        color: white;
        padding: 8px;
        font-size: 12px;
        font-weight: bold;
    }
    
    .soap-toolbar {
        background-color: #f0f0f0;
        padding: 5px;
        border-bottom: 1px solid #ccc;
    }
    
    .soap-sections {
        display: flex;
        flex-direction: column;
        height: 500px;
    }
    
    .soap-section {
        flex: 1;
        display: flex;
        border-bottom: 1px solid #ccc;
    }
    
    .soap-section:last-child {
        border-bottom: none;
    }
    
    .soap-letter {
        background: linear-gradient(to bottom, #e0e0e0, #d0d0d0);
        border-right: 1px solid #ccc;
        width: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        font-weight: bold;
        color: #333;
    }
    
    .soap-content {
        flex: 1;
        background-color: white;
        padding: 0px;
    }
    
    /* Tabs do lado direito */
    .right-tabs {
        background-color: #f0f0f0;
        border: 1px solid #ccc;
        margin-bottom: 10px;
    }
    
    .tab-header {
        background: linear-gradient(to bottom, #e0e0e0, #d0d0d0);
        padding: 3px 8px;
        font-size: 10px;
        font-weight: bold;
        border-bottom: 1px solid #ccc;
    }
    
    .tab-content {
        background-color: white;
        padding: 5px;
        font-size: 10px;
        min-height: 100px;
    }
    
    /* Remover estilos do Streamlit */
    .stButton > button {
        background: linear-gradient(to bottom, #f0f0f0, #e0e0e0);
        border: 1px solid #999;
        padding: 2px 8px;
        font-size: 11px;
        font-family: "Segoe UI", Tahoma, Arial, sans-serif;
        color: #333;
        border-radius: 0px;
        height: auto;
    }
    
    .stButton > button:hover {
        background: linear-gradient(to bottom, #e0e0e0, #d0d0d0);
        border: 1px solid #999;
        color: #333;
    }
    
    .stTextArea > div > div > textarea {
        background-color: white;
        border: 1px solid #ccc;
        font-family: "Segoe UI", Tahoma, Arial, sans-serif;
        font-size: 11px;
        border-radius: 0px;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar estado da sessão
if 'current_screen' not in st.session_state:
    st.session_state.current_screen = 'agenda'
if 'selected_patient' not in st.session_state:
    st.session_state.selected_patient = None

# Dados das consultas (exatamente como no SClínico)
consultas_data = [
    {"hora": "09:00", "jul": "1", "ano": "2018", "estado": "Processado", "nome": "▼ Adultos", "consultas": "M", "info": "M", "elect": "", "agendado": ""},
    {"hora": "09:30", "jul": "2", "ano": "2018", "estado": "Processado", "nome": "▼ Adultos", "consultas": "M", "info": "M", "elect": "", "agendado": ""},
    {"hora": "10:15", "jul": "3", "ano": "2018", "estado": "Processado", "nome": "▼ Adultos", "consultas": "M", "info": "M", "elect": "", "agendado": ""},
    {"hora": "11:00", "jul": "4", "ano": "2018", "estado": "Processado", "nome": "▼ Adultos", "consultas": "M", "info": "M", "elect": "", "agendado": ""},
    {"hora": "11:30", "jul": "5", "ano": "2018", "estado": "Processado", "nome": "▼ Adultos", "consultas": "M", "info": "M", "elect": "", "agendado": ""},
    {"hora": "12:15", "jul": "6", "ano": "2018", "estado": "Processado", "nome": "▼ Adultos", "consultas": "M", "info": "M", "elect": "", "agendado": ""},
    {"hora": "12:54", "jul": "7", "ano": "2018", "estado": "Processado", "nome": "▼ Adultos", "consultas": "M", "info": "M", "elect": "", "agendado": ""},
    {"hora": "13:01", "jul": "8", "ano": "2018", "estado": "Em Espera", "nome": "José Cristina Santos Estácio", "consultas": "24 anos", "info": "▼ Adultos", "elect": "M", "agendado": ""},
    {"hora": "13:33", "jul": "9", "ano": "2018", "estado": "Processado", "nome": "▼ Adultos", "consultas": "M", "info": "M", "elect": "", "agendado": ""},
    {"hora": "14:12", "jul": "10", "ano": "2018", "estado": "Processado", "nome": "▼ Adultos", "consultas": "M", "info": "M", "elect": "", "agendado": ""},
    {"hora": "14:21", "jul": "11", "ano": "2018", "estado": "Processado", "nome": "▼ Adultos", "consultas": "M", "info": "M", "elect": "", "agendado": ""},
    {"hora": "15:30", "jul": "12", "ano": "2018", "estado": "Processado", "nome": "▼ Adultos", "consultas": "M", "info": "M", "elect": "", "agendado": ""},
    {"hora": "16:09", "jul": "13", "ano": "2018", "estado": "Processado", "nome": "▼ Adultos", "consultas": "M", "info": "M", "elect": "", "agendado": ""},
    {"hora": "17:27", "jul": "14", "ano": "2018", "estado": "Processado", "nome": "▼ Adultos", "consultas": "M", "info": "M", "elect": "", "agendado": ""},
    {"hora": "18:06", "jul": "15", "ano": "2018", "estado": "Processado", "nome": "▼ Adultos", "consultas": "M", "info": "M", "elect": "", "agendado": ""},
    {"hora": "18:45", "jul": "16", "ano": "2018", "estado": "Processado", "nome": "▼ Adultos", "consultas": "M", "info": "M", "elect": "", "agendado": ""},
    {"hora": "19:24", "jul": "17", "ano": "2018", "estado": "Processado", "nome": "▼ Adultos", "consultas": "M", "info": "M", "elect": "", "agendado": ""},
    {"hora": "20:02", "jul": "18", "ano": "2018", "estado": "Processado", "nome": "▼ Adultos", "consultas": "M", "info": "M", "elect": "", "agendado": ""}
]

def generate_calendar():
    """Gera o calendário de julho 2018"""
    cal = calendar.monthcalendar(2018, 7)
    
    calendar_html = """
    <div class="calendar-section">
        <div class="calendar-header">JUL 2018</div>
        <div class="calendar-grid">
            <div class="calendar-day" style="font-weight: bold;">S</div>
            <div class="calendar-day" style="font-weight: bold;">T</div>
            <div class="calendar-day" style="font-weight: bold;">Q</div>
            <div class="calendar-day" style="font-weight: bold;">Q</div>
            <div class="calendar-day" style="font-weight: bold;">S</div>
            <div class="calendar-day" style="font-weight: bold;">S</div>
            <div class="calendar-day" style="font-weight: bold;">D</div>
    """
    
    for week in cal:
        for day in week:
            if day == 0:
                calendar_html += '<div class="calendar-day"></div>'
            elif day == 5:  # 5 de julho (hoje)
                calendar_html += f'<div class="calendar-day today">{day}</div>'
            else:
                calendar_html += f'<div class="calendar-day">{day}</div>'
    
    calendar_html += """
        </div>
    </div>
    """
    return calendar_html

def show_agenda_screen():
    """Mostra o ecrã principal com a agenda exatamente como no SClínico"""
    
    # Barra de título
    st.markdown('<div class="title-bar">SClínico - Dr(a) Bessa Cardoso - UCSP Breiner Porto</div>', unsafe_allow_html=True)
    
    # Barra de menu
    st.markdown('<div class="menu-bar">Perfil MEDICO ▼ | AGENDA | ▶ Consultas do Dia | Consultas Urgentes | Consultas Domiciliares | Medidas LESCO CARDOSO ▼ | Horário - Períodos Todos os Períodos ▼</div>', unsafe_allow_html=True)
    
    # Container principal
    col1, col2, col3 = st.columns([2, 6, 2])
    
    with col1:
        st.markdown('<div class="left-panel">', unsafe_allow_html=True)
        
        # Calendário
        st.markdown(generate_calendar(), unsafe_allow_html=True)
        
        # Notas/Tarefas do dia
        st.markdown('<div class="section-title">NOTAS/TAREFAS DO DIA</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-content">Data: <br/>Assunto:</div>', unsafe_allow_html=True)
        
        # Nova Mensagem
        st.markdown('<div class="section-title">MENSAGENS INTERNAS</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-content">Nova Mensagem | [dropdown icon]</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="center-panel">', unsafe_allow_html=True)
        
        # Header das consultas
        st.markdown('<div class="consultation-header">▶ Consultas do Dia | Consultas Urgentes | Consultas Domiciliares</div>', unsafe_allow_html=True)
        
        # Controles
        st.markdown('<div class="consultation-controls">▶ Dia Escolhido | Executar | Medica | LESCO CARDOSO</div>', unsafe_allow_html=True)
        
        # Botão principal para nova consulta
        if st.button("📋 Nova Consulta / Registo Clínico", key="new_consultation", type="primary"):
            st.session_state.current_screen = 'consulta'
            st.rerun()
        
        st.markdown('<br>', unsafe_allow_html=True)
        
        # Cabeçalho da tabela
        header_html = """
        <div class="consultation-table">
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 3fr 1fr 1fr 1fr 1fr; background: linear-gradient(to bottom, #e8e8e8, #d8d8d8); border-bottom: 1px solid #ccc; padding: 4px 8px; font-size: 11px; font-weight: bold;">
                <div>Hora</div>
                <div>Jul</div>
                <div>Ano</div>
                <div>Estado</div>
                <div>Processos</div>
                <div>Nome do Utente</div>
                <div>Consulta</div>
                <div>Info</div>
            </div>
        """
        
        # Linhas de dados
        for i, consulta in enumerate(consultas_data):
            row_class = "consultation-row"
            if consulta["estado"] == "Em Espera":
                row_class += " waiting"
                
            onclick_script = f"""
            <div class="{row_class}" onclick="document.getElementById('patient_btn_{i}').click();">
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 3fr 1fr 1fr 1fr 1fr; padding: 3px 8px;">
                    <div>{consulta["hora"]}</div>
                    <div>{consulta["jul"]}</div>
                    <div>{consulta["ano"]}</div>
                    <div>{consulta["estado"]}</div>
                    <div></div>
                    <div>{consulta["nome"]}</div>
                    <div>{consulta["consultas"]}</div>
                    <div>{consulta["info"]}</div>
                </div>
            </div>
            """
            header_html += onclick_script
            
            # Botão invisível para capturar o clique
            if st.button("", key=f"patient_btn_{i}", help=f"Abrir consulta - {consulta['nome']}", 
                        label_visibility="hidden"):
                st.session_state.selected_patient = consulta
                st.session_state.current_screen = 'consulta'
                st.rerun()
        
        header_html += "</div>"
        st.markdown(header_html, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="right-panel">', unsafe_allow_html=True)
        
        # Agendado Familiar
        st.markdown('<div class="right-section-title">AGENDADO FAMILIAR</div>', unsafe_allow_html=True)
        st.markdown('<div class="right-section-content">45678</div>', unsafe_allow_html=True)
        
        # Consultas Agendadas
        st.markdown('<div class="right-section-title">CONSULTAS AGENDADAS</div>', unsafe_allow_html=True)
        st.markdown('<div class="right-section-content">Médico<br/>Andrea Remcho Areas Bazilio<br/>Teresita Alexandrina Garces Leitao</div>', unsafe_allow_html=True)
        
        # Últimas consultas
        st.markdown('<div class="right-section-title">ÚLTIMAS CONSULTAS</div>', unsafe_allow_html=True)
        st.markdown('<div class="right-section-content">Profissional<br/>02/07/2018 Consulta de Enfermagem Licinda<br/>02/07/2018 Consulta Licinda<br/>02/07/2018 Consulta Licinda</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def show_consultation_screen():
    """Mostra o ecrã de consulta SOAP exatamente como no SClínico"""
    
    patient_name = st.session_state.selected_patient["nome"] if st.session_state.selected_patient else "LESCO MARCELA ARAUJO CARDOSO"
    
    # Barra de título
    st.markdown(f'<div class="title-bar">Registo Clínico da Consulta - Dr(a) Bessa Cardoso - UCSP Breiner Porto</div>', unsafe_allow_html=True)
    
    # Header da consulta
    st.markdown(f'<div class="soap-header">Nome: {patient_name} | Utente: 52 anos | BI/Brasao: 11919855</div>', unsafe_allow_html=True)
    
    # Toolbar
    toolbar_html = """
    <div class="soap-toolbar">
        <span>Episódio corrente:</span>
    </div>
    """
    st.markdown(toolbar_html, unsafe_allow_html=True)
    
    # Layout principal
    main_col, right_col = st.columns([4, 1])
    
    with main_col:
        # Seções SOAP
        st.markdown('<div class="soap-sections">', unsafe_allow_html=True)
        
        # Seção S
        st.markdown('''
        <div class="soap-section">
            <div class="soap-letter">S</div>
            <div class="soap-content">
        ''', unsafe_allow_html=True)
        
        s_content = st.text_area("", height=120, key="soap_s", label_visibility="hidden", 
                                placeholder="Sintomas subjetivos, queixas do paciente...")
        
        st.markdown('</div></div>', unsafe_allow_html=True)
        
        # Seção O
        st.markdown('''
        <div class="soap-section">
            <div class="soap-letter">O</div>
            <div class="soap-content">
        ''', unsafe_allow_html=True)
        
        o_content = st.text_area("", height=120, key="soap_o", label_visibility="hidden",
                                placeholder="Observações objetivas, exame físico, sinais vitais...")
        
        st.markdown('</div></div>', unsafe_allow_html=True)
        
        # Seção A
        st.markdown('''
        <div class="soap-section">
            <div class="soap-letter">A</div>
            <div class="soap-content">
        ''', unsafe_allow_html=True)
        
        a_content = st.text_area("", height=120, key="soap_a", label_visibility="hidden",
                                placeholder="Avaliação, diagnóstico, impressão clínica...")
        
        st.markdown('</div></div>', unsafe_allow_html=True)
        
        # Seção P
        st.markdown('''
        <div class="soap-section">
            <div class="soap-letter">P</div>
            <div class="soap-content">
        ''', unsafe_allow_html=True)
        
        p_content = st.text_area("", height=120, key="soap_p", label_visibility="hidden",
                                placeholder="Plano terapêutico, medicação, seguimento...")
        
        st.markdown('</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with right_col:
        # Tabs do lado direito
        st.markdown('''
        <div class="right-tabs">
            <div class="tab-header">Alertas</div>
            <div class="tab-content"></div>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('''
        <div class="right-tabs">
            <div class="tab-header">Episódios activos</div>
            <div class="tab-content"></div>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('''
        <div class="right-tabs">
            <div class="tab-header">Consulta corrente</div>
            <div class="tab-content"></div>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('''
        <div class="right-tabs">
            <div class="tab-header">Todos os episódios</div>
            <div class="tab-content"></div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Botões de ação na parte inferior
    st.markdown("<br>", unsafe_allow_html=True)
    
    button_col1, button_col2, button_col3, button_col4, button_col5, button_col6 = st.columns(6)
    
    with button_col1:
        if st.button("💾 Guardar"):
            st.success("Registo guardado!")
    
    with button_col2:
        if st.button("🖨️ Imprimir"):
            st.info("Documento preparado para impressão")
    
    with button_col3:
        if st.button("📧 Enviar"):
            st.info("Documento enviado")
    
    with button_col4:
        if st.button("📁 Arquivo"):
            st.info("Documento arquivado")
    
    with button_col5:
        if st.button("🔄 Atualizar"):
            st.info("Interface atualizada")
    
    with button_col6:
        if st.button("❌ Sair"):
            st.session_state.current_screen = 'agenda'
            st.session_state.selected_patient = None
            st.rerun()

# Controle principal
def main():
    if st.session_state.current_screen == 'agenda':
        show_agenda_screen()
    elif st.session_state.current_screen == 'consulta':
        show_consultation_screen()

if __name__ == "__main__":
    main()
