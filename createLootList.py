import random
import os
import sys
import json
import argparse
import math


def ArgParser(args, config):
    parser = argparse.ArgumentParser(description='Create a loot list for D&D')
    parser.add_argument('-n', '--number', type=int, default=10, help='Number of items to generate. Default: 10')
    parser.add_argument('-s', '--sets', type=str, default=config["Sets"], help='Comma deliminated list of which rarity of items to include in the list. --number must be equal to or greater than the number of sets included.')
    parser.add_argument('-j', '--jsonPath', type=str, default='./Resources/Loot.json', help='Path to the json file containing the loot. Default: ./Resources/Loot.json')

    parsedArgs = parser.parse_args(args)
    VerifyArgs(parsedArgs, config)

    return parsedArgs

def VerifyArgs(parser, config):
    if parser.number < 1:
        print('Number of items must be greater than 0')
        exit(1)

    if parser.number > 100:
        print('I promise you do not need more than 100 items in this list.')
        exit(1)

    if parser.sets == '':
        print('Sets must be specified')
        exit(1)

    if parser.number < len(parser.sets.split(',')):
        print('Number of items must be greater than or equal to the number of sets included')
        print('Number of items: ' + str(parser.number))
        print('Number of sets: ' + str(len(parser.sets.split(','))))
        exit(1)

    for set in parser.sets.split(','):
        if set not in config['Sets'].split(','):
            print('Invalid set: ' + set)
            print('Valid sets: Common, Uncommon, Rare, Legendary')
            exit(1)

def matchNumberToDice(number, dice):
    for key in dice.keys():
        if number <= dice[key]:
            return key
    return

def GetItemSets(LootJson):
    #get keys from json
    Keys = LootJson.keys()
    return Keys

def GetRandomItem(Set):
    #get random item from set
    Items = Set.keys()
    Item = random.choice(list(Items))
    return Item

def CalculateDistribution(Number, Distribution):
    DistributionNumbers = {}
    for set in Distribution.keys():
        percent = math.floor(Number * (Distribution[set] / 100))
        if percent < 1:
            DistributionNumbers[set] = 1
        else:
            DistributionNumbers[set] = percent

    #print('Distribution: ' + str(DistributionNumbers))

    return DistributionNumbers
        

def GenerateLootList(LootJson, Number, Sets, Distribution):
    LootList = []
    DistributionNumbers = CalculateDistribution(Number, Distribution)
    for set in Sets:
        loop = 0
        for i in range(0, DistributionNumbers[set]):
            loop += 1
            item = GetRandomItem(LootJson[set])
            LootList.append({item: LootJson[set][item]})
            LootJson[set].pop(item)

            if len(LootJson[set]) < 1:
                print('No more items in set: ' + set)
                break
            if len(LootList) >= Number:
                print('Enough Items Added. Number of items in list: ' + str(len(LootList)))
                return LootList
        #print('loop: ' + str(loop))
    
    #print('Sets :' + str(Sets))
    #print('Number: ' + str(Number))
    #print('Number of items in list: ' + str(len(LootList)))
    return LootList

def formatOutput(LootList, diceToUse, Dice):
    output = f'\nRoll a {diceToUse} to determine your loot.\n\n'
    diceRangeList = diceDistributionBuilder(LootList, diceToUse, Dice)

    if len(LootList) != len(diceRangeList):
        print('Something went wrong, the number of loot items doesn not match the dice ranges. Internal code error.')
        exit(1)

    for x, item in enumerate(LootList):
        itemKey = list(item.keys())[0]
        itemData = list(item.values())[0]
        itemEntry = f"\n{diceRangeList[x]}: {itemKey}\n"

        for key in itemData.keys():
            itemEntry += f"       {key}: {itemData[key]}\n"

        output += itemEntry

    return output

def diceDistributionBuilder(LootList, diceToUse, Dice):
    LootListSize = len(LootList)
    #print(f"{Dice[diceToUse]} / {LootListSize}")
    diceRange = round(Dice[diceToUse] / LootListSize)
    diceRangeBonus = Dice[diceToUse] % LootListSize

    #print('Dice to use: ' + diceToUse)
    #print(diceRange)
    #print(diceRangeBonus)

    diceRangeList = []

    for item in range(len(LootList)):
        diceRangeList.append(diceRange)
        if diceRangeBonus > 0:
            diceRangeList[item] += 1
            diceRangeBonus -= 1

    #print(diceRangeList)
    #print(sum(diceRangeList))

    number = 1

    for i in range(len(diceRangeList)):
        tmpNum = diceRangeList[i]
        if number == (number + diceRangeList[i] - 1):
            diceRangeList[i] = f"{number}"
        else:
            diceRangeList[i] = f"{number}-{number + diceRangeList[i] - 1}"
        number += tmpNum

    #print(diceRangeList)

    return diceRangeList


def main():
    config = json.load(open('./Configs/config.json')) #refactor this into a real config object
    args = ArgParser(sys.argv[1:], config)
    LootJson = json.load(open(args.jsonPath))
    DistributionPercentages = config['DistributionPercentages']
    Dice = config['Dice']

    SetsList = args.sets.split(',')
    diceToUse = matchNumberToDice(args.number, Dice)

    LootList = GenerateLootList(LootJson, args.number, SetsList, DistributionPercentages)
    #print(LootList)

    output = formatOutput(LootList, diceToUse, Dice)

    print(output)

    return

if __name__ == "__main__":
    main()