#  coding: utf-8 
import mimetypes
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos, Junyao Cui
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)

        root = "./www"
        response_ = None
        method, path_, http_ = self.parse_request(self.data)
        
        path = root + path_

        if path_[-1] == "/":
            path = path + "index.html"

        if method == "GET":
            if os.path.isdir(path) and path_[-1] != "/":
                    # redirect
                    response_ = "HTTP/1.1 301 Moved Permanently\r\nLocation:"+path_+"/"+"\r\n\r\n"
            elif os.path.isfile(path):
                ext_type = self.get_ext(path)
                if ext_type != None:
                    content = self.get_content(path)
                    if content != "ERROR":
                        response_ = "HTTP/1.1 200 OK\r\nContent-Type: " + ext_type + "\r\n\r\n" + content + "\r\n"
                    else:
                        response_ = "HTTP/1.1 404 Not Found\r\nConnection: close\r\n"
                else:
                    response_ = "HTTP/1.1 404 Not Found\r\nConnection: close\r\n"
            else:
                response_ = "HTTP/1.1 404 Not Found\r\nConnection: close\r\n"
        else:
            response_ = "HTTP/1.1 405 Method Not Allowed\r\nConnection: close\r\n"

        self.request.sendall(bytearray(response_,'utf-8'))

    # https://stackoverflow.com/questions/18563664/socketserver-python
    def parse_request(self, data):
        # https://stackoverflow.com/questions/606191/convert-bytes-to-a-string
        lines = data.decode("utf-8").splitlines()
        
        method, path, http_ = lines[0].split()
        return method, path, http_
    
    def get_ext(self, path_):
        root, ext = os.path.splitext(path_)
        if ext == ".html":
            return "text/html"
        elif ext == ".css":
            return "text/css"
        else:
            return None

    def get_content(self, path_):
        try:
            file = open(path_, "r")
        except Exception:
            return "ERROR"
        
        content = file.read()
        file.close()
        return content
    

        

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
