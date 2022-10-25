# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
from MyAPI import MyAPI

hostName = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        api = MyAPI()
        rs = api.get()
        self.send_response(200)
        self.send_header("Content-type", "application/json charset=utf-8")
        self.end_headers()
        self.wfile.write(bytes(rs, 'utf-8'))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
