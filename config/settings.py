# Configuraciones de los tipos de camiones
TRUCK_TYPES = {
    "Camioneta 3.5 toneladas": {
        "max_weight_capacity": 3.5,
        "min_fuel_capacity": 240, # Asumiendo un valor único si no hay rango
        "max_fuel_capacity": 240,
    },
    "Camión Rabón": {
        "max_weight_capacity": 9,
        "min_fuel_capacity": 150,
        "max_fuel_capacity": 300,
    },
    "Camión Torton": {
        "max_weight_capacity": 18,
        "min_fuel_capacity": 400,
        "max_fuel_capacity": 800,
    },
    "Tráiler Sencillo": {
        "max_weight_capacity": 30,
        "min_fuel_capacity": 500,
        "max_fuel_capacity": 900,
    }
}

# Rutas GPS predefinidas (Ejemplos)
# Cada ruta es una lista de tuplas (latitud, longitud)
GPS_ROUTES = {
    "Ruta 1: Sayula - Ciudad Guzmán": [
        (19.880306232537567, -103.5974233225158),
        (19.87974122224069, -103.58978439208178),
        (19.87998336975749, -103.5840337365865),
        (19.875866811647732, -103.57579399139924),
        (19.867552652578283, -103.55296303077623),
        (19.86351649582973, -103.54068924367438),
        (19.85786570381317, -103.52309395447243),
        (19.85358711290675, -103.51193596104223),
        (19.847935967232353, -103.50670028962115),
        (19.832676869038995, -103.49768806832259),
        (19.824683422406242, -103.4945981619888),
        (19.805142195373566, -103.48618675544348),
        (19.798439486071146, -103.48378349643052),
        (19.78543704006512, -103.47846199221523),
        (19.77388739373882, -103.47065140042315),
        (19.765164028406172, -103.45906425689333),
        (19.750058555517278, -103.45726181263362),
        (19.746504118752444, -103.45803428874493),
        (19.746746469228338, -103.46275497609179),
        (19.75223964797367, -103.46498657374667),
        (19.746718699919295, -103.47183961676143),
        (19.72054271856955, -103.48986405935854),
        (19.731449898772873, -103.49904794201517),
        (19.740902185932043, -103.50582856565885),
    ],
    "Ruta 2: Costa a Montaña": [
        (20.6534, -105.2253), # Puerto Vallarta (Inicio)
        (20.7000, -105.1500),
        (20.9180, -104.8944), # Tepic
        (21.1000, -104.5000),
        (21.5079, -104.8951), # Cerca de Sierra Madre Occidental
        (21.8854, -102.2916), # Aguascalientes (Fin)
    ],
    "Ruta 3: Ruta Corta Urbana": [
        (20.6736, -103.3440), # Guadalajara Centro
        (20.6750, -103.3500),
        (20.6700, -103.3600),
        (20.6650, -103.3700), # Zapopan Cercano
        (20.6600, -103.3800),
    ]
}

# Constantes de simulación
DEFAULT_DOOR_OPEN_PROBABILITY = 5 # %
DEFAULT_PANIC_BUTTON_PROBABILITY = 2 # %
DEFAULT_OVERWEIGHT_PROBABILITY = 10 # %
LOW_FUEL_THRESHOLD = 20 # %
FUEL_CONSUMPTION_RATE = 0.5 # % del tanque consumido por paso de GPS
SIMULATION_STEP_DELAY_SECONDS = 2 # Tiempo entre pasos de GPS
DOOR_OPEN_PAUSE_SECONDS = 5 # Tiempo extra si la puerta se abre
