import argparse
import json
from os.path import dirname

from PIL import Image, ImageDraw, ImageFont

class SheetFiller:
	def __init__(self) -> None:
		self.redColor: tuple[int, int, int] = (193, 36, 34)
		self.image = Image.open(dirname(__file__) + "/NPC sheet.png")

		self.drawTo = ImageDraw.Draw(self.image)

		self.fontCache: dict[int, ImageFont.FreeTypeFont] = {}

		self.character: dict[str,str] = {}
		
	def	genFont(self, size: int) -> ImageFont.FreeTypeFont:
		if (font := self.fontCache.get(size)) is None:
			font = ImageFont.truetype(dirname(__file__) + "/ArchitectsDaughter-Regular.ttf", size)
			self.fontCache[size] = font

		return font
	

	def big(self, pos: tuple[int, int], text: str) -> None:
		self.drawTo.text(xy = pos, text=text, fill=self.redColor, font=self.genFont(270), stroke_width=6, stroke_fill=self.redColor)

	def demographic(self, pos: tuple[int, int], text: str) -> None:
		self.drawTo.text(xy = pos, text=text, fill=self.redColor, font=self.genFont(170), stroke_width=4, stroke_fill=self.redColor)

	def bigStat(self, pos: tuple[int, int], text: str, boxWidth: int) -> None:
		_,_,w,_ = self.drawTo.textbbox((0,0), text, font=self.genFont(270))
		newPos = (pos[0]+boxWidth/2-w/2, pos[1])

		self.drawTo.text(xy = newPos, text=text, fill=self.redColor, font=self.genFont(270), stroke_width=6, stroke_fill=self.redColor)

	def smallStat(self, pos: tuple[int, int], text: str, boxWidth: int) -> None:
		_,_,w,_ = self.drawTo.textbbox((0,0), text, font=self.genFont(220))
		newPos = (pos[0]+boxWidth/2-w/2, pos[1])

		self.drawTo.text(xy = newPos, text=text, fill=self.redColor, font=self.genFont(220), stroke_width=5, stroke_fill=self.redColor)

	def hitDice(self, pos: tuple[int, int], text: str) -> None:
		self.drawTo.text(xy = pos, text=text, fill=self.redColor, font=self.genFont(145), stroke_width=3, stroke_fill=self.redColor)

	def textBlock(self, pos: tuple[int, int], text: str, boxWidth: int) -> None:

		allWords = text.split(" ")
		allLines = []
		line = []

		while allWords:
			word = allWords[0]
			newText = " ".join(line + [word])

			if word.count("\n") > 0:
				allLines.append(" ".join(line))
				line = []

				allWords[0] = word.replace("\n", "")

			elif self.genFont(100).getlength(newText) > boxWidth:
				allLines.append(" ".join(line))
				line = []
			else:
				line += [word]
				allWords = allWords[1:]
		if line:
			allLines.append(" ".join(line))

		y = pos[1]
		for textLine in  allLines:
			_,_,w,_ = self.drawTo.textbbox((0,0), textLine, font=self.genFont(100))
			newPos = (pos[0]+boxWidth/2-w/2, y)

			self.drawTo.text(xy = newPos, text=textLine, fill=self.redColor, font=self.genFont(100), stroke_width=2, stroke_fill=self.redColor)

			y += 115


	def lookupDraw(self, category: str, text: str) -> None:
		match category:
			case "name": self.big((712, 720), text)

			case "class": self.demographic((3765, 604), text)
			case "race": self.demographic((3765, 1000), text)
			case "alignment": self.demographic((5015, 624), text)
			case "background": self.demographic((5071, 1000), text)
			case "age": self.demographic((6284, 634), text)
			case "gender": self.demographic((6248, 1000), text)

			case "str_mod": self.bigStat((409, 1948), text, 619)
			case "dex_mod": self.bigStat((1248, 1948), text, 619)
			case "con_mod": self.bigStat((2087, 1948), text, 619)
			case "int_mod": self.bigStat((409, 2947), text, 619)
			case "wis_mod": self.bigStat((1248, 2947), text, 619)
			case "cha_mod": self.bigStat((2087, 2947), text, 619)

			case "str": self.smallStat((521, 2349), text, 394)
			case "dex": self.smallStat((1360, 2349), text, 394)
			case "con": self.smallStat((2200, 2349), text, 394)
			case "int": self.smallStat((521, 3347), text, 394)
			case "wis": self.smallStat((1360, 3347), text, 394)
			case "cha": self.smallStat((2200, 3347), text, 394)

			case "ac": self.bigStat((511, 4119), text, 467)
			case "initiative": self.bigStat((1216, 4143), text, 617)
			case "speed": self.bigStat((2030, 4143), text, 617)

			case "current_health": self.bigStat((3005, 1974), text, 650)
			case "max_health": self.bigStat((3845, 1974), text, 650)
			case "hit_dice": self.hitDice((3499, 2651), text)

			case "characteristics": self.textBlock((4826, 1801), text, 2222)
			case "voice": self.textBlock((4825, 2550), text, 2224)
			case "goals": self.textBlock((4825, 3242), text, 2224)
			case "other_notes": self.textBlock((4825, 3957), text, 2222)

			case "abilities": self.textBlock((2951, 3180), text, 1598)

	def FillSheet(self, file: str) -> None:
		self.loadJSON(file)

		for key in self.character:
			self.lookupDraw(key, self.character[key])

		# self.image.save(dirname(__file__) + "/"+file.removesuffix(".json")+"Done.png")
		self.image.save(file.removesuffix(".json")+"Done.png")


	def loadJSON(self, file: str) -> None:
		# with open(dirname(__file__) + "/"+file+".json") as f:
		with open(file) as f:
			self.character = json.load(f)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		prog= "npcSheetFiller",
		description= "Generates DnD NPC sheets based off of a json file"
	)
	parser.add_argument("file", help="the json file that will be loaded and generated from.")
	args = parser.parse_args()

	# file = input("filename: ").strip()#.removesuffix(".json")
	# file = "dariusBlack"

	sf = SheetFiller()
	sf.FillSheet(args.file)

	print("Successfully filled sheet")
