import random
import os
import sys
import json
import argparse
import math


def ArgParser(args):
    parser = argparse.ArgumentParser(description='Create a loot list for D&D')
    parser.add_argument('-n', '--number', type=int, default=10, help='Number of items to generate. Default: 10')
    parser.add_argument('-s', '--sets', type=str, default='Common,Uncommon,Rare,Legendary', help='Comma deliminated list of which rarity of items to include in the list. --number must be equal to or greater than the number of sets included. Default: Common,Uncommon,Rare,Legendary')
    parser.add_argument('-j', '--jsonPath', type=str, default='./Resources/Loot.json', help='Path to the json file containing the loot. Default: ./Resources/Loot.json')

    parsedArgs = parser.parse_args(args)
    VerifyArgs(parsedArgs)

    return parsedArgs

def VerifyArgs(parser):
    if parser.number < 1:
        print('Number of items must be greater than 0')
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
        if set not in ['Common', 'Uncommon', 'Rare', 'Legendary']:
            print('Invalid set: ' + set)
            print('Valid sets: Common, Uncommon, Rare, Legendary')
            exit(1)

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

    return DistributionNumbers
        

def GenerateLootList(LootJson, Number, Sets, Distribution):
    LootList = []
    DistributionNumbers = CalculateDistribution(Number, Distribution)
    for set in Sets:
        for i in range(0, DistributionNumbers[set]):
            LootList.append(GetRandomItem(LootJson[set]))
            if len(LootList) >= Number:
                return LootList

    return LootList


def main():
    #print formated json
    #print(json.dumps(LootJson, indent=4, sort_keys=True))
    args = ArgParser(sys.argv[1:])
    LootJson = json.load(open(args.jsonPath))
    DistributionPercentages = {'Common': 50, 'Uncommon': 30, 'Rare': 15, 'Legendary': 5}
    SetsList = args.sets.split(',')

    LootList = GenerateLootList(LootJson, args.number, SetsList, DistributionPercentages)

    print(LootList)

    return LootList

if __name__ == "__main__":
    main()