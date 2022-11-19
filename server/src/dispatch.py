from loguru import logger
from pymitter import EventEmitter


class Signal:
    _bus = EventEmitter()

    def __init__(self, name: str):
        self._name = name

    def connect(self, func=None):
        return self._bus.on(self._name, func)

    async def emit(self, **kwargs):
        logger.debug(f"Emit {self._name}.")
        await self._bus.emit_async(self._name, **kwargs)

    def listeners(self):
        return self._bus.listeners(self._name)
