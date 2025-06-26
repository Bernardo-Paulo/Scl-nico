import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

# Configuração da página
st.set_page_config(
    page_title="SClínico - Sistema de Gestão Clínica",
    page_icon="🏥",
    layout="wide"
)

# CSS personalizado para simular o aspeto do SClínico
st.markdown("""
<style>
    .main-header {
        background-color: #2E86AB;
        color: white;
        padding: 1rem;
        border-radius: 5px;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .consultation-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        background-color: #f8f9fa;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    
    .consultation-card:hover {
        background-color: #e9ecef;
    }
    
    .soap-section {
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 1rem;
        margin: 0.5rem 0;
        background-color: white;
    }
    
    .patient-info {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    
    .button-container {
        text-align: center;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar estado da sessão
if 'current_screen' not in st.session_state:
    st.session_state.current_screen = 'consultas'
if 'selected_consultation' not in st.session_state:
    st.session_state.selected_consultation = None
if 'patient_number' not in st.session_state:
    st.session_state.patient_number = ''
if 'soap_data' not in st.session_state:
    st.session_state.soap_data = {
        'S': '', 'O': '', 'A': '', 'P': ''
    }

# Dados simulados das consultas
def generate_consultations():
    """Gera consultas simuladas para o dia"""
    consultations = []
    today = datetime.now()
    
    # Nomes portugueses comuns
    names = [
        "João Silva", "Maria Santos", "António Ferreira", "Ana Costa",
        "Carlos Pereira", "Isabel Rodrigues", "Manuel Oliveira", "Teresa Almeida",
        "Francisco Martins", "Catarina Sousa", "José Carvalho", "Luísa Fernandes"
    ]
    
    # Especialidades médicas
    specialties = [
        "Medicina Geral e Familiar", "Cardiologia", "Pediatria", 
        "Ginecologia", "Ortopedia", "Dermatologia"
    ]
    
    for i in range(8):
        time_slot = (today.replace(hour=9, minute=0) + timedelta(minutes=30*i)).strftime("%H:%M")
        consultation = {
            'id': f'C{i+1:03d}',
            'time': time_slot,
            'patient': random.choice(names),
            'patient_number': f'{random.randint(100000000, 999999999)}',
            'specialty': random.choice(specialties),
            'doctor': f'Dr. {random.choice(["Silva", "Costa", "Ferreira", "Santos"])}',
            'status': random.choice(['Agendada', 'Em curso', 'Concluída'])
        }
        consultations.append(consultation)
    
    return consultations

def show_consultations_screen():
    """Mostra o ecrã das consultas do dia"""
    st.markdown('<div class="main-header"><h1>🏥 SClínico - Consultas do Dia</h1></div>', unsafe_allow_html=True)
    
    # Data atual
    today = datetime.now().strftime("%d/%m/%Y")
    st.markdown(f"### 📅 Consultas de {today}")
    
    # Gerar consultas
    consultations = generate_consultations()
    
    # Mostrar consultas em cards
    for consultation in consultations:
        col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
        
        with col1:
            st.write(f"**{consultation['time']}**")
            st.write(f"Paciente: {consultation['patient']}")
        
        with col2:
            st.write(f"Nº Utente: {consultation['patient_number']}")
            st.write(f"Especialidade: {consultation['specialty']}")
        
        with col3:
            st.write(f"Médico: {consultation['doctor']}")
            status_color = "🟢" if consultation['status'] == 'Concluída' else "🟡" if consultation['status'] == 'Em curso' else "🔴"
            st.write(f"Estado: {status_color} {consultation['status']}")
        
        with col4:
            if st.button(f"Abrir SOAP", key=f"btn_{consultation['id']}", type="primary"):
                st.session_state.selected_consultation = consultation
                st.session_state.current_screen = 'soap'
                st.rerun()
        
        st.divider()
    
    # Botão para Power Automate (simulação)
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    if st.button("🔄 Sincronizar com Power Automate", type="secondary"):
        st.success("Dados sincronizados com Power Automate!")
    st.markdown('</div>', unsafe_allow_html=True)

def show_soap_screen():
    """Mostra o ecrã do SOAP"""
    if st.session_state.selected_consultation is None:
        st.error("Nenhuma consulta selecionada!")
        return
    
    consultation = st.session_state.selected_consultation
    
    st.markdown('<div class="main-header"><h1>🏥 SClínico - Registo SOAP</h1></div>', unsafe_allow_html=True)
    
    # Botão Sair no topo
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← Sair", key="exit_soap", type="secondary"):
            st.session_state.current_screen = 'consultas'
            st.rerun()
    
    # Informações do paciente
    st.markdown('<div class="patient-info">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Paciente:** {consultation['patient']}")
        st.write(f"**Hora:** {consultation['time']}")
    with col2:
        st.write(f"**Médico:** {consultation['doctor']}")
        st.write(f"**Especialidade:** {consultation['specialty']}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 3º Passo: Guardar número de utente
    st.markdown("### 3º Passo: Número de Utente")
    patient_number = st.text_input(
        "Número de Utente:",
        value=consultation['patient_number'],
        key="patient_number_input"
    )
    st.session_state.patient_number = patient_number
    
    # 4º Passo: Dados SOAP
    st.markdown("### 4º Passo: Registo SOAP")
    
    # S - Subjetivo
    st.markdown('<div class="soap-section">', unsafe_allow_html=True)
    st.markdown("**S - Subjetivo (Sintomas relatados pelo paciente)**")
    soap_s = st.text_area(
        "Queixas do paciente, história da doença atual:",
        height=100,
        key="soap_s",
        placeholder="Ex: Paciente refere dor de cabeça há 3 dias, localizada na região temporal..."
    )
    st.session_state.soap_data['S'] = soap_s
    st.markdown('</div>', unsafe_allow_html=True)
    
    # O - Objetivo
    st.markdown('<div class="soap-section">', unsafe_allow_html=True)
    st.markdown("**O - Objetivo (Observações clínicas)**")
    soap_o = st.text_area(
        "Exame físico, sinais vitais, exames complementares:",
        height=100,
        key="soap_o",
        placeholder="Ex: TA: 120/80 mmHg, FC: 75 bpm, Temp: 36.5°C. Exame neurológico normal..."
    )
    st.session_state.soap_data['O'] = soap_o
    st.markdown('</div>', unsafe_allow_html=True)
    
    # A - Avaliação
    st.markdown('<div class="soap-section">', unsafe_allow_html=True)
    st.markdown("**A - Avaliação (Diagnóstico)**")
    soap_a = st.text_area(
        "Diagnóstico principal e diferenciais:",
        height=100,
        key="soap_a",
        placeholder="Ex: Cefaleia tensional. Excluir causas secundárias..."
    )
    st.session_state.soap_data['A'] = soap_a
    st.markdown('</div>', unsafe_allow_html=True)
    
    # P - Plano
    st.markdown('<div class="soap-section">', unsafe_allow_html=True)
    st.markdown("**P - Plano (Tratamento e seguimento)**")
    soap_p = st.text_area(
        "Tratamento, medicação, seguimento:",
        height=100,
        key="soap_p",
        placeholder="Ex: Paracetamol 1g 8/8h SOS. Reavaliação em 7 dias se persistir..."
    )
    st.session_state.soap_data['P'] = soap_p
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Botões de ação
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("💾 Guardar SOAP", type="primary"):
            st.success("Registo SOAP guardado com sucesso!")
            
    with col2:
        if st.button("📄 Gerar Relatório", type="secondary"):
            # Mostrar resumo dos dados guardados
            st.info("**Dados Guardados:**")
            st.write(f"**Nº Utente:** {st.session_state.patient_number}")
            for key, value in st.session_state.soap_data.items():
                if value:
                    st.write(f"**{key}:** {value[:100]}{'...' if len(value) > 100 else ''}")
    
    with col3:
        if st.button("🔄 Enviar Power Automate", type="secondary"):
            # Simular envio para Power Automate
            data_to_send = {
                "patient_number": st.session_state.patient_number,
                "consultation_time": consultation['time'],
                "soap_data": st.session_state.soap_data,
                "timestamp": datetime.now().isoformat()
            }
            st.success("Dados enviados para Power Automate!")
            st.json(data_to_send)

# Main App Logic
def main():
    # Sidebar com informações
    with st.sidebar:
        st.markdown("### 🏥 SClínico")
        st.markdown("**Sistema de Gestão Clínica**")
        st.markdown("---")
        st.markdown(f"**Utilizador:** Dr. Sistema")
        st.markdown(f"**Data:** {datetime.now().strftime('%d/%m/%Y')}")
        st.markdown(f"**Hora:** {datetime.now().strftime('%H:%M')}")
        st.markdown("---")
        
        # Informações da sessão atual
        if st.session_state.current_screen == 'soap' and st.session_state.selected_consultation:
            st.markdown("### 📋 Consulta Atual")
            consultation = st.session_state.selected_consultation
            st.write(f"**Paciente:** {consultation['patient']}")
            st.write(f"**Hora:** {consultation['time']}")
            st.write(f"**Nº Utente:** {consultation['patient_number']}")
    
    # Mostrar ecrã apropriado
    if st.session_state.current_screen == 'consultas':
        show_consultations_screen()
    elif st.session_state.current_screen == 'soap':
        show_soap_screen()

if __name__ == "__main__":
    main()
