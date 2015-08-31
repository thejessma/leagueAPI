from __future__ import division
import json
import urllib2

statsAPItem11 = {}
statsAPItem14 = {}

itemData = {}

genStats11 = {"APGold": 0, "utilGold": 20}
genStats14 = {"APGold": 0, "utilGold": 20}
APGoldRatio_count14 = 0
APGoldRatio_count11 = 0

idAPItem = [1026, 1058, 3089, 3157, 3285, 3116, 3003, 3048, 3027, 3136, 3151, 3135, 3115, 3152, 3165, 3174]
idAPItem11 = [ 
{ "gold": 860},
{"gold":1600, "AP":80},
{"gold":3300}, 
{"gold":3300, "AP": 120},
{"gold": 3300, "AP":120},
{"gold":2900},
{"gold":2700, "AP": 60},
{"AP":60},
{"gold":2800, "AP":20},
{"gold": 1480},
{"gold": 2900, "AP": 50},
{"gold":2295, "AP": 70},
{"gold":2920, "AP":60},
{},
{},
{}]

with open("itemData.json", "r") as f:
	data = f.read()
	itemData = json.loads(data)

itemDataFile11 = open("itemDataFile11.json", "w")
itemDataFile14 = open("itemDataFile14.json", "w")

for i in range(len(idAPItem)):
	itemS = str(idAPItem[i])
	statsAPItem14[itemS] = {}
	for index in ["name", "sanitizedDescription", "gold", "stats"]:
		statsAPItem14[itemS][index] = itemData["data"][itemS][index]
	if len(itemData["data"][itemS]["stats"]) == 1 and len(statsAPItem14[itemS]["sanitizedDescription"]) < 20:
		statsAPItem14[itemS]["APGoldRatio"] = itemData["data"][itemS]["gold"]["total"] / itemData["data"][itemS]["stats"]["FlatMagicDamageMod"]
		genStats14["APGold"] += statsAPItem14[itemS]["APGoldRatio"]
		APGoldRatio_count14 += 1

genStats14["APGold"] = genStats14["APGold"] / APGoldRatio_count14

for i in range(len(idAPItem)):
	itemS = str(idAPItem[i])
	APGold = itemData["data"][itemS]["stats"]["FlatMagicDamageMod"] * genStats14["APGold"]
	
	utilGold = itemData["data"][itemS]["gold"]["total"] - APGold
	util = utilGold / genStats14["utilGold"]


	### Treat Rabadon by converting AP Bonus utility value to AP.
	if itemS == "3089":
		statsAPItem14[itemS]["stats"]["FlatMagicDamageMod"] = statsAPItem14[itemS]["stats"]["FlatMagicDamageMod"] + (utilGold / genStats14["APGold"])

	### Treat pure AP items with APGold 100% of total Gold.
	if itemS in ["1026", "1058", "3089"]:
		APGold = itemData["data"][itemS]["gold"]["total"]
		util = 0
		utilGold = 0

	statsAPItem14[itemS]["util"] = util
	statsAPItem14[itemS]["utilGold"] = utilGold
	statsAPItem14[itemS]["APGold"] = APGold
	print itemData["data"][itemS]["name"]
	print statsAPItem14[itemS]["APGold"]
	print statsAPItem14[itemS]["utilGold"]
	print statsAPItem14[itemS]["util"]



### TREAT Older Verstion 11 ###

for i in range(len(idAPItem)):
	itemS = str(idAPItem[i])
	statsAPItem11[itemS] = {}
	for index in ["name", "sanitizedDescription", "gold", "stats"]:
		statsAPItem11[itemS][index] = itemData["data"][itemS][index]
	if "gold" in idAPItem11[i]:
		statsAPItem11[itemS]["gold"]["total"] = idAPItem11[i]["gold"]
	if "AP" in idAPItem11[i]:
		statsAPItem11[itemS]["stats"]["FlatMagicDamageMod"] = idAPItem11[i]["AP"]
	if len(itemData["data"][itemS]["stats"]) == 1 and len(statsAPItem11[itemS]["sanitizedDescription"]) < 20:
		statsAPItem11[itemS]["APGoldRatio"] = statsAPItem14[itemS]["gold"]["total"] / statsAPItem11[itemS]["stats"]["FlatMagicDamageMod"]
		genStats11["APGold"] += statsAPItem11[itemS]["APGoldRatio"]
		APGoldRatio_count11 += 1
	### Treat Rabadon's Deathcap with 1% AP Bonus valued at 1.35 gold.

genStats11["APGold"] = genStats11["APGold"] / APGoldRatio_count11

for i in range(len(idAPItem)):
	itemS = str(idAPItem[i])
	APGold = itemData["data"][itemS]["stats"]["FlatMagicDamageMod"] * genStats11["APGold"]
	utilGold = itemData["data"][itemS]["gold"]["total"] - APGold
	util = utilGold / genStats11["utilGold"]

	### Treat Rabadon by converting AP Bonus utility value to AP.
	if itemS == "3089":
		statsAPItem11[itemS]["stats"]["FlatMagicDamageMod"] = statsAPItem11[itemS]["stats"]["FlatMagicDamageMod"] + (utilGold / genStats14["APGold"])
		
	### Treat pure AP items with APGold 100% of total Gold.
	if itemS in ["1026", "1058", "3089"]:
		APGold = itemData["data"][itemS]["gold"]["total"]
		util = 0
		utilGold = 0

	statsAPItem11[itemS]["util"] = util
	statsAPItem11[itemS]["utilGold"] = utilGold
	statsAPItem11[itemS]["APGold"] = APGold
	print itemData["data"][itemS]["name"]
	print statsAPItem11[itemS]["APGold"]
	print statsAPItem11[itemS]["utilGold"]
	print statsAPItem11[itemS]["util"]

print genStats14
print genStats11


itemDataFile11.write(json.dumps(statsAPItem11))
itemDataFile14.write(json.dumps(statsAPItem14))





