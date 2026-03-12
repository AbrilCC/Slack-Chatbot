from django.shortcuts import render
# This file is used at Django REST Framework to define http methods (like controller.ts in typescript)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from slack_sdk import WebClient #to send messages to Slack back (like Prisma as DB client)


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

        #Check if the request comes from Slack (deprecated, see it later)
        #if slack_message.get('token') != SLACK_VERIFICATION_TOKEN:
        #    return Response(status = status.HTTP_403_FORBIDDEN)
        
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

            # If the user messaged '@bot [...] Hi [...]', it answers back (only greetings)
            if 'hi' in text.lower():
                Client.chat_postMessage(
                    channel = channel,
                    text = bot_text)
                return Response(status = status.HTTP_200_OK)
        
        return Response(status = status.HTTP_200_OK)
    
