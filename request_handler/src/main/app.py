import sys

if("/" not in sys.path):
    sys.path.append("/")
    sys.path.append("/request_handler")
print(sys.path)

from request_handler.src.main.server.server import Server




if __name__ == "__main__":
    server = Server()
    server.start()


