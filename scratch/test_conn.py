import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5)
try:
    s.connect(('10.1.0.4', 443))
    print('SUCCESS: Connected to 10.1.0.4:443')
    s.close()
except Exception as e:
    print('FAILED:', e)

