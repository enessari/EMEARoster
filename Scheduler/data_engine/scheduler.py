from datetime import datetime, timedelta
import logging

from lib import get_all_users

logger = logging.getLogger('roster')


class Scheduler:

    def __init__(self, from_date=None, to_date=None):
        """
        Initalize parameters
        """
        self.weekends = ['Sun', 'Sat']
        self.today = datetime.now()
        self.roster_rows = {}

        # If not from date and till date given then we generate a date of 30 days period
        if not from_date and not to_date:
            self.from_date = self.today - timedelta(days=3)
            self.to_date = self.today + timedelta(days=30)
        else:
            self.from_date = datetime.strptime(from_date + ' 00:00:00', '%Y/%m/%d %H:%M:%S')
            self.to_date = datetime.strptime(to_date + ' 00:00:00', '%Y/%m/%d %H:%M:%S')

    def generate_date_range_rows(self):
        """
        This function calculates the dates b/w from date to till date, this helps in building up the columns list
        """
        logging.info("Starting method to get the table headers")

        # Variable
        counter = 0
        collector = []
        n_days = (self.to_date - self.from_date).days

        # Increment in a while loop to generate the table heading ...
        while counter != n_days + 1:
            collect_date = self.from_date + timedelta(days=counter)
            collector.append(
                collect_date.strftime("%a") + ', ' + collect_date.strftime('%Y/%m/%d')
            )
            counter += 1

        # Insert the from date and till date on the row to populate the date field
        self.roster_rows['today_date_roster_format'] = datetime.strftime(self.today, '%a, %Y/%m/%d')
        self.roster_rows['from_date'] = datetime.strftime(self.from_date, '%Y/%m/%d')
        self.roster_rows['to_date'] = datetime.strftime(self.to_date, '%Y/%m/%d')
        self.roster_rows['today_date'] = datetime.strftime(self.today, '%Y/%m/%d')

        logging.info("Finished collecting table headers")
        return collector

    def get_rows(self):

        self.roster_rows['headers'] = self.generate_date_range_rows()
        self.roster_rows['users'] = get_all_users()

        return self.roster_rows



