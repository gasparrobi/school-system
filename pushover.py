import http.client, urllib
import time


class pushover:
	# APP token
	token = "ahxexkf15auiyfju8xqau6paxazi44"

	# USER token
	user = "uKxGwAWrY7nvdikymmEP2fbqNoQwEJ"

	conn = http.client.HTTPSConnection("api.pushover.net:443")

	@classmethod
	def send_pushover(cls, msg="Someone just registered on codezero.nobrainers.io"):
		cls.conn.request("POST", "/1/messages.json",
		  urllib.parse.urlencode({
		    "token": cls.token,
		    "user": cls.user,
		    "message": msg,
		  }), { "Content-type": "application/x-www-form-urlencoded" })
		cls.conn.getresponse()