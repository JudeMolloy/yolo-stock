web: gunicorn yolo:app
celery_worker: celery worker -A celery_worker.celery -l info --concurrency 2
celery_beat: celery beat -A celery_worker.celery -l info