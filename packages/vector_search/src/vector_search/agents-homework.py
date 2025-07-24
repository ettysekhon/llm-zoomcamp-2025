import random

from openai import OpenAI

from vector_search.chat_assistant import ChatAssistant, ChatInterface, Tools
from vector_search.settings import OPENAI_API_KEY

known_weather_data = {"berlin": 20.0}


def get_weather(city: str) -> float:
    city = city.strip().lower()
    if city in known_weather_data:
        return known_weather_data[city]
    return round(random.uniform(-5, 35), 1)


get_weather_tool = {
    "type": "function",
    "name": "get_weather",
    "description": "Get the weather for a given city",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "The city to get the weather for"}
        },
        "required": ["city"],
        "additionalProperties": False,
    },
}


def set_weather(city: str, temp: float) -> str:
    city = city.strip().lower()
    known_weather_data[city] = temp
    return "OK"


set_weather_tool = {
    "type": "function",
    "name": "set_weather",
    "description": "Set the weather for a given city",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "The city to set the weather for",
            },
            "temp": {
                "type": "number",
                "description": "The temperature to set for the city",
            },
        },
        "required": ["city", "temp"],
        "additionalProperties": False,
    },
}

if __name__ == "__main__":
    tools = Tools()
    tools.add_tool(get_weather, get_weather_tool)
    tools.add_tool(set_weather, set_weather_tool)

    client = OpenAI(api_key=OPENAI_API_KEY)

    developer_prompt = (
        "You are a helpful assistant that can answer user questions "
        "and, when appropriate, call the get_weather or set_weather functions."
    )

    chat_interface = ChatInterface()
    assistant = ChatAssistant(
        tools=tools,
        developer_prompt=developer_prompt,
        chat_interface=chat_interface,
        client=client,
    )

    assistant.run()
