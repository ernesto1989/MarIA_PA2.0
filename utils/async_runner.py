'''
    Script que genera un thread específico para envío de todas las notificaciones.
'''
import asyncio
import threading


class AsyncRunner:

    def __init__(self):

        self.loop = asyncio.new_event_loop()

        self.thread = threading.Thread(
            target=self._run_loop,
            daemon=True
        )

        self.thread.start()

    def _run_loop(self):

        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def run(self, coro):
        future = asyncio.run_coroutine_threadsafe(
            coro,
            self.loop
        )

        try:
            return future.result()
        except Exception:
            raise


async_runner = AsyncRunner()