# Install OpenAI SDK first: `pip3 install openai`
from openai import OpenAI

# Initialize the client with your custom API endpoint
client = OpenAI(
    api_key="sk-b34acc64df3049c78a5e8fc162e16d9b",  # Replace with your actual API key
    base_url="https://api.deepseek.com"  # Ensure this is the correct base URL
)

try:
    # Make the API call
    response = client.chat.completions.create(
        model="deepseek-chat",  # Ensure this model name is correct
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "Hello"},
        ],
        stream=False
    )
    # Print the response
    print(response.choices[0].message.content)
except Exception as e:
    print(f"An error occurred: {e}")