from base_module import *
import re

# Matches a sed-style regex
regexReplace = re.compile("s/((\\\\\\\\|(\\\\[^\\\\])|[^\\\\/])+)/((\\\\\\\\|(\\\\[^\\\\])|[^\\\\/])*)((/(.*))?)")

requiredBeardBotVersion = 0.1
class BeardBotModule(ModuleBase):
	"""Applies a sed-style regex to the most-recent applicable message.
	"""
	messages = []
	original_messages = []
	def on_channel_message(self, source_name, source_host, message):
		regex = regexReplace.match(message)
		if regex:
			search = regex.groups()[0]
			replace = regex.groups()[3]
			flags = regex.groups()[8]
			if flags == None:
				flags = ""
			
			self.do_substitution(search, replace, flags)
		else:
			self.remember_message(message)
	
	def remember_message(self, message, original=True):
		self.messages.append(message)
		self.messages = self.messages[-5:]
		
		if original:
			self.original_messages.append(message)
			self.original_messages = self.original_messages[-5:]
			

	def do_substitution(self, search, replace, flags):
		messages = self.original_messages if 'o' in flags else self.messages

		for message in reversed(messages):
			if "g" in flags:
				count = 0
			else:
				count = 1
			
			new = re.sub(search, replace, message, count)
			if new != message:
				self.bot.say(new)
				self.remember_message(new, False)
				break
