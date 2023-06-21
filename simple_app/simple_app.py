HELLO_WORLD = b"Hello world!\n"
from urllib.parse import parse_qs

def simple_app(environ, start_response):
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0

    request_body = environ['wsgi.input'].read(request_body_size)
    d = parse_qs(environ['QUERY_STRING'])
    print(environ['QUERY_STRING'])
    print(d)

    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    response_body = ('GET: ' + str(d) + '\n' + 'POST: ' + str(request_body) + '\n').encode('utf8')

    start_response(status, response_headers)
    return [response_body]

application = simple_app
