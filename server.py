import json
import random
from http.server import HTTPServer, BaseHTTPRequestHandler

host = ('0.0.0.0', 8080)


def test_completed():
    return random.choice([True, False])


def get_test_report():
    return {'status': 'NOT OK', 'massage': 'IN TESTING'}


class Request(BaseHTTPRequestHandler):
    def do_GET(self):
        if test_completed():
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(get_test_report()).encode())
        else:
            self.send_response(422)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(get_test_report()).encode())


if __name__ == '__main__':
    server = HTTPServer(host, Request)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()
