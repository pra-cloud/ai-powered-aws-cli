import os
import openai
import subprocess
from pathlib import Path


# Load API key from environment variable
OPENAI_API_KEY = ""

openai.api_key = OPENAI_API_KEY

# Conversation memory
conversation_history = []

def get_ai_generated_cli_command(user_task, history):
    """Ask ChatGPT to generate the AWS CLI command based on user task and conversation history."""
    prompt = f"""
    You are an AWS expert and a casual assistant. Here's the conversation history: {history}
    The user just asked: "{user_task}"
    Respond naturally, and if it requires an AWS CLI command, generate that. Also, if any parameters are missing, ask for them.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["choices"][0]["message"]["content"].strip()

def extract_aws_cli_command(response):
    """Extracts the actual AWS CLI command from the AI's response."""
    if "aws" in response.lower():
        # Look for the first AWS CLI command in the response and return it
        lines = response.splitlines()
        for line in lines:
            if line.strip().lower().startswith("aws"):
                return line.strip()
    return None

def execute_aws_cli(command):
    """Executes the generated AWS CLI command."""
    print(f"\nExecuting: {command}\n")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        print("Success:", result.stdout)
    else:
        print("Error:", result.stderr)

def main():
    global conversation_history

    print("Hey there! I'm your AWS Assistant. How can I help today?")

    while True:
        # Step 1: Get user input
        user_task = input("\nEnter AWS task (or type 'exit' to quit): ").strip()

        if user_task.lower() == "exit":
            print("Goodbye! Have a great day!")
            break

        # Step 2: Add user input to history
        conversation_history.append(f"User: {user_task}")

        # Step 3: AI generates the command or asks for details
        ai_response = get_ai_generated_cli_command(user_task, conversation_history)

        # Step 4: Extract CLI command if present
        command = extract_aws_cli_command(ai_response)

        if command:
            print(f"\nAI's response: {ai_response}")
            # Execute the command
            execute_aws_cli(command)
        else:
            print(f"\nAI's response: {ai_response}")

        # Step 5: Store AI's response in history
        conversation_history.append(f"AI: {ai_response}")

if __name__ == "__main__":
    main()
