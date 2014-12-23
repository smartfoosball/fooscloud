import os

from django.conf import settings
from wechatpy import WeChatClient


def get_qrcode(scene_id):
    qr_dir = os.path.join(settings.MEDIA_ROOT, 'qrcode')
    qrcode = os.path.join(qr_dir, '%d.jpg' % scene_id)
    if not os.path.exists(qr_dir):
        os.makedirs(qr_dir)
    if os.path.exists(qrcode):
        return qrcode
    client = WeChatClient(settings.WX_APPID, settings.WX_SECRET)
    # id,mac
    # 1,c89346469d77
    data = {"action_name": "QR_LIMIT_SCENE", "action_info": {"scene": {"scene_id": scene_id}}}
    resp = client.create_qrcode(data)
    resp = client.show_qrcode(resp.get('ticket'))
    with open(qrcode, 'wb') as f:
        f.write(resp.content)
    return qrcode


if __name__=='__main__':
    print get_qrcode(1)
