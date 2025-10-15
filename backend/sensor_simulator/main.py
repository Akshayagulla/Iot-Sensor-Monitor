import asyncio
import importlib
import pkgutil
import httpx
from backend.sensor_simulator.base_sensor import BaseSensor

# --- Config ---
MAIN_SERVER_URL = "http://localhost:8000/api/v1/readings/ingest"
SEND_INTERVAL = 3
LOCATIONS = ["lab", "server-room", "storage-room"]
SENSORS_PER_LOCATION = 1

# --- Load sensor classes dynamically ---
def load_sensor_classes():
    import backend.sensor_simulator.sensors as sensors_pkg
    sensor_classes = []
    for _, name, _ in pkgutil.iter_modules(sensors_pkg.__path__):
        module = importlib.import_module(f"{sensors_pkg.__name__}.{name}")
        for attr in dir(module):
            cls = getattr(module, attr)
            if isinstance(cls, type) and issubclass(cls, BaseSensor) and cls is not BaseSensor:
                sensor_classes.append(cls)
    return sensor_classes

SENSOR_CLASSES = load_sensor_classes()
ALL_SENSORS = []

# --- Instantiate sensors ---
sensor_counter = 0
for sensor_cls in SENSOR_CLASSES:
    stype = sensor_cls.get_type()
    for loc in LOCATIONS:
        for i in range(SENSORS_PER_LOCATION):
            sensor_id = sensor_counter + 1
            name = f"{stype[:3]}{sensor_id:03d}"
            ALL_SENSORS.append(sensor_cls(sensor_id, name, loc))
            sensor_counter += 1

# --- Sensor sending task ---
async def send_readings(sensor: BaseSensor):
    async with httpx.AsyncClient() as client:
        while True:
            data = sensor.to_payload()
            try:
                response = await client.post(MAIN_SERVER_URL, json=data)
                if response.status_code != 200:
                    print(f"[{sensor.path}] → {response.status_code} :: {response.text} :: {data}")
                else:
                    print(f"[{sensor.path}] → {response.status_code} :: {data}")
            except Exception as e:
                print(f"[Error] {sensor.path}: {e}")
            await asyncio.sleep(SEND_INTERVAL)

# --- Main asyncio entry point ---
async def main():
    print(f"Starting simulator for {len(ALL_SENSORS)} sensors:")
    for s in ALL_SENSORS:
        print(" •", s.path)
    # Create all tasks
    tasks = [asyncio.create_task(send_readings(s)) for s in ALL_SENSORS]
    # await asyncio.gather(*tasks)
    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        print("Simulator stopped")


if __name__ == "__main__":
    asyncio.run(main())
