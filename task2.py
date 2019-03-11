import requests
from datetime import datetime
import numpy as np
import json
import math
import matplotlib.pyplot as plot




# IDEA:
# Get the phabricator Id of the user --> used user.search
# Get all the tasks the user subscribed to. --> used maniphest.search
# For each task the user Subscribed, get all the transactions, get the user subscription time -->used transaction.search
# Plot Statistics

name = ''


def val_date(date, format):
	'''
		Validate the Date format
	'''

	try:
		datetime.strptime(date, format)
		return date
	except:
		print('Enter the date in ' + format +' format!!')
		exit(-1)

def getSubscribedTimeForTask(token, taskPHid):
	'''
		Get the week to which the user subscribed the task to.
	'''

	uri = 'https://phabricator.wikimedia.org/api/transaction.search'
	data = {
		'api.token': token,
		'objectIdentifier': taskPHid,
	}
	response = requests.post(uri, data=data)
	return response.text

def getTimeStamp(token, taskPHid, userPHid, month, year, i=None):
	'''
		Classify the received tasks to the timeStamps
	'''
	response = []
	responseData = json.loads(getSubscribedTimeForTask(token, taskPHid))
	try:
		for i in responseData['result']['data']:
			print
			if i['authorPHID'] == userPHid[0]:
				response.append(i)
		date = datetime.utcfromtimestamp(min([j['dateCreated'] for j in response]))
	except: 
		# No data avialable
		return -1

	if int(month) == date.month and int(year) == date.year:
		return math.ceil(float(date.day)/7)
	else:
		return -1


def getUserPatches(token, name):
	'''
		Get all the changes performed by the user (in phabricator)
	'''
	
	uri = 'https://phabricator.wikimedia.org/api/maniphest.search'
	data = {
		'api.token': token,
	  'constraints[subscribers][0]': name
	}
	
	print('The request is processing...')
	response = requests.post(uri, data=data)
	
	if response.status_code == 200:
		userActivities = json.loads(response.text)
		taskPHid = []

		for i in userActivities['result']['data']:
			taskPHid.append(i['phid'])
		return taskPHid

	else:
		print('There is no data found with given information.')
		exit(-1)

def getPHiD(token):
	'''
		Get the PHiD of the user
	'''
	uri = 'https://phabricator.wikimedia.org/api/user.search'
	data = {
		'api.token': token,
		'constraints[usernames][0]': name
	}

	print('Getting phabricator ID, please wait.....')
	response = requests.post(uri, data=data)

	try: 
		responseData = json.loads(response.text)['result']['data']
		result = [i['phid'] for i in responseData]
		return result
	except:
		print('Error in fetching the PHiD')
		exit(-1)


if __name__ == '__main__':
	name = input("Enter your name: ")
	token = input("Enter your token: ")
	
	# Get the PHID
	phid, taskPHids, temp = getPHiD(token), '', 0

	while(1):
		# Get the year, month
		year = val_date(input('Enter the year: '), "%Y")
		month = val_date(input('Enter month(in number format): '), "%m")
		weeks = [[], [], [], []]

		# Fetch all the User Tasks
		taskPHids = getUserPatches(token, name)

		# For Every Task, Get the timeStamp.
		for i in range(0, len(taskPHids)):

			week = getTimeStamp(token, taskPHids[i], phid, month, year, i)

			if week != -1 and week != 5:
				weeks[week-1].append(week)

		print('Specify in which format should the data has to be mentioned ?\n1. Table\n2. Histogram')
		format = input('Enter the number: ')
		print('User Stats: ' + name)
		if int(format) == 1:
			# Draw the table
			print('------------------------')
			print('| Week | Subscriptions |')
			print('------------------------')
			print('| 1   |  ' + str(len(weeks[0])) + '|')
			print('| 2   |  ' + str(len(weeks[1])) + '|')
			print('| 3   |  ' + str(len(weeks[2])) + '|')
			print('| 4   |  ' + str(len(weeks[3])) + '|')
			print('------------------------')
		elif int(format) == 2:
			# Plot the histogram
			labels = ['week 1', 'week 2', 'week 3', 'week 4']
			len_week = [len(i) for i in weeks]
			len_week=np.array(len_week)
			x=np.arange(3)
			plot.bar(labels, len_week)
			plot.xlabel('time')
			plot.ylabel('tasks subscribed')
			plot.show()
		else:
			print('Please Enter the correct format!')
		

		print('Perform the operation again?\n1.Yes\n2.No')
		abort = int(input())
		if abort == 2:
			break