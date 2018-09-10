import socket
import socketserver
import os.path
import base64
from datetime import datetime

server_name = "Python Light-Weight Server"
date_formatting = "%a, %d %b %Y %H:%M:%S KST"
home_dir = os.path.expanduser("~") + "\\webroot"

image_list = ['gif', 'jpg', 'jpeg', 'png', 'svg']
image_mime = ['image/gif', 'image/jpeg', 'image/jpeg', 'image/png', 'image/svg']

class ServerHandler(socketserver.BaseRequestHandler):
    def handle(self):
        socket = self.request

        data = socket.recv(65535)
        request_data = data.decode().split()

        request_method = request_data[0]
        request_object = home_dir + request_data[1]
        request_version = request_data[2]

        sendEncoded = True

        if request_object[len(request_object) - 1] == '/':
            request_object += "index.html"

        if request_method == "GET":
            if (os.path.exists(request_object)):
                response_object = request_object.split('.')
                
                if response_object[1] == 'html':
                    file = open(request_object, 'r', encoding='utf8')
                    file_content = file.read()
                    response_data = "{0} 200 OK\nServer: {1}\nDate: {2}\nContent-Type: text/html\n\n{3}".format(request_version, server_name, datetime.now().strftime(date_formatting), file_content)
                    file.close()

                elif response_object[1] == 'css':
                    file = open(request_object, 'r', encoding='utf8')
                    file_content = file.read()
                    response_data = "{0} 200 OK\nServer: {1}\nDate: {2}\nContent-Type: text/css\n\n{3}".format(request_version, server_name, datetime.now().strftime(date_formatting), file_content)
                    file.close()

                elif response_object[1] == 'js':
                    file = open(request_object, 'r', encoding='utf8')
                    file_content = file.read()
                    response_data = "{0} 200 OK\nServer: {1}\nDate: {2}\nContent-Type: text/javascript\n\n{3}".format(request_version, server_name, datetime.now().strftime(date_formatting), file_content)
                    file.close()

                elif response_object[1] in image_list:
                    file = open(request_object, "rb")
                    file_size = os.path.getsize(request_object)
                    file_content = file.read(file_size)
                    response_data = "{0} 200 OK\nServer: {1}\nDate: {2}\nContent-Type: {3}\nContent-Length: {4}\n\n".format(request_version, server_name, datetime.now().strftime(date_formatting), image_mime[image_list.index(response_object[1])], file_size)
                    socket.send(response_data.encode())
                    socket.send(file_content)
                    sendEncoded = False
                    file.close()

            else:
                file = open(home_dir + "/404.html", "r", encoding='utf8')
                file_content = file.read()
                response_data = "{0} 404 Not Found\nServer: {1}\nDate: {2}\n\n{3}".format(request_version, server_name, datetime.now().strftime(date_formatting), file_content)
                file.close()
        else:
            response_data = "{0} 405 Method Not Allowed\nServer: {1}\nDate: {2}\n".format(request_version, server_name, 
            datetime.now().strftime('%a, %d %b %Y %H:%M:%S KST'))

        if sendEncoded:
            socket.send(response_data.encode())
        
        socket.close()

if __name__ == '__main__':
    server = socketserver.TCPServer(('localhost', 12345), ServerHandler)
    server.serve_forever()