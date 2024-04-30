import pyperclip
import time
import openai
import pyttsx3

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
    
    # 设置OpenAI客户端的本地服务器地址
    openai.api_base = "http://localhost:1234/v1"
    
    # 调用API
    completion = openai.ChatCompletion.create(
        model="local-model",  # 替换为您本地模型的名字
        messages=messages,
        temperature=0.7,
    )
    
    # 打印API的响应，并朗读
    response_message = completion.choices[0].message
    print(response_message.content)
    speak_text(response_message.content)

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
