from tornado import web, ioloop


class IndexHandler(web.RequestHandler):
    def get(self):
        print("11111")
        print(self.reverse_url("index"))
        self.redirect("/")


if __name__ == "__main__":
    """ 
    This is the main entry point for the application.
    """
    app = web.Application(
        [
            web.URLSpec("/", IndexHandler, name="index"),  # 方法1 适合跳转后处理请求
            web.URLSpec("/index/", web.RedirectHandler, {"url": "/"}),  # 方法2  适合直接跳转
        ],
        debug=True,
    )
    app.listen(8888)
    ioloop.IOLoop.current().start()
