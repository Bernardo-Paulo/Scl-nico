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
    
    /* Botão do nome do paciente - mesmo estilo do texto */
    .patient-name-button button {
        background-color: transparent !important;
        border: none !important;
        color: black !important;
        font-size: 10px !important;
        font-weight: bold !important;
        padding: 3px !important;
        height: auto !important;
        text-align: left !important;
        width: 100% !important;
        border-radius: 0 !important;
        box-shadow: none !important;
    }
    
    .patient-name-button button:hover {
        background-color: #E8F4FD !important;
        color: black !important;
    }
    
    .patient-name-button button:focus {
        background-color: transparent !important;
        outline: none !important;
        box-shadow: none !important;
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
    
    /* Linha clicável */
    .clickable-row {
        cursor: pointer !important;
        transition: background-color 0.2s;
    }
    
    .clickable-row:hover {
        background-color: #E8F4FD !important;
    }
    
    /* Esconder botões de seleção */
    .hidden-buttons {
        position: absolute !important;
        left: -9999px !important;
        opacity: 0 !important;
        pointer-events: none !important;
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
if 'consultation_soap_data' not in st.session_state:
    st.session_state.consultation_soap_data = {}

# Gerar consultas (só uma vez)
def generate_consultations():
    if not st.session_state.consultations:
        consultations = []
        today = datetime.now()
        
        names = [
            "SILVA, JOÃO CARLOS", "SANTOS, MARIA JOSÉ", "FERREIRA, ANTÓNIO MANUEL", 
            "COSTA, ANA RITA", "PEREIRA, CARLOS ALBERTO", "RODRIGUES, ISABEL MARIA",
            "OLIVEIRA, MANUEL JOAQUIM"
        ]
        
        # Dados SOAP pré-preenchidos para os primeiros 5 utentes
        soap_examples = {
            0: {  # SILVA, JOÃO CARLOS
                'S': 'Paciente queixa-se de dor torácica há 2 dias, tipo pontada, que piora com esforço. Nega dispneia ou palpitações. Refere episódios anteriores similares.',
                'O': 'TA: 140/85 mmHg, FC: 78 bpm, FR: 16 irpm, Temp: 36.2°C. Auscultação cardíaca: sopro sistólico grau II/VI. Auscultação pulmonar normal. Abdómen mole, depressível.',
                'A': 'Dor torácica atípica. Suspeita de cardiopatia isquémica. Hipertensão arterial controlada.',
                'P': 'ECG + Analises (troponinas, colesterol). Referenciação para cardiologia. Manter anti-hipertensor. Reavaliação em 1 semana.'
            },
            1: {  # SANTOS, MARIA JOSÉ
                'S': 'Paciente refere cefaleia há 1 semana, tipo pressão, localizada na região occipital. Piora com stress e melhora com repouso. Nega náuseas ou alterações visuais.',
                'O': 'TA: 160/95 mmHg, FC: 82 bpm, temperatura: 36.1°C. Exame neurológico: sem alterações. Fundo de olho: sem papiledema. Pescoço: sem rigidez.',
                'A': 'Cefaleia tensional. Hipertensão arterial não controlada.',
                'P': 'Aumentar dose de anti-hipertensor. Paracetamol 1g se dor. Medição TA domiciliária. Retorno em 1 semana.'
            },
            2: {  # FERREIRA, ANTÓNIO MANUEL
                'S': 'Paciente diabético tipo 2, vem para consulta de rotina. Refere cumprimento da medicação. Nega sintomas de hipoglicemia. Dieta controlada.',
                'O': 'Peso: 78kg, IMC: 26.5. TA: 130/80 mmHg. Glicemia capilar: 145 mg/dl. Pés sem lesões. Pulsos periféricos presentes.',
                'A': 'Diabetes mellitus tipo 2 em controlo razoável. Ligeiro excesso de peso.',
                'P': 'Manter metformina 850mg 2x/dia. HbA1c + perfil lipídico. Consulta nutrição. Retorno em 3 meses.'
            },
            3: {  # COSTA, ANA RITA
                'S': 'Jovem de 28 anos com queixas de ansiedade e insónia há 3 semanas. Refere stress laboral aumentado. Nega sintomas depressivos. Sem antecedentes psiquiátricos.',
                'O': 'Estado geral: bom. TA: 115/70 mmHg, FC: 88 bpm. Orientada no tempo e espaço. Humor: ansioso. Discurso: coerente.',
                'A': 'Perturbação de ansiedade relacionada com stress. Insónia secundária.',
                'P': 'Técnicas de relaxamento. Higiene do sono. Valeriana 300mg ao deitar. Reavaliação em 2 semanas. Se não melhorar, considerar ansiolítico.'
            },
            4: {  # PEREIRA, CARLOS ALBERTO
                'S': 'Paciente de 45 anos com lombalgia há 5 dias após carregar peso. Dor tipo mecânica, sem irradiação. Melhora com repouso e anti-inflamatórios.',
                'O': 'Marcha: normal. Coluna lombar: contratura muscular paravertebral. Lasègue: negativo bilateral. Força e sensibilidade membros inferiores: normal.',
                'A': 'Lombalgia mecânica aguda. Contratura muscular paravertebral.',
                'P': 'Ibuprofeno 600mg 8/8h x 5 dias. Aplicação calor local. Evitar esforços. Fisioterapia se não melhorar. Retorno SOS.'
            }
        }
        
        for i in range(7):  # Reduzido para 7 utentes
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
            
            # Adicionar dados SOAP se existirem para esta consulta
            if i in soap_examples:
                st.session_state.consultation_soap_data[i] = soap_examples[i]
        
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
                📅 Agenda - {} - Consultas do Dia
            </div>
        </div>
        """.format(datetime.now().strftime("%d.%m.%Y")), unsafe_allow_html=True)
        
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
        
        # Lista de consultas com botões funcionais
        for i, consultation in enumerate(consultations):
            is_selected = consultation['id'] == st.session_state.selected_consultation_id
            bg_color = "#B4D7FF" if is_selected else "#FFFFFF" if i % 2 == 0 else "#F8F8F8"
            text_color = "black"
            status = "Livre"
            
            # Indicador se tem dados SOAP
            soap_indicator = "📋" if consultation['id'] in st.session_state.consultation_soap_data else ""
            
            # Criar colunas para a linha da consulta
            cols = st.columns([0.6, 0.6, 0.8, 1.2, 3, 0.8, 0.4, 0.5])
            
            with cols[0]:
                st.markdown(f'<div style="background-color: {bg_color}; color: {text_color}; padding: 3px; border: 1px solid #ccc; font-size: 10px; text-align: center;">{consultation["time"]}</div>', unsafe_allow_html=True)
            
            with cols[1]:
                end_time = (datetime.strptime(consultation['time'], '%H:%M') + timedelta(minutes=30)).strftime('%H:%M')
                st.markdown(f'<div style="background-color: {bg_color}; color: {text_color}; padding: 3px; border: 1px solid #ccc; font-size: 10px; text-align: center;">{end_time}</div>', unsafe_allow_html=True)
            
            with cols[2]:
                st.markdown(f'<div style="background-color: {bg_color}; color: {text_color}; padding: 3px; border: 1px solid #ccc; font-size: 10px; text-align: center;">{status}</div>', unsafe_allow_html=True)
            
            with cols[3]:
                st.markdown(f'<div style="background-color: {bg_color}; color: {text_color}; padding: 3px; border: 1px solid #ccc; font-size: 10px; text-align: center;">{consultation["patient_number"]}</div>', unsafe_allow_html=True)
            
            with cols[4]:
                # Container com estilo para o botão do nome
                st.markdown(f'<div style="background-color: {bg_color}; border: 1px solid #ccc; padding: 0; margin: 0;" class="patient-name-button">', unsafe_allow_html=True)
                # Botão clicável para o nome do paciente
                patient_button_key = f"patient_{consultation['id']}"
                if st.button(f"{soap_indicator} {consultation['patient']}", 
                           key=patient_button_key,
                           help="Clique para selecionar, duplo-clique para abrir SOAP",
                           use_container_width=True):
                    if st.session_state.selected_consultation_id == consultation['id']:
                        # Duplo clique simulado - se já estava selecionado, abre SOAP
                        st.session_state.current_screen = 'soap'
                        st.rerun()
                    else:
                        # Primeiro clique - seleciona
                        st.session_state.selected_consultation_id = consultation['id']
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            
            with cols[5]:
                st.markdown(f'<div style="background-color: {bg_color}; color: {text_color}; padding: 3px; border: 1px solid #ccc; font-size: 10px; text-align: center;">S Adultos</div>', unsafe_allow_html=True)
            
            with cols[6]:
                st.markdown(f'<div style="background-color: {bg_color}; color: {text_color}; padding: 3px; border: 1px solid #ccc; font-size: 10px; text-align: center;">M</div>', unsafe_allow_html=True)
            
            with cols[7]:
                # Botão SOAP individual
                soap_key = f"soap_{consultation['id']}"
                if st.button("📋", key=soap_key, help="Abrir SOAP", disabled=False):
                    st.session_state.selected_consultation_id = consultation['id']
                    st.session_state.current_screen = 'soap'
                    st.rerun()
        
        # Informações do médico
        st.markdown("""
        <div style="background-color: #F0F0F0; border: 1px solid #ccc; padding: 8px; margin-top: 10px;">
            <div style="display: flex; justify-content: space-between; font-size: 11px;">
                <div style="flex: 1;">
                    <strong>AGREGADO FAMILIAR:</strong><br>
                    <div style="background-color: white; border: 1px solid #ccc; padding: 3px; margin: 2px 0;">
                        <div>🔹 Família selecionada</div>
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
                            <div>02/07/2025 - Consulta de Enfermagem - Lucinda</div>
                            <div>15/07/2025 - Consulta Médica - Dr. Cardoso</div>
                            <div>20/07/2025 - Consulta de Enfermagem - Lucinda</div>
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
                    <div><strong>Consultas anteriores:</strong></div>
                    <div>📋 25/06 - SILVA, JOÃO - Cardiologia</div>
                    <div>📋 24/06 - FERREIRA, ANTÓNIO - Diabetes</div>
                    <div>📋 24/06 - RODRIGUES, ISABEL - Plan. Familiar</div>
                    <div>📋 23/06 - ALMEIDA, TERESA - Pneumonia</div>
                    <div>22/06 - SANTOS, MARIA - Rotina</div>
                    <div>22/06 - COSTA, ANA - Hipertensão</div>
                    <div>21/06 - PEREIRA, CARLOS - Check-up</div>
                    <div>21/06 - OLIVEIRA, MANUEL - Ortopedia</div>
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
    age = datetime.now().year - int(selected_consultation['birth_date'][:4])
    st.markdown(f"""
    <div class="patient-info-box">
        <strong>Utente:</strong> {selected_consultation['patient']} | 
        <strong>Nº:</strong> {selected_consultation['patient_number']} | 
        <strong>Data Nasc:</strong> {selected_consultation['birth_date']} ({age} anos) | 
        <strong>Hora:</strong> {selected_consultation['time']}
    </div>
    """, unsafe_allow_html=True)
    
    # Número de utente
    st.markdown("**Número de Utente:**")
    patient_number = st.text_input("", value=selected_consultation['patient_number'], key="patient_num")
    st.session_state.patient_number = patient_number
    
    # Carregar dados SOAP existentes se houver
    consultation_id = selected_consultation['id']
    if consultation_id in st.session_state.consultation_soap_data:
        saved_soap = st.session_state.consultation_soap_data[consultation_id]
    else:
        saved_soap = {'S': '', 'O': '', 'A': '', 'P': ''}
    
    # Registo SOAP
    st.markdown("**Registo SOAP:**")
    
    # Container para as caixas SOAP
    st.markdown('<div class="soap-container">', unsafe_allow_html=True)
    
    # S - Subjetivo
    st.markdown('<div class="soap-label">S - Subjetivo</div>', unsafe_allow_html=True)
    soap_s = st.text_area("", height=80, key="soap_s", 
                         value=saved_soap['S'],
                         placeholder="Sintomas e queixas do utente...")
    
    # O - Objetivo  
    st.markdown('<div class="soap-label">O - Objetivo</div>', unsafe_allow_html=True)
    soap_o = st.text_area("", height=80, key="soap_o", 
                         value=saved_soap['O'],
                         placeholder="Observações clínicas, exame físico...")
    
    # A - Avaliação
    st.markdown('<div class="soap-label">A - Avaliação</div>', unsafe_allow_html=True)
    soap_a = st.text_area("", height=80, key="soap_a", 
                         value=saved_soap['A'],
                         placeholder="Diagnóstico e avaliação clínica...")
    
    # P - Plano
    st.markdown('<div class="soap-label">P - Plano</div>', unsafe_allow_html=True)
    soap_p = st.text_area("", height=80, key="soap_p", 
                         value=saved_soap['P'],
                         placeholder="Plano terapêutico e seguimento...")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Atualizar dados da sessão
    st.session_state.soap_data = {
        'S': soap_s, 'O': soap_o, 'A': soap_a, 'P': soap_p
    }
    
    # Botões de ação
    st.markdown("---")
    col1, col2, col3, col4 = st.columns([1, 1, 1, 6])
    
    with col1:
        if st.button("Guardar", key="save_soap"):
            # Guardar dados SOAP para esta consulta
            st.session_state.consultation_soap_data[consultation_id] = {
                'S': soap_s, 'O': soap_o, 'A': soap_a, 'P': soap_p
            }
            st.success("✅ SOAP guardado!")
    
    with col2:
        if st.button("Imprimir", key="print_soap"):
            st.info("🖨️ Enviado para impressão")
            # Mostrar prévia
            with st.expander("📄 Prévia da impressão"):
                st.markdown(f"""
                **REGISTO SOAP - {selected_consultation['patient']}**
                
                **Data:** {now.strftime("%d/%m/%Y %H:%M")}  
                **Utente:** {selected_consultation['patient_number']}
                
                **S - Subjetivo:**  
                {soap_s or "Não preenchido"}
                
                **O - Objetivo:**  
                {soap_o or "Não preenchido"}
                
                **A - Avaliação:**  
                {soap_a or "Não preenchido"}
                
                **P - Plano:**  
                {soap_p or "Não preenchido"}
                """)
    
    with col3:
        if st.button("Exportar", key="export_soap"):
            # Dados para Power Automate
            export_data = {
                "utente_numero": st.session_state.patient_number,
                "utente_nome": selected_consultation['patient'],
                "utente_idade": age,
                "data_consulta": datetime.now().strftime("%Y-%m-%d"),
                "hora_consulta": selected_consultation['time'],
                "medico": "Dr(a) Bessa Cardoso",
                "unidade": "Ucsp Bremer Porto",
                "soap": {
                    "subjetivo": soap_s,
                    "objetivo": soap_o, 
                    "avaliacao": soap_a,
                    "plano": soap_p
                },
                "timestamp": now.isoformat()
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
