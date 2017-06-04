from itertools import takewhile, count
from random import shuffle, random
from collections import OrderedDict
import datetime
from lib import get_all_users


class Shuffler:

    def __init__(self, from_date, to_date):
        """
        Initalize variables
        """
        self.sdate = datetime.datetime.strptime(from_date + ' 00:00:00', '%Y/%m/%d %H:%M:%S')
        self.edate = datetime.datetime.strptime(to_date + ' 00:00:00', '%Y/%m/%d %H:%M:%S')

    def get_weekend_dates(self):
        """
        From the provided dates extract all the weekdays
        """
        g = (self.sdate + datetime.timedelta(days=x) for x in count(0))
        g = (x for x in g if x.weekday() not in (5, 6))
        g = takewhile(lambda x: x <= self.edate, g)
        return g

    def assign_week_to_user(self, all_users, all_dates):
        """
        From the obtained dates , randomize the allocation of a week to users
        """

        # Variables
        store_last_week_no = -1
        starter = -1
        collector = OrderedDict()
        picked_user = ""

        # Get the length of users list
        total_users = len(all_users)

        # Loop through the dates
        for all_date in all_dates:

            # Get the week number
            dates_weeknumber = all_date.isocalendar()[1]

            # if the dates are not of the same week then reset or find a new user
            if dates_weeknumber != store_last_week_no:

                # If we have used up the entire list then reset the counter
                if starter >= total_users - 1:
                    starter = -1

                # Get the user from the lot
                store_last_week_no = dates_weeknumber
                starter += 1
                picked_user = all_users[starter]

            # Store / collect all the users
            collector[datetime.datetime.strftime(all_date, '%Y/%m/%d')] = picked_user

        return collector

    def shuffle(self):
        """
        Get the list of dates and users and shuffle to generate a roster.
        """

        # All dates ( without weekend )
        all_dates = self.get_weekend_dates()

        # All Participating users
        all_users = get_all_users()

        # Shuffle all the users
        shuffle(all_users, random)

        # Assign a week to user & return the result
        return self.assign_week_to_user(all_users, all_dates)