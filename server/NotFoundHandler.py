import tornado


class NotFoundHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_status(404)
        self.write("404: Not Found")
