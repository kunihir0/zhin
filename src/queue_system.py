"""
A reusable, advanced queue system for managing asynchronous tasks.
"""
import asyncio
from logger import get_logger

log = get_logger(__name__)

class QueueManager:
    """
    Manages a queue of asynchronous tasks with a pool of workers.
    """
    def __init__(self, worker_coro, num_workers=5, name="QueueManager"):
        """
        Initializes the QueueManager.

        Args:
            worker_coro: The coroutine to execute for each task.
            num_workers: The number of concurrent workers.
            name: A name for this queue manager instance for logging.
        """
        self.name = name
        self.queue = asyncio.Queue()
        self.worker_coro = worker_coro
        self.num_workers = num_workers
        self.workers = []
        self._started = False

    async def add_task(self, task_data):
        """
        Adds a task to the queue.
        """
        await self.queue.put(task_data)
        log.debug(f"[{self.name}] Added task: {task_data}")

    async def _worker(self, worker_name):
        """
        The worker function that processes tasks from the queue.
        """
        log.debug(f"[{self.name}] Worker {worker_name} started")
        while True:
            try:
                task_data = await self.queue.get()
                log.debug(f"[{self.name}] Worker {worker_name} processing task: {task_data}")
                await self.worker_coro(task_data)
                self.queue.task_done()
                log.debug(f"[{self.name}] Worker {worker_name} finished task: {task_data}")
            except asyncio.CancelledError:
                log.debug(f"[{self.name}] Worker {worker_name} cancelled.")
                break
            except Exception:
                log.exception(f"[{self.name}] Worker {worker_name} encountered an error while processing {task_data}")


    async def start(self):
        """
        Starts the worker pool.
        """
        if self._started:
            log.warning(f"[{self.name}] Manager already started.")
            return

        for i in range(self.num_workers):
            worker_name = f"worker-{i+1}"
            worker_task = asyncio.create_task(self._worker(worker_name))
            self.workers.append(worker_task)
        self._started = True
        log.info(f"[{self.name}] Started {self.num_workers} workers.")

    async def join(self):
        """
        Waits until all tasks in the queue have been processed.
        """
        if not self._started:
            log.warning(f"[{self.name}] Manager not started. Cannot join.")
            return
        await self.queue.join()
        log.info(f"[{self.name}] All tasks have been processed.")

    async def stop(self):
        """
        Stops all workers.
        """
        if not self._started:
            log.warning(f"[{self.name}] Manager not started. Cannot stop.")
            return

        for worker in self.workers:
            worker.cancel()
        await asyncio.gather(*self.workers, return_exceptions=True)
        self._started = False
        log.info(f"[{self.name}] All workers have been stopped.")