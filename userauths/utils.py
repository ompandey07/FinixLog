from .models import ActivityLog

def create_log(task, user):
    ActivityLog.objects.create(task=task, user=user)