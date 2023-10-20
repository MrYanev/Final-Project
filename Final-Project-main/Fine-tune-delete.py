import os
import openai

openai.api_key = os.getenv("API_KEY")
openai.File.delete("File-ID")

#Reference OpenAI
#https://platform.openai.com/docs/guides/fine-tuning