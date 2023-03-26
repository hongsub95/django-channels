from django.urls import path
from chat import views

app_name="chat"

urlpatterns = [
    path('',views.index,name='index'),
    path('<int:room_pk>/chat/',views.room_chat,name='room_chat'),
    path('new/',views.room_new,name='room_new'),
    path('<int:room_pk>/delete/',views.room_delete,name="room_delete"),
    path('<int:room_pk>/users/',views.room_users,name="room_users")
]