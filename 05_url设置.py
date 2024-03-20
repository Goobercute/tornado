from tornado import web, ioloop


class MainHandler(web.RequestHandler):
    async def get(self):
        self.write("Hello, world1")


class MainHandler2(web.RequestHandler):
    async def get(self):
        self.write("index2")


class MainHandler3(web.RequestHandler):
    async def get(self):
        self.write("index3")


class MainHandler4(web.RequestHandler):
    async def get(self, num):
        self.write("id ")
        self.write(num)


class MainHandler5(web.RequestHandler):
    async def get(self, str):
        self.write("username ")
        self.write(str)


class MainHandler6(web.RequestHandler):
    async def get(self, name, pwd):
        self.write(f"username {name} and password {pwd}")


class redirectHandler(web.RequestHandler):
    async def get(self, ):
        self.redirect(self.reverse_url("3"))


class redirectHandler2(web.RequestHandler):
    def initialize(self, name, pwd):
        self.name = name
        self.pwd = pwd
        print(name, "===========", pwd)

    async def get(self):
        self.redirect(self.reverse_url("3"))


args = {
    "name": "zhangsan",
    "pwd": "123"
}

if __name__ == "__main__":
    """ 
    This is the main entry point for the application.
    """
    app = web.Application(
        [
            (r"/", MainHandler),
            (r"/2/", MainHandler2),  # 末尾加上/，访问时也要加上/
            web.URLSpec(r"/3/?", MainHandler3, name="3"),
            (r"/4/(\d+)/?", MainHandler4),
            (r"/5/(\w+)/?", MainHandler5),  # 匹配顺序是从上到下
            # (r"/6/(\w+)/(\w+)/?", MainHandler6),
            (r"/6/(?P<name>\w+)/(?P<pwd>\w+)/?", MainHandler6),
            web.URLSpec(r"/redirect", redirectHandler),
            web.URLSpec(r"/redirect2", redirectHandler2, args),
        ],
        debug=True,  # 末尾加上/，访问时也要加上/
    )
    app.listen(8888)
    ioloop.IOLoop.current().start()

''' 
url编写规则
    1. 完整匹配
    2. 正则匹配
    3. 通过url传递参数
    4. 重定向（1. url反转 name属性 reverse_url 2. web.URLSpec）
'''
