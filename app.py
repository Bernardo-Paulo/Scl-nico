import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

# Configuração da página
st.set_page_config(
    page_title="SClínico",
    page_icon="🏥",
    layout="wide"
)

# CSS personalizado para imitar o SClínico
st.markdown("""
<style>
    /* Remover padding padrão do Streamlit */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    
    /* Header do SClínico */
    .sclinico-header {
        background-color: #4a90e2;
        color: white;
        padding: 0.5rem 1rem;
        margin: -1rem -2rem 1rem -2rem;
        font-size: 18px;
        font-weight: bold;
    }
    
    /* Botão SOAP no topo */
    .soap-button-container {
        text-align: left;
        margin: 1rem 0;
        padding: 0.5rem;
        background-color: #f0f0f0;
        border: 1px solid #ccc;
    }
    
    /* Tabela de consultas estilo SClínico */
    .consultation-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 12px;
        margin-top: 1rem;
    }
    
    .consultation-table th {
        background-color: #e6e6e6;
        border: 1px solid #999;
        padding: 4px 8px;
        text-align: left;
        font-weight: bold;
        font-size: 11px;
    }
    
    .consultation-table td {
        border: 1px solid #ccc;
        padding: 4px 8px;
        background-color: white;
        font-size: 11px;
    }
    
    .consultation-row {
        cursor: pointer;
    }
    
    .consultation-row:hover {
        background-color: #f0f8ff !important;
    }
    
    .consultation-row.selected {
        background-color: #d4edda !important;
    }
    
    .consultation-row.selected td {
        background-color: #d4edda !important;
    }
    
    /* Estilo SOAP */
    .soap-container {
        display: flex;
        flex-direction: column;
        gap: 0;
        margin-top: 1rem;
    }
    
    .soap-box {
        margin-bottom: 0;
        padding: 0;
    }
    
    .soap-label {
        background-color: #e6e6e6;
        border: 1px solid #999;
        padding: 4px 8px;
        font-weight: bold;
        font-size: 12px;
        margin: 0;
        text-align: left;
    }
    
    .soap-input {
        border: 1px solid #ccc;
        border-top: none;
        padding: 8px;
        min-height: 60px;
        font-size: 11px;
        font-family: Arial, sans-serif;
        resize: vertical;
        width: 100%;
        margin-bottom: 0;
    }
    
    /* Informações do utente */
    .patient-info-box {
        background-color: #f8f9fa;
        border: 1px solid #ccc;
        padding: 8px;
        margin-bottom: 1rem;
        font-size: 12px;
    }
    
    /* Botões estilo SClínico */
    .sclinico-button {
        background-color: #f0f0f0;
        border: 1px solid #999;
        padding: 4px 12px;
        font-size: 11px;
        cursor: pointer;
        margin-right: 5px;
    }
    
    .sclinico-button:hover {
        background-color: #e0e0e0;
    }
    
    .sclinico-button:disabled {
        background-color: #f8f8f8;
        color: #999;
        cursor: not-allowed;
    }
    
    /* Esconder elementos do Streamlit */
    .stButton button {
        background-color: #f0f0f0;
        border: 1px solid #999;
        color: black;
        font-size: 11px;
        padding: 4px 12px;
        height: auto;
    }
    
    .stTextArea textarea {
        font-size: 11px !important;
        font-family: Arial, sans-serif !important;
        border: 1px solid #ccc !important;
        padding: 8px !important;
        min-height: 60px !important;
    }
    
    .stTextInput input {
        font-size: 11px !important;
        border: 1px solid #ccc !important;
        padding: 4px 8px !important;
    }
    
    /* Remover labels do Streamlit */
    .stTextArea label, .stTextInput label {
        display: none !important;
    }
    
    /* Data e hora no canto */
    .date-info {
        position: absolute;
        top: 10px;
        right: 20px;
        font-size: 11px;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar estado da sessão
if 'current_screen' not in st.session_state:
    st.session_state.current_screen = 'consultas'
if 'selected_consultation_id' not in st.session_state:
    st.session_state.selected_consultation_id = None
if 'consultations' not in st.session_state:
    st.session_state.consultations = []
if 'patient_number' not in st.session_state:
    st.session_state.patient_number = ''
if 'soap_data' not in st.session_state:
    st.session_state.soap_data = {
        'S': '', 'O': '', 'A': '', 'P': ''
    }

# Gerar consultas (só uma vez)
def generate_consultations():
    if not st.session_state.consultations:
        consultations = []
        today = datetime.now()
        
        names = [
            "SILVA, JOÃO CARLOS", "SANTOS, MARIA JOSÉ", "FERREIRA, ANTÓNIO MANUEL", 
            "COSTA, ANA RITA", "PEREIRA, CARLOS ALBERTO", "RODRIGUES, ISABEL MARIA",
            "OLIVEIRA, MANUEL JOAQUIM", "ALMEIDA, TERESA CRISTINA", "MARTINS, FRANCISCO JOSÉ",
            "SOUSA, CATARINA ISABEL", "CARVALHO, JOSÉ ANTÓNIO", "FERNANDES, LUÍSA MARIA"
        ]
        
        for i in range(12):
            time_slot = (today.replace(hour=8, minute=30) + timedelta(minutes=30*i)).strftime("%H:%M")
            consultation = {
                'id': i,
                'time': time_slot,
                'patient': names[i] if i < len(names) else f"PACIENTE {i+1}",
                'patient_number': f'{random.randint(100000000, 999999999)}',
                'birth_date': f"{random.randint(1940, 2000)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
                'room': f"Gab. {random.randint(1, 6)}",
                'status': 'Agendada'
            }
            consultations.append(consultation)
        
        st.session_state.consultations = consultations
    
    return st.session_state.consultations

def show_consultations_screen():
    # Header
    st.markdown('<div class="sclinico-header">SClínico - Consultas do Dia</div>', unsafe_allow_html=True)
    
    # Data e hora
    now = datetime.now()
    st.markdown(f'<div class="date-info">{now.strftime("%d/%m/%Y %H:%M")}</div>', unsafe_allow_html=True)
    
    # Botão SOAP no topo
    st.markdown('<div class="soap-button-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 8, 1])
    with col1:
        soap_disabled = st.session_state.selected_consultation_id is None
        if st.button("SOAP", disabled=soap_disabled, key="soap_btn"):
            if st.session_state.selected_consultation_id is not None:
                st.session_state.current_screen = 'soap'
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Gerar consultas
    consultations = generate_consultations()
    
    # Tabela de consultas
    st.markdown("**Consultas Agendadas:**")
    
    # Criar tabela HTML
    table_html = """
    <table class="consultation-table">
        <thead>
            <tr>
                <th>Hora</th>
                <th>Nome do Utente</th>
                <th>Nº de Utente</th>
                <th>Data Nasc.</th>
                <th>Gabinete</th>
                <th>Estado</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for consultation in consultations:
        selected_class = "selected" if consultation['id'] == st.session_state.selected_consultation_id else ""
        table_html += f"""
            <tr class="consultation-row {selected_class}" onclick="selectConsultation({consultation['id']})">
                <td>{consultation['time']}</td>
                <td>{consultation['patient']}</td>
                <td>{consultation['patient_number']}</td>
                <td>{consultation['birth_date']}</td>
                <td>{consultation['room']}</td>
                <td>{consultation['status']}</td>
            </tr>
        """
    
    table_html += """
        </tbody>
    </table>
    
    <script>
        function selectConsultation(id) {
            // Usar o sistema de callback do Streamlit seria ideal aqui
            // Por agora, usaremos os botões individuais
        }
    </script>
    """
    
    st.markdown(table_html, unsafe_allow_html=True)
    
    # Botões invisíveis para seleção (workaround)
    st.markdown("**Selecionar consulta:**")
    cols = st.columns(6)
    for i, consultation in enumerate(consultations):
        with cols[i % 6]:
            if st.button(f"{consultation['time']}", key=f"select_{consultation['id']}", 
                        help=f"Selecionar {consultation['patient']}"):
                st.session_state.selected_consultation_id = consultation['id']
                st.rerun()

def show_soap_screen():
    # Header
    st.markdown('<div class="sclinico-header">SClínico - Registo SOAP</div>', unsafe_allow_html=True)
    
    # Data e hora
    now = datetime.now()
    st.markdown(f'<div class="date-info">{now.strftime("%d/%m/%Y %H:%M")}</div>', unsafe_allow_html=True)
    
    # Botão Sair
    col1, col2 = st.columns([1, 9])
    with col1:
        if st.button("Sair", key="exit_soap"):
            st.session_state.current_screen = 'consultas'
            st.rerun()
    
    # Encontrar consulta selecionada
    selected_consultation = None
    for consultation in st.session_state.consultations:
        if consultation['id'] == st.session_state.selected_consultation_id:
            selected_consultation = consultation
            break
    
    if selected_consultation is None:
        st.error("Consulta não encontrada!")
        return
    
    # Informações do utente
    st.markdown(f"""
    <div class="patient-info-box">
        <strong>Utente:</strong> {selected_consultation['patient']} | 
        <strong>Nº:</strong> {selected_consultation['patient_number']} | 
        <strong>Data Nasc:</strong> {selected_consultation['birth_date']} | 
        <strong>Hora:</strong> {selected_consultation['time']}
    </div>
    """, unsafe_allow_html=True)
    
    # 3º Passo: Número de utente
    st.markdown("**Número de Utente:**")
    patient_number = st.text_input("", value=selected_consultation['patient_number'], key="patient_num")
    st.session_state.patient_number = patient_number
    
    # 4º Passo: Caixas SOAP alinhadas à esquerda
    st.markdown("**Registo SOAP:**")
    
    # Container para as caixas SOAP
    st.markdown('<div class="soap-container">', unsafe_allow_html=True)
    
    # S - Subjetivo
    st.markdown('<div class="soap-label">S - Subjetivo</div>', unsafe_allow_html=True)
    soap_s = st.text_area("", height=80, key="soap_s", placeholder="Sintomas e queixas do utente...")
    st.session_state.soap_data['S'] = soap_s
    
    # O - Objetivo  
    st.markdown('<div class="soap-label">O - Objetivo</div>', unsafe_allow_html=True)
    soap_o = st.text_area("", height=80, key="soap_o", placeholder="Observações clínicas, exame físico...")
    st.session_state.soap_data['O'] = soap_o
    
    # A - Avaliação
    st.markdown('<div class="soap-label">A - Avaliação</div>', unsafe_allow_html=True)
    soap_a = st.text_area("", height=80, key="soap_a", placeholder="Diagnóstico e avaliação clínica...")
    st.session_state.soap_data['A'] = soap_a
    
    # P - Plano
    st.markdown('<div class="soap-label">P - Plano</div>', unsafe_allow_html=True)
    soap_p = st.text_area("", height=80, key="soap_p", placeholder="Plano terapêutico e seguimento...")
    st.session_state.soap_data['P'] = soap_p
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Botões de ação
    st.markdown("---")
    col1, col2, col3, col4 = st.columns([1, 1, 1, 6])
    
    with col1:
        if st.button("Guardar", key="save_soap"):
            st.success("✅ SOAP guardado!")
    
    with col2:
        if st.button("Imprimir", key="print_soap"):
            st.info("🖨️ Enviado para impressão")
    
    with col3:
        if st.button("Exportar", key="export_soap"):
            # Dados para Power Automate
            export_data = {
                "utente_numero": st.session_state.patient_number,
                "utente_nome": selected_consultation['patient'],
                "data_consulta": datetime.now().strftime("%Y-%m-%d"),
                "hora_consulta": selected_consultation['time'],
                "soap": {
                    "subjetivo": st.session_state.soap_data['S'],
                    "objetivo": st.session_state.soap_data['O'], 
                    "avaliacao": st.session_state.soap_data['A'],
                    "plano": st.session_state.soap_data['P']
                }
            }
            st.success("📤 Dados exportados para Power Automate!")
            with st.expander("Ver dados exportados"):
                st.json(export_data)

# Main App
def main():
    # Mostrar ecrã apropriado
    if st.session_state.current_screen == 'consultas':
        show_consultations_screen()
    elif st.session_state.current_screen == 'soap':
        show_soap_screen()

if __name__ == "__main__":
    main()
