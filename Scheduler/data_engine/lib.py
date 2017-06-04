import logging, datetime
from Core.models import RosterUser, RosterAudit

logger = logging.getLogger('roster')

def get_all_users():
    """
    Getting all the users in the Users table
    """

    logging.info("Getting all the users in the Users table")

    # Variables
    collector = []

    # Get all Users
    for user in RosterUser.objects.all().extra(select={'lower_name': 'lower(first_name)'}).order_by('lower_name'):
        users_name = user.first_name + " " + user.last_name
        collector.append(users_name)

    return collector


def save_shuffle_schedule(saved_rows):
    """
    When requested to save the state of the shuffle, update the row
    """
    logging.info("Saving the state of the shuffle rows")

    temp_collector = []
    for saved_date, saved_user in saved_rows.items():

        # Convert Date
        dt = datetime.datetime.strftime(datetime.datetime.strptime(saved_date, '%Y/%m/%d'), '%a, %Y/%m/%d')

        # Disable rows
        RosterAudit.objects.filter(audit_date=dt).filter(engineer=saved_user[0]).update(
            active=False)

        # collect new state
        temp_collector.append(RosterAudit(
            engineer=saved_user[0],
            audit_date=dt,
            audit_date_field=datetime.datetime.strftime(datetime.datetime.strptime(saved_date, '%Y/%m/%d'), '%Y-%m-%d'),
            active=True
        ))

    # Update new state
    RosterAudit.objects.bulk_create(temp_collector)


def get_audit_rows(from_date, to_date):
    """
    Get the audit rows
    """
    logging.info("Getting all audits from the audit table")

    # variable
    collector = []
    from_date = datetime.datetime.strftime(datetime.datetime.strptime(from_date, '%Y/%m/%d'), '%Y-%m-%d')
    to_date = datetime.datetime.strftime(datetime.datetime.strptime(to_date, '%Y/%m/%d'), '%Y-%m-%d')

    # loop through audits
    for audit in RosterAudit.objects.filter(audit_date_field__gte=from_date).filter(audit_date_field__lte=to_date):
        collector.append({
            'date': datetime.datetime.strftime(datetime.datetime.strptime(audit.audit_date, '%a, %Y/%m/%d'), '%Y/%m/%d'),
            'engg': audit.engineer
        })

    return collector


def delete_audits_by_dates(from_date, to_date):
    """
    Delete the audit rows from given dates
    """

    logging.info("Delete audits based on given dates ...")

    collector = get_audit_rows(from_date, to_date)
    from_date = datetime.datetime.strftime(datetime.datetime.strptime(from_date, '%Y/%m/%d'), '%Y-%m-%d')
    to_date = datetime.datetime.strftime(datetime.datetime.strptime(to_date, '%Y/%m/%d'), '%Y-%m-%d')
    RosterAudit.objects.filter(audit_date_field__gte=from_date).filter(audit_date_field__lte=to_date).delete()
    return collector


def update_audit_table(rows):
    """
    Updating audit table
    """

    logging.info("Updating audits tables ...")

    temp_collector = []

    for row in rows:

        # Convert Date
        dt = datetime.datetime.strftime(datetime.datetime.strptime(row['date'], '%Y/%m/%d'), '%a, %Y/%m/%d')

        # Disable rows
        RosterAudit.objects.filter(audit_date=dt).filter(engineer=row['engineer']).update(
            active=False)

        # collect new state
        temp_collector.append(RosterAudit(
            engineer=row['engineer'],
            audit_date=dt,
            audit_date_field=datetime.datetime.strftime(datetime.datetime.strptime(row['date'], '%Y/%m/%d'), '%Y-%m-%d'),
            active=True
        ))

    # Update new state
    RosterAudit.objects.bulk_create(temp_collector)

    # If any weekends are updated, remove them
    delete_weekend_rows()


def delete_audit_rows(rows):
    """
    Delete Audit rows
    """
    logging.info("Deleting audit rows ...")

    for row in rows:

        # Convert Date
        dt = datetime.datetime.strftime(datetime.datetime.strptime(row['date'], '%Y/%m/%d'), '%a, %Y/%m/%d')

        # delete rows
        RosterAudit.objects.filter(audit_date=dt).filter(engineer=row['engineer']).delete()


def delete_weekend_rows():
    """
    No volunteering work on the weekend so lets remove them.
    """

    logging.info("removing weekend volunteering work")

    RosterAudit.objects.filter(audit_date__startswith="Sun").delete()
    RosterAudit.objects.filter(audit_date__startswith="Sat").delete()



