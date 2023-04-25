import hashlib
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

from datetime import datetime, timedelta
from django.db.models.functions import Now

from django.utils import timezone

from api.models import License

# Task Libs
class Task:

    @classmethod
    def create_seed(cls):
        s = "%s%s" % ('serapi', time.time())
        seed = hashlib.md5(s.encode('utf-8')).hexdigest()[:16]
        return seed
    
    @classmethod
    def release_license(cls):

        print(" Revisando Licensias ")

        # Time clean
        one_h_ago = timezone.now() - timezone.timedelta(minutes=30)

        # Get Licenses for clean
        licenses = License.objects.filter(reserved__lte=one_h_ago)

        for license in licenses:
            license.delete()

            print(license)

# Create Cronjob
class Scheduler:
    def release_license(self):
        scheduler = BackgroundScheduler(timezone='UTC')

        # Tasks schedule
        scheduler.add_job(func=Task.release_license,
                          trigger="cron",
                          day_of_week="*",
                          hour="*",
                          minute="*",
                          second="30")

        scheduler.start()

        atexit.register(lambda: scheduler.shutdown())