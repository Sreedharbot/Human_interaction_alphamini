import logging
import asyncio

import mini.mini_sdk as Mini
from mini.dns.dns_browser import WiFiDevice


Mini.set_log_level(logging.INFO)
Mini.set_log_level(logging.DEBUG)
Mini.set_robot_type(Mini.RobotType.EDU)


async def get_device_by_name():
    result: WiFiDevice = await Mini.get_device_by_name("00418", 10)
    print(f"test_get_device_by_name result:{result}")
    return result


async def connection(dev: WiFiDevice) -> bool:
    return await Mini.connect(dev)


async def start_run_program():
    await Mini.enter_program()


async def shutdown():
    await Mini.quit_program()
    await Mini.release()



async def main():
    device: WiFiDevice = await get_device_by_name()
    if device:
        await connection(device)
        await start_run_program()
        await shutdown()

if __name__ == '__main__' :
    asyncio.run(main())

#sample Code 1







