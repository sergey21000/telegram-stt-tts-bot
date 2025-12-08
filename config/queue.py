import os


class QueueConfig:
    N_MAX_CONCURRENT_TASKS_IN_QUEUE: int = os.cpu_count()

    SEMAPHORE_VALUE: int = N_MAX_CONCURRENT_TASKS_IN_QUEUE
    NUM_WORKERS_QUEUE: int = N_MAX_CONCURRENT_TASKS_IN_QUEUE
