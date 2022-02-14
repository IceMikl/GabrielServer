import sys

if ("/" not in sys.path):
    sys.path.append("/")
    sys.path.append("/db_manager")
print(sys.path)

from db_manager.src.main.server.server import Server

if __name__ == "__main__":
    server = Server()
    server.start()



