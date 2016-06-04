from django.conf.urls import include, url
from .views import BotView
urlpatterns = [
                  url(r'^66d2b8f4a09cd35cb23076a1da5$', BotView.as_view()) 
               ]