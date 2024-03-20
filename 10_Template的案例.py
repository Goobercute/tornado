from tornado import web, ioloop


class MainHandler(web.RequestHandler):
    def get(self):
        self.write("Hello, world123")


if __name__ == "__main__":
    """ 
    This is the main entry point for the application.
    """
    app = web.Application([(r"/", MainHandler)], debug=True)
    app.listen(8888)
    ioloop.IOLoop.current().start()
