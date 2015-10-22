import json
import urllib2
import time

matchID = []

with open("EUW5514.json", "r") as f:
	data = f.read()
	matchID = json.loads(data)
	f.close()

matchDataFile = open("matchDataFile-EUW14N.json", "w")

matchIDString = map(str, matchID)

matchData = []

for i in range(0, len(matchID)):

	success = False
	for j in range(20):
		try: 
			matchData.append(json.load(urllib2.urlopen("https://euw.api.pvp.net/api/lol/euw/v2.2/match/" + matchIDString[i] + "?api_key=94cfaa23-27dd-42a0-9434-6cbbdbd6b42a")))
			success = True
			break		
		except urllib2.HTTPError, err:
			if err.code in [429, 500, 503]:
				print "error happened"
				time.sleep(2)
			else:
				raise
	if not success:
		print 'SOMETHING WENT WRONG!!! WE FAILED 20 TIMES!!!'



	matchDataFile.write(json.dumps(matchData[i]))
	matchDataFile.write(", ")
	matchDataFile.write("\n")

matchDataFile.close()



