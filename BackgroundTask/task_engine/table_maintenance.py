from django.db import connection, transaction
import logging, datetime

cursor = connection.cursor()

logger = logging.getLogger('roster-extender')


class Maintenance:
    def __init__(self):
        self.table_list = [
            'Core_rosteruser',
            'Core_rosteraudit',
            'BackgroundTask_lastrun',
        ]

        # Keep the space, do not remove
        self.maintenance_tasks = [
            'ALTER TABLE ', 'OPTIMIZE TABLE ', 'ANALYZE TABLE '
        ]

        # Delete data from the historical table, if its n days old (one week old)
        self.n_days = 7

    def date_diff(self):
        """
        Provide difference of date based on the number of days required to purge
        """
        return datetime.datetime.now() - datetime.timedelta(days=self.n_days)

    def execute_command(self, table):
        """
        Execute table maintenance tasks
        """
        logging.info("Performing maintenance task on table: {0}".format(table))
        for task in self.maintenance_tasks:
            logging.info("Executing task: {0}".format(task))
            command = task + table
            cursor.execute(command)
            transaction.commit()

    def run_table_maintenance(self):
        """
        Start the table maintenance program ...
        """
        # Maintenance task
        logging.info("Executing table Maintenance on roster tables...")
        for table in self.table_list:
            self.execute_command(table)