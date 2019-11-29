"""Async helper"""
import asyncio
from concurrent import futures

executor = futures.ThreadPoolExecutor(max_workers=5)


async def async_call(blocking_func, *args):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        executor, blocking_func, *args
    )
    return result
