import json, requests, re
from pprint import pprint


from django.shortcuts import render

from django.views import generic
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.utils.decorators import method_decorator

# Create your views here.
# Helper function

PAGE_ACCESS_TOKEN = "EAADoIXguGCMBAKRcW1uHZCzCE0AdZBnEY70da13nbW9IajnaT7ZCcai74ijsK3LASCsT5CTqzZBNLaIprzrTGGibBdfDp147t30PIPhAJ7S59b4WZBngbCZCCHZBcwUcNNcdXq79OFwNV7xNWYHZC4VB3ukm1tIXSPQlem6TslIuFwZDZD"
VERIFY_TOKEN = "2318934571"


def post_facebook_message(fbid, recevied_message):
    tokens = re.sub(r"[^a-zA-Z0-9\s]", ' ', recevied_message).lower().split()
    text = "Ублюдок, мать твою, а ну иди сюда, говно собачье! Что, решил ко мне лезть?! Ты, засранец вонючий, мать твою, а? Ну, иди сюда,﻿ попробуй меня трахнуть, я тебя сам трахну, ублюдок, онанист чертов, будь ты проклят!"

    user_details_url = "https://graph.facebook.com/v2.6/%s" % fbid
    user_details_params = {'fields': 'first_name,last_name,profile_pic', 'access_token': PAGE_ACCESS_TOKEN}
    user_details = requests.get(user_details_url, user_details_params).json()

    print (user_details, user_details_params, user_details_url, tokens)

    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    response_msg = json.dumps({"recipient": {"id": fbid},
                               "message": {
                                           "attachment": {'type': 'image',
                                                          'payload': {'url':'https://dl.dropboxusercontent.com/u/20018982/raccoon_food.jpg'}}}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
    pprint(status.json())
    print ('*'*50)
    response_msg = json.dumps({"recipient": {"id": fbid},
                               "message": {"attachment":{
      "type":"template",
      "payload":{
        "template_type":"button",
        "text":"What do you want to do next?",
        "buttons":[
          {
            "type":"web_url",
            "url":"https://petersapparel.parseapp.com",
            "title":"Show Website"
          },
          {
            "type":"postback",
            "title":"Start Chatting",
            "payload":"answer to question and more more and more"
          },
            {
                "type": "postback",
                "payload":"answer to question and more more and more",
                "title": "Shsfsdfsafdow Website"
            },


        ]
      }
    }
                                  }})


    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
    pprint(status.json())



# Create your views here.
class BotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')
        
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events 
                if 'message' in message:
                    # Print the message to the terminal
                    pprint(message)    
                    # Assuming the sender only sends text. Non-text messages like stickers, audio, pictures
                    # are sent as attachments and must be handled accordingly. 
                    post_facebook_message(message['sender']['id'], message['message']['text'])
                if 'postback' in message:
                    print (message)
        return HttpResponse()    