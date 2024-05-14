import django_schedules

@django_schedules.register(mins=0, hour=0)
def run_at_midnight(**kwargs):
    print('hello')

@django_schedules.register(mins=30, hour=9, day_of_month=2, month='5,11', lock=False, job_name='foobar')
def bar(**kwargs):
    """
    Run on 2.5. and 2.11. at 18:03.
    Don't use locking (allow to run this job more than once at the same time).
    The job will be called 'foobar'.'
    """
    print('hello')