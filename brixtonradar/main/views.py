from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
import models

def index(request):
    data= {}
    return render_to_response('main/index.html', data, context_instance = RequestContext(request))


def event(request, event_id):
    data= {}
    data['event'] = get_object_or_404(models.Event, pk=event_id)
    return render_to_response('main/event.html', data, context_instance = RequestContext(request))
