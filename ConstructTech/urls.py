from django.urls import path
from . import views

app_name ='ConstructTech'

urlpatterns = [
    path('', views.index, name='index'),  # Index page URL
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('projects/', views.projects, name='projects'),
    path('contact/', views.contact, name='contact'),
    path('request-a-quote/', views.request_quote, name='request_quote'),
    path('show-quote/', views.show_quote, name='show_quote'),  # Add this line
    path('update-quote/<int:quote_id>/', views.update_quote, name='update_quote'),
    path('delete-quote/<int:quote_id>/', views.delete_quote, name='delete_quote'),
    path('upload/',views.upload_image,name='upload_image'),
    path('pay/', views.pay, name='pay'),  # Expect an ID in the URL
    path('stk/', views.stk, name='stk'),  # send the stk push prompt
    path('token/', views.token, name='token'),  # generate the token for that particular transaction
         
]

