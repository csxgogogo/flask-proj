from celery import Celery

broker_url = 'redis://localhost/0'
backend = 'redis://localhost/1'
celery_app = Celery("tasks", broker=broker_url, backend=backend)


@celery_app.task(name='tow-sum-task')
def add(a: int, b: int) -> int:
    return a + b
