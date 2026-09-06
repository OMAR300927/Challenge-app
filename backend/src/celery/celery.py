from celery import Celery

from ..core.config import settings

celery_app = Celery(
  'challenge_app',
  broker=settings.broker_url,
  include=["src.celery.task"]
)
