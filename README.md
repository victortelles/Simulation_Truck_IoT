# Camión Seguro IoT - Simulación con Streamlit

Este proyecto simula los sensores IoT de un camión utilizando Python y Streamlit para visualizar los datos en tiempo real.

## Características

- **Selección de Tipo de Camión:** Elige entre diferentes tipos de camiones (Camioneta 3.5t, Rabón, Torton, Tráiler Sencillo) con capacidades de peso y combustible variables.
- **Simulación de Sensores:**
    - **GPS:** Sigue una ruta predefinida con coordenadas Latitud/Longitud.
    - **Puerta:** Estado ON (abierta) / OFF (cerrada) con probabilidad configurable de apertura durante la ruta.
    - **Botón de Pánico:** Estado ON / OFF con probabilidad configurable de activación. Genera una alerta con la última ubicación conocida.
    - **Pesaje:** Simula la carga del camión y detecta posibles sobrepesos según la capacidad del camión seleccionado.
    - **Combustible:** Muestra el nivel de combustible en porcentaje y simula el consumo durante el recorrido.
- **Panel de Control Interactivo:** Configura las probabilidades de eventos (puerta, pánico, sobrepeso).
- **Dashboard en Tiempo Real:**
    - Visualización del mapa con la ubicación actual del camión.
    - Gráficos tipo "gauge" o barras de progreso para el nivel de combustible y el peso del contenedor.
    - Barra de progreso general de la ruta.
    - Historial de alertas (Puerta abierta, Pánico, Sobrepeso, Combustible bajo).
- **Flujo de Simulación:** Carga -> Recorrido GPS (con eventos) -> Descarga.

## Requisitos

- Python 3.8 o superior
- pip (Administrador de paquetes de Python)

## Instalación

1.  **Clona el repositorio (si aplica):**
    ```bash
    git clone https://github.com/victortelles/Simulation_Truck_IoT.git
    cd camion-seguro-iot
    ```

2.  **Crea un entorno virtual (recomendado):**
    ```bash
    python -m venv venv
    ```
    *   En Windows: `venv\Scripts\activate`
    *   En macOS/Linux: `source venv/bin/activate`

3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

## Ejecución

1.  Asegúrate de que tu entorno virtual esté activado.
2.  Navega hasta el directorio raíz del proyecto (`Camion-IoT`).
3.  Ejecuta la aplicación Streamlit:
    ```bash
    streamlit run app.py
    ```
4.  Abre tu navegador web y ve a la dirección local que indica Streamlit (generalmente `http://localhost:8501`).

## Uso

1.  Utiliza la barra lateral para seleccionar el **Tipo de Camión** y la **Ruta GPS**.
2.  Ajusta las **Probabilidades de Eventos** (Puerta Abierta, Botón de Pánico, Sobrepeso) usando los sliders.
3.  Haz clic en el botón **▶️ Iniciar Simulación**.
4.  Observa el dashboard: el mapa se actualizará con la ubicación, los gráficos mostrarán el estado de los sensores y el historial de alertas registrará los eventos importantes.
5.  Puedes detener la simulación en cualquier momento con el botón **⏹️ Detener Simulación**.
6.  Una vez que el camión completa la ruta, la simulación finalizará automáticamente después del proceso de descarga.
