from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'accounts'

urlpatterns =[
    path('register/',views.register,name="register"),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='accounts:login'), name='logout'),

]