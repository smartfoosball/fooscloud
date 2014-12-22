from django.conf import settings
from wechatpy import WeChatClient


def qrcode(scene_id):
    client = WeChatClient(settings.WX_APPID, settings.WX_SECRET)
    # id,mac
    # 1,c89346469d77
    data = {"action_name": "QR_LIMIT_SCENE", "action_info": {"scene": {"scene_id": scene_id}}}
    resp = client.qrcode.create(data)
    resp = client.qrcode.show(resp.get('ticket'))
    return resp


if __name__=='__main__':
    print qrcode(1)
