from asyncio import Queue
import asyncio
from logging import info, debug
from events import sort_done_event, detect_done_event
import os
import socket
from values import SORTER_IP
import rpyc

def is_computer_online(addr):
    return True if os.system("ping -n 1 -w 1000 " + addr) == 0 else False

def is_port_open(addr, port):
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    location = (addr, port)
    result_of_check = a_socket.connect_ex(location)

    result = False

    if result_of_check == 0:
       debug("Port is open")
       result = True
    else:
        debug("Port is not open")
    a_socket.close()

    return result

async def main(globalstate, pipe: Queue):
    while True:
        await detect_done_event.wait()
        detect_done_event.clear()

        info("Hello from Sorting, using IP " + SORTER_IP)
        if not is_computer_online(SORTER_IP):
            info("Sorter Computer isn't online, skipping")

            print("Working ")
            sort_done_event.set()
            continue

        debug("Sorter online")

        tryno = 1

        while True:
            if is_port_open(SORTER_IP, 18861):
                break

            tryno +=1
            info("Retrying Connect; n="+str(tryno))

        
        conn = rpyc.connect("192.168.188.24", 18861, config={
            "sync_request_timeout": 3600
        })
        
        eventloop = asyncio.get_event_loop()
        await eventloop.run_in_executor(None, conn.root.sort(globalstate["current_part"]))

        