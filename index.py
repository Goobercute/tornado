from tornado import web, ioloop

from handlers.host_handler import Host_Handler, Hosts_Handler
from handlers.vdbench_handlers import Vdbench_Result_Handler

if __name__ == "__main__":
    handlers = [
        (r"/vdbench_result", Vdbench_Result_Handler),
        (r"/vdbench_file_upload", Vdbench_File_Handler),
        (r"/host", Host_Handler),
        (r"/host/(\d+)", Host_Handler),
        (r"/hosts", Hosts_Handler)
        # (r"/vdbench_file_upload", Vdbench_File_Handler),
    ]
    app = web.Application(handlers, debug=True)
    app.listen(8888)
    ioloop.IOLoop.current().start()
