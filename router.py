# server
import tornado.ioloop
import tornado.web
from   tornado.options import options

# system
import os
import sys

#handlers
from rest.commands import *
from rest.examples import *
from rest.popular import *

port = 80

if __name__ == "__main__":
	tornado.options.parse_command_line()
	application = tornado.web.Application([
		("/commands", CommandsHandler),
		("/commands/([a-z0-9]+)", CommandHandler),
		("/commands/([a-z0-9]+)/examples", CommandExamplesHandler),
		("/commands/([a-z0-9]+)/examples/([a-f0-9]{24})", CommandExampleHandler),
		("/examples", ExamplesHandler),
		("/examples/([a-f0-9]{24})", ExampleHandler),
		("/examples/([a-f0-9]{24})/upvotes", ExampleUpvotesHandler),
		("/examples/([a-f0-9]{24})/downvotes", ExampleDownvotesHandler),
		("/examples/([a-f0-9]{24})/commands", ExampleCommandsHandler),
		("/examples/([a-f0-9]{24})/commands/([a-z0-9]+)", ExampleCommandHandler),
		("/popular/commands", PopularCommandsHandler),
		("/popular/examples", PopularExamplesHandler),
		("/()$", tornado.web.StaticFileHandler, {'path':os.path.dirname(os.path.abspath(__file__))+'/webapp/index.html'}),
		("/(.*)", tornado.web.StaticFileHandler, {'path':os.path.dirname(os.path.abspath(__file__))+'/webapp/'}),
	])
	application.listen(port)
	tornado.ioloop.IOLoop.instance().start()
