import random
import functools
from typing import Union

		# "blacklistFollow": [
		# 	"p", "t", "d", "k", "f", "v", "s", "yh", "ts", "ch", "j", "m", "n", "r", "l", "y", "w",
		# ]

Vowels: list[dict[str, Union[str, int]]] = [
	{
		"sound": "i",
		"weight": 1,
	},
	{
		"sound": "e",
		"weight": 1,
	},
	{
		"sound": "a",
		"weight": 1,
	},
	{
		"sound": "u",
		"weight": 2,
	}
]
Consonants: list[dict[str, Union[str, int, list[str]]]] = [
	{
		"sound": "p",
		"weight": 15,
		"blacklistFollow": [
			"p", "t", "d", "k", "v", "ts", "ch", "j",
		]
	},
	{
		"sound": "t",
		"weight": 10,
		"blacklistFollow": [
			"p", "t", "d", "k", "v", "ts", "j", "m", "n",
		]
	},
	{
		"sound": "d",
		"weight": 20,
		"blacklistFollow": [
			"p", "t", "d", "k", "f", "v", "s", "yh", "ts", "ch", "j", "m", "n",
		]
	},
	{
		"sound": "k",
		"weight": 10,
		"blacklistFollow": [
			"p", "t", "d", "k", "ts", "ch", "j",
		]
	},
	{
		"sound": "f",
		"weight": 10,
		"blacklistFollow": [
			"p", "t", "d", "k", "v", "s", "yh", "ts", "ch", "j", "m", "n",
		]
	},
	{
		"sound": "v",
		"weight": 13,
		"blacklistFollow": [
			"p", "t", "d", "k", "f", "v", "s", "yh", "ts", "ch", "j"
		]
	},
	{
		"sound": "s",
		"weight": 10,
		"blacklistFollow": [
			"f", "v", "ts", "ch",
		]
	},
	{
		"sound": "yh",
		"weight": 5,
		"blacklistFollow": [
			"p", "t", "d", "k", "f", "v", "yh", "ts", "ch", "j", "m", "n", "r", "l", "y", "w",
		]
	},
	{
		"sound": "h",
		"weight": 10,
		"blacklistFollow": [
			"p", "t", "d", "k", "f", "v", "s", "yh", "ts", "ch", "j", "m", "n", "y",
		]
	},
	{
		"sound": "ts",
		"weight": 7,
		"blacklistFollow": [
			"p", "t", "d", "k", "f", "v", "s", "yh", "ts", "ch", "j", "m", "n",
		]
	},
	{
		"sound": "ch",
		"weight": 10,
		"blacklistFollow": [
			"p", "t", "d", "k", "f", "v", "yh", "h", "ts", "ch", "j", "m", "n",
		]
	},
	{
		"sound": "j",
		"weight": 25,
		"blacklistFollow": [
			"p", "t", "d", "k", "f", "v", "yh", "ts", "ch", "j", "m", "n",
		]
	},
	{
		"sound": "m",
		"weight": 10,
		"blacklistFollow": [
			"p", "t", "d", "k", "f", "v", "s", "yh", "ts", "ch", "j",
		]
	},
	{
		"sound": "n",
		"weight": 10,
		"blacklistFollow": [
			"p", "t", "d", "k", "f", "v", "s", "ts", "ch", "j",
		]
	},
	{
		"sound": "r",
		"weight": 30,
		"blacklistFollow": [
			"p", "t", "d", "k", "f", "v", "s", "yh", "ts", "ch", "j", "m", "n", "l", "y", "w",
		]
	},
	{
		"sound": "l",
		"weight": 20,
		"blacklistFollow": [
			"p", "t", "d", "k", "f", "v", "s", "yh", "ts", "ch", "j", "m", "n",
		]
	},
	{
		"sound": "y",
		"weight": 20,
		"blacklistFollow": [
			"p", "t", "d", "k", "f", "v", "s", "yh", "ts", "ch", "j", "m", "n", "r", "y",
		]
	},
	{
		"sound": "w",
		"weight": 10,
		"blacklistFollow": [
			"p", "t", "d", "k", "f", "v", "s", "yh", "ts", "ch", "j", "m", "n", "w",
		]
	}
]
PreConsts: list[dict[str,int]] = [
	{
		"count": 1,
		"weight": 20,
	},
	{
		"count": 0,
		"weight": 1,
	},
	{
		"count": 2,
		"weight": 8,
	}
]
PostConsts: list[dict[str,int]] = [
	{
		"count": 1,
		"weight": 1,
	},
	{
		"count": 0,
		"weight": 10,
	}
]
SyllableCount: list[dict[str,int]] = [
	{
		"count": 1,
		"weight": 3,
	},
	{
		"count": 2,
		"weight": 5,
	},
	{
		"count": 3,
		"weight": 2
	}
]

def getMaxWeight(list: list[dict[str, Union[str, int, list[str]]]]) -> int:
	return functools.reduce(lambda acc, item: acc+item, map(lambda i: int(i["weight"]), list))
	# return functools.reduce(lambda acc, item: acc +item["weight"], list)

def doWeightedRoll(list: list[dict[str, Union[str, int, list[str]]]], blacklistKey: str = "", blacklist: list[str] = []) -> dict[str, Union[str, int, list[str]]]:
	maxWeight: int = getMaxWeight(list)

	chosen: Union[str, int] = None
	while True:
		index: int = random.randint(1, maxWeight)
		
		currentPos: int = 0
		for i in list:
			currentPos += i["weight"]
			if currentPos >= index:
				chosen = i
				break
		if chosen == None:
			print("something went wrong")
		
		if len(blacklist) != 0 and blacklistKey != "":
			if blacklist.count(chosen[blacklistKey]) > 0:
				chosen = None
				continue
			else:
				break
		else:
			break
	return chosen

def genWord() -> list[list[str]]:
	syllableCount: int = doWeightedRoll(SyllableCount)["count"]
	word: list[list[str]] = []

	for _ in range(syllableCount):
		syllable: list[str] = []

		preConstCount: int = doWeightedRoll(PreConsts)["count"]
		previousPreRoll: dict[str, Union[str, int, list[str]]] = {}
		for i in range(preConstCount):
			roll: dict[str, Union[str, int, list[str]]] = {}
			if i == 0:
				roll = doWeightedRoll(Consonants)
			else :
				roll = doWeightedRoll(Consonants, "sound", previousPreRoll["blacklistFollow"])
			previousPreRoll = roll
			syllable.append(roll["sound"])
		
		v = doWeightedRoll(Vowels)["sound"]
		if random.randint(0,1) == 0:
			v += "ː"
		syllable.append(v)
		
		postConstCount: int = doWeightedRoll(PostConsts)["count"]
		previousPostRoll:dict[str, Union[str, int, list[str]]] = {}
		for i in range(postConstCount):
			roll: dict[str, Union[str, int, list[str]]] = {}
			if i == 0:
				roll = doWeightedRoll(Consonants)
			else :
				roll = doWeightedRoll(Consonants, "sound", previousPostRoll["blacklistFollow"])
			previousPostRoll = roll
			syllable.append(roll["sound"])
		
		word.append(syllable)
	
	return word

def compileWord(word: list[list[str]]) -> str:
	final = ""
	for syllable in word:
		for sound in syllable:
			final += sound
	
	return final

def printWord(word: list[list[str]], doPrint: bool = True) -> str:
	splitWord = ""
	for i in range(len(word)):
		syllable = word[i]
		for sound in syllable:
			splitWord += sound
		if i != len(word)-1:
			splitWord += "-"

	w: str = f"{compileWord(word)} ({splitWord})"

	if doPrint:
		print(w)

	return w

def main() -> None:
	wordCount = 0
	while True:
		strWordCount = input("How many words? ")
		try:
			wordCount = int(strWordCount)
		except ValueError:
			if strWordCount == "inf":
				wordCount=-1
				break
			print("Please input an integer")
			continue
		else:
			break
	
	if wordCount > 0:
		for _ in range(wordCount):
			printWord(genWord())
	else:
		while True:
			leave = input(printWord(genWord(), False))
			if leave != "":
				break


if __name__ == '__main__':
	main()
