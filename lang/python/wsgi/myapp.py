def app(env, start_response):
    data = 'Hello world'
    start_response('200 OK', [
        ('Content-Type', 'text/plain'),
        ('Content-Length', len(data))
        ])
    return iter([data])
