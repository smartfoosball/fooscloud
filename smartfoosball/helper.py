# coding:utf-8
from models import GWUser
from gservice.client import GServiceClient
from datetime import datetime
import time
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage


def request_gw_user(appid, user, pwd):
    _id = 1
    _gw_user = GWUser.objects.get(id=_id)  # must exists. and id = 1
    two_hour = 3600 * 2
    token_expire_ts = lambda dt, offset: time.mktime(
        dt.timetuple()) + offset
    if _gw_user.expire_at < token_expire_ts(datetime.now(), two_hour):
        # token expire
        resp = GServiceClient(appid).login_by_username(user, pwd).json()
        _gw_user.uid = resp['uid']
        _gw_user.token = resp['token']
        _gw_user.expire_at = resp['expire_at']
        _gw_user.save()
    return {'uid': _gw_user.uid, 'token': _gw_user.token, 'expire_at': _gw_user.expire_at}


def get_gservice_client2(appid, user, pwd):
    resp = request_gw_user(appid, user, pwd)
    g = GServiceClient(appid)
    g.set_token(resp['token'])
    return g


def dj_simple_pagination(datas, page=1, page_count=10):
    paginator = Paginator(datas, page_count)
    try:
        datas = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        datas = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        datas = paginator.page(paginator.num_pages)
    return datas
