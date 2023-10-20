import os
import openai

openai.api_key = os.getenv("API_KEY")
content = openai.File.download("File-ID")

#Reference OpenAI
#https://platform.openai.com/docs/guides/fine-tuning