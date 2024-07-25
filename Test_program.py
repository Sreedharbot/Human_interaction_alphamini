
import asyncio
import logging


import mini.mini_sdk as MiniSdk
from mini.apis.api_observe import ObserveInfraredDistance
from mini.dns.dns_browser import WiFiDevice
from mini.pb2.codemao_observeinfrareddistance_pb2 import ObserveInfraredDistanceResponse

MiniSdk.set_log_level(logging.INFO)
MiniSdk.set_log_level(logging.DEBUG)
MiniSdk.set_robot_type(MiniSdk.RobotType.EDU)


async def get_device_by_name():
    result: WiFiDevice = await MiniSdk.get_device_by_name("00418", 10)
    print(f"test_get_device_by_name result:{result}")
    return result

async def connection(dev: WiFiDevice) -> bool:
    return await MiniSdk.connect(dev)

async def start_run_program():
    await MiniSdk.enter_program()

async def test_ObserveInfraredDistance():

    observer: ObserveInfraredDistance = ObserveInfraredDistance()


    def handler(msg: ObserveInfraredDistanceResponse):
        print("distance = {0}".format(str(msg.distance)))

    observer.set_handler(handler)
    observer.start()
    await asyncio.sleep(0)




if __name__ == '__main__':
    device: WiFiDevice = asyncio.get_event_loop().run_until_complete(get_device_by_name())
    if device:
        asyncio.get_event_loop().run_until_complete(connection(device))
        asyncio.get_event_loop().run_until_complete(start_run_program())
        asyncio.get_event_loop().run_until_complete(test_ObserveInfraredDistance())
        asyncio.get_event_loop().run_forever()
