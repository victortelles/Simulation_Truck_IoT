import datetime
import random
from config.settings import TRUCK_TYPES, GPS_ROUTES
from utils.helpers import generate_random_value, calculate_percentage

class Truck:
    """Representa el estado y las propiedades de un camión."""

    def __init__(self, truck_type, route_name):
        if truck_type not in TRUCK_TYPES:
            raise ValueError(f"Tipo de camión desconocido: {truck_type}")
        if route_name not in GPS_ROUTES:
            raise ValueError(f"Ruta desconocida: {route_name}")

        self.truck_type = truck_type
        self.config = TRUCK_TYPES[truck_type]
        self.route_name = route_name
        self.route = GPS_ROUTES[route_name]

        # Propiedades dinámicas
        self.max_weight_capacity = self.config["max_weight_capacity"]
        self.fuel_capacity = generate_random_value(
            self.config["min_fuel_capacity"], self.config["max_fuel_capacity"]
        )

        # Inicializar el combustible con un valor predeterminado del 88% de la capacidad total
        self.current_fuel = 0.88 * self.fuel_capacity

        # Estado actual (se inicializa al comenzar simulación)
        self.current_weight = 0.0
        self.door_open = False
        self.panic_button_on = False
        self.current_location_index = -1 # -1 indica antes de empezar la ruta
        self.alerts = []
        self.simulation_start_time = None
        self.simulation_end_time = None
        self.is_loading = False
        self.is_unloading = False
        self.is_en_route = False


    def start_loading(self):
        """Inicia el proceso de carga."""
        self.is_loading = True
        # Simula una carga inicial aleatoria (e.g., 70-95% de capacidad)
        self.current_weight = generate_random_value(0.7 * self.max_weight_capacity, 0.95 * self.max_weight_capacity)
        self.is_loading = False # Termina carga inmediatamente para este ejemplo
        # Llena el tanque al inicio con un valor aleatorio entre 20% y 90% de la capacidad
        self.current_fuel = generate_random_value(0.9 * self.fuel_capacity, 0.9 * self.fuel_capacity)
        self.add_alert("INFO", "Inicio de carga de contenedor.")
        self.add_alert("INFO", f"Contenedor cargado con {self.current_weight:.2f} toneladas.")
        self.add_alert("INFO", f"Tanque de combustible inicial: {self.current_fuel:.2f} L.")


    def start_route(self):
        """Inicia el recorrido del camión."""
        if self.current_weight <= 0:
            self.add_alert("ERROR", "No se puede iniciar la ruta, el camión está vacío.")
            return False
        self.simulation_start_time = datetime.datetime.now()
        self.current_location_index = 0
        self.is_en_route = True
        self.add_alert("INFO", f"Simulación iniciada. Ruta: {self.route_name}")
        return True

    def advance_route(self):
        """Avanza al siguiente punto en la ruta GPS."""
        if not self.is_en_route:
            return False # No está en ruta

        if self.current_location_index < len(self.route) - 1:
            self.current_location_index += 1
            return True # Avanzó
        else:
            self.finish_route()
            return False # Llegó al final

    def finish_route(self):
        """Marca la finalización de la ruta."""
        self.is_en_route = False
        self.simulation_end_time = datetime.datetime.now()
        self.add_alert("INFO", "Ruta completada.")
        self.start_unloading()

    def start_unloading(self):
        """Inicia el proceso de descarga."""
        self.is_unloading = True
        self.add_alert("INFO", "Inicio de descarga de contenedor.")
        # En una simulación real, esto podría tomar tiempo
        # Aquí simulamos descarga instantánea
        self.current_weight = 0.0
        self.is_unloading = False
        self.add_alert("INFO", "Descarga completada.")


    def consume_fuel(self, rate_percentage):
        """Consume una cantidad de combustible basada en un porcentaje."""
        if self.is_en_route:
            consumption = (rate_percentage / 100.0) * self.fuel_capacity
            self.current_fuel = max(0, self.current_fuel - consumption)

    def set_door_status(self, is_open):
        """Establece el estado de la puerta."""
        if self.door_open != is_open:
            self.door_open = is_open
            status = "abierta" if is_open else "cerrada"
            self.add_alert("ALERTA", f"Puerta {status}.", self.get_current_location())

    def trigger_panic_button(self):
        """Activa el botón de pánico."""
        self.panic_button_on = True # Se mantiene activo hasta reset manual? O solo evento? Asumimos evento.
        self.add_alert("PANICO", "¡Botón de pánico activado!", self.get_current_location())
        # Podríamos resetearlo aquí o dejarlo activo: self.panic_button_on = False

    def check_overweight(self):
        """Verifica si hay sobrepeso y añade alerta si es necesario."""
        # Esta verificación podría ocurrir al cargar o durante el viaje si algo cambia
        if self.current_weight > self.max_weight_capacity:
            overload = self.current_weight - self.max_weight_capacity
            self.add_alert("ADVERTENCIA", f"Sobrepeso detectado: {overload:.2f} toneladas por encima del límite.", self.get_current_location())
            return True
        return False

    def check_low_fuel(self, threshold_percentage):
        """Verifica si el nivel de combustible es bajo."""
        fuel_percentage = self.get_fuel_percentage()
        if self.is_en_route and fuel_percentage <= threshold_percentage:
            self.add_alert("ADVERTENCIA", f"Nivel bajo de combustible: {fuel_percentage:.1f}%", self.get_current_location())
            return True
        return False


    def add_alert(self, alert_type, message, location=None):
        """Añade una alerta al historial."""
        timestamp = datetime.datetime.now()
        log_entry = f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')} - [{alert_type}] {message}"
        if location:
            log_entry += f" en ({location[0]:.4f}, {location[1]:.4f})"
        self.alerts.append(log_entry)
        # Mantiene solo las últimas N alertas si es necesario
        # self.alerts = self.alerts[-100:]

    def get_current_location(self):
        """Obtiene las coordenadas GPS actuales."""
        if self.is_en_route and 0 <= self.current_location_index < len(self.route):
            return self.route[self.current_location_index]
        return None

    def get_fuel_percentage(self):
        """Obtiene el nivel de combustible como porcentaje."""
        return calculate_percentage(self.current_fuel, self.fuel_capacity)

    def get_weight_percentage(self):
        """Obtiene el peso actual como porcentaje de la capacidad máxima."""
        return calculate_percentage(self.current_weight, self.max_weight_capacity)

    def get_route_progress(self):
        """Obtiene el progreso de la ruta como porcentaje."""
        if not self.route or len(self.route) <= 1:
            return 0.0
        if not self.is_en_route and self.simulation_end_time: # Si terminó
            return 100.0
        if self.current_location_index < 0: # Si no ha empezado
            return 0.0
        # Progreso basado en el índice actual
        progress = (self.current_location_index / (len(self.route) - 1)) * 100.0
        return min(progress, 100.0) # Asegura que no pase de 100
