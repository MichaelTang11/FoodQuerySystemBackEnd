import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import logging
from Common.GetServiceIP import ip
from Common.DBConnection import con
from url import url
import time
import threading


def main():
    LOG_FORMAT = "%(asctime)s === %(module)s === %(funcName)s === %(levelname)s === %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
    application = tornado.web.Application(url, cookie_secret="dj2SOjWryYSaDiFjy2s4cjj")
    http_server = tornado.httpserver.HTTPServer(application)
    tornado.options.parse_command_line()
    http_server.listen(1000)
    print('Development server is running at http://' + ip + ':1000')
    threading.Thread(target=keep_connection_alive).start()
    tornado.ioloop.IOLoop.instance().start()


def keep_connection_alive():
    while True:
        con.ping()
        time.sleep(600)


if __name__ == '__main__':
    main()
