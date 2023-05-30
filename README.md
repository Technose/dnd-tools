# DnD-Tools

This repository contains a set of tools that a GM might find useful to streamline their workflows for running and crafting campaigns.

Tools Available:
createLootList.py

How to use createLootList.py:

This script takes a Json containing items seperated by Rarity and outputs a weighted list of items. 

This script does require some setup, you can find examples of how the inputs for this script are taken in and what the result is by looking at `Resources/exampleItemList.csv` and `Resources/exampleGeneratedJson.json`

Using a program like Goodle Sheets or Excel, craft a list of Items you would like to use with this generator. The only required Collumn headers needed are `Name` and `Rarity`, all other collumns can be extra information and will be processed individually.

Export your spreadsheet to a CSV format using `|` as a deliminator preferably, though you can configure this deliminator in the command invocation.

Once you have your CSV with your items, you can use `./Tools/CreateLootJson.py` to turn this plain text list into a Json that the  `createLootList.py` can take in and use

Example invocation:
```
py .\Tools\CreateLootJson.py --path .\Resources\exampleItemList.csv --output .\Resources\exampleGeneratedJson.json
```

With the Json created you can now invoke the `createLootList.py` script to obtain a list of random items taken from the Loot Json file.

example invocation:
```
py .\createLootList.py --jsonPath .\Resources\exampleGeneratedJson.json --number 10
```

example output:
```
Number of items in list: 5
['item2', 'item3', 'item4', 'item5', 'item1']
```