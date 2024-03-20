from tornado import web, ioloop, template


class IndexHandler(web.RequestHandler):
    def get(self):
        args = "Template"
        self.write(f"<h1>Hello, {args}</h1>")


class IndexHandler2(web.RequestHandler):
    def get(self):
        args = "Template2"
        t = template.Template("<h2>Hello, {{args}}</h2>")
        self.write(t.generate(args=args))


class IndexHandler3(web.RequestHandler):
    def get(self):
        args = "Template3"
        loder = template.Loader("./template/")
        self.write(loder.load("template.html").generate(args=args))


class IndexHandler4(web.RequestHandler):
    def get(self):
        args = "Template4"
        self.render("./template/template.html", args=args)


if __name__ == "__main__":
    app = web.Application(
        [
            (r"/1/", IndexHandler),
            (r"/2/", IndexHandler2),
            (r"/3/", IndexHandler3),
            (r"/4/", IndexHandler4),
        ],
        debug=True,
    )
    app.listen(8888)
    ioloop.IOLoop.current().start()
