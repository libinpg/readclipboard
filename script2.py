import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def send_request(session, url, data):
    """发送单个请求并返回响应时间"""
    start_time = time.time()
    response = session.post(url, json=data)
    response_time = time.time() - start_time
    return response.status_code, response_time

def main():
    # LLM服务器的地址
    url = "http://localhost:1234/v1/chat/completions"

    # 请求数据
    data = {
        "messages": [
            {"role": "system", "content": "Always answer in rhymes."},
            {"role": "user", "content": "Introduce yourself."}
        ],
        "temperature": 0.7,
        "max_tokens": -1,
        "stream": False
    }

    # 并发请求的数量
    num_requests = 50

    # 使用Session保持连接
    with requests.Session() as session:
        with ThreadPoolExecutor(max_workers=num_requests) as executor:
            # 提交所有请求
            futures = [executor.submit(send_request, session, url, data) for _ in range(num_requests)]

            # 等待所有请求完成并计算指标
            start_time = time.time()
            response_times = []
            for future in as_completed(futures):
                status_code, response_time = future.result()
                response_times.append(response_time)
                print(f"Status Code: {status_code}, Response Time: {response_time} seconds")

            total_time = time.time() - start_time

    # 计算和打印性能指标
    average_response_time = sum(response_times) / len(response_times)
    print(f"Total Time for {num_requests} requests: {total_time} seconds")
    print(f"Average Response Time: {average_response_time} seconds")

if __name__ == "__main__":
    main()
