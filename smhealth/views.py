from django.db import connections
from django.db.utils import OperationalError
from django.http import HttpResponse
from rest_framework.decorators import api_view


@api_view(["GET"])
def check_health(request):
    db_conn = connections["default"]

    try:
        db_conn.cursor()

    except OperationalError as e:
        return HttpResponse(f"Connection failure: {e}", status=200)

    else:
        return HttpResponse("Connection OK", status=200)
