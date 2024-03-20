import time

from tornado import web, ioloop


class MainHandler(web.RequestHandler):
    def get(self):
        time.sleep(3)
        self.write("Hello, world1")


class MainHandler2(web.RequestHandler):
    def get(self):
        self.write("Hello, world2")


if __name__ == "__main__":
    """ 
    This is the main entry point for the application.
    """
    app = web.Application([
        (r"/", MainHandler),
        (r"/2", MainHandler2)
    ], debug=True)  # 列表装的路由，sleep会让两个handler都等待
    app.listen(8888)
    ioloop.IOLoop.current().start()
