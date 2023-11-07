import openai
import os
import chainlit as cl
import glob

# Configure OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the folder containing PNG data
png_data_folder = "png_data_folder/"

async def bot_response(name: str, system_instruction_path: str, lesson_content_path: str, message: str):
    with open(system_instruction_path, "r") as system_file:
        system_instruction = system_file.read()

    with open(lesson_content_path, "r") as lesson_file:
        lesson_content = lesson_file.read()

    chat_completion = openai.ChatCompletion.create(
        model="gpt-4", messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": message},
            {"role": "assistant", "content": lesson_content}
        ]
    )

    response_message = chat_completion["choices"][0]["message"]["content"]
    
    # Process PNG files in the specified folder
    png_files = glob.glob(os.path.join(png_data_folder, "*.png"))
    for png_file in png_files:
        await process_png_file(png_file)
    
    await cl.Message(author=name, content=f"{name} says: {response_message}", indent=1).send()

    # Return response message for further analysis
    return response_message

async def process_png_file(png_file):
    # Implement your logic to process each PNG file here
    pass

@cl.on_message
async def main(message: str):
    response = await bot_response("Vader", "system_instruction_vader.txt", "lesson_vader.ipynb", message)
    
    if "##SkywalkerSection" in response:
        response = await bot_response("Skywalker", "system_instruction_skywalker.txt", "lesson_skywalker.ipynb", message)
    elif "##KenobiSection" in response:
        response = await bot_response("Kenobi", "system_instruction_kenobi.txt", "lesson_kenobi.ipynb", message)
    elif "##LukeSection" in response:
        response = await bot_response("Luke", "system_instruction_luke.txt", "lesson_luke.ipynb", message)

    # If Skywalker or Kenobi have done their part, let Vader take over again
    if "##VaderReturn" in response:
        await bot_response("Vader", "system_instruction_vader.txt", "lesson_vader.ipynb", message)