from django.db import models

# Create your models here.
import uuid

class TrafficTracker(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    load_time = models.DateTimeField(auto_now_add=True, editable=False)
    leave_time = models.DateTimeField(auto_now=True, null=True)
    screen_height = models.CharField(max_length=20, null=True)
    screen_width = models.CharField(max_length=20, null=True)

    def __repr__(self):
        return f"load_time:{self.load_time}, leave_time:{self.leave_time}, screen_height:{self.screen_height}, screen_width:{self.screen_width},"

    def __str__(self):
        return f"load_time:{self.load_time}, leave_time:{self.leave_time}"


class ButtonTracker(models.Model):
    session = models.ForeignKey(TrafficTracker, null=True, on_delete=models.CASCADE)
    detail = models.CharField(max_length=254, null=True)
    click_time = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f"click_time:{self.click_time}, detail:{self.detail}"