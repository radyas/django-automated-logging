from django.http import JsonResponse
from django.shortcuts import render

from automated_logging.decorators import ignore_view
from testmodels.models import OrdinaryTest, M2MTest, Base
import random


@ignore_view(methods=['GET'])
def save_test(request):
    """just for testing the save capabilities internally"""

    # print('hello there young man')
    # base = Base.objects.get(pk='2fd93db1-bcba-4282-b97f-4fd88f8a3cd8')
    # print(base.id)

    # m2m = M2MTest.objects.get(pk='16b18608-11dd-47f7-a7d6-c1bb427110ac')
    # m2m.test.remove(base)
    # m2m.test.add(base)
    # m2m.save()
    ordinary = OrdinaryTest.objects.filter()[0]
    ordinary.test = str(random.randint(0, 10000000))
    ordinary.save(update_fields=['test'])

    return JsonResponse({})
