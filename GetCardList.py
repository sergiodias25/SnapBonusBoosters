import json
import os
import platform

is_android = 'ANDROID_STORAGE' in os.environ

def isSystemWindows():
    return platform.system() == 'Windows'

def isSystemLinux():
    return platform.system() == 'Linux'

def isSystemMobile():
    if platform.system() == 'Linux' and is_android:
        return True
    return False

def CalculateMissingBoostersToUpgrade(rarity, boosterCount):
    match rarity:
        case "Common":
            return 5 - boosterCount if boosterCount < 5 else 0
        case "Uncommon":
            return 10 - boosterCount if boosterCount < 10 else 0
        case "Rare":
            return 20 - boosterCount if boosterCount < 20 else 0
        case "Epic":
            return 30 - boosterCount if boosterCount < 30 else 0
        case "Legendary":
            return 40 - boosterCount if boosterCount < 40 else 0
        case "UltraLegendary":
            return 50 - boosterCount if boosterCount < 50 else 0
        case _:
            return 0

collectionFilePath = '~/AppData/Locallow/Second Dinner/SNAP/Standalone/States/nvprod/CollectionState.json'
if isSystemLinux():
    collectionFilePath = '~/.steam/steam/steamapps/compatdata/1997040/pfx/drive_c/users/steamuser/AppData/LocalLow/Second Dinner/SNAP/Standalone/States/nvprod/CollectionState.json'
if isSystemMobile():
    collectionFilePath = '/sdcard/Android/data/com.nvsgames.snap/files/Standalone/States/nvprod/CollectionState.json'
collectionPath = os.path.expanduser(collectionFilePath)

with open(collectionPath, encoding="utf-8-sig") as collection_json_file:
        data = json.load(collection_json_file)

        # get card split list 
        filteredListWithoutInfinitySplitsAndCustomCards = list(filter(lambda x : x['RarityDefId'] != 'Infinity' and 'Custom' not in x, data['ServerState']['Cards']))
        #helaFilteredList = list(filter(lambda x : x['CardDefId'] == 'Hela', filteredListWithoutInfinitySplitsAndCustomCards))
        cardList = filteredListWithoutInfinitySplitsAndCustomCards

        # get card boosters
        tempBoosterList = dict()
        for card in data['ServerState']['CardDefStats']['Stats'].items():
            if card[0] != '$type':
                cardData = json.loads(str(card[1]).replace("'", "\"").replace("True", "\"True\""))
                if 'Boosters' in cardData:
                    tempBoosterList[card[0]] = cardData['Boosters']

        finalBoosterList = json.loads(json.dumps(tempBoosterList));

dict_var = {}
for card in cardList:
    boosterCount = finalBoosterList[card['CardDefId']] if card['CardDefId'] in finalBoosterList else 0
    boostersMissingToUpgrade = CalculateMissingBoostersToUpgrade(card['RarityDefId'], boosterCount)
    if boostersMissingToUpgrade > 0:
        cardDescritption = card['ArtVariantDefId'] + " - Variant" if 'ArtVariantDefId' in card else card['CardDefId'] + " - Base"
        boostersDescription = " boosters" if boostersMissingToUpgrade > 1 else " booster"
        dict_var[cardDescritption] = { "Text": str(boostersMissingToUpgrade) + boostersDescription + " missing - " + cardDescritption + " - " + card['RarityDefId'], "Boosters": str(boostersMissingToUpgrade)}

sortedDict = sorted(dict_var.items(), key=lambda x: ('%02d' % int(x[1]['Boosters']), x[0]))
print()
print(" ----- " + str(len(sortedDict)) + " cards in your collection can appear in the Bonus Boosters section in the shop. " + " -----")
print("Get the displayed number of boosters by playing the game normally to remove the card from the rotation:")
print()
for i in range (0, len(sortedDict)):
    print(sortedDict[i][1]['Text'])
