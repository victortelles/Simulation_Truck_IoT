import time
import datetime
import streamlit as st
from simulation.truck import Truck
from utils.helpers import check_probability
from config.settings import (
    FUEL_CONSUMPTION_RATE, SIMULATION_STEP_DELAY_SECONDS, LOW_FUEL_THRESHOLD,
    DOOR_OPEN_PAUSE_SECONDS
)
import random

class Simulator:
    """Orquesta la simulación del camión y sus sensores."""

    def __init__(self, truck_type, route_name, probabilities):
        self.truck = Truck(truck_type, route_name)
        self.probabilities = probabilities # Diccionario con probabilidades de eventos
        self.running = False
        self._stop_requested = False

    def start(self):
        """Inicia el ciclo de simulación."""
        if self.running:
            st.warning("La simulación ya está en curso.")
            return

        self.running = True
        self._stop_requested = False
        self.truck.alerts = [] # Limpia alertas anteriores
        self.truck.add_alert("INFO", "Iniciando simulación...")

        # Placeholder para UI, se actualizará en el bucle
        status_placeholder = st.empty()
        map_placeholder = st.empty()
        charts_placeholder = st.container() # Usar contenedor para agrupar gráficos
        alerts_placeholder = st.empty()

        try:
            # 1. Carga
            status_placeholder.info("🚚 Iniciando carga del contenedor...")
            time.sleep(1) # Simular tiempo de preparación
            self.start_loading()
            self.truck.check_overweight() # Verificar sobrepeso inicial

            # Actualizar UI después de la carga
            self._update_ui(status_placeholder, map_placeholder, charts_placeholder, alerts_placeholder)
            status_placeholder.success("✅ Carga completada. Iniciando ruta...")
            time.sleep(1)

            # 2. Iniciar Ruta
            if not self.truck.start_route():
                status_placeholder.error("❌ No se pudo iniciar la ruta.")
                self.running = False
                return

            # 3. Ciclo de Simulación (Recorrido GPS)
            while self.truck.is_en_route and not self._stop_requested:
                current_location = self.truck.get_current_location()
                status_placeholder.info(f"📍 En ruta... Ubicación actual: ({current_location[0]:.4f}, {current_location[1]:.4f})")

                # Simular eventos aleatorios
                self._simulate_events(current_location)

                # Consumir combustible
                self.truck.consume_fuel(FUEL_CONSUMPTION_RATE)
                self.truck.check_low_fuel(LOW_FUEL_THRESHOLD)

                # Actualizar UI
                self._update_ui(status_placeholder, map_placeholder, charts_placeholder, alerts_placeholder)

                # Pausa por puerta abierta
                if self.truck.door_open:
                    status_placeholder.warning(f"🚪 Puerta abierta detectada. Pausando {DOOR_OPEN_PAUSE_SECONDS} segundos...")
                    time.sleep(DOOR_OPEN_PAUSE_SECONDS)

                # Esperar antes del siguiente paso
                time.sleep(SIMULATION_STEP_DELAY_SECONDS)

                # Avanzar en la ruta
                if not self.truck.advance_route():
                    break # Termina el bucle si advance_route devuelve False (llegó al final o error)


            if self._stop_requested:
                self.truck.add_alert("INFO", "Simulación detenida por el usuario.")
                status_placeholder.warning("⏹️ Simulación detenida.")
            else:
                # 4. Descarga (si completó la ruta)
                status_placeholder.info("🏁 Ruta completada. Iniciando descarga...")
                time.sleep(1)
                self.start_unloading()
                status_placeholder.success("✅ Descarga completada. Simulación finalizada.")
                self._update_ui(status_placeholder, map_placeholder, charts_placeholder, alerts_placeholder) # Última actualización


        except Exception as e:
            st.error(f"Error durante la simulación: {e}")
            self.truck.add_alert("ERROR", f"Error inesperado: {e}")
        finally:
            self.running = False
            # Asegurar que la UI final refleje el estado
            self._update_ui(status_placeholder, map_placeholder, charts_placeholder, alerts_placeholder)
            # Si no fue detenido, marca como finalizado
            if not self._stop_requested and not self.truck.is_en_route:
                final_message = "✅ Simulación finalizada."
                if alerts_placeholder: # Asegurar que el placeholder existe
                    alerts_placeholder.success(final_message)
                else:
                    st.success(final_message)


    def stop(self):
        """Solicita detener la simulación."""
        self._stop_requested = True
        self.running = False # Marca como no corriendo inmediatamente
        self.truck.add_alert("INFO", "Simulación detenida por el usuario.")

    def resume(self):
        """Reanuda la simulación desde el punto donde se detuvo."""
        if self.running:
            st.warning("La simulación ya está en curso.")
            return

        if not self.truck.is_en_route:
            st.error("No se puede reanudar, la simulación ya ha finalizado.")
            return

        self._stop_requested = False
        self.running = True
        self.truck.add_alert("INFO", "Simulación reanudada.")

        # Reanuda el ciclo de simulación
        self.start()

    def _simulate_events(self, location):
        """Simula la ocurrencia de eventos aleatorios."""
        # Sensor de Puerta
        if check_probability(self.probabilities.get('door_open', 0)):
            self.truck.set_door_status(True)
        else:
            if self.truck.door_open:
                self.truck.set_door_status(False)

        # Botón de Pánico
        if check_probability(self.probabilities.get('panic_button', 0)):
            self.truck.trigger_panic_button()

        # Pérdida de peso
        weight_loss_percentage = random.uniform(0.1, 0.5)  # Simula pérdida de peso entre 0.1% y 0.5%
        self.truck.current_weight -= (weight_loss_percentage / 100) * self.truck.max_weight_capacity
        if self.truck.current_weight < 0:
            self.truck.current_weight = 0

        if self.truck.current_weight < 0.1 * self.truck.max_weight_capacity:
            self.truck.add_alert("ADVERTENCIA", "Pérdida de peso significativa detectada.")

    def _update_ui(self, status_placeholder, map_placeholder, charts_placeholder, alerts_placeholder):
        """Actualiza los componentes de la interfaz de Streamlit."""
        # Limpia placeholders antes de actualizar
        status_placeholder.empty()
        map_placeholder.empty()
        charts_placeholder.empty()
        alerts_placeholder.empty()

        # Mapa (usando st.map)
        current_location = self.truck.get_current_location()
        if current_location:
            import pandas as pd
            map_data = pd.DataFrame({'lat': [current_location[0]], 'lon': [current_location[1]]})
            map_placeholder.map(map_data, zoom=13)

        # Gráficos
        with charts_placeholder:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("⛽ Nivel de Combustible")
                fuel_percentage = self.truck.get_fuel_percentage()
                st.progress(int(fuel_percentage) / 100.0, text=f"{fuel_percentage:.1f}%")

            with col2:
                st.subheader("⚖️ Peso del Contenedor")
                weight_percentage = self.truck.get_weight_percentage()
                st.progress(min(weight_percentage / 100.0, 1.0), text=f"{self.truck.current_weight:.2f} / {self.truck.max_weight_capacity:.2f} Ton ({weight_percentage:.1f}%)")

        # Historial de Alertas
        with alerts_placeholder.container():
            st.subheader("🚨 Historial de Alertas")
            if self.truck.alerts:
                for alert in reversed(self.truck.alerts[-10:]):
                    if "[PANICO]" in alert:
                        st.error(alert)
                    elif "[ALERTA]" in alert or "[ADVERTENCIA]" in alert:
                        st.warning(alert)
                    else:
                        st.info(alert)
            else:
                st.info("No hay alertas por el momento.")

    def _simulate_loading_or_unloading(self, action, max_weight):
        """Simula la carga o descarga del camión con una barra de progreso."""
        progress = st.progress(0)
        for i in range(101):
            time.sleep(0.05)  # Ajusta el tiempo para visualizar mejor
            progress.progress(i, text=f"{action}... {i}% completado")
        if action == "Cargando":
            self.truck.current_weight = max_weight
        elif action == "Descargando":
            self.truck.current_weight = 0

    def start_loading(self):
        """Inicia el proceso de carga."""
        self._simulate_loading_or_unloading("Cargando", self.truck.max_weight_capacity)

    def start_unloading(self):
        """Inicia el proceso de descarga."""
        self._simulate_loading_or_unloading("Descargando", 0)
