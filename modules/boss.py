from base_module import *

requiredBeardBotVersion = 0.4
class BeardBotModule(ModuleBase):
	"""Do actions like a boss
Do an action:
*   /me [action]
"""
	def __init__(self, newBot):
		ModuleBase.__init__(self, newBot)

	def on_action(self, source_name, source_host, message):
		self.bot.say("Like a boss")
