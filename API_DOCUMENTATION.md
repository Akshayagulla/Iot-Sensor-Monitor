# IoT Sensor API Documentation

## Base URL
```
http://localhost:8000
```

## API Endpoints

### Sensors Management

#### Create a Sensor
**POST** `/api/sensors/`

Creates a new sensor in the system.

**Request Body:**
```json
{
  "name": "Temperature Sensor 1",
  "location": "Living Room",
  "sensor_type": "temperature"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "Temperature Sensor 1",
  "location": "Living Room",
  "sensor_type": "temperature"
}
```

**Status Codes:**
- `201 Created` - Sensor created successfully
- `422 Unprocessable Entity` - Validation error

---

#### List All Sensors
**GET** `/api/sensors/`

Retrieves a list of all sensors in the system.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Temperature Sensor 1",
    "location": "Living Room",
    "sensor_type": "temperature"
  },
  {
    "id": 2,
    "name": "Humidity Sensor 1",
    "location": "Bedroom",
    "sensor_type": "humidity"
  }
]
```

**Status Codes:**
- `200 OK` - Success

---

### Sensor Readings

#### Create a Reading
**POST** `/api/readings/`

Creates a new sensor reading.

**Request Body:**
```json
{
  "sensor_id": 1,
  "value": 23.5,
  "unit": "°C"
}
```

**Response:**
```json
1
```
*Returns the ID of the created reading*

**Status Codes:**
- `200 OK` - Reading created successfully
- `422 Unprocessable Entity` - Validation error

---

#### Get Readings for a Sensor
**GET** `/api/readings/sensor/{sensor_id}`

Retrieves all readings for a specific sensor.

**Path Parameters:**
- `sensor_id` (integer, required) - ID of the sensor (must be > 0)

**Response:**
```json
[
  {
    "sensor_id": 1,
    "value": 23.5,
    "unit": "°C"
  },
  {
    "sensor_id": 1,
    "value": 24.1,
    "unit": "°C"
  }
]
```

**Status Codes:**
- `200 OK` - Success
- `422 Unprocessable Entity` - Invalid sensor_id

---

### WebSocket Real-time Updates

#### WebSocket Connection
**WS** `/ws`

Establishes a WebSocket connection for real-time updates.

**Connection URL:**
```
ws://localhost:8000/ws
```

**Message Format:**
The server broadcasts messages when new readings are created:

```json
{
  "type": "reading.created",
  "data": {
    "id": 123,
    "sensorId": 1,
    "value": 23.5,
    "unit": "°C"
  }
}
```

---

## Data Models

### Sensor
```json
{
  "id": 1,
  "name": "string",
  "location": "string",
  "sensor_type": "temperature" | "humidity"
}
```

### Reading
```json
{
  "sensor_id": 1,
  "value": 23.5,
  "unit": "°C"
}
```

### Sensor Types
- `temperature` - Temperature sensors (unit: °C)
- `humidity` - Humidity sensors (unit: %)

---

## Error Responses

### Validation Error (422)
```json
{
  "detail": [
    {
      "loc": ["body", "name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### Not Found Error (404)
```json
{
  "detail": "Not Found"
}
```

---

## Usage Examples

### Python Client Example
```python
import httpx
import asyncio

async def create_sensor():
    async with httpx.AsyncClient() as client:
        # Create a temperature sensor
        response = await client.post(
            "http://localhost:8000/api/sensors/",
            json={
                "name": "Office Temperature",
                "location": "Office Room 101",
                "sensor_type": "temperature"
            }
        )
        sensor = response.json()
        print(f"Created sensor: {sensor}")
        
        # Create a reading
        reading_response = await client.post(
            "http://localhost:8000/api/readings/",
            json={
                "sensor_id": sensor["id"],
                "value": 22.5,
                "unit": "°C"
            }
        )
        reading_id = reading_response.json()
        print(f"Created reading: {reading_id}")

asyncio.run(create_sensor())
```

### JavaScript Client Example
```javascript
// Create a sensor
const sensorResponse = await fetch('http://localhost:8000/api/sensors/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    name: 'Living Room Temperature',
    location: 'Living Room',
    sensor_type: 'temperature'
  })
});

const sensor = await sensorResponse.json();

// Create a reading
const readingResponse = await fetch('http://localhost:8000/api/readings/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    sensor_id: sensor.id,
    value: 23.2,
    unit: '°C'
  })
});

const readingId = await readingResponse.json();
```

### WebSocket Client Example
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onmessage = function(event) {
  const message = JSON.parse(event.data);
  if (message.type === 'reading.created') {
    console.log('New reading:', message.data);
  }
};
```

---

## Sensor Simulator Integration

The sensor simulator sends data to the `/api/readings/` endpoint. Based on the current simulator configuration:

**Simulator Endpoint:** `http://localhost:8000/ingest`

**Note:** The simulator is currently configured to send to `/ingest` but the actual API endpoint is `/api/readings/`. You may need to update the simulator configuration to match the API.

---

## Running the Server

1. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```

2. Start the server:
   ```bash
   cd backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. Access the interactive API documentation:
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

---

## Environment Variables

The server can be configured using environment variables:

- `DATABASE_URL` - Database connection string
- `DEBUG` - Enable debug mode (true/false)
- `CORS_ALLOW_ORIGINS` - Comma-separated list of allowed CORS origins