import json
import urllib2
import time

matchID = []

with open("EUW11N.json", "r") as f:
	data = f.read()
	matchID = json.loads(data)
	f.close()

matchDataFile = open("matchDataFile-EUW11N.json", "w")

matchIDString = map(str, matchID)

matchData = []

for i in range(0, len(matchID)):
	index = 0
	if i % 10 == 0:
		time.sleep(12)

	print "request: " +  str(i)

	success = False
	for j in range(20):
		try: 
			matchData.append(json.load(urllib2.urlopen("https://euw.api.pvp.net/api/lol/euw/v2.2/match/" + matchIDString[i] + "?api_key=98d79efb-f067-465a-b246-50c65eac27e8")))
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



	matchDataFile.write(json.dumps(matchData[index]))
	matchDataFile.write(", ")
	matchDataFile.write("\n")
	index += 1

matchDataFile.close()



