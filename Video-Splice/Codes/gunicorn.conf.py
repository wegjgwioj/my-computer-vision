'''Gunicorn 配置文件'''
# gunicorn.conf.py
workers = 4            # 工作进程数，建议设置为 (2 x CPU核心数) + 1
bind = '0.0.0.0:5000'  # 监听所有 IP 的 5000 端口
timeout = 120          # 超时时间（秒），防止请求处理过长被超时断开