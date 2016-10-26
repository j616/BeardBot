#!/usr/bin/env python
__version__ = 0.4
__author__ = "Jonathan Heathcote, James Sandford"

import sys
sys.path.append("./modules")
import traceback
import pickle
import irc.strings
import irc.buffer
from irc.bot import SingleServerIRCBot
from irc.client import NickMask
from optparse import OptionParser

class IncompatibleModuleError(Exception):
	"""
	For raising when a module too new for this server is loaded
	"""
	pass

class BeardBot(SingleServerIRCBot):
		def __init__(self, channel, server, port=6667, password=None, name="beardbot", noadmin=False):
			SingleServerIRCBot.__init__(self, [(server, port, password)],
			                            name, "The Beardy-Based Botulator")
			# The channel the bot is a member of
			self.channel = channel
			
			# The last place a message was recieved from (used by "reply")
			self.last_message_sender = self.channel

			# If bot should have no administrators
			self.noadmin = noadmin
			
			# The loaded modules
			self.modules = {}
			
			#list of nicks to ignore
			self.ignore = []
			
			# Try to load previously loaded modules
			try:
				old_modules = pickle.load(open(self.channel + "_modules.db", "r"))
				for module in old_modules:
					try:
						self.load_module(module)
					except Exception, e:
						traceback.print_exc(file=sys.stdout)
			except:
				# Otherwise just start the admin
				try:
					self.load_module("admin")
				except Exception, e:
					print e
			finally:
				# There was a .db, but it didn't contain admin...
				if "admin" not in self.modules:
					try:
						self.load_module("admin")
					except Exception, e:
						print e
		
		def get_nick(self):
			"""Get the bot's nickname"""
			return self.connection.get_nickname()
		def set_nick(self, nick):
			"""Set the bot's nickname"""
			self.connection.nick(nick)
		nick = property(fget=get_nick, fset=set_nick)
		
		def say(self, message):
			"""Send a message to the channel"""
			self.pm(self.channel, message)
		
		def reply(self, message):
			"""Send a message to the last person to speak"""
			self.pm(self.last_message_sender, message)
		
		def pm(self, user, message):
			"""Send a message to a user"""
			message = message.replace("\r","\n")
			for part in message.split("\n"):
				self.connection.privmsg(user, part.encode("UTF8"))

		def action(self, message):
			message = message.replace("\r", "\n")
			for part in message.split("\n"):
				self.connection.action(self.channel, part.encode("UTF8"))
		
		def on_nicknameinuse(self, c, e):
			c.nick(c.get_nickname() + "_")
		
		def on_welcome(self, c, e):
			c.join(self.channel)
			#c.privmsg(self.channel, "Hi there, I'm beardy. If I'm annoying, tell me to die.")
		
		def on_privmsg(self, c, e):
			# Handle a message recieved from the channel
			source_name = e.source.nick.lower()
			source_host = e.source.host
			message = e.arguments[0].decode("UTF8")
			
			if source_name in self.ignore:
				return
			
			self.last_message_sender = source_name
			
			for module in self.modules.values():
				try:
					module.handle_private_message(source_name, source_host, message)
				except Exception, e:
					traceback.print_exc(file=sys.stdout)
			
			if message == "die":
				# Force the bot to die
				self.die("Someone killed me... It was you, " + e.source.nick.lower())
			elif message == "panic:reloadadmin":
				# Restart the admin module if something is going wrong
				try:
					self.load_module("admin")
				except Exception, e:
					print e

		def on_action(self, c, e):
			source_name = e.source.nick.lower()
			source_host = e.source.host
			message = e.arguments[0].decode("UTF8")
			
			if source_name in self.ignore:
				return

			for module in self.modules.values():
				try:
					module.handle_action(source_name, source_host, message)
				except Exception, e:
					traceback.print_exc(file=sys.stdout)

			
		def on_pubmsg(self, c, e):
			# Handle a message recieved from the channel
			source_name = e.source.nick.lower()
			source_host = e.source.host
			message = e.arguments[0]
			
			if source_name in self.ignore:
				return
			
			self.last_message_sender = self.channel
			
			# If a message was addressed specifically to the bot, note this and strip
			# this from the message
			addressed_to_BeardBot = False
			if irc.strings.lower(message).startswith("%s: " % self.nick.lower()):
				message = message.split(": ", 1)[-1]
				addressed_to_BeardBot = True
			elif irc.strings.lower(message).startswith("%s, " % self.nick.lower()):
 				message = message.split(", ", 1)[-1]
				addressed_to_BeardBot = True

			# Alert each module that a message has arrived
			for module in self.modules.values():
				try:
					if addressed_to_BeardBot:
						module.handle_addressed_message(source_name, source_host, message.decode("UTF8"))
					else:
						module.handle_channel_message(source_name, source_host, message.decode("UTF8"))
				except Exception, e:
					traceback.print_exc(file=sys.stdout)

		def on_part(self, c, e):
			source_name = e.source.nick.lower()
			source_host = e.source.host
			
			if source_name in self.ignore:
				return
			
			for module in self.modules.values():
				try:
					module.handle_on_part(source_name, source_host, None)
				except Exception, e:
					traceback.print_exc(file=sys.stdout)

		def on_quit(self, c, e):
			source_name = e.source.nick.lower()
			source_host = e.source.host
			
			if source_name in self.ignore:
				return
			
			for module in self.modules.values():
				try:
					module.handle_on_quit(source_name, source_host, None)
				except Exception, e:
					traceback.print_exc(file=sys.stdout)

		def on_nick(self, c, e):
			source_before = e.source.nick.lower()
			source_after = e.target.nick.lower()
			source_host = e.source.host
			
			if source_before in self.ignore:
				return

			for module in self.modules.values():
				try:
					module.handle_on_change_nick(source_before, source_host, source_after)
				except Exception, e:
					traceback.print_exc(file=sys.stdout)
		
		def load_module(self, module_name):
			"""
			Try to (re)load the named module.
			"""
			module = __import__(module_name)
			reload(module)
			if module_name in self.modules:
				self.unload_module(module_name)
			
			if module.requiredBeardBotVersion > __version__:
				raise IncompatibleModuleError("%s requires BeardBot version %s"%(
				                              module_name,
				                              module.requiredBeardBotVersion))
			
			# Try to load the module with a refrence to this bot
			self.modules[module_name] = module.BeardBotModule(self)
		
		def unload_module(self, module_name):
			self.modules[module_name].die()
			del self.modules[module_name]
			
		def add_ignore(self, user_nick):
			if not user_nick in self.ignore:
				self.ignore.append(user_nick)
				
		def rm_ignore(self, user_nick):
			if user_nick in self.ignore:
				self.ignore.remove(user_nick)
				
		def ls_ignore(self):
			return self.ignore
		
		def die(self, *args, **kwargs):
			# Store a list of loaded modules before going down
			pickle.dump(self.modules.keys(), open(self.channel + "_modules.db", "w"))
			
			# Kill all the modules
			for module in self.modules.values():
				module.die()
			
			# Disconnect and quit
			SingleServerIRCBot.die(self, *args, **kwargs)

def main():
	# Parse command line arguments.
	parser = OptionParser()

	parser.add_option("-r", "--room",     dest="room",     default="#uhc")
	parser.add_option("-s", "--server",   dest="server",   default="irc.quakenet.org")
	parser.add_option("-p", "--port",     dest="port",     default=6667)
	parser.add_option("-P", "--password", dest="password", default=None)
	parser.add_option("-n", "--name",     dest="name",     default="beardbot")
	parser.add_option("-a", "--noadmin",  dest="noadmin",  default=False, action="store_true")	

	(options, args) = parser.parse_args()

	#prepend a '#' to the room if there isn't one.
	room = options.room if options.room.startswith('#') else ("#" + options.room)
	server = options.server
	port = options.port
	password = options.password
	name = options.name
	noadmin = options.noadmin

	print "Starting '%s' in room '%s' on '%s'..." % (name, room, server)

	if noadmin:
		print "With no admin"
	
	# Avoid UTF8 decode error with non-UTF8 input
	irc.client.ServerConnection.buffer_class = irc.buffer.LenientDecodingLineBuffer
	# Run the bot.
	bot = BeardBot(room, server, port=port, password=password, name=name, noadmin=noadmin)
	
	try:
		bot.start()
	except KeyboardInterrupt:
		bot.die()

if __name__ == "__main__":
	main()
