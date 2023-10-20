import os  
import openai

openai.api_key = os.getenv('API_KEY')
openai.Embedding.create(
    model='text-embedding-ada-002',
    inpup='Headlines/articles go here' 
)

#References OpenAi
#https://platform.openai.com/docs/guides/fine-tuning