from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from journaiapp.prompt import generate_prompt
import google.generativeai as genai
import os
import json

# Configure the API key for the generative model
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')


@api_view(['POST'])
def new_trip(request):
    if request.method == 'POST':
        # Parse the incoming JSON request
        trip_data = JSONParser().parse(request)
        prompt = generate_prompt(trip_data)

        # Generate content based on the prompt
        response = model.generate_content(prompt)
        response_text = response.text

        # Find the first and last occurrence of '{' and '}'
        start_index = response_text.find('{')
        end_index = response_text.rfind('}')

        if start_index != -1 and end_index != -1 and start_index < end_index:
            json_str = response_text[start_index:end_index + 1]
            try:
                # Parse the JSON string
                data = json.loads(json_str)
                return JsonResponse({"data": data}, status=status.HTTP_201_CREATED)
            except json.JSONDecodeError as e:
                # Return an error if JSON parsing fails
                return JsonResponse({"error": "Failed to parse JSON", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Return an error if no valid JSON is found
            return JsonResponse({"error": "No valid JSON found in the response"}, status=status.HTTP_400_BAD_REQUEST)
