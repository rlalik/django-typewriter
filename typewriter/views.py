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

def parse(request):
    tw = PyTypeWriter()

    if request.method == 'POST':
        json_data = json.loads(request.body)

        pattern = json_data['pattern'].encode('utf-8')
        fps = int(json_data['fps'])
        inline = json_data['inline']

        tw.setPattern(pattern)
        tw.setFrameRate(fps)

        res = tw.parse()
        if res < 0:
            frame_dict = {
                'result' : 'failed',
                'fps' : fps,
                'frames' : -res-1,
                'dump': pattern.decode()
            }

            return HttpResponse(
                content=DjangoJSONEncoder().encode(frame_dict),
                content_type='application/json',
                status=400)

        tw_dump = {}

        f = 0
        while (tw.isEnd() == False):
            tw_dump[f] = tw.render(f).decode()
            f += 1

        frame_dict = {
            'result' : 'ok',
            'fps' : fps,
            'frames' : tw.count(),
            'dump': tw_dump
        }

        return HttpResponse(
            content=DjangoJSONEncoder().encode(frame_dict),
            content_type='application/json',
            status=200)
    else:
        frame_dict = {
            'result' : 'invalid',
            'fps' : fps,
            'frames' : 0,
            'dump': ""
        }

        return HttpResponse(
            content=DjangoJSONEncoder().encode(frame_dict),
            content_type='application/json',
            status=400)
