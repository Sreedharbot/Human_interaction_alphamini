import logging
import asyncio

import mini.mini_sdk as Mini
from mini.dns.dns_browser import WiFiDevice

from mini.apis import errors
from mini.apis.api_sound import StartPlayTTS, StopPlayTTS, ControlTTSResponse
from mini.apis.api_sound import StopAllAudio, StopAudioResponse
from mini.apis.base_api import MiniApiResultType




Mini.set_log_level(logging.INFO)
Mini.set_log_level(logging.DEBUG)
Mini.set_robot_type(Mini.RobotType.EDU)



async def _play_tts():
    block: StartPlayTTS = StartPlayTTS(text="hello! i'm Aravind, test, test, test")
    # return  (), response is `ControlTTSResponse`
    (resultType, response) = await block.execute()
    print(f'{response}')
    return()



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

async def test_stop_play_tts():

    block: StartPlayTTS = StartPlayTTS(is_serial=False, text="Hello, I am Prabu, la la la la la la la la la la la la la la la la la la la la la la la")
    await block.execute()
    await asyncio.sleep(3)

    (resultType, response) = await StopPlayTTS().execute()

    print(f'test_stop_play_tts result: {response}')
    print('resultCode = {0}, error = {1}'.format(response.resultCode, errors.get_speech_error_str(response.resultCode)))

async def main():
    device: WiFiDevice = await get_device_by_name()
    if device:
        await connection(device)
        await start_run_program()
        await _play_tts()
        await test_stop_play_tts()
        await shutdown()

if __name__ == '__main__' :
    asyncio.run(main())

#sample Code 1







