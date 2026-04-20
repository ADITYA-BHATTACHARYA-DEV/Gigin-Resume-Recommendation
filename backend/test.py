import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

try:
    print(f"Using Key: {os.getenv('GROQ_API_KEY')[:5]}...")
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant", # Using a smaller model for a faster test
        messages=[{"role": "user", "content": "Hello, are you there?"}]
    )
    print("✅ CONNECTION SUCCESSFUL!")
    print(f"Response: {completion.choices[0].message.content}")
except Exception as e:
    print(f"❌ CONNECTION FAILED: {e}")