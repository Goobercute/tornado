from tornado import web, ioloop
from tornado.options import define, options, parse_command_line

# 定义key 接受命令行参数  --port=8887
define("port", default=8888, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode", type=bool)

parse_command_line()  # 解析命令行参数


class MainHandler(web.RequestHandler):
    async def get(self):  # 用async 协程
        self.write("Hello, world")


if __name__ == "__main__":
    app = web.Application([(r"/", MainHandler)], debug=options.debug)
    app.listen(options.port)  # 从命令行接受参数
    ioloop.IOLoop.current().start()
