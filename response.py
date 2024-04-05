import openai
import os
from dotenv import load_dotenv
from prompts import *



load_dotenv()
# Set up OpenAI API credentials
openai.api_key = 'API Key'
from openai import OpenAI
client = OpenAI(api_key =os.getenv('OPENAI_API_KEY'))



def get_response(chats):
    response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=chats,
    temperature=1,
    max_tokens=4000,
    top_p=1,
    frequency_penalty=0.8,
    presence_penalty=0
    )
    # print(response.choices[0].message)
    response_dict={'content':response.choices[0].message.content}
    if response_dict!=None:
        return response_dict

    else :
        return 'Failed to Generate response!'
    

def get_summary(chats):
    text=parse_dialogue(chats)
    # print(text)
    response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=[
        {
        "role": "user",
        "content": summarise_prompt(text)
        }
    ],
    temperature=1,
    max_tokens=4000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )

    # print(response.choices[0].message.content)
    response_dict={'content':response.choices[0].message.content}
    if response!=None:
        return response_dict

    else :
        return 'Failed to Generate response!'





def parse_dialogue(dialogue_list):
    parsed_dialogue = ''
    for dialogue in dialogue_list:
        content = dialogue['content']
        parsed_dialogue += f"{content}\n"
    return parsed_dialogue



# chats=[{'role': 'system', 'content': 'You are assistant of Dr. Dr. Patil, you will ask patients the expected details from the doctor  .  \n    Doctor will order you to ask some details in between make sure you change your questionaire based on that.'}, {'role': 'user', 'content': '<DOCTOR> Introduction session and intial information . \n                          Ask patient as many questions you can to guage the intial situation and \n                          level of emergency on patients side .\n                          End the conversation with thank you when enough 10-15 questions are asked. Make sure you only ask one question at one time . \n        Otherwise the patient will die answering.'}, {'role': 'assistant', 'content': 'Can you please state your name and age for the record?'}, {'role': 'user', 'content': '<PATIENT> raj 24'}, {'role': 'assistant', 'content': 'What brings you in to see us today, Raj?'}, {'role': 'user', 'content': '<PATIENT> i am angry'}, {'role': 'assistant', 'content': "I'm sorry to hear that. Can you tell me more about why you're feeling angry?"}, {'role': 'user', 'content': '<PATIENT> i am feelingback pain'}, {'role': 'assistant', 'content': 'Where is the back pain located specifically, Raj?'}, {'role': 'user', 'content': '<PATIENT> lower back'}, {'role': 'assistant', 'content': "On a scale of 1 to 10, how would you rate the severity of your lower back pain, with 10 being the worst pain you've ever experienced?"}, {'role': 'user', 'content': '<PATIENT> 10'}, {'role': 'assistant', 'content': 'Have you experienced any recent injury or strain to your lower back that could be causing this severe pain?'}, {'role': 'user', 'content': '<PATIENT> no'}, {'role': 'assistant', 'content': 'Are you experiencing any other symptoms along with the severe lower back pain, such as numbness or tingling in your legs?'}, {'role': 'user', 'content': '<PATIENT> no'}, {'role': 'assistant', 'content': 'Have you tried any home remedies or over-the-counter medications to help alleviate the lower back pain?'}, {'role': 'user', 'content': '<PATIENT> no'}, {'role': 'assistant', 'content': 'Do you have a history of any chronic medical conditions that could be contributing to your lower back pain, Raj?'}, {'role': 'user', 'content': '<PATIENT> no'}, {'role': 'assistant', 'content': 'Are you currently taking any medications, either prescribed or over-the-counter, for any other conditions?'}, {'role': 'user', 'content': '<PATIENT> no'}, {'role': 'assistant', 'content': 'Have you had any previous episodes of severe lower back pain in the past, Raj?'}, {'role': 'user', 'content': '<PATIENT> no'}, {'role': 'assistant', 'content': "Thank you for providing all this information, Raj. Based on what you've shared, it's important for us to further assess your severe lower back pain. Please wait as I inform the doctor about your situation. Thank you for your cooperation.\n"}]
# print(get_summary(chats))
