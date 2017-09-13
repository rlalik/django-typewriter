from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.serializers.json import DjangoJSONEncoder

#from .models import TypeWriter
from pytypewriter import PyTypeWriter

import json

tw = None
parse_inline = True

# Create your views here.
def index(request):
    context = {}
    return render(
        request,
        'typewriter/index.html',
        context,
    )

def frame(request):
    global tw

    if tw == NoneType:
        tw = PyTypeWriter

    frame = request.POST.get('frame')
    frame_dict = {
        'name' : 'typewriter',
        'frame' : frame,
        'text': tw.render(frame)
    }
    res = { 'response' : [ frame_dict] }

    super(UploadFinished, self).__init__(
        content=DjangoJSONEncoder().encode(res),
        content_type='application/json',
        status=200,
        *args, **kwargs
    )

def parse(request):
    #global tw

    #if tw == NoneType:
    tw = PyTypeWriter()

    print(request.body)
    if request.method == 'POST':
        json_data = json.loads(request.body)

        pattern = json_data['pattern'].encode('utf-8')
        fps = int(json_data['fps'])
        inline = json_data['inline']

        tw.setRawString(pattern)
        tw.setFrameRate(fps)

        tw.parse()
        tw.debug()

        tw_dump = {}

        f = 0
        while (tw.isEnd() == False):
            tw_dump[f] = tw.render(f).decode()
            f += 1

        frame_dict = {
                'name' : 'typewriter',
                'fps' : fps,
                'frames' : tw.count(),
                'dump': tw_dump
            }

        return HttpResponse(
            content=DjangoJSONEncoder().encode(frame_dict),
            content_type='application/json',
            status=200)
    else:
        return HttpResponse(
            content=DjangoJSONEncoder().encode({}),
            content_type='application/json',
            status=400)
