# import logging
# logging.getLogger("transformers").setLevel(logging.ERROR)
# from transformers import GPT2TokenizerFast



# message = "Hello, chatgpt"
# tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

# count_b = len(tokenizer(message)["input_ids"])
# print(count_b)


import os
from dotenv import dotenv_values

config = dotenv_values(".env")
string_mag = int(config.get("TIMER-DOOR"))
print(string_mag, type(string_mag))