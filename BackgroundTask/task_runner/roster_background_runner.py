import logging, os

from django.contrib.auth.models import User
from django.utils import timezone

from BackgroundTask.task_engine.table_maintenance import Maintenance
from BackgroundTask.models import LastRun

logger = logging.getLogger('roster-extender')
logging.basicConfig(format='%(asctime)s:[%(levelname)s]: %(message)s', level=logging.INFO)


class BackgroundTask:

    def __init__(self):
        self.admin_username = 'admin'
        self.admin_email = 'admin@mail.com'
        self.admin_pass = os.environ['ADMIN_PASS']
        self.when_to_run = {
            'table_maintenance': 86400     # Once a day
        }

    def check_last_run_table(self, component):
        """
        Get all the date/time of the last run by components ..
        """
        logging.info("Getting the last run time in seconds for component: {0}".format(component))
        last_record_time = '2000-01-01 00:00:00'
        last_run = LastRun.objects.filter(component=component).values('last_run')
        for last_run in last_run:
            last_record_time = (timezone.now() - last_run['last_run']).total_seconds()
        return last_record_time

    def update_last_run_time(self, component):
        """
        Once the component run is completed update the lastrun table...
        """
        logging.info("Updating the time when it was last run: {0}".format(component))
        LastRun.objects.filter(component=component).update(
            last_run=timezone.now()
        )

    def run_check_for_table_maintenance(self):
        """
        Run the component to do table maintainence ...
        """
        logging.info("Checking if its time to do table maintenance....")
        if self.when_to_run['table_maintenance'] < self.check_last_run_table('table_maintenance'):
            logging.info("Yes, its time to do table maintenance...")
            Maintenance().run_table_maintenance()
            self.update_last_run_time('table_maintenance')
        else:
            logging.info("No, we have still not reached the slot to do maintenance work... skip.")

    def create_super_user(self):
        """
        Created SuperUser if not exits
        """

        if User.objects.filter(username=self.admin_username).count() == 0:
            User.objects.create_superuser(self.admin_username, self.admin_email, self.admin_pass)
            logging.info('Superuser created.')
        else:
            logging.info('Superuser creation skipped.')

    def run_task(self):
        """
        Execute all the tasks ...
        """
        self.create_super_user()
        self.run_check_for_table_maintenance()