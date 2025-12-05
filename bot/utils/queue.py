import asyncio
import concurrent
from typing import Any, Awaitable, Callable
from loguru import logger

from config.config import Config
from bot.init.worker_models import get_worker_models


def warmup_func():
    pass


class LimitedLLMQueue:
    def __init__(self, semaphore_value: int, num_workers_queue: int, max_workers_pool: int):
        self.queue = asyncio.Queue()
        self.semaphore = asyncio.Semaphore(semaphore_value)
        self.pool = concurrent.futures.ProcessPoolExecutor(
            max_workers=max_workers_pool,
            initializer=get_worker_models,
        )
        self.num_workers_queue = num_workers_queue
        self.workers = []
        self._active = 0

    def get_position(self) -> int:
        return self._active + self.queue.qsize() + 1

    async def add_task(self, queue_kwargs: dict[str, Any]) -> int:
        position = self.get_position()
        await self.queue.put(queue_kwargs)
        return position

    async def worker(self, worker_func: Callable[..., Awaitable[Any]]) -> None:
        while True:
            queue_kwargs = await self.queue.get()
            try:
                async with self.semaphore:
                    self._active += 1
                    await worker_func(**queue_kwargs, pool=self.pool)
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
                # raise e
            finally:
                self._active -= 1
                self.queue.task_done()

    async def start_workers(self, worker_func: Awaitable, warmup_pool: bool = False) -> None:
        if warmup_pool:
            loop = asyncio.get_running_loop()
            futures = [loop.run_in_executor(self.pool, warmup_func) for _ in range(self.pool._max_workers)]
            await asyncio.gather(*futures)

        for i in range(self.num_workers_queue):
            worker_task = asyncio.create_task(self.worker(worker_func))
            self.workers.append(worker_task)

    async def stop_workers(self):
        for worker in self.workers:
            worker.cancel()
        await asyncio.gather(*self.workers, return_exceptions=True)
        self.pool.shutdown(wait=True)
