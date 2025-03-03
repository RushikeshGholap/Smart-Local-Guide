from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('reviews/', reviews_list, name='reviews_list'),
    path('businesses/', business_list, name='business_list'),

]