import openai
import os
import json
#import tiktoken # for token counting
import numpy as np
from collections import defaultdict
from dotenv import dotenv_values
config = dotenv_values(".env")

openai.api_key = config.get("API-KEY")

path = 'train_data/finetune_data/ft_data.jsonl'
path_save ='train_data/finetune_data'


def save_file(file_path, content):
    with open(file_path, 'r', encoding='utf-8') as outfile:
        outfile.write(content)

def upload_ftdata():
    with open(path, "rb") as file:
        response = openai.File.create(
            file = file,
            purpose = 'fine-tune'
        )
    file_id = response['id']

    print(f"File uload with id: {file_id}")


def finetune_create(file_id):
    #file_id = "file-eiULcQtrnSQyVJwhHGdExPEF"
    model_name = "gpt-3.5-turbo"

    response = openai.FineTuningJob.create(
        training_file = file_id,
        model = model_name
    )

    job_id = response['id']
    print(f"Job id: {job_id}")

def delete_model(file_id):
    openai.Model.delete(file_id)


#delete_model('ft:gpt-3.5-turbo-0613:personal::7wRy2L5v')
# Cancel a job
#print(openai.FineTuningJob.cancel("ftjob-7ZVuQkHlfYGpu8ZnKPlM4jww"))
#List 10 fine-tuning jobs
#print(openai.FineTuningJob.list(limit=10))

# Retrieve the state of a fine-tune
#response = openai.FineTuningJob.retrieve("ftjob-f3Dl7vElzUPJqRXGVZucolDD")
# response = openai.FineTuningJob.retrieve("file-S4eQr1BX3qYfOYaDMlZhNGV9")
# print(response)


# content = openai.File.download("file-1djjiPydEyVwwZPNw9CNPPC4")
# ans = content.decode()
# with open('results2.csv', 'w') as f:
#     f.write(ans)

# #upload_ftdata()
# #finetune_create('file-vGTkWXr1wwxh1bX2zSzXp2JR')

# import pandas as pd

# # Assuming you have your data in a pandas DataFrame
# # Replace 'your_data' with your actual data source
# df = pd.read_csv('results2.csv')

# # Count the number of rows where train_accuracy is equal to 1
# num_rows_with_accuracy_1 = len(df[df['train_accuracy'] == 1])

# # Calculate the percentage
# percentage_accuracy_1 = (num_rows_with_accuracy_1 / len(df)) * 100

# print(f"Percentage of train_accuracy equal to 1: {percentage_accuracy_1}%")