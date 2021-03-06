from __future__ import division
import json
import urllib2

##define patch number
k = 0

data = []
dataItem = {}

patch = ["11", "14"]

with open("championList-EUNE"+patch[k]+"S.json", "r") as f:
	matchData = f.read()
	data = json.loads(matchData)

with open("itemDataFile"+patch[k]+".json", "r") as f:
	itemData = f.read()
	dataItem = json.loads(itemData)

### Given Champion id, returns champion name
def getChampionName(idChampion):
	champion = data[str(idChampion)]["name"]
	return champion

### Given item id, returns item name
def getItemName(idItem):
	with open("itemData.json", "r") as f:
		data = f.read()
		itemData = json.loads(data)
	item = itemData["data"][str(idItem)]

	return item["name"]

### The AP Items changed in Path 5.13

idAPItem = [1026, 1058, 3089, 3157, 3285, 3116, 3003, 3048, 3027, 3136, 3151, 3135, 3115, 3152, 3165, 3174]

### For a certain champion, return percentage he chooses the item
def statsItemChoice(item, championData):
	total = len(championData)
	count = 0
	for i in range(total):
		for k in range(7):
			if championData[i]["item"+str(k)] == item:
				count = count + 1
				break
	if count > 0:
		return count/total

### For a certain champion, return percentage he chooses the item and wins
def statsItemWin(item, championData):
	total = len(championData)
	count = 0
	for i in range(total):
		for k in range(7):
			if championData[i]["item"+str(k)] == item and championData[i]["winner"] == True:
				count = count + 1
				break
	if count > 0:
		return count/total

### If None, then pass over champion as he does not use the item
### For a certain champion, return average number of kills when he chooses the item
def statsItemKills(item, championData):
	total = len(championData)
	count = [0 for i in range(total)]
	for i in range(total):
		for k in range(7):
			if championData[i]["item"+str(k)] == item:
				count[i] = championData[i]["kills"]
				break
	average = sum(count)
	if average > 0:
		return average / len(count)

### For a certain champion, return number of kills on average
def averageKills(championData):
	total = len(championData)
	count = [0 for i in range(total)]
	for i in range(total):
		count[i] = championData[i]["kills"]
	average = sum(count)
	return average / len(count)

### For a certain champion, return delta of average kills with item 
def deltaKills(item, championData):
	itemAverage = statsItemKills(item, championData)
	if itemAverage != None:
		totalAverage = averageKills(championData)
		return itemAverage - totalAverage

### For a certain item, get percentage the player wins
def statsItemWinAll(item, data):
	total = len(data)
	count = 0
	for i in range(total):
		for k in range(7):
			if data[i]["item"+str(k)] == item:
				count += 1
				break
	return count / total

### For a set of items, calculate the total Unit AP
def calculateUnitAP(itemSet):
	total = 0
	for item in itemSet:
		total += itemSet[item]["stats"]["FlatMagicDamageMod"]
	return total

### For a set of items, calculate the total Unit Utility
def calculateUntUtil(itemSet):
	total = 0
	for item in itemSet:
		total += itemSet[item]["util"]
	return total

### For a certain champion, return average item set AP
def totalAP(championData):
	total = 0
	for i in range(len(championData)):
		totalSetAP = 0
		for j in range(7):
			idItem = championData[i]["item"+str(j)]
			if idItem in idAPItem:
				totalSetAP += dataItem[str(idItem)]["stats"]["FlatMagicDamageMod"]
		total += totalSetAP
	return total / len(championData)

### For a certain champion, return average item set utility 
def totalUtil(championData):
	total = 0
	for i in range(len(championData)):
		totalSetUtil = 0
		for j in range(7):
			idItem = championData[i]["item"+str(j)]
			if idItem in idAPItem:
				totalSetUtil += dataItem[str(idItem)]["util"]
		total += totalSetUtil
	return total / len(championData)

### For a certain champion, return the percentage of winning
def winPercent(championData):
	total = len(championData)
	win_count = 0
	for i in range(total):
		if championData[i]["winner"] == True:
			win_count += 1
	return win_count / total

### For a certain champion, return the item most often used
#def highItem(championData):

### Returns the average of all champions' total AP
def averageTotalAP():
	total = 0
	total_count = 0
	for i in data:
		if totalAP(data[i]["players"]) > 40:
			AP = totalAP(data[i]["players"])
			total += AP
			total_count +=1
	return total / total_count

def mainRole(championData):
	AP = totalAP(championData)
	averageAP = averageTotalAP()
	if AP > averageAP:
		return "AP"
	return "UTIL"

### Return in an array the AP Items in order of choice
def itemChoiceByChampion(championData):
	championItems = []
	for j in idAPItem:
		if statsItemChoice(j, championData) != None and statsItemChoice(j, championData) > 0.05:
			itemIndex = {}
			itemIndex["item"] = j
			itemIndex["stats"] = statsItemChoice(j, championData)
			championItems.append(itemIndex)
	return championItems

### For a champion, get their average X (Util) and Y (AP)
def coordinateByChampion(championData):
	championCoordinate = {}	
	if totalAP(championData) > 40:
		util = totalUtil(championData)
		AP = totalAP(championData)
		championCoordinate["x"] = util
		championCoordinate["y"] = AP
	return championCoordinate

def main():
	indexDict = {}
	for i in data:
		if len(coordinateByChampion(data[i]["players"])) != 0:
			indexDict[i] = {}
			indexDict[i]["name"] = data[i]["name"]
			indexDict[i]["coordinate"] = coordinateByChampion(data[i]["players"])
			indexDict[i]["win"] = winPercent(data[i]["players"])
			indexDict[i]["kills"] = averageKills(data[i]["players"])
			indexDict[i]["role"] = mainRole(data[i]["players"])
			indexDict[i]["items"] = itemChoiceByChampion(data[i]["players"])
	return indexDict

main()