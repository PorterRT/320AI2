import openai
import os
import chainlit as cl

# Configure OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

@cl.on_message  # this function will be called every time a user inputs a message in the UI
async def main(message: str):
    
    # Fetch response from OpenAI GPT-4.0 with pirate instruction
    chat_completion = openai.ChatCompletion.create(
        model="gpt-4", messages=[
            {"role": "system", "content": "speak like darth vader"},
            {"role": "user", "content": message}
        ]
    )
    
    response_message = chat_completion["choices"][0]["message"]["content"]
    
    # this is an intermediate step (you can modify this as per your requirements)
    await cl.Message(author="Vader", content=f" {response_message}", indent=1).send()

    # send back the final answer (or another formatted response)
    await cl.Message(content=f"Vader says: {response_message}").send()