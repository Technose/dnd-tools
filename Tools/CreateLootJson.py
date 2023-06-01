import json
import os
import sys
import argparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dndpy import logger

def argParse(args):
    parser = argparse.ArgumentParser(description='Create Json File')
    parser.add_argument('--path', '-p', type=str, required=True, help='Path of the CSV file')
    parser.add_argument('--output', '-o', type=str, required=True, help='Path of the output file')
    parser.add_argument('--delimiter', '-d', type=str, required=False, default='|', help='Delimiter of the CSV file')
    parser.add_argument('--verbose', '-v', action='store_true', required=False, help='Verbose output')
    
    return parser.parse_args(args)

def verifyArgs(parser, log):
    if parser.path == '':
        log.Error('Path must be specified')
        exit(1)

    if not os.path.exists(parser.path):
        log.Error('Path does not exist')
        exit(1)

    if not os.path.isfile(parser.path):
        log.Error('Path is not a file')
        exit(1)
    
def getCSV(path):
    with open(path, 'r') as file:
        csv = file.read()
    return csv

def getJsonKeysFromCSV(csv, log):
    keys = csv.split('\n')[0].split('|')
    verifyCSVKeysHasNameAndRarity(keys, log)

    return keys

def verifyCSVKeysHasNameAndRarity(keys, log):
    if 'Name' not in keys:
        log.Error('CSV file does not have a Name column')
        exit(1)
    if 'Rarity' not in keys:
        log.Error('CSV file does not have a Rarity column')
        exit(1)

def convertCSVLineToList(csvLine):
    return csvLine.split('|')

def addItemToLootJson(csvLine, keys, lootJson):
    keyDetails = keys.copy()
    itemData = convertCSVLineToList(csvLine)
    itemName = itemData[keyDetails.index('Name')]
    itemRarity = itemData[keyDetails.index('Rarity')]

    itemData, keyDetails = removeIndexFromTwoLists(keyDetails.index('Name'), itemData, keyDetails)

    itemDetails = {}
    for i in range(len(keyDetails)):
        itemDetails[keyDetails[i]] = itemData[i]

    if itemRarity not in lootJson.keys():
        lootJson[itemRarity] = {}
    
    lootJson[itemRarity][itemName] = itemDetails

    return lootJson

def verifyCSVLineIsNotEmpty(csvLine):
    if csvLine == '':
        return False
    return True

def removeIndexFromTwoLists(index, list1, list2):
    list1.pop(index)
    list2.pop(index)

    return list1, list2

def addItemsToLootJson(csv, keyDetails, lootJson):
    csvLines = csv.split('\n')
    for line in csvLines[1:]:
        if verifyCSVLineIsNotEmpty(line):
            lootJson = addItemToLootJson(line, keyDetails, lootJson)

    return lootJson

def writeJsonToFile(lootJson, path, log):
    lootJson = json.dumps(lootJson, indent=4)

    try:
        with open(path, 'w+') as file:
            file.write(lootJson)
    except:
        log.Error('Error writing to file')
        exit(1)
    log.Write('Generated Json file at ' + path)

def outputImportantStatsForJson(lootJson, log):
    totalItems = 0
    itemsPerRarity = {}
    for rarity in lootJson.keys():
        itemsPerRarity[rarity] = len(lootJson[rarity])
        totalItems += len(lootJson[rarity])
    log.Write('Total Items: ' + str(totalItems))
    log.Write('Items Per Rarity: ' + str(itemsPerRarity))
    Sets = ""
    for rarity in lootJson.keys():
        Sets += rarity + ","
    log.Write('Sets: ' + Sets[:-1])
    
    distribution = {}
    for rarity in lootJson.keys():
        distribution[rarity] = round(itemsPerRarity[rarity] / totalItems * 100)

    log.Write('Distribution Percentages: ' + str(distribution))

def main():
    args = argParse(sys.argv[1:])
    log = logger.Logger(args.verbose)
    verifyArgs(args, log)
    csv = getCSV(args.path)
    keyDetails = getJsonKeysFromCSV(csv, log)

    lootJson = addItemsToLootJson(csv, keyDetails, {})
    outputImportantStatsForJson(lootJson, log)

    writeJsonToFile(lootJson, args.output, log)
    return

if __name__ == "__main__":
    main()