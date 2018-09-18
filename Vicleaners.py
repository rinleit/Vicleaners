# -*- coding: utf-8 -*-
from pyvi import ViTokenizer
import re

__specChar__ = {u'&': u'và',u'@': u'a còng', u'^': u'mũ', u'$': u'đô la', u'%': u'phần trăm', u'*' : u'sao', u'+': u'cộng', u'>': u'dấu lớn', u'<': u'dấu bé', u'/': u'phần', u'=': u'bằng'}
__number__ = {0: u'không', 1: u'một', 2: u'hai', 3: u'ba', 4: u'bốn', 5: u'năm', 6: u'sáu', 7: u'bảy', 8: u'tám', 9: u'chín', 10: u'mười'}
__currency__ = {u'VND': u'việt nam đồng', u'USD': 'đô la mỹ'}
__doluong__ = {u'km': u'ki lô mét', u'cm': u'xen ti mét', u'dm': u'đề xi mét', u'mm': u'mi li mét', u'nm':u'na nô mét'}
__cannang__ = {u'kg': u'ki lô gam', u'g': 'gam'}


flatten = lambda *n: (e for a in n
	for e in (flatten(*a) if isinstance(a, (tuple, list)) else (a,)))

# Regular expression matching whitespace:
_whitespace_re = re.compile(r'\s+')

class cleaners(object):
	def __init__(self, text=None):
		if text == None:
			print("Text not None!")
			return
		self.str = text
		self.raw = text
		self.word_sent = []
		self.result = []

	def split_word_sent(self, text):
		self.word_sent = ViTokenizer.tokenize(text).split()
		return self.word_sent

	@staticmethod
	def collapse_whitespace(text):
		return re.sub(_whitespace_re, ' ', text)
	
	def lower(self, text):
		return str(text).lower()
	
	def do(self):
		text = cleaners.collapse_whitespace(self.str)
		ws = self.split_word_sent(text)
		for chars in ws:
			if "_" in chars:
				chars = chars.split("_")
			else:
				chars = [chars]

			for char in chars:
				char = self.specChar(char)
				char = self.currency(char)
				char = self.doluong(char)
				char = self.cannang(char)
				char = self.processNum(char)
				self.result.append(char)

		return self.join_str(flatten(self.result)).lower()

	def strip(self):
		self.str = self.str.strip()
		return self.str

	def join_str(self, list_str):
		return " ".join(list_str)

	def specChar(self, text):
		try:
			if len(text) == 1:
				return __specChar__[text]
			else:
				for char in __specChar__:
					if char in text:
						text = text.replace(char,u" " + __specChar__[char] + u" ")
				result = []
				for char in text.split():
					char = self.currency(char)
					char = self.doluong(char)
					char = self.cannang(char)
					char = self.processNum(char)
					result.append(char)
				return self.join_str(result)
		except:
			return text

	def currency(self, text):
		try:
			return __currency__[text]
		except:
			return text

	def doluong(self, text):
		try:
			return __doluong__[text]
		except:
			return text  

	def cannang(self, text):
		try:
			return __cannang__[text]
		except:
			return text

	def processNum(self, text):
		try:
			if len(text) > 1:
				
				output = u''
				splitChar = ''
				res = [text]

				if ',' in text:
					res = text.split(',')
					splitChar =','

				if '.' in text:
					res = text.split('.')
					splitChar = '.'

				if '/' in text:
					res = text.split('/')
					splitChar = '/'

				if len(res) > 1:

					if splitChar in ['.', ',']:
						for i, map in enumerate(res):
							if i < len(res) - 1:
								output += self.num_to_text(map, 0) + u" phẩy "
							else: 
								output += self.num_to_text(map, 0)

					if splitChar in ['/']:
						if len(res) == 3:
							if int(res[0]) <=31 and int(res[1]) <=12 and int(res[2]) % 1000 > 0:
								return u"ngày " + self.num_to_text(res[0], 0) + u" tháng " + self.num_to_text(res[1], 0) + u" năm " + self.num_to_text(res[2], 0)
						elif len(res) == 2:
							if int(res[0]) <= 31 and int(res[1]) <= 12:
								return u"ngày " + self.num_to_text(res[0], 0) + u" tháng " + self.num_to_text(res[1], 0)
							elif int(res[0]) <= 12 and len(res[1]) == 4:
								return u"tháng " + self.num_to_text(res[0], 0) + u" năm " + self.num_to_text(res[1], 0)
							
						for i, map in enumerate(res):
							if i < len(res) - 1:
								output += self.num_to_text(map, 0) + u" phần "
							else: 
								output += self.num_to_text(map, 0)

					return output
				else: 
					if str(text).isdigit():
						return self.num_to_text(text, 0).split()
			return text
		except:
			return text

	def num_to_text(self, text, flag):
		try:
			num = int(text)
			if num <= 10: 
				if flag==0:
					return __number__[num]
				return u"linh " + __number__[num]
			if num//1000000000 > 0:
				if num%1000000000 == 0: 
					return self.num_to_text(num//1000000000, 0) + u" tỷ"
				if num%1000000000 != 0: 
					return self.num_to_text(num//1000000000, 0) + u" tỷ " + self.num_to_text(num%1000000000, 1)
			if num//1000000 > 0:
				if num%1000000 == 0: 
					return self.num_to_text(num//1000000, 0) + u" triệu"
				if num%1000000 != 0: 
					return self.num_to_text(num//1000000, 0) + u" triệu " + self.num_to_text(num%1000000, 2)
			else:
				if flag==1:
					return self.num_to_text(num//1000000, 0) + u" triệu " + self.num_to_text(num%1000000, 2)
			if num//1000 > 0:
				if num%1000 == 0: 
					return self.num_to_text(num//1000, 0) + u" nghìn"
				if num%1000 != 0: 
					return self.num_to_text(num//1000, 0) + u" nghìn " + self.num_to_text(num%1000, 3)
			else:
				if flag==2:
					return self.num_to_text(num//1000, 0) + u" nghìn " + self.num_to_text(num%1000, 3)
			if num//100 > 0:
				if num%100 == 0: 
					return self.num_to_text(num//100, 0) + u" trăm"
				if num%100 != 0: 
					return self.num_to_text(num//100, 0) + u" trăm " + self.num_to_text(num%100, 4)
			else:
				if flag==3:
					return self.num_to_text(num//100, 0) + u" trăm " + self.num_to_text(num%100, 4)
			if num//10 > 0:
				if num >= 20:
					if num%10 != 0:
						if num%10 == 1:
							return self.num_to_text(num//10, 0) + u" mươi mốt"
						if num%10 == 5:
							return self.num_to_text(num//10, 0) + u" mươi lăm"
						return self.num_to_text(num//10, 0) + u" mươi " + self.num_to_text(num%10, 0)
					else:
						return self.num_to_text(num//10, 0) + u" mươi"
				else:
					if num == 15: 
						return u"mười lăm"
					return u"mười " + self.num_to_text(num%10, 0)
		except:
			return text

if __name__ == "__main__":
	with open("input.txt", mode="r", encoding="utf-8") as f:
		for line in f:
			print("Input:\n[%s]" % (line))
			ret = cleaners(line).do()
			print("Output:\n[%s]" % ret)

	


	



	

