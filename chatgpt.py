import openai
import json
import re
#openai.api_key = "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"
openai.api_key = "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"
#model_id = 'ft:gpt-3.5-turbo-0613:personal::7xt5PHUf'
model_id = 'ft:gpt-3.5-turbo-0613:personal::7xt5PHUf'
def generate_response(user_input, role="user"):

    array_exit = ["", "Bye ChatGPT", " Bye ChatGPT", "bye", "bye chat", " bye", " see you"]
    if user_input in array_exit:
        return None

    #message_history.append({'role': 'system', 'content': 'provide the following fields in a JSON dict, where applicable: command, device, ask_time, ask_weather, location'})
    message_history.append({'role': 'system', 'content': 'Interpret the following user input and convert it into JSON of the form { "intent": ["string"], "device":["string"], "location":[ "string"], "ask_time":boolean, "ask_weather":boolean,"role":"assistant","content":""} . Only return JSON with 2 lines. User input:'})
    message_history.append({"role": role, "content": f"{user_input}"})
    completion = openai.ChatCompletion.create(
        model=model_id,
        messages=message_history
    )
    response = completion.choices[0].message.content
    print(completion.choices[0].message.content.strip())
    message_history.append({"role": "assistant", "content": f"{response}"}) 
    return response

message_history = []

while True:
    prompt = input('User:')
    conversation = generate_response(prompt,role="user")
    if conversation is None :
        break
    try:
        parsed_response = json.loads(conversation)

        # Extract intent and entities from the parsed response
        command = [parsed_response['intent'] if parsed_response['intent'] else None]
        device = [parsed_response['device'] if parsed_response['device'] else []]
        ask_time = [parsed_response['ask_time'] if parsed_response['ask_time'] else False]
        ask_weather =[ parsed_response['ask_weather'] if parsed_response['ask_weather'] else False]
        location = [parsed_response['location'] if parsed_response['location'] else None]
        #     # Print the intent and entities
        print("Intent:", command)
        print("Entities:", device)
        print("Ask time:", ask_time)
        print("Ask weather:", ask_weather)
        print("Location:", location)
    except json.JSONDecodeError:
        print("Error: Unable to decode JSON response from the model.")

