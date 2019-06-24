from rest_framework.decorators import api_view
from psycopg2 import connect
from django.http import HttpResponse


# Create your views here.
def postgres_test():
    try:
        conn = connect(dbname="smarttraffic", user="postgres", host="192.168.99.100", password="example", connect_timeout=1)
        conn.close()
        return True
    except:
        return False

@api_view(['GET'])
def get_connection_health(request):
    # try to make connection to DB...
    conn = postgres_test()
    if request.method == 'GET':
        if conn:
            return HttpResponse("Correcta", status=200)
        else:
            return HttpResponse("Bad", status=500)


