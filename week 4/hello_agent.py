def hello_agent(user_message):
    message = user_message.lower()

    if "hello" in message or "hi" in message:
        return "Hello! I am your Smart Government Services Support Agent."

    if "government" in message:
        return "I can help you with government services."

    return "Hello! How can I help you today?"


print("=== Hello Agent ===")
print("Type 'exit' to stop.")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Agent: Goodbye!")
        break

    response = hello_agent(user_input)
    print("Agent:", response)