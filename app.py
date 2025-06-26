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
    # Header azul do SClínico
    st.markdown("""
    <div style="background-color: #4472C4; color: white; padding: 5px 10px; margin: -1rem -2rem 0 -2rem; font-size: 14px; font-weight: bold;">
        📋 SClínico - Dr(a) Bessa Cardoso - Ucsp Bremer Porto
    </div>
    """, unsafe_allow_html=True)
    
    # Barra de ferramentas com botão SOAP
    st.markdown("""
    <div style="background-color: #E7E6E6; padding: 8px; margin: 0 -2rem; border-bottom: 1px solid #ccc;">
        <div style="display: flex; align-items: center; gap: 15px; font-size: 12px;">
            <span>Perfil: MÉDICO</span>
            <span>AGENDA</span>
            <span style="color: #0066CC;">▶ Consultas do Dia</span>
            <span>Consultas Urgentes</span>
            <span>Consultas Domiciliárias</span>
            <span style="margin-left: auto;">{}</span>
        </div>
    </div>
    """.format(datetime.now().strftime("%d/%m/%Y %H:%M")), unsafe_allow_html=True)
    
    # Botão SOAP no topo
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 8, 1])
    with col1:
        soap_disabled = st.session_state.selected_consultation_id is None
        if st.button("📋 SOAP", disabled=soap_disabled, key="soap_btn_top", 
                    help="Abrir registo SOAP da consulta selecionada"):
            if st.session_state.selected_consultation_id is not None:
                st.session_state.current_screen = 'soap'
                st.rerun()
    
    # Layout principal em 2 colunas
    col_main, col_side = st.columns([8, 2])
    
    with col_main:
        # Lista de consultas principal
        st.markdown("""
        <div style="background-color: #F0F0F0; border: 1px solid #ccc; margin-bottom: 10px;">
            <div style="background-color: #4472C4; color: white; padding: 3px; font-size: 11px; font-weight: bold;">
                📅 Agenda - 07.07.2018 - Consultas do Dia
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Cabeçalho das consultas
        st.markdown("""
        <div style="display: flex; background-color: #E7E6E6; padding: 5px; border: 1px solid #ccc; font-size: 11px; font-weight: bold;">
            <div style="width: 60px;">H. Iníc</div>
            <div style="width: 60px;">H. Fim</div>
            <div style="width: 80px;">Estado</div>
            <div style="width: 120px;">Processo</div>
            <div style="flex: 1;">Nome do Utente</div>
            <div style="width: 80px;">Consultas</div>
            <div style="width: 40px;">Tipo</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Gerar consultas
        consultations = generate_consultations()
        
        # JavaScript para seleção e duplo clique
        st.markdown("""
        <script>
            function selectConsultation(id) {
                // Simular clique no botão correspondente
                const button = document.querySelector(`[data-testid="stButton"][title*="${id}"]`);
                if (button) {
                    button.click();
                }
            }
            
            function openSOAP(id) {
                // Primeiro selecionar a consulta
                selectConsultation(id);
                // Depois abrir SOAP (simular clique no botão SOAP)
                setTimeout(() => {
                    const soapButton = document.querySelector('[data-testid="stButton"] button[title*="SOAP"]');
                    if (soapButton && !soapButton.disabled) {
                        soapButton.click();
                    }
                }, 100);
            }
        </script>
        """, unsafe_allow_html=True)
        
        # Lista de consultas com clique direto
        for i, consultation in enumerate(consultations):
            is_selected = consultation['id'] == st.session_state.selected_consultation_id
            bg_color = "#B4D7FF" if is_selected else "#FFFFFF" if i % 2 == 0 else "#F8F8F8"
            
            # Consulta em destaque (tipo SClínico)
            if i == 7:  # Uma consulta em destaque
                bg_color = "#4472C4"
                text_color = "white"
            else:
                text_color = "black"
            
            st.markdown(f"""
            <div style="display: flex; background-color: {bg_color}; color: {text_color}; padding: 3px 5px; border: 1px solid #ccc; font-size: 10px; cursor: pointer;" 
                 onclick="selectConsultation('{consultation['id']}')" ondblclick="openSOAP('{consultation['id']}')">
                <div style="width: 60px;">{consultation['time']}</div>
                <div style="width: 60px;">{(datetime.strptime(consultation['time'], '%H:%M') + timedelta(minutes=30)).strftime('%H:%M')}</div>
                <div style="width: 80px;">{'Em Espera' if i == 7 else 'Livre'}</div>
                <div style="width: 120px;">{consultation['patient_number']}</div>
                <div style="flex: 1; font-weight: bold; cursor: pointer;" onclick="openSOAP('{consultation['id']}')" 
                     title="Clique para selecionar, duplo-clique para abrir SOAP">{consultation['patient']}</div>
                <div style="width: 80px;">S Adultos</div>
                <div style="width: 40px;">M</div>
            </div>
            """, unsafe_allow_html=True)
            
        # Botões invisíveis para seleção (necessários para o Streamlit)
        st.markdown('<div style="display: none;">', unsafe_allow_html=True)
        for consultation in consultations:
            if st.button(f"Select", key=f"sel_{consultation['id']}", 
                        help=f"Selecionar {consultation['patient']}", 
                        disabled=False):
                st.session_state.selected_consultation_id = consultation['id']
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Informações do médico
        st.markdown("""
        <div style="background-color: #F0F0F0; border: 1px solid #ccc; padding: 8px; margin-top: 10px;">
            <div style="display: flex; justify-content: space-between; font-size: 11px;">
                <div style="flex: 1;">
                    <strong>AGREGADO FAMILIAR:</strong><br>
                    <div style="background-color: white; border: 1px solid #ccc; padding: 3px; margin: 2px 0;">
                        <div>🔹 LISBOA</div>
                        <div>Andrea Ramalho Areias Baptista 26|21|05 1500</div>
                        <div>Ana Sousa Baptista Barreiros Graf 34|03|05 2000</div>
                        <div>Teresinha Marcellino Garcez Lisboa 44|21|05 2012</div>
                    </div>
                </div>
                <div style="flex: 1; margin-left: 20px;">
                    <strong>CONSULTAS AGENDADAS:</strong><br>
                    <div style="background-color: white; border: 1px solid #ccc; padding: 3px; margin: 2px 0; min-height: 80px;">
                        <div style="font-size: 10px;">
                            <div>📅 Próximas consultas:</div>
                            <div>02/07/2018 - Consulta de Enfermagem - Lucinda</div>
                            <div>02/07/2018 - Consulta de Enfermagem - Lucinda</div>
                            <div>02/07/2018 - Consulta de Enfermagem - Lucinda</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_side:
        # Últimas consultas
        st.markdown("""
        <div style="background-color: #F0F0F0; border: 1px solid #ccc; padding: 10px;">
            <div style="background-color: #4472C4; color: white; padding: 3px; font-size: 11px; font-weight: bold;">
                ÚLTIMAS CONSULTAS
            </div>
            <div style="padding: 5px; font-size: 10px;">
                <div style="background-color: white; border: 1px solid #ccc; padding: 3px; margin: 2px 0;">
                    <div style="font-weight: bold;">Horário - Previsões</div>
                    <div>Todos os Períodos</div>
                </div>
                <div style="background-color: white; border: 1px solid #ccc; padding: 3px; margin: 2px 0; min-height: 400px;">
                    <div>Consultas:</div>
                    <div>S Adultos - M</div>
                    <div>S Adultos - M</div>
                    <div>S Adultos - M</div>
                    <div>S Adultos - M</div>
                    <div>S Adultos - M</div>
                    <div>S Adultos - M</div>
                    <div>S Adultos - M</div>
                    <div>S Adultos - M</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

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
