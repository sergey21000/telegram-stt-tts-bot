from bot.utils.queue import LimitedLLMQueue
from config.queue import QueueConfig


llm_queue: LimitedLLMQueue = LimitedLLMQueue(
    semaphore_value=QueueConfig.SEMAPHORE_VALUE,
    num_workers_queue=QueueConfig.NUM_WORKERS_QUEUE,
)
