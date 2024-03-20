import json

from tornado import web, ioloop


class IndexHandler(web.RequestHandler):
    # def initialize(self, db=None):
    #     # 初始化函数
    #     self.db = db

    # def prepare(self):
    #     # 打印日志 打印文件
    #     print("prepare1")

    # def on_finish(self) -> None:
    #     # 清理内容
    #     print("on_finish")

    async def get(self):
        print("prepare2")
        name = self.get_argument()  # http://xxxxxx/?q=123
        names = self.get_arguments()  # http://xxxxxx/?q=123&q=456&q=789
        # name = self.get_query_argument("q")  # http://xxxxxx/?q=123
        # names = self.get_query_arguments("q")  # http://xxxxxx/?q=123&q=456&q=789
        print(name)
        print(names)
        self.write("get函数")

    async def post(self):
        # 获取表单数据
        # get_argument()  get_arguments() 既可以用于parms也可以用于body
        # 如果是get_argument() 会默认从请求体中获取
        # 如果是get_arguments() 会默认从params和body中获取

        name = self.get_body_argument("q")
        names = self.get_body_arguments("q")
        # name = self.get_argument()
        # names = self.get_arguments()
        args = self.request.body.decode("utf-8")
        json.loads(args)
        print(name)
        print(names)
        self.write("post函数")
        await self.finish("'msg': '成功访问'")

    # 还有put delete head options等方法


if __name__ == "__main__":
    app = web.Application([(r"/", IndexHandler)], debug=True)
    app.listen(8888)
    ioloop.IOLoop.current().start()
