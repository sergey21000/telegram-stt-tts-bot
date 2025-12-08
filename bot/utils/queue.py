import asyncio
import concurrent
from typing import Any, Awaitable, Callable
from loguru import logger

from config.config import Config


def warmup_func():
    pass


class LimitedLLMQueue:
    def __init__(self, semaphore_value: int, num_workers_queue: int):
        self.queue = asyncio.Queue()
        self.semaphore = asyncio.Semaphore(semaphore_value)
        self.num_workers_queue = num_workers_queue
        self.workers = []
        self._active = 0

    def get_position(self) -> int:
        return self._active + self.queue.qsize() + 1

    async def add_task(self, queue_kwargs: dict[str, Any]) -> int:
        position = self.get_position()
        await self.queue.put([queue_kwargs, position])
        return position

    async def worker(self, worker_func: Callable[..., Awaitable[Any]]) -> None:
        while True:
            queue_kwargs, position = await self.queue.get()
            try:
                async with self.semaphore:
                    self._active += 1
                    await worker_func(**queue_kwargs, position=position)
            except Exception as e:
                logger.exception(str(e), exc_info=True)
                await queue_kwargs['bot'].send_message(
                    chat_id=queue_kwargs['user_message'].from_user.id,
                    text='❌ Error processing queue function',
                )
                if Config.ADMIN_CHAT_ID:
                    await queue_kwargs['bot'].send_message(
                        chat_id=Config.ADMIN_CHAT_ID,
                        text=f'❌ Error processing queue function: {e}',
                    )
            finally:
                self._active -= 1
                self.queue.task_done()

    async def start_workers(self, worker_func: Awaitable) -> None:
        for i in range(self.num_workers_queue):
            worker_task = asyncio.create_task(self.worker(worker_func))
            self.workers.append(worker_task)

    async def stop_workers(self):
        for worker in self.workers:
            worker.cancel()
        await asyncio.gather(*self.workers, return_exceptions=True)
