import numpy as np
import random

def generate_random_value(min_val, max_val):
    """Genera un valor flotante aleatorio dentro de un rango."""
    return random.uniform(min_val, max_val)

def check_probability(probability_percent):
    """Devuelve True con una probabilidad dada en porcentaje."""
    return random.random() < (probability_percent / 100.0)

def calculate_percentage(current_value, max_value):
    """Calcula el porcentaje de un valor actual respecto a un máximo."""
    if max_value == 0:
        return 0.0
    return (current_value / max_value) * 100.0

def format_alert(timestamp, alert_type, message, location=None):
    """Formatea un mensaje de alerta con información relevante."""
    log_entry = f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')} - [{alert_type}] {message}"
    if location:
        log_entry += f" en ({location[0]:.4f}, {location[1]:.4f})"
    return log_entry
