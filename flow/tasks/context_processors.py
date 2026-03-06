from .models import Notification

def unread_notifications(request):
    #pra colocar o símbolo de notificação 
    if request.user.is_authenticated:
        count = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count()
        return {'unread_notif_count': count}
    return {'unread_notif_count': 0}