# Third-party imports
from fastapi import FastAPI, Form, Depends, Request
from twilio.rest import Client
from decouple import config
import requests  
import json 

app = FastAPI()

account_sid = config("TWILIO_ACCOUNT_SID")
auth_token = config("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)
twilio_number = config('TWILIO_NUMBER')
dify_url = config('DIFY_URL')
dify_api_key = config('DIFY_API_KEY')
conversation_ids = {}

@app.get("/")
async def index():
    return {"msg": "working"}


@app.post("/message")
async def reply(request: Request, Body: str = Form()):
    form_data = await request.form()
    whatsapp_number = form_data['From'].split("whatsapp:")[-1]
    url = dify_url
    headers = {  
        'Content-Type': 'application/json',  
        'Authorization': f"Bearer {dify_api_key}",  
    }  
    data = {  
        'inputs': {},  
        'query': Body,  
        'response_mode': 'streaming',  
        'conversation_id': conversation_ids.get(whatsapp_number, ''),  
        'user': whatsapp_number,  
    }  
    response = requests.post(url, headers=headers, data=json.dumps(data), stream=True)  
    answer = []  
    for line in response.iter_lines():  
        if line:  
            decoded_line = line.decode('utf-8')  
            if decoded_line.startswith('data: '):  
                decoded_line = decoded_line[6:]  
            try:  
                json_line = json.loads(decoded_line) 
                if "conversation_id" in json_line:
                    conversation_ids[whatsapp_number] = json_line["conversation_id"]
                if json_line["event"] == "agent_thought":  
                    answer.append(json_line["thought"])  
            except json.JSONDecodeError: 
                print(json_line)  
                continue  

    merged_answer = ''.join(answer)  

    try:  
        # Split the message into smaller parts if it's too long  
        message_parts = [merged_answer[i:i + 1590] for i in range(0, len(merged_answer), 1590)]  
    
        for part in message_parts:  
            message = client.messages.create(  
                from_=f"whatsapp:{twilio_number}",  
                body=f"AI: {part}",  
                to=f"whatsapp:{whatsapp_number}"  
            )  
            print(f"Message part sent to {whatsapp_number}: {message.body}")  
    
        print(conversation_ids)  
    except Exception as e:  
        print(f"Error sending message to {whatsapp_number}: {e}")  


    return ""