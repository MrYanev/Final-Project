import os  
import openai

openai.api_key = os.getenv('API_KEY')
openai.FineTune.create(training_file='file-name')

#Reference OpenAI
#https://platform.openai.com/docs/guides/fine-tuning
