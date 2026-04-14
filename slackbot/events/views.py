from django.shortcuts import render
# This file is used at Django REST Framework to define http methods (like controller.ts in typescript)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from slack_sdk import WebClient #to send messages to Slack back (like Prisma as DB client)
from .utils import analyze_jobs_csv
import requests


SLACK_VERIFICATION_TOKEN = getattr(settings, 'SLACK_VERIFICATION_TOKEN', None)
SLACK_BOT_USER_TOKEN = getattr(settings, 'SLACK_BOT_USER_TOKEN', None)
Client = WebClient(token = SLACK_BOT_USER_TOKEN)

# self is an Events instance
# response equals @Body
# *args is a list of the arguments the function is called with
# **kwargs is an arg json dictionary
class Events(APIView):
    def post(self, request, *args, **kwargs):
        slack_message = request.data
        #print(slack_message)

        #Special Slack handshake when connecting to our server
        if slack_message.get('type') == 'url_verification':
            return Response(
                {"challenge": slack_message['challenge']},
                status = status.HTTP_200_OK
            )
                
        #Greet bot:
        if 'event' in slack_message:
            event_message = slack_message.get('event')
            #The bot must ignore its own message or it'll get in an infinite loop
            if event_message.get('subtype') == 'bot_message': #Slack has events subtypes
                return Response(status = status.HTTP_200_OK)
            user = event_message.get('user')
            text = event_message.get('text')
            channel = event_message.get('channel')
            bot_text = 'Hewwo <@{}> :wave:'.format(user)
            text = text.lower()

            # If the user messaged '@bot [...] Hi [...]', it answers back (only greetings)
            if 'hi' in text:
                Client.chat_postMessage(
                    channel = channel,
                    text = bot_text)
                return Response(status = status.HTTP_200_OK)
            
        #Data Analysis bot:
            if 'analyze' in text:
                category = None
                if "by industry" in text:
                    category = "industry"
                elif "by sex" in text:
                    category = "sex"
                elif "by age" in text:
                    category = "age"
                if not category:
                    Client.chat_postMessage(
                        channel=channel,
                        text="Please specify category: industry / sex / age")
                    return Response(status=200)
                
                if 'files' not in event_message:
                    Client.chat_postMessage(
                        channel=channel,
                        text="Please attach a CSV file")
                    return Response(status=200)
                
                else:
                    file_url = event_message['files'][0]['url_private']
                    headers = {"Authorization": f"Bearer {SLACK_BOT_USER_TOKEN}"}
                    response = requests.get(file_url, headers=headers)
                    with open("temp.csv", "wb") as f:
                        f.write(response.content)
                    file_path = "temp.csv"
                    print(response.headers.get("content-type"))

                    try:
                        summary, plot_path = analyze_jobs_csv(file_path, category)
                        Client.chat_postMessage(
                                channel = channel,
                                text = f"Analysis complete for {category}.\n Summary: {summary}")     
                        Client.files_upload_v2(
                                channel = channel,
                                file = plot_path)
                    except Exception as e:
                        print("ERROR:", e)
                        Client.chat_postMessage(
                            channel=channel,
                            text=f"Error processing file: {str(e)}")


        return Response(status = status.HTTP_200_OK)
    
