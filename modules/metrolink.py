from base_module import *
import requests, bs4, difflib

requiredBeardBotVersion = 0.1
class BeardBotModule(ModuleBase):
	"""Check live Metrolink departures:
*   Trams <stop name>
where <stop name> is the name of the stop you'd like tram times for.
*	Trams
will just print the line statuses"""

	def getStations(self):
		r = requests.get('http://beta.tfgm.com/api/public-transport/stations/')
		return r.json()

	def getMetrolinkStations(self):
		stations = self.getStations()
		metrolinkStations = [station for station in stations if station["mode"] == "tram"]
		return metrolinkStations

	def getDepartures(self, stationHref):
		departures = []

		url = "http://beta.tfgm.com" + stationHref + "?layout=false"
		stopInfo = requests.get(url).text
		stopInfoBS = bs4.BeautifulSoup(stopInfo, "html.parser")
		departuresHTML = stopInfoBS.find(id="departure-items")
		if departuresHTML != None:
			departuresHTML = departuresHTML.find_all("tr")

			for departure in departuresHTML:
				thisDeparture = {}
				thisDeparture["destination"] = departure.find("td", {"class":"departure-destination"}).text
				thisDeparture["carriages"] = departure.find("td", {"class": "departure-carriages"}).find("span").text
				thisDeparture["wait"] = departure.find("td", {"class": "departure-wait"}).find("span", {"class":"figure"}).text
				departures.append(thisDeparture)

		return departures

	def getHrefFromId(self, thisId):
		for station in self.stations:
			if station["id"] == thisId:
				return station["href"]
		return None

	def getStationDepartures(self, station):
		return self.getDepartures(self.getHrefFromId(station))

	def findClosestIDFromName(self, name):
		stationNames = [station["name"] for station in self.stations]
		name = difflib.get_close_matches(name, stationNames, cutoff=0.3, n=1)[0]
		for station in self.stations:
			if station["name"] == name:
				return station["id"]
		return None

	def stationNameFromID(self, thisId):
		for station in self.stations:
			if station["id"] == thisId:
				return station["name"]
		return None

	def departureToString(self, departure):
		thisString = ""
		thisString = thisString + departure["destination"] + " - "
		thisString = thisString + departure["carriages"] + " - "
		thisString = thisString + departure["wait"] + "mins"
		return thisString

	def getLineStatuses(self):
		r = requests.get('http://beta.tfgm.com/api/statuses/tram')
		statuses = r.json()['items']
		for status in statuses:
			if "detail" in status:
				status["detail"] = status["detail"].replace("<p>", "")
				status["detail"] = status["detail"].replace("</p>", " ")
				status["detail"] = status["detail"].strip()
		return statuses

	def lineStatusToString(self, status):
		outStatus = status["name"] + " - "
		outStatus = outStatus + status["status"]
		if "detail" in status:
			outStatus = outStatus + " - " + status["detail"]
		return outStatus

	@on_channel_match("^Trams$")
	def on_chan_trams_status(self, source_name, source_host, message):
		self.bot.say("The current line statuses on Metrolink are:-")
		for status in self.getLineStatuses():
			self.bot.say(self.lineStatusToString(status))

	@on_private_match("^Trams$")
	def on_priv_trams_status(self, source_name, source_host, message):
		self.bot.pm(source_name, "The current line statuses on Metrolink are:-")
		for status in self.getLineStatuses():
			self.bot.pm(source_name, self.lineStatusToString(status))


	@on_channel_match("^Trams((?:\s(?:\w+))+)", re.I)
	def on_chan_trams_station(self, source_name, source_host, message, stationName):
		stationID = self.findClosestIDFromName(stationName.strip())
		if stationID == None:
			self.bot.say("Sorry, I can't find that station")
		else:
			stationName = self.stationNameFromID(stationID)
			stationDepartures = self.getStationDepartures(stationID)
			if stationDepartures == []:
				self.bot.say("I can't find any trams from " + stationName + " any time soon")
			else:
				self.bot.say("The next departures from " + stationName + " are:-")
				for departure in stationDepartures:
					self.bot.say(self.departureToString(departure))

	@on_private_match("^Trams((?:\s(?:\w+))+)", re.I)
	def on_priv_trams_station(self, source_name, source_host, message, stationName):
		stationID = self.findClosestIDFromName(stationName.strip())
		if stationID == None:
			self.bot.pm(source_name, "Sorry, I can't find that station")
		else:
			stationName = self.stationNameFromID(stationID)
			stationDepartures = self.getStationDepartures(stationID)
			if stationDepartures == []:
				self.bot.pm(source_name, "I can't find any trams from " + stationName + " any time soon")
			else:
				self.bot.pm(source_name, "The next departures from " + stationName + " are:-")
				for departure in stationDepartures:
					self.bot.pm(source_name, self.departureToString(departure))

	def __init__(self, newBot):
		ModuleBase.__init__(self, newBot)
		self.stations = self.getMetrolinkStations()