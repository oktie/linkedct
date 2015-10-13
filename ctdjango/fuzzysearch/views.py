from django.shortcuts import render_to_response
from django.conf import settings

# Create your views here.
def index(request):
    return render_to_response('fuzzysearch/index.html',
        {'endpoint_url' : "/fuzzysearch/srch2/",
         'root_url' : settings.CONFIG['ROOT']})
