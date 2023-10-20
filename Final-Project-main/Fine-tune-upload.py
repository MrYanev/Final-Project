import os
import openai

openai.api_key = os.getenv("API_KEY")
openai.File.create(
    file = open("File.jsonl", "rb"),
    purpose='fine-tune'
)

#Reference OpenAI
#https://platform.openai.com/docs/guides/fine-tuning