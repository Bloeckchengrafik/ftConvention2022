import asyncio
from concurrent.futures import ThreadPoolExecutor
import sys
import keyboard
import easygui

executor = ThreadPoolExecutor(1, "adialogbox")


def maximize_console():
    keyboard.press('f11')


async def ainput(string: str) -> str:
    await asyncio.get_event_loop().run_in_executor(
        None, lambda s=string: sys.stdout.write(s+' '))
    sys.stdout.flush()
    return await asyncio.get_event_loop().run_in_executor(
        None, sys.stdin.readline)


async def adialogbox(prompt: str = "") -> str:
    return await asyncio.get_event_loop().run_in_executor(executor, easygui.enterbox, prompt)


def prRed(skk): return "\033[91m {}\033[00m" .format(skk)


def prCyan(skk): return "\033[96m {}\033[00m" .format(skk)
