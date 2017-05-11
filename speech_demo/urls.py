from django.conf.urls import url
from django.contrib import admin
from recognize.views import SpeechToText

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^recognize/$', SpeechToText.as_view())
]
