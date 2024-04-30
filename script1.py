import pyperclip
import time
from zhipuai import ZhipuAI
import pyttsx3

# 请填写你的APIKey
api_key = "ffc9d43b0e8c632864622509da627302.EfQ97Gf6iFwcDLly"
client = ZhipuAI(api_key=api_key)

# 初始化语音引擎
engine = pyttsx3.init()

def speak_text(text):
    # 设置语音引擎的语速
    engine.setProperty('rate', 150)
    # 朗读文本
    engine.say(text)
    # 执行朗读
    engine.runAndWait()

def call_api_with_clipboard_content():
    # 获取当前剪切板内容
    clipboard_content = pyperclip.paste()
    
    # 构建API请求的消息
    messages = [
        {"role": "system", "content": "你作为英义易通助手，根据我发送的内容，用简单的英文解释意思，同时给出例句"},
        {"role": "user", "content": clipboard_content},
    ]
    
    # 调用API
    response = client.chat.completions.create(
        model="glm-4",
        messages=messages,
        stream=True,
    )
    
    # 打印API的响应，并朗读
    spoken_text = ""
    for chunk in response:
        if chunk.choices[0].delta.content:
            spoken_text += chunk.choices[0].delta.content
            print(chunk.choices[0].delta.content)
    speak_text(spoken_text)

# 检查剪切板内容是否发生变化，并在发生变化时调用API
def monitor_clipboard_and_call_api():
    last_clipboard_content = ""
    while True:
        current_clipboard_content = pyperclip.paste()
        
        if current_clipboard_content != last_clipboard_content:
            print("剪切板内容已更新，调用API解释内容...")
            call_api_with_clipboard_content()
            last_clipboard_content = current_clipboard_content
        
        time.sleep(1)

# 运行监控
monitor_clipboard_and_call_api()
