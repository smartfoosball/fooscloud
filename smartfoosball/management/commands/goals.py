from django import db
from django.conf import settings
from django.core.management.base import BaseCommand
from smartfoosball.models import Game, Goal

from gservice.client import GServiceClient

import time


class Command(BaseCommand):
    help = 'Check goals from gizwits'

    def handle(self, *args, **options):
        gsc = GServiceClient(settings.GW_APPID)
        ts  = 0
        d_team = {'red': 1, 'blue': 2}
        d_position = {'red_van': 1, 'red_rear': 2, 'blue_van': 3, 'blue_rear': 4}
        while True:
            try:
                game = Game.objects.filter(status=Game.Status.playing.value).first()
                data = gsc.retrieve_product_histroy_data(
                    settings.PRODUCT_KEY, start_ts=ts, limit=10).json()['data']
                if len(data) == 0:
                    db.reset_queries()
                    time.sleep(3)
                    continue

                if ts == 0:
                    ts = data[0]['ts']
                    print "ignore first data"
                    continue

                ts = data[0]['ts']
                if not game:
                    db.reset_queries()
                    time.sleep(3)
                    continue

                for i in data:
                    if i['attr'] == 6:
                        game.blue_score = i['val']
                    elif i['attr'] == 7:
                        game.red_score = i['val']
                game.save()
                db.reset_queries()
                time.sleep(3)
            except Exception, e:
                print str(e)
