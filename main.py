from fastapi import FastAPI, HTTPException, status, Header
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import os
import json
from generate_prompt import generate_prompt

app = FastAPI()

# Enable CORS
origins = [
    "http://localhost:5173",
    "https://journai.anshg.co"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure the API key for the generative model
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# Backend API key
API_KEY = os.environ.get("API_KEY")

# Access Key to stop Gemini Abuse
ACCESS_KEY = os.environ.get("ACCESS_KEY")

@app.post("/api/newtrip")
async def create_new_trip(trip_data: dict, authorization: str = Header(None)):

    # Check if the authorization header is provided and starts with 'Bearer '
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid or missing Authorization header")

    # Extract the API key from the 'Bearer ' token
    api_key = authorization[len("Bearer "):]

    # Check if the API key matches the backend API key
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key")

    # Parse the incoming JSON request
    prompt = generate_prompt(trip_data)

    # Generate content based on the prompt
    response = model.generate_content(prompt)
    response_text = response.text

    start_index = response_text.find('{')
    end_index = response_text.rfind('}')

    if start_index != -1 and end_index != -1 and start_index < end_index:
        json_str = response_text[start_index:end_index + 1]
        try:
            data = json.loads(json_str)
            return {"data": data}, status.HTTP_201_CREATED
        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=400, detail=f"Failed to parse JSON: {str(e)}")
    else:
        raise HTTPException(
            status_code=400, detail="No valid JSON found in the response")
