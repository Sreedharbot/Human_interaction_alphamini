import asyncio
import logging

import mini.mini_sdk as Mini
from mini.dns.dns_browser import WiFiDevice

from mini.apis.api_observe import ObserveSpeechRecognise
from mini.apis.api_sound import StartPlayTTS, StopPlayTTS, ControlTTSResponse
from mini.pb2.codemao_speechrecognise_pb2 import SpeechRecogniseResponse

#from test.test_connect import test_connect, shutdown
#from test.test_connect import test_get_device_by_name, test_start_run_program

a = None

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


# 测试监听语音识别
async def test_speech_recognise():
    """

    # SpeechRecogniseResponse.text

    # SpeechRecogniseResponse.isSuccess

    # SpeechRecogniseResponse.resultCode

    """
    # 语音监听对象
    observe: ObserveSpeechRecognise = ObserveSpeechRecognise()

    # 处理器
    # SpeechRecogniseResponse.text
    # SpeechRecogniseResponse.isSuccess
    # SpeechRecogniseResponse.resultCode
    def handler(msg: SpeechRecogniseResponse):
        print(f'=======handle speech recognise:{msg}')
        print("{0}".format(str(msg.text)))

        # if str(msg.text)[-1].isalpha() is False:
        #     if str(msg.text)[:-1].lower() == "Hello":
        #         asyncio.create_task(__tts())
 
        if str(msg.text).lower() == "Hello":
            # 监听到"悟空", tts打个招呼
            a = 1
            return a
            
         
        elif str(msg.text).lower() == "stop":
            # 监听到结束, 停止监听
            observe.stop()
            # 结束event_loop
            asyncio.get_running_loop().run_in_executor(None, asyncio.get_running_loop().stop)

    observe.set_handler(handler)
    observe.start()
    
    await asyncio.sleep(0)

async def test():
        task = asyncio.create_task(__tts)
        await task


async def __tts():
    block: StartPlayTTS = StartPlayTTS(is_serial=False,text="Hello I'm Chiti 'The Robot' ")
    await block.execute()
    await asyncio.sleep(2.2)
    (resultType, response) = await StopPlayTTS().execute()
    print(f'test_stop_play_tts result: {response}')
    return()



if __name__ == '__main__':
    device: WiFiDevice = asyncio.get_event_loop().run_until_complete(get_device_by_name())
    if device:
        asyncio.get_event_loop().run_until_complete(connection(device))
        asyncio.get_event_loop().run_until_complete(start_run_program())
        asyncio.get_event_loop().run_until_complete(test_speech_recognise())
        if a == 1:
            asyncio.run(test())
            a = 0
        # 定义了事件监听对象,必须让event_loop.run_forver()
        asyncio.get_event_loop().run_forever()
        asyncio.get_event_loop().run_until_complete(shutdown())
