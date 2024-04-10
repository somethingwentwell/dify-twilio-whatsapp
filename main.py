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

@app.get("/")
async def index():
    return {"msg": "working"}


@app.post("/message")
async def reply(request: Request, Body: str = Form()):
    print(Body)
    form_data = await request.form()
    print(form_data)
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
        'conversation_id': '',  
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
                if json_line["event"] == "agent_message":  
                    answer.append(json_line["answer"])  
            except json.JSONDecodeError:   
                continue  

    merged_answer = ''.join(answer)  

    try:
        message = client.messages.create(
        from_=f"whatsapp:{twilio_number}",
        body=f"AI: {merged_answer}",
        to=f"whatsapp:{whatsapp_number}"
        )
        print(f"Message sent to {whatsapp_number}: {message.body}")
    except Exception as e:
        print(f"Error sending message to {whatsapp_number}: {e}")

    return ""