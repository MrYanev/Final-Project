import os
import openai

openai.api_key = os.getenv("API_KEY")
openai.FineTune.cancel(id="The-To-Cancel")


#Reference OpenAI
#https://platform.openai.com/docs/guides/fine-tuning