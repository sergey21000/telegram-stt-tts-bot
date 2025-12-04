
import os
import asyncio
import logging
import time
import concurrent.futures
import ctypes


# имитация какой либо модели
class FakeModels:
    def __init__(self):
        print(f"[FakeModels] ⏳ Загрузка модели в PID {os.getpid()}...")
        time.sleep(2)
        print(f"[FakeModels] ✅ Модель загружена в PID {os.getpid()}")

# глобальная переменная в которую будем устанавливать модели
MODELS = None

# инициализатор для пула 
def pool_initializer():
    global MODELS
    # если модели еще не загружены то загрузить их
    # PID показывает уникальный ID процесса, который для каждого процесса в пуле будет свой
    if MODELS is None:
        print(f'[Init] PID {os.getpid()} — загружаем модели...')
        MODELS = FakeModels()
    else:
        print(f'[Init] PID {os.getpid()} — модели уже есть')


# функция для прогрева пула (должны быть pickle-able - не лямбда, не onnxruntime модель и тд)
def warmup_func():
    # ничего не делает, просто используется для старта процессов
    return None


# основная функция, которую будем выполнять в пуле процессов
# и выводить ID процесса, хэш модели и реальный физический адрес модели через ctypes
# из за различий в механизмах fork() и spawn на Windows все атрибуты у моделей будут разные, 
# на linux будут разные только реальные адреса объектов в памяти
def worker_task(x: int) -> str:
    global MODELS
    print(f'PID={os.getpid()}, hash={hash(MODELS)}, address={ctypes.addressof(ctypes.py_object(MODELS))}')
    time.sleep(1)
    return f'Результат {x} (PID {os.getpid()})'


# асинхронная очередь (имитация LimitedLLMQueue)
class MiniPool:
    def __init__(self, max_workers: int):
        # инициализация пула
        self.pool = concurrent.futures.ProcessPoolExecutor(
            # сколько процессов в пуле
            max_workers=max_workers,
            # функция инициализации которая запустится как торлько будет запущен пул (хотя бы один из процессов)
            initializer=pool_initializer,
            # опциональные аргументы для функции initializer
            initargs=(),
        )

    async def run(self):
        # получение экземпляра цикла событий
        loop = asyncio.get_running_loop()
        # прогреваем пул  - запускаем функцию которая ничего не делает чтобы вызвать initializer для пула
        # можно этого не делать тогда initializer будет вызван когла запустим основную функцию
        futures = [loop.run_in_executor(self.pool, warmup_func) for _ in range(self.pool._max_workers)]
        await asyncio.gather(*futures)
        # поскольку warmup_func ничего не делает, pool закончит ее выполнят ьи будет готов выполнять задачи дальше
        print('\n✅ Все процессы инициализированы и готовы работать!\n')
        # запуск основной функции в параллельно в пуле процессов
        tasks = [loop.run_in_executor(self.pool, worker_task, i) for i in range(4)]
        results = await asyncio.gather(*tasks)
        print('Результаты:', results)


# запуск с нужным числом процессов
if __name__ == '__main__':
    asyncio.run(MiniPool(max_workers=2).run())


# Windows:
# [Init] PID 15260 — загружаем модели...
# [Init] PID 14032 — загружаем модели...
# [FakeModels] ⏳ Загрузка модели в PID 15260...
# [FakeModels] ⏳ Загрузка модели в PID 14032...
# [FakeModels] ✅ Модель загружена в PID 14032
# [FakeModels] ✅ Модель загружена в PID 15260

# ✅ Все процессы инициализированы и готовы работать!

# PID=14032, hash=102225476697, address=1635640092440
# PID=15260, hash=104993074265, address=1679921260312
# PID=15260, hash=104993074265, address=1679921260312
# PID=14032, hash=102225476697, address=1635640092440
# Результаты: ['Результат 0 (PID 14032)', 'Результат 1 (PID 15260)', 'Результат 2 (PID 15260)', 'Результат 3 (PID 14032)']



# Linux (Google Colab):
# [Init] PID 11171 — загружаем модели...
# [FakeModels] ⏳ Загрузка модели в PID 11171...
# [Init] PID 11172 — загружаем модели...
# [FakeModels] ⏳ Загрузка модели в PID 11172...
# [FakeModels] ✅ Модель загружена в PID 11171

# ✅ Все процессы инициализированы и готовы работать!

# [FakeModels] ✅ Модель загружена в PID 11172
# PID=11171, hash=1080424140588, address=17286784484896
# PID=11172, hash=1080424140588, address=17286784484768
# PID=11171, hash=1080424140588, address=17286784484896
# PID=11172, hash=1080424140588, address=17286784484768
# Результаты: ['Результат 0 (PID 11171)', 'Результат 1 (PID 11172)', 'Результат 2 (PID 11171)', 'Результат 3 (PID 11172)']