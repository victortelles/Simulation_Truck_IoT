import time
import streamlit as st
from config.settings import TRUCK_TYPES, GPS_ROUTES, DEFAULT_DOOR_OPEN_PROBABILITY, DEFAULT_PANIC_BUTTON_PROBABILITY, DEFAULT_OVERWEIGHT_PROBABILITY
from simulation.simulator import Simulator

def configuration_panel():
    """Muestra el panel de configuración en la barra lateral."""
    st.sidebar.header("⚙️ Configuración de Simulación")

    # Selección de tipo de camión
    truck_type = st.sidebar.selectbox(
        "Seleccione el tipo de camión:",
        options=list(TRUCK_TYPES.keys()),
        key="config_truck_type" # Clave única para estado de sesión
    )

    # Mostrar capacidades basadas en el tipo de camión seleccionado
    if truck_type:
        config = TRUCK_TYPES[truck_type]
        st.sidebar.markdown(f"**Capacidad Máx:** {config['max_weight_capacity']} Toneladas")
        st.sidebar.markdown(f"**Tanque Combustible:** {config['min_fuel_capacity']} - {config['max_fuel_capacity']} L")

    # Selección de ruta GPS
    route_name = st.sidebar.selectbox(
        "Seleccione la ruta GPS:",
        options=list(GPS_ROUTES.keys()),
        key="config_route_name"
    )

    st.sidebar.subheader("Probabilidades de Eventos (%)")

    # Configuración de probabilidades
    door_prob = st.sidebar.slider(
        "🚪 Puerta Abierta",
        min_value=0,
        max_value=100,
        value=DEFAULT_DOOR_OPEN_PROBABILITY,
        step=1,
        key="config_door_prob"
    )

    panic_prob = st.sidebar.slider(
        "🆘 Botón de Pánico",
        min_value=0,
        max_value=100,
        value=DEFAULT_PANIC_BUTTON_PROBABILITY,
        step=1,
        key="config_panic_prob"
    )

    overweight_prob = st.sidebar.slider(
        "⚖️ Sobrepeso (al cargar)", # Aclarar cuándo aplica
        min_value=0,
        max_value=100,
        value=DEFAULT_OVERWEIGHT_PROBABILITY,
        step=1,
        key="config_overweight_prob"
    )


    return {
        "truck_type": truck_type,
        "route_name": route_name,
        "probabilities": {
            "door_open": door_prob,
            "panic_button": panic_prob,
            "overweight": overweight_prob,
        }
    }


def simulation_controls():
    """Muestra los botones de control de la simulación."""
    col1, col2 = st.columns(2)
    start_button_pressed = False
    stop_button_pressed = False

    # Validar de forma segura si la simulación está corriendo
    simulator = st.session_state.get("simulator", None)
    is_running = getattr(simulator, "running", False)

    with col1:
        if st.button("▶️ Iniciar Simulación", key="start_sim_button", disabled=is_running, use_container_width=True):
            start_button_pressed = True

    with col2:
        if st.button("⏹️ Detener Simulación", key="stop_sim_button", disabled=not is_running, use_container_width=True):
            stop_button_pressed = True

    return start_button_pressed, stop_button_pressed


def display_dashboard(simulator):
    """Muestra el dashboard principal con gráficos y alertas."""
    if not simulator:
        st.info("Configure y ejecute la simulación para ver el dashboard.")
        return

    st.header("📊 Dashboard en Tiempo Real")

    # Crear placeholders si no existen o si la simulación se reinicia
    if 'status_placeholder' not in st.session_state:
        st.session_state.status_placeholder = st.empty()
    if 'map_placeholder' not in st.session_state:
        st.session_state.map_placeholder = st.empty()
    if 'charts_placeholder' not in st.session_state:
        st.session_state.charts_placeholder = st.container()
    if 'alerts_placeholder' not in st.session_state:
        st.session_state.alerts_placeholder = st.empty()


    # Actualizar la UI con los datos actuales del simulador
    # La actualización real ocurre dentro del bucle del simulador,
    # aquí solo nos aseguramos de que los placeholders estén listos.
    # Si la simulación no está corriendo pero existe, muestra el último estado.
    if not simulator.running:
        simulator._update_ui(
            st.session_state.status_placeholder,
            st.session_state.map_placeholder,
            st.session_state.charts_placeholder,
            st.session_state.alerts_placeholder
        )
    # Si está corriendo, el bucle interno se encarga. No necesitamos llamar _update_ui aquí.


def main_layout():
    """Define la estructura principal de la aplicación Streamlit."""
    st.set_page_config(page_title="Camión Seguro IoT", layout="wide", page_icon="🚚")

    # --- Estilo CSS (Opcional) ---
    st.markdown("""
    <style>
        /* Ajustar colores - Ejemplo */
        /* .stApp { background-color: #F0F2F5; } */
        /* .stButton>button { background-color: #29ABE2; color: white; border-radius: 5px;} */
        /* .stButton>button:hover { background-color: #1F8CBF; } */
        /* .stSlider [data-baseweb="slider"] > div:nth-child(2) { background: #FFA500 !important; } */ /* Color del slider */
        /* .stProgress > div > div > div > div { background-color: #29ABE2; } */ /* Color barra progreso */
        /* .stAlert, .stWarning { border-radius: 5px; } */
        /* h1, h2, h3 { color: #4A5568; } */

        /* Estilo para el botón detener */
         /* Específico para la key del botón detener */
        /* button[data-testid="stButton"][kind="secondary"] { */
          /* background-color: #FFA500 !important; */ /* Naranja para detener */
          /* color: white !important; */
        /* } */
        /* button[data-testid="stButton"][kind="secondary"]:hover { */
          /* background-color: #E69500 !important; */
        /* } */

         /* Mejor selector para botones (puede necesitar ajuste basado en versiones de Streamlit) */
        div[data-testid="stHorizontalBlock"] > div:nth-child(1) button {
             background-color: #29ABE2; /* Azul para Iniciar */
            color: white;
            border-radius: 5px;
        }
        div[data-testid="stHorizontalBlock"] > div:nth-child(1) button:hover {
            background-color: #1F8CBF;
        }
        div[data-testid="stHorizontalBlock"] > div:nth-child(1) button:disabled {
            background-color: #cccccc;
            color: #666666;
        }


        div[data-testid="stHorizontalBlock"] > div:nth-child(2) button {
            background-color: #FFA500; /* Naranja para Detener */
            color: white;
            border-radius: 5px;
        }
        div[data-testid="stHorizontalBlock"] > div:nth-child(2) button:hover {
            background-color: #E69500;
        }
        div[data-testid="stHorizontalBlock"] > div:nth-child(2) button:disabled {
            background-color: #cccccc;
            color: #666666;
        }

         /* Centrar título */
         h1 { text-align: center; }

    </style>
    """, unsafe_allow_html=True)

    st.title("🚚 Simulación de Sensores IoT para Camiones Seguros")

    # --- Barra Lateral ---
    config = configuration_panel()

    st.divider() # Separador visual

    # --- Controles ---
    start_pressed, stop_pressed = simulation_controls()

    # --- Dashboard ---
    # Recuperar el simulador del estado de sesión si existe
    simulator = st.session_state.get('simulator', None)
    display_dashboard(simulator)

    # --- Lógica de Simulación ---
    # Inicializar el simulador si no existe en el estado de sesión
    if 'simulator' not in st.session_state:
        st.session_state.simulator = None

    # Manejar el botón de inicio
    if start_pressed:
        # Crear una nueva instancia del simulador con la configuración actual
        st.session_state.simulator = Simulator(
            config["truck_type"],
            config["route_name"],
            config["probabilities"]
        )
        # Limpiar placeholders viejos antes de empezar
        if 'status_placeholder' in st.session_state: st.session_state.status_placeholder.empty()
        if 'map_placeholder' in st.session_state: st.session_state.map_placeholder.empty()
        if 'charts_placeholder' in st.session_state: st.session_state.charts_placeholder.empty() # Contenedor no se limpia con empty()
        if 'alerts_placeholder' in st.session_state: st.session_state.alerts_placeholder.empty()
        # Iniciar la simulación (esto correrá en el hilo principal de Streamlit)
        st.session_state.simulator.start()
        # Forzar re-run para actualizar estado de botones después de que start() termine (o sea interrumpido)
        st.rerun()


    # Manejar el botón de detener
    if stop_pressed and st.session_state.simulator:
        print("Botón detener presionado, llamando a simulator.stop()") # Depuración
        # Detener la simulación
        st.session_state.simulator.stop()
        # Mostrar mensaje de información
        st.info("Deteniendo simulación...") # Mensaje inmediato
        time.sleep(0.5) # Pequeña pausa para que el mensaje se vea
        st.rerun() # Forzar re-run para actualizar el estado del botón detener
