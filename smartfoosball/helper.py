#coding:utf-8
from models import GWUser
from gservice.client import GServiceClient
from django.conf import settings


def get_gservice_client(appid):
    return GServiceClient(appid)
