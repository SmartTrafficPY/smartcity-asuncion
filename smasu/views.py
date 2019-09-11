from django.http import HttpResponse
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def empty(request, pk):
    return HttpResponse(status=204)
