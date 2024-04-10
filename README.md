# dify-twilio-whatsapp

## Build docker image

```
docker buildx build --platform linux/amd64 --no-cache  -t warching/dify-whatsapp .
```

## Run the App

```
docker compose up -d
```

## Localtunnel

```
lt --port 8000
```

## Set up Twilio webhook

https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn?frameUrl=%2Fconsole%2Fsms%2Fwhatsapp%2Flearn%3Fx-target-region%3Dus1

## Set up template

https://console.twilio.com/us1/develop/sms/content-template-builder

```
AI: {{1}}
```