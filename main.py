import ntplib
import time
import datetime
import sys
import os

# NTP服务器列表
ntp_servers = [
    'time.windows.com',
    'time.apple.com',
    'ntp2.nim.ac.cn',
    'ntp1.nim.ac.cn',
    'ntp.ntsc.ac.cn',
    'ntp.tuna.tsinghua.edu.cn',
    'time.cloudflare.com'
]


def ntp_time(_ntp_servers):
    while True:
        for ntp_server in _ntp_servers:
            try:
                # 创建一个NTP客户端
                client = ntplib.NTPClient()

                # 向NTP服务器发送请求
                response = client.request(ntp_server)

                # 获取NTP服务器返回的时间戳
                _ntp_time = response.tx_time

                # 将NTP时间戳转换为本地时间
                local_time = time.localtime(_ntp_time)

                # 格式化输出时间
                print(f"NTP Server: {ntp_server}")
                print(f"Adjusted Time: {time.strftime('%Y-%m-%d %H:%M:%S', local_time)}")

                return local_time
            except Exception as _e:
                # 处理其他未捕获的异常
                print(f"An unexpected error occurred: {str(_e)}")
                print(f"Failed to get time from {ntp_server}. Trying the next server...")
                continue


def set_system_time(local_time):
    # 将时间元组转换为datetime对象
    dt = datetime.datetime(*local_time[:6])

    # 格式化时间字符串
    time_string = dt.strftime('%Y-%m-%d %H:%M:%S')

    if sys.platform == 'win32':
        # Windows系统
        os.system(f'date {dt.strftime("%Y-%m-%d")}')
        os.system(f'time {dt.strftime("%H:%M:%S")}')
    elif sys.platform == 'linux' or sys.platform == 'darwin':
        # Linux或macOS系统
        os.system(f'sudo date -s "{time_string}"')
    else:
        print("Unsupported operating system.")


if __name__ == '__main__':
    try:
        adjusted_time = ntp_time(ntp_servers)
        set_system_time(adjusted_time)
    except Exception as e:
        print(str(e))
    input("按任意键退出...")
