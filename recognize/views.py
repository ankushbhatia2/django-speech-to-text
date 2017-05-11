from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from django.views import generic
from os import path
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import speech_recognition as sr
import requests
import json

class SpeechToText(generic.View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({'response':'Please use the post method',
                             'status':400})

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        if 'audio_url' in incoming_message:
            headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                       "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.7",
                       "Accept-Encoding": "gzip,deflate",
                       "Accept-Language": "en-us,en;q=0.5",
                       "Connection": "keep-alive",
                       "Keep-Alive": "115",
                       "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.16) Gecko/20110319 Firefox/3.6.16"}

            req = requests.get(incoming_message['audio_url'], headers=headers, stream=True)
            with open('converter.wav', 'wb') as f:
                f.write(req.content)

            AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "converter.wav")

            r = sr.Recognizer()
            with sr.AudioFile(AUDIO_FILE) as source:
                audio = r.record(source)
            try:
                return JsonResponse({'text':r.recognize_sphinx(audio),
                                     'response':'Conversion successful',
                                     'status':200})
            except:
                return JsonResponse({'response': 'No content received from audio',
                                     'status': 204})
        else:
            return JsonResponse({'response':'Please check your JSON Format',
                                 'status':400})
