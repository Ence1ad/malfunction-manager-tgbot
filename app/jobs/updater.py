import warnings
from pytz_deprecation_shim import PytzUsageWarning
from django.conf import settings

from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import get_all
import logging
logger = logging.getLogger(__name__)


# def register_all_middlewares(scheduler):
#     dp.setup_middleware(SchedulerMiddleware(scheduler))
# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after our job has run.
@util.close_old_connections
# Удаляет все записи если они старее чем 1800 секунд (30 мин)
def delete_old_job_executions(max_age=1800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        warnings.filterwarnings(action="ignore", category=PytzUsageWarning)
        scheduler = AsyncIOScheduler()
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # Добавляем расписание для функции get_all
        scheduler.add_job(
            get_all,
            trigger=CronTrigger(day_of_week='mon-sun', hour=8, minute=0, timezone='Europe/Moscow'),  # Every days
            # trigger=CronTrigger(second="*/10"),  # Every 10 seconds
            # trigger=CronTrigger(minute="*/1"),  # Every 10 seconds
            id="every day breaking list",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
            timezone='Europe/Moscow'

        )
        if settings.DEBUG:
            logger.info("Added job 'rewrite_day_menu'.")

        # Добавляем расписание для функции delete_old_job_executions
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(hour="*/12", timezone='Europe/Moscow'),
            # day_of_week="mon", hour="00", minute="00"
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,

        )
        if settings.DEBUG:
            logger.info(
                "Added job: 'delete_old_job_executions'."
            )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
