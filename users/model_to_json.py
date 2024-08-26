import json
from django.core.serializers import serialize
from django.forms.models import model_to_dict
from users.models import PortalUser


users = PortalUser.objects.all()
# one_user = PortalUser.objects.get(pk=3)


def qs_to_json1(query_set):
    json_users = json.dumps([model_to_dict(item) for item in query_set], ensure_ascii=False)
    return json_users


def qs_to_json2(query_set):
    json_users = serialize('json', query_set)
    return json_users
