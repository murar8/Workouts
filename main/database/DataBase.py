# -*- coding: utf-8 -*-
#! /usr/bin/python2.7
#  DataBaseUtils.py
#
#  Copyright 2015 Lorenzo Murarotto <lnzmrr@gmail.com>


import sqlite3
import datetime



class WoDataBase(object):
	"""Interfaces with SQLite database"""
	def __init__(self):
		self.baseConnection=sqlite3.connect("main/database/workouts.db")
		self.baseConnection.text_factory=str
		
		
	def __date_interval(self, dateInit, dateFinal):

		"""returns all dates between specified days
		dateInit,dateFinal==str"""
		
		start = datetime.datetime.strptime(dateInit, "%Y-%m-%d")
		end = datetime.datetime.strptime(dateFinal, "%Y-%m-%d")
		step = datetime.timedelta(days=1)

		dates = []
		while start <= end:
			dates.append(start.strftime("%Y-%m-%d"))
			start += step

		return dates

	def add(self, date, excercise, sets, reps, weight, notes):
		"""accepts an excercise and inserts it into the database
			startDate,excercise,notes=strings
			sets,reps,weight=integers
		"""
		if not notes:
			notes="none"
			
		assert type(sets) == int and type(reps) == int and type(weight) == int
		assert type(excercise) == str and type(notes) == str
		assert type(date) == str and len(date) == 10
		assert date[4] == "-" and date[7] == "-"
		assert not len(excercise)==0 and not sets==0 and not reps==0

		with self.baseConnection as connection:

			cursor = connection.cursor()

			cursor.execute("CREATE TABLE IF NOT EXISTS Workouts(\
					Id INTEGER PRIMARY KEY AUTOINCREMENT,\
					Date TEXT,Excercise TEXT,Sets INTEGER,\
					Reps INTEGER,Weight INTEGER,Notes TEXT);")

			cursor.execute("INSERT INTO Workouts\
					(id,date,excercise,sets,reps,weight,notes)\
					VALUES(?,?,?,?,?,?,?);",
					(None, date, excercise, sets, reps, weight, notes))

	def delete(self, Id):
		"""accepts an excercise and deletes it from the database."""
		assert type(Id)==int

		with self.baseConnection as connection:

			cursor = connection.cursor()

			cursor.execute("DELETE FROM Workouts WHERE Id=?;", (int(Id),))

	def retrieve_all(self):
		"""returns a list of tuples containing
			ID,DATE,EXCERCISE,SETS,REPS,WEIGHT,NOTES."""

		with self.baseConnection as connection:

			cursor = connection.cursor()

			cursor.execute("SELECT * FROM Workouts ORDER BY DATE(Date) ASC;")
			return [elem for elem in cursor.fetchall()]

	def retrieve_by_date(self, date):

		"""returns a list of tuples containing
			ID,DATE,EXCERCISE,SETS,REPS,WEIGHT,NOTES
			with the specified YYYY-MM-DD."""

		assert type(date) == str and len(date) == 10
		assert date[4] == "-" and date[7] == "-"

		with self.baseConnection as connection:

			cursor = connection.cursor()

			cursor.execute("SELECT * FROM Workouts WHERE Date=? ORDER BY DATE(Date) ASC;", (date,))
			return [elem for elem in cursor.fetchall()]

	def retrieve_by_interval(self, dateInit, dateFinal):
		"""retrieves from a database all the items in a specified time period"""
		
		for date in dateInit, dateFinal:
			assert type(date) == str and len(date) == 10
			assert date[4] == "-" and date[7] == "-"

		with self.baseConnection as connection:

			cursor = connection.cursor()

			workouts = []
			for date in self.__date_interval(dateInit, dateFinal):
				cursor.execute("SELECT * FROM Workouts WHERE Date=? ORDER BY DATE(Date) ASC;", (date,))
				workouts += [elem for elem in cursor.fetchall()]

			return workouts

	def retrieve_by_excercise(self,excercise):
		"""retrieves all entries for a given excercise"""
		assert type(excercise)==str
		
		with self.baseConnection as connection:

			cursor = connection.cursor()

			cursor.execute("SELECT * FROM Workouts WHERE Excercise=? ORDER BY DATE(Date) ASC;",\
								(excercise,))
			return [elem for elem in cursor.fetchall()]
			
	def retrieve_excercises(self):
		"""returns a list of all different excercises"""
		with self.baseConnection as connection:

			cursor = connection.cursor()

			cursor.execute("SELECT DISTINCT Excercise FROM Workouts;")

			return [elem[0] for elem in cursor.fetchall()]
			
	def retrieve_last_workout_by_excercise(self,excercise):
		"""returns last workout voice with given excercise"""
		assert type(excercise)==str
		with self.baseConnection as connection:

			cursor = connection.cursor()

			cursor.execute("SELECT * FROM workouts WHERE Excercise=? "
							"ORDER BY Id DESC LIMIT 1;",(excercise,))
			
			return cursor.fetchall()[0]
			
if __name__ == "__main__":
        """for debug only"""
	workouts = WoDataBase()
	
	for i in range(2008,2014):
		workouts.add(str(i)+"-04-10", "heyg", 8, 6, 15, "nooneone")

	print workouts.retrieve_all()
	print
	print workouts.retrieve_by_date("2010-02-03")
	print
	print workouts.retrieve_excercises()
	print
	print workouts.retrieve_by_interval("2012-12-10", "2015-02-02")
	print
	print workouts.retrieve_by_excercise("trie")
	print
	print workouts.retrieve_last_workout_by_excercise("ala")
