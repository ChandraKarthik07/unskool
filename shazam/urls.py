
from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.home,name='home' ),
    path('login_page/',views.login_page,name='login_page' ),
    path('logout_page/',views.logout_page,name='logout_page' ),        
    path('signup/',views.signup,name='signup' ),


    path('home/',views.home,name='home' ),
    path('room/<int:pk>',views.room,name='room' ),
    path('createroom/',views.createroom,name='createroom' ),
    path('updateroom/<int:pk>',views.updateroom,name='updateroom' ),
    path('delete/<int:pk>',views.delete,name='delete' ),



]
