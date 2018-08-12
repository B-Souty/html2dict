#! /usr/bin/env python3

import sys
from http.server import BaseHTTPRequestHandler, HTTPServer


TEST_HTML_FILE = sys.argv[1]
TEST_HTML_STRING = open(TEST_HTML_FILE, 'r').read()


class HTTPServer_RequestHandler(BaseHTTPRequestHandler):

    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Send message back to client
        message = TEST_HTML_STRING
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return


def start_server():

    print('starting server...')
    server_address = ('127.0.0.1', 8081)
    httpd = HTTPServer(server_address, HTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()



if __name__ == "__main__":
    start_server()
