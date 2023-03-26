from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from django.db import models
from django.conf.global_settings import AUTH_USER_MODEL
from django.db.models.signals import post_delete

from config.json_extended import ExtendedJSONEncoder,ExtendedJSONDecoder
# Create your models here.

class OnlineUserMixins(models.Model):
    class Meta:
        abstract = True
    
    online_user_set = models.ManyToManyField(
        AUTH_USER_MODEL,
        through="RoomMember",
        blank=True,
        related_name="joined_room_set",
    )
    
    def get_online_user(self):
        return self.online_user_set.all()
    
    def get_online_username(self):
        qs = self.get_online_user().values_list("username",flat=True)
        return list(qs)
    def is_joined_user(self,user):
        return self.get_online_user().filter(pk=user.pk).exists()
    
    def user_join(self, channel_name, user) -> bool: 
        try:
            room_member = RoomMember.objects.get(room=self, user=user) 
        except RoomMember.DoesNotExist:
            room_member = RoomMember(room=self, user=user)
            is_new_join = len(room_member.channel_names) == 0
            room_member.channel_names.add(channel_name) 
            if room_member.pk is None:
                room_member.save() 
            else:
                room_member.save(update_fields=["channel_names"]) 
            return is_new_join
        
    def user_leave(self, channel_name, user) -> bool:
        """현 Room으로부터 최종접속종료 여부를 반환합니다."""
        try:
            room_member = RoomMember.objects.get(room=self, user=user) 
        except RoomMember.DoesNotExist:
            return True
        room_member.channel_names.remove(channel_name) 
        if not room_member.channel_names:
            room_member.delete() 
            return True
        else:
            room_member.save(update_fields=["channel_names"]) 
            return False

class Room(OnlineUserMixins):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="owned_room_set"
    )
    class Meta:
        ordering = ["-pk"]
    @property
    def chat_group_name(self):
        return self.make_chat_group_name(room=self)
    @staticmethod
    def make_chat_group_name(room=None, room_pk=None): 
        return "chat-%d" % (room_pk or room.pk)

def room__on_post_delete(instance:Room,**kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        instance.chat_group_name,
        {
            "type":"chat.room.delete",
        }
    )

post_delete.connect(
    room__on_post_delete,
    sender=Room,
    dispatch_uid="room__on_post_delete"
)

class RoomMember(models.Model):
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE
    )
    channel_names = models.JSONField(default=set,encoder=ExtendedJSONEncoder,decoder=ExtendedJSONDecoder)   #다수 접속한 내역