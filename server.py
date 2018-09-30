import handler
import server_logger
import sys
import time
import uuid
import uwsgi

logger = server_logger.get_logger('server')

# initializes Handler class needed to handle API requests
handler.factory.get_instance()

def handle_v1_hello_get(request_id, env):
    message = handler.factory.get_instance().get_greeting_message()

    logger.info("GET request for RequestId: %s returned message %s", request_id, message)

    return 200, message


def handle_v1_hello(request_method, resource_requested, request_id, env):
    try:
        logger.info('%s - %s %s Hello V1', request_id, request_method, resource_requested)

        if request_method == 'GET':
            return handle_v1_hello_get(request_id, env)
        else:
            logger.warn('Unknown hello request method received: %s', request_method)
            return '404 Method Not Allowed', [('Content-Type', 'application/json; charset=utf-8'), ('Allow', 'GET')]
    except:
        logger.exception('%s Error handling V1 hello API', request_id)
        return '500 Internal Server Error', [('Content-Type', 'application/json; charset=utf-8')]


def handle_v1_status(request_method, request_id):
    logger.info('%s - %s Status V1', request_id, request_method)

    response_body = []

    if request_method != 'GET':
        logger.warn('Unknown status request method received: %s', request_method)
        return 404, ["Method Not Allowed"]

    logger.info("Health check request received")

    status_code = handler.factory.get_instance().get_health_status()
    if status_code == 200:
        response_body.append("Healthy")
    else:
        response_body.append("Unhealthy")

    return status_code, response_body


def application(env, start_response):
    """uWSGI server handler entry point"""
    start_time = time.time()
    request_method = env.get('REQUEST_METHOD')
    request_path = env.get('PATH_INFO')
    request_id = str(uuid.uuid1())

    try:
        if request_path and request_path.startswith('/v1/hello'):
            (status, response_body) = handle_v1_hello(request_method, request_path, request_id, env)
        elif request_path and request_path.startswith('/v1/status'):
            (status, response_body) = handle_v1_status(request_method, request_id)
        else:
            logger.info('Unknown request uri received: %s', request_path)
            (status, response_body) = ('400 Bad Request', [])
    except:
        logger.exception('%s Unexpected exception in request handler', env.get('X-REQUESTID', ''))
        (status, response_body) = ('500 Internal Server Error', [])
    finally:
        end_time = time.time()
        request_duration_in_ms = str(int((end_time - start_time) * 1000))

        logger.info('%s - %s %s Response [%s] after %sms', request_id, request_method, request_path, status, request_duration_in_ms)
        start_response(str(status), [])

        return response_body


def shutdown():
    handler.factory.get_instance().shutdown()
    logger.info('Successfully shutdown uWSGI server')
    sys.exit(0)


# Catches the SIGTERM signal that gets called during service stop.
# Calls the shutdown function to gracefully stop the service.
# Works with Control-C for MacOS
uwsgi.atexit = shutdown
