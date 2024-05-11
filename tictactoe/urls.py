from django.contrib import admin
from django.urls import path

from game.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('game/<int:id>/<str:name>', game),
]
