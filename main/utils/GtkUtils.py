# -*- coding: utf-8 -*-
#
#  DataBaseUtils.py
#
#  Copyright 2015 Lorenzo Murarotto <lnzmrr@gmail.com>

class GtkUtils(object):
	"""set of utilities for the application"""
	
	def update_store(self,store,items):
		"""updates the store of a tree with specified items.
		Accepts:
		A list of lists in the form:
		[[item0,item1,...],[item0,item1,...],...]"""
		store.clear()
		for row in items:
			store.append(row)
		
	def date_to_string(self,date):
		"""accept a GtkCalendar date and returns
		a string in the form YYYY-MM-DD"""
		result=""
		result+=str(date[0])+"-"
		if date[1]<9:
			result+="0"+str(date[1]+1)+"-"
		else:
			result+=str(date[1]+1)+"-"
		if date[2]<10:
			result+="0"+str(date[2])
		else:
			result+=str(date[2])
		return result

	def is_later(self,dateA,dateB):
		"""returns True if dateA is later than dateB
		dateA,dateB==str"""
		if int(dateA[0:4])>int(dateB[0:4]):
			return True
		if int(dateA[0:4])==int(dateB[0:4]):
			if int(dateA[5:7])>int(dateB[5:7]):
				return True
			if int(dateA[5:7])==int(dateB[5:7]):
				if int(dateA[8:11])>int(dateB[8:11]):
					return True
		
		return False	
