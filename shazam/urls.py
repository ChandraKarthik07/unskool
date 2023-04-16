
from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.home,name='home' ),
    path('login_page/',views.login_page,name='login_page' ),
    path('logout_page/',views.logout_page,name='logout_page' ),        
    path('signup/',views.signup,name='signup' ),
    path('profile_page/<str:pk>',views.profile_page,name='profile_page' ),
    path('communi',views.communi,name='communi'),

    path('topics/',views.topics,name='topics' ),
    path('activity/',views.activity,name='activity' ),
    path('home/',views.home,name='home' ),
    path('room/<int:pk>',views.room,name='room' ),
    path('createroom/',views.createroom,name='createroom' ),
    path('updateroom/<int:pk>',views.updateroom,name='updateroom' ),
    path('delete/<int:pk>',views.delete,name='delete' ),
    path('deletemsg/<int:pk>',views.deletemsg,name='deletemsg' ),
    path('update-user/',views.updateUser,name='update-user' ),
    path('more/',views.more,name='more' ),
    path("followToggle/<str:author>/",views.followToggle, name="followToggle")





]
