#!/usr/bin/env python3
"""
API Documentation Generator for IoT Sensor Server

This script generates comprehensive API documentation from the FastAPI application.
Run this script to get up-to-date API documentation.
"""

import json
import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

try:
    from backend.app.main import app
    from fastapi.openapi.utils import get_openapi
    
    def generate_api_docs():
        """Generate OpenAPI schema and print formatted documentation."""
        
        # Get the OpenAPI schema
        openapi_schema = get_openapi(
            title=app.title,
            version="1.0.0",
            description="IoT Sensor Management API",
            routes=app.routes,
        )
        
        print("=== IoT Sensor API Documentation ===\n")
        print(f"Title: {openapi_schema['info']['title']}")
        print(f"Version: {openapi_schema['info']['version']}")
        print(f"Description: {openapi_schema['info']['description']}")
        print(f"Base URL: http://localhost:8000")
        print("\n" + "="*50 + "\n")
        
        # Print all available endpoints
        print("AVAILABLE ENDPOINTS:\n")
        
        for path, methods in openapi_schema['paths'].items():
            print(f"Path: {path}")
            for method, details in methods.items():
                if method.upper() in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
                    print(f"  {method.upper()}: {details.get('summary', 'No description')}")
                    if 'parameters' in details:
                        print("    Parameters:")
                        for param in details['parameters']:
                            print(f"      - {param['name']} ({param['in']}): {param.get('description', 'No description')}")
                    if 'requestBody' in details:
                        print("    Request Body: Required")
                    if 'responses' in details:
                        print("    Responses:")
                        for status_code, response_info in details['responses'].items():
                            print(f"      - {status_code}: {response_info.get('description', 'No description')}")
            print()
        
        # Print data models
        print("DATA MODELS:\n")
        if 'components' in openapi_schema and 'schemas' in openapi_schema['components']:
            for model_name, model_info in openapi_schema['components']['schemas'].items():
                print(f"Model: {model_name}")
                if 'properties' in model_info:
                    for prop_name, prop_info in model_info['properties'].items():
                        prop_type = prop_info.get('type', 'unknown')
                        print(f"  - {prop_name}: {prop_type}")
                print()
        
        # Save full OpenAPI schema to file
        with open('openapi_schema.json', 'w') as f:
            json.dump(openapi_schema, f, indent=2)
        print("Full OpenAPI schema saved to: openapi_schema.json")
        
        return openapi_schema
    
    if __name__ == "__main__":
        try:
            schema = generate_api_docs()
            print("\n✅ API documentation generated successfully!")
            print("\nTo view interactive documentation:")
            print("1. Start the server: uvicorn app.main:app --reload")
            print("2. Visit: http://localhost:8000/docs (Swagger UI)")
            print("3. Or visit: http://localhost:8000/redoc (ReDoc)")
            
        except Exception as e:
            print(f"❌ Error generating API documentation: {e}")
            sys.exit(1)

except ImportError as e:
    print(f"❌ Error importing FastAPI app: {e}")
    print("Make sure you're running this script from the project root directory.")
    print("And that all dependencies are installed: pip install -r backend/requirements.txt")
    sys.exit(1)
