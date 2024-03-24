from openai import OpenAI

# Initialize OpenAI client with your API key
client = OpenAI(api_key='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') # Replace with your own API KEY

# Define the user input as a string variable
user_input = "Linux.RAT.Keylogger-lkm"

# Create chat completion request with dynamic user input
completion = client.chat.completions.create(
  model="gpt-4-0125-preview",
  messages=[
    {"role": "system", "content": "You are a cyber security specialist, when given the name of a malware you provide guidance on how the user might have caught it and what it could have caused, then offer advice on best practices for protecting against the malware."},
    {"role": "user", "content": user_input}  # Use the variable user_input here
  ]
)

# Print the generated response
print(completion.choices[0].message)
