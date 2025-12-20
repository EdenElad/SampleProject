from __future__ import annotations

import asyncio
import json
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, TypedDict

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


@dataclass
class User:
    id: int
    name: str
    email: Optional[str] = None  # typing


class Config(TypedDict):
    env: str
    debug: bool


@contextmanager
def timer(label: str):
    start = time.perf_counter()
    try:
        yield
    finally:
        logging.info("%s took %.3fs", label, time.perf_counter() - start)


def cpu_work(x: int) -> int:
    return x * x


async def main():
    user = User(1, "Elad")
    cfg: Config = {"env": "local", "debug": True}

    # pathlib + json
    p = Path("config.json")
    p.write_text(json.dumps(cfg), encoding="utf-8")
    loaded = json.loads(p.read_text(encoding="utf-8"))

    logging.info("user=%s loaded=%s", user, loaded)

    # concurrent.futures
    with timer("thread pool"):
        with ThreadPoolExecutor() as ex:
            results = list(ex.map(cpu_work, range(5)))
    logging.info("results=%s", results)

    from concurrent.futures import as_completed

    with ThreadPoolExecutor() as ex:
        futures = [ex.submit(cpu_work, i) for i in range(5)]

        for fut in as_completed(futures):
            result = fut.result()
            print("first available result:", result)  # פה תעשה מה שאתה רוצה

    # asyncio
    await asyncio.sleep(0.1)
    logging.info("async done")


    async def a():
        for i in range(3):
            print("A", i)
            time.sleep(0.2)  # ❌ חוסם את הלופ

    async def b():
        for i in range(3):
            print("B", i)
            await asyncio.sleep(0.2)

    asyncio.run(await asyncio.gather(a(), b()))

import asyncio

async def a():
    await asyncio.sleep(0.2)

async def b():
    await asyncio.sleep(0.1)
if __name__ == "__main__":
    asyncio.run(main())
