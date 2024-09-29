from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # The user receiving the notification
    message = models.TextField()  # The notification message
    created_at = models.DateTimeField(auto_now_add=True)  # When the notification was created
    is_read = models.BooleanField(default=False)  # Has the user read the notification?

    def __str__(self):
        return f"Notification for {self.user.username} - {self.message[:20]}"
