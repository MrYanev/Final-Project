import os  
import openai

openai.api_key = os.getenv('API_KEY')
openai.File.list()


#Reference OpenAI
#https://platform.openai.com/docs/guides/fine-tuning