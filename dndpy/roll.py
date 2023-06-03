import math
import random
import sys
import os
import json

import logger

def rollDie(parsedInput, die, log):
    numberOfDice = parsedInput[0]
    dieType = parsedInput[1]
    mathSymbol = parsedInput[2]
    modifier = parsedInput[3]

    log.Write(f'Rolling: {numberOfDice} {dieType} {mathSymbol} {modifier}')

    total = 0
    outputString = ""
    for i in range(0, numberOfDice):
        roll = random.randint(1, die[dieType])
        total += roll
        outputString += f'{roll} + '

    outputString = outputString[:-3]

    if mathSymbol == '+':
        total += int(modifier)
        outputString = f'({outputString}) + {modifier} = {total}'
    elif mathSymbol == '-':
        total -= int(modifier)
        outputString = f'({outputString}) - {modifier} = {total}'

    return outputString
    

def parseInput(input, log):
    inputArray = []
    if input == '':
        log.Error('No input')
        exit(1)

    if 'd' in input:
        dIndex = input.find('d')
        inputArray.append(input[:dIndex])
        inputArray.append(input[dIndex:])
    else:
        log.Error('Invalid input: unable to find d in input. ex d20')
        log.Error('Input: ' + input)
        exit(1)

    print(inputArray)

    if '+' in inputArray[1]:
        plusIndex = inputArray[1].find('+')
        inputArray.append(inputArray[1][plusIndex])
        inputArray.append(inputArray[1][plusIndex+1:])
        inputArray[1] = inputArray[1][:plusIndex]
    elif '-' in inputArray[1]:
        plusIndex = inputArray[1].find('-')
        inputArray.append(inputArray[1][plusIndex])
        inputArray.append(inputArray[1][plusIndex+1:])
        inputArray[1] = inputArray[1][:plusIndex]
    else:
        inputArray.append('+')
        inputArray.append('')

    print(inputArray)

    return inputArray

def verifyInput(inputArray, input, dice, log):
    if len(inputArray) != 4:
        log.Error('Invalid input: unable to parse input. input should look like 1d20+1, d10-3, 2d6, etc.')
        log.Error('Input: ' + input)
        exit(1)

    #Verify first value
    if inputArray[0] == '':
        inputArray[0] = 1

    #check if first value can be a number
    try:
        int(inputArray[0])
    except ValueError:
        log.Error('Invalid input: unable to parse input. input should look like 1d20+1, d10-3, 2d6, etc.')
        log.Error('Input: ' + input)
        exit(1)
    # End Verify first value

    #Verify second value
    if inputArray[1] not in dice.keys():
        diceString = str(dice.keys())[11:-2]
        log.Error('Invalid input: unable to parse input. input should look like 1d20+1, d10-3, 2d6, etc.')
        log.Error(f"Expected {diceString} got '{inputArray[1]}'")
        log.Error('Input: ' + input)
        exit(1)

    # End Verify second value

    #Verify fourth value
    if inputArray[3] == '':
        inputArray[3] = 0

    #check if fourth value can be a number
    try:
        int(inputArray[3])
    except ValueError:
        log.Error('Invalid input: unable to parse input. input should look like 1d20+1, d10-3, 2d6, etc.')
        log.Error('Input: ' + input)
        exit(1)

    # End Verify fourth value

    inputArray[0] = int(inputArray[0])
    
    return

def main():
    config = json.load(open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Configs/config.json')), 'r'))
    log = logger.Logger(True)
    dice = config["Dice"]
    input = sys.argv[1]
    log.Debug(input)

    parsedInput = parseInput(input, log)
    verifyInput(parsedInput, input, dice, log)

    result = rollDie(parsedInput, dice, log)

    log.Write(result)

    return

if __name__ == '__main__':
    main()