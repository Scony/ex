# server
import tornado.ioloop
import tornado.web
from   tornado.options import define, options

# database
import pymongo
from bson.objectid import ObjectId
import json

# system
import os
import sys

#handlers
from rest.test import *
from rest.commands import *
from rest.examples import *
from rest.votes import *
from rest.popular import *

connection = pymongo.Connection('localhost')
db = connection['ex']

define("port", default=80, help="run on the given port", type=int)

class RootHandler(tornado.web.RequestHandler):
	def get(self):
		self.set_status(303)
		self.set_header("Location", "/webapp/")

if __name__ == "__main__":
	tornado.options.parse_command_line()
	application = tornado.web.Application([
		("/", RootHandler),
		("/commands", CommandsHandler),
		("/commands/popular", PopularCommandsHandler),
		("/commands/([a-z0-9]+)", CommandHandler),
		("/commands/([a-z0-9]+)/examples", CommandExamplesHandler),
		("/commands/([a-z0-9]+)/examples/([a-f0-9]{24})", CommandExampleHandler),
		("/examples", ExamplesHandler),
		("/examples/popular", PopularExamplesHandler),
		("/examples/([a-f0-9]{24})", ExampleHandler),
		("/examples/([a-f0-9]{24})/upvotes", ExampleUpvotesHandler),
		("/examples/([a-f0-9]{24})/upvotes/([a-f0-9]{24})", ExampleVoteHandler),
		("/examples/([a-f0-9]{24})/downvotes", ExampleDownvotesHandler),
		("/examples/([a-f0-9]{24})/downvotes/([a-f0-9]{24})", ExampleVoteHandler),
		("/examples/([a-f0-9]{24})/commands", ExampleCommandsHandler),
		("/examples/([a-f0-9]{24})/commands/([a-z0-9]+)", ExampleCommandHandler),
		("/votes", VotesHandler),
		("/webapp/()$", tornado.web.StaticFileHandler, {'path':os.path.dirname(os.path.abspath(__file__))+'/webapp/index.html'}),
		("/webapp/(.*)", tornado.web.StaticFileHandler, {'path':os.path.dirname(os.path.abspath(__file__))+'/webapp/'}),
	])
	application.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
