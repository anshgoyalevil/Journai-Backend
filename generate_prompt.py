import json


def generate_prompt(trip_data):
    """Generates the prompt based on Trip Data"""

    prompt = "Design a trip itenary with the following details. If there are multiple destinations, design accordingly. Budget is in dollar:\n"

    string_trip_data = json.dumps(trip_data)

    prompt += string_trip_data

    post_prompt = "\nThe response must be in JSON format, with the following schema. Make sure there is no syntax error in that json. Only one day per itenerary object. For next days, use same destination title and I would club that day in \n"

    response_schema = {
        "trip": [
            {
                "destination": "string",
                "budget": "float",
                "duration": "int",
                "itinerary": {
                    "day": "int",
                    "activities": [{
                        "name": "string",
                        "cost": "float",
                        "duration": "int"
                    }]
                }
            }
        ]
    }

    post_prompt += json.dumps(response_schema)
    prompt += post_prompt

    return prompt
