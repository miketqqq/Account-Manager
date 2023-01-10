from django.http import HttpResponse
from .models import TrafficTracker

# Create your views here.
from datetime import datetime
import json


def on_load(request):
    if request.method == 'POST':
        if not request.session.get('track_id', None):
            data = json.loads(request.body)
            height = data['height']
            width = data['width']
            tracker = TrafficTracker.objects.create(
                screen_height=height,
                screen_width=width,
            )
            request.session['track_id'] = tracker.id
    return HttpResponse('load') 

def on_close(request):
    if request.method == 'POST':
        tracker_id = request.session['track_id'] 
        tracker = TrafficTracker.objects.get(id=tracker_id)
        tracker.leave_time = datetime.now()
        tracker.save()

    return HttpResponse('close') 