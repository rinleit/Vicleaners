# -*- coding: utf-8 -*-
# Cleaners for Vietnamese
# A Module in TTS Synthesis
# Dev by R.
# Date : 09/2018

from pyvi import ViTokenizer
from rules import _spec_char, _currency, _d_unit, _w_unit, _number, short_dict
import re

flatten = lambda *n: (e for a in n
	for e in (flatten(*a) if isinstance(a, (tuple, list)) else (a,)))

# Regular expression matching whitespace:
_whitespace_re = re.compile(r'\s+')
_string_ascii_re = re.compile(r'[a-z]+')
_number_re = re.compile(r'[0-9]+')
_fnumber_re = re.compile(r'[0-9]+(\.|\,)[0-9]+')
_numbers_re = re.compile(r'[0-9]+(\,|\.)[0-9]+((\.|\,)[0-9]*)+')
_date_re = re.compile(r'([0-9]{2}\/)?[0-9]{2}(\/[0-9]{4})?')
_fraction_re = re.compile(r'[0-9]+(\/[0-9]+)+')
_unit_re = re.compile(r'([0-9]+)?[a-z]{5}')


def num_to_text(text, flag):
	try:
		num = int(text)
		if num <= 10: 
			if flag == 0:
				return _number[num]
			return u"linh " + _number[num]
		if num//1000000000 > 0:
			if num%1000000000 == 0: 
				return num_to_text(num//1000000000, 0) + u" tỷ"
			if num%1000000000 != 0: 
				return num_to_text(num//1000000000, 0) + u" tỷ " + num_to_text(num%1000000000, 1)
		if num//1000000 > 0:
			if num%1000000 == 0: 
				return num_to_text(num//1000000, 0) + u" triệu"
			if num%1000000 != 0: 
				return num_to_text(num//1000000, 0) + u" triệu " + num_to_text(num%1000000, 2)
		else:
			if flag == 1:
				return num_to_text(num//1000000, 0) + u" triệu " + num_to_text(num%1000000, 2)
		if num//1000 > 0:
			if num%1000 == 0: 
				return num_to_text(num//1000, 0) + u" nghìn"
			if num%1000 != 0: 
				return num_to_text(num//1000, 0) + u" nghìn " + num_to_text(num%1000, 3)
		else:
			if flag == 2:
				return num_to_text(num//1000, 0) + u" nghìn " + num_to_text(num%1000, 3)
		if num//100 > 0:
			if num%100 == 0: 
				return num_to_text(num//100, 0) + u" trăm"
			if num%100 != 0: 
				return num_to_text(num//100, 0) + u" trăm " + num_to_text(num%100, 4)
		else:
			if flag == 3:
				return num_to_text(num//100, 0) + u" trăm " + num_to_text(num%100, 4)
		if num//10 > 0:
			if num >= 20:
				if num%10 != 0:
					if num%10 == 1:
						return num_to_text(num//10, 0) + u" mươi mốt"
					if num%10 == 5:
						return num_to_text(num//10, 0) + u" mươi lăm"
					return num_to_text(num//10, 0) + u" mươi " + num_to_text(num%10, 0)
				else:
					return num_to_text(num//10, 0) + u" mươi"
			else:
				if num == 15: 
					return u"mười lăm"
				return u"mười " + num_to_text(num%10, 0)
	except:
		return text


def normalize_numbers(text):
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
							output += num_to_text(map, 0) + u" phẩy "
						else: 
							output += num_to_text(map, 0)

				if splitChar in ['/']:
					if len(res) == 3:
						if int(res[0]) <=31 and int(res[1]) <=12 and len(res[2]) == 4:
							return u"ngày " + num_to_text(res[0], 0) + u" tháng " + num_to_text(res[1], 0) + u" năm " + num_to_text(res[2], 0)
					elif len(res) == 2:
						if int(res[0]) <= 31 and int(res[1]) <= 12:
							return u"ngày " + num_to_text(res[0], 0) + u" tháng " + num_to_text(res[1], 0)
						elif int(res[0]) <= 12 and len(res[1]) == 4:
							return u"tháng " + num_to_text(res[0], 0) + u" năm " + num_to_text(res[1], 0)
							
					for i, map in enumerate(res):
						if i < len(res) - 1:
							output += num_to_text(map, 0) + u" phần "
						else: 
							output += num_to_text(map, 0)

				if str(text).isdigit():
					return num_to_text(text, 0).split()
				
				return output

		return text
	except:
		return text


def c_unit(text):
	try:
		return _currency[text]
	except:
		return text

def d_unit(text):
	try:
		return _d_unit[text]
	except:
		return text  

def w_unit(text):
	try:
		return _w_unit[text]
	except:
		return text


def _remove_commmas(m):
	text = m.group(0).replace(',', '')
	text = text.replace('.', '')
	return text

def _fnumber_(m):
	text = m.group(0)
	text = normalize_numbers(text)
	return text

def _number_(m):
	text = m.group(0)
	text = num_to_text(text, 0)
	return " "+ text +" "

def _fraction_(m):
	text = m.group(0)
	text = normalize_numbers(text)
	return text

def __unit(text):
	text = c_unit(text)
	text = w_unit(text)
	text= d_unit(text)

def _unit_(m):
	text = m.group(1)
	text = re.sub(_number, _number_, text)
	text = re.sub(_string_ascii_re, __unit, text)
	return text

def _short_dict(text):
	d = short_dict()
	try:
		return d[text]
	except:
		return text

def _normalize_numbers(text):
	text = re.sub(_numbers_re, _remove_commmas, text)
	text = re.sub(_fraction_re, _fraction_, text)
	text = re.sub(_fnumber_re, _fnumber_, text)
	text = re.sub(_number_re, _number_, text)
	return text

def _specChar(text):
	try:
		if len(text) == 1:
			return _spec_char[text]
		else:
			for char in _spec_char:
				if char in text:
					text = text.replace(char,u" " + _spec_char[char] + u" ")
			result = []
			for char in text.split():
				char = _normalize_numbers(char)
				char = c_unit(char)
				char = d_unit(char)
				char = w_unit(char)
				result.append(char)
			return cleaners.join_str(result)
	except:
		return text

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

	@staticmethod
	def lower(text):
		return str(text).lower()
	
	def do(self):
		text = cleaners.collapse_whitespace(self.str)
		text = cleaners.lower(text)

		ws = self.split_word_sent(text)

		# print(ws)

		for chars in ws:
			if "_" in chars:
				chars = chars.split("_")
			else:
				chars = [chars]

			for char in chars:
				char = _short_dict(char)
				char = _normalize_numbers(char)
				char = _specChar(char)
				char = c_unit(char)
				char = d_unit(char)
				char = w_unit(char)
				self.result.append(char)

		return cleaners.join_str(flatten(self.result))

	def strip(self):
		self.str = self.str.strip()
		return self.str

	@staticmethod
	def join_str(list_str):
		return " ".join(list_str)

if __name__ == "__main__":
	with open("input.txt", mode="r", encoding="utf-8") as f:
		for line in f:
			print("Input:\n[%s]" % (line))
			ret = cleaners(line).do()
			print("Output:\n[%s]" % ret)
