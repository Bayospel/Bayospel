import os
from openai import OpenAI
from dotenv import load_dotenv

# This tells Python to look at the .env file you just made
load_dotenv()

# This pulls the key safely from the system environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_ai_response(user_input):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are Bayospel, a cybersecurity expert and loyal AI assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices.message.content
    except Exception as e:
        return f"Error: {e}"

