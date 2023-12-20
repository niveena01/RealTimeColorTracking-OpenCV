from . import views
from django.urls import path, include

urlpatterns =[
    path('', views.home, name='home'),
    path('live_color_capture/', views.live_color_capture, name='live_color_capture'),

]