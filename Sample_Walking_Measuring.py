import logging
import asyncio
import time

#libraries for connecting alphamini
import mini.mini_sdk as Mini
from mini.dns.dns_browser import WiFiDevice

#libraries for alphamini to move.
from mini.apis.api_action import MoveRobot, MoveRobotDirection, MoveRobotResponse
from mini.apis.base_api import MiniApiResultType

#libraries for measuring distances from the object 
from mini.apis.api_observe import ObserveInfraredDistance
from mini.pb2.codemao_observeinfrareddistance_pb2 import ObserveInfraredDistanceResponse

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



async def forward_move_robot(i):
    block: MoveRobot = MoveRobot(step=i, direction=MoveRobotDirection.FORWARD)
    (resultType, response) = await block.execute()
    print(f'test_move_robot result:{response}')

    assert resultType == MiniApiResultType.Success, 'test_move_robot timetout'
    assert response is not None and isinstance(response, MoveRobotResponse), 'test_move_robot result unavailable'
    assert response.isSuccess, 'move_robot failed'


async def stop_robot():
    block: MoveRobot = MoveRobot(step=0, direction=MoveRobotDirection.FORWARD)
    (resultType, response) = await block.execute()
    print(f'test_move_robot result:{response}')

    assert resultType == MiniApiResultType.Success, 'test_move_robot timetout'
    assert response is not None and isinstance(response, MoveRobotResponse), 'test_move_robot result unavailable'
    assert response.isSuccess, 'move_robot failed'

async def turn_robot():
    block: MoveRobot = MoveRobot(step=3, direction=MoveRobotDirection.LEFTWARD)
    (resultType, response) = await block.execute()
    print(f'test_move_robot result:{response}')

    assert resultType == MiniApiResultType.Success, 'test_move_robot timetout'
    assert response is not None and isinstance(response, MoveRobotResponse), 'test_move_robot result unavailable'
    assert response.isSuccess, 'move_robot failed'

async def T_ObserveInfraredDistance():
 
    observer: ObserveInfraredDistance = ObserveInfraredDistance()

    def handler(msg: ObserveInfraredDistanceResponse):
        print("distance = {0}".format(str(msg.distance)))
        time.sleep(2)
        if msg.distance < 500:
            observer.stop()
            await asyncio.run(forward_move_robot)
        #   asyncio.create _task(turn())

    observer.set_handler(handler)
    observer.start()
    await asyncio.sleep(0)


async def stop():
    await stop_robot()

async def turn():
    await turn_robot()

async def move_forward():
    await forward_move_robot(1)


if __name__ == '__main__' :
    device: WiFiDevice = asyncio.get_event_loop().run_until_complete(get_device_by_name())
    if device:
        asyncio.get_event_loop().run_until_complete(connection(device))
        asyncio.get_event_loop().run_until_complete(start_run_program())
        asyncio.get_event_loop().run_until_complete(T_ObserveInfraredDistance())
        #asyncio.run(forward_move_robot(10))
        asyncio.get_event_loop().run_forever()

