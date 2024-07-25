import asyncio
import logging

from mini import mini_sdk as MiniSdk
from mini.apis.api_action import GetActionList, GetActionListResponse, RobotActionType
from mini.apis.api_action import MoveRobot, MoveRobotDirection, MoveRobotResponse
from mini.apis.api_action import PlayAction, PlayActionResponse

from mini.dns.dns_browser import WiFiDevice


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


# async def test_get_action_list():
#     """Get action list demo

#      Get the list of built-in actions of the robot and wait for the reply result

#     """
#     # action_type: INNER refers to the unmodifiable action file built into the robot, and CUSTOM is an action that can be modified by the developer placed in the sdcard/customize/action directory
#     block: GetActionList = GetActionList(action_type=RobotActionType.INNER)
#     # response:GetActionListResponse
#     (resultType, response) = await block.execute()

#     print(f'test_get_action_list result:{response}')

#     assert resultType == MiniApiResultType.Success, 'test_get_action_list timetout'
#     assert response is not None and isinstance(response,
#                                                GetActionListResponse), 'test_get_action_list result unavailable'
#     assert response.isSuccess, 'get_action_list failed'





async def forward_move_robot():
   
    block: MoveRobot = MoveRobot(step=3, direction=MoveRobotDirection.LEFTWARD)
    (resultType, response) = await block.execute()
    print(f'test_move_robot result:{response}')

    assert resultType == MiniApiResultType.Success, 'test_move_robot timetout'
    assert response is not None and isinstance(response, MoveRobotResponse), 'test_move_robot result unavailable'
    assert response.isSuccess, 'move_robot failed'


async def main():
    device: WiFiDevice = await get_device_by_name()
    if device:
        await MiniSdk.connect(device)
        await MiniSdk.enter_program()
        await forward_move_robot()
        await MiniSdk.quit_program()
        await MiniSdk.release()


if __name__ == '__main__':
    asyncio.run(main())
