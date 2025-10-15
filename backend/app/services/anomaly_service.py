async def detect_anomaly(reading):
    """
    Placeholder anomaly detection logic.
    Replace with actual ML or statistical analysis later.
    """
    temp, hum = reading.temperature, reading.humidity
    anomalies = []

    if temp > 45:
        anomalies.append("temperature_spike")
    if hum < 20:
        anomalies.append("humidity_drop")

    return anomalies
