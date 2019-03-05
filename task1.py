import requests
from datetime import datetime
import json

name = ''

def val_date(date):
	# Validate the Date Input Format

	try:
		datetime.strptime(date, '%Y-%M-%d')
	except ValueError:
		print('Enter the date in YYYY-MM-DD format!!')
		exit(-1)

def check_response(response):
	# Checks if the request is successful

	if response.status_code == 200:
		print('The request is successfull!!')
		print('User: ' + name)
		print('Merged patches: ' + str(len(json.loads(response.text.replace(")]}'", "")))))
	else:
		print('There is no data found with given information.')
		exit(-1)


def get_user_commits(uri, fetch_type, obj):
	# Performs the 'GET' request to the server.

	params = '+status: "merged"'
	if fetch_type == 2:
		params += '+after:"' + obj['after'] + '"+before:"' + obj['before'] + '"'

	uri = uri + params
	print('The request is processing...')
	response = requests.get(uri)
	
	check_response(response)



if __name__ == '__main__':

	uri = 'https://gerrit.wikimedia.org/r/changes/?q=owner:'
	while(1):
		name = raw_input("Enter your name: ")

		uri = uri + name
		print("How do you want to fetch the commits:\n1. Fetch all commits\n2. Fetch commits between a timestamp")
		
		fetch_type = int(raw_input("Enter 1 or 2: "))
		obj = {}
		
		if fetch_type == 1:
			get_user_commits(uri, fetch_type, obj)

		elif fetch_type == 2:
			print("Enter dates in YYYY-MM-DD format")
			
			obj['after'] = raw_input("Enter Start Date: ")
			val_date(obj['after'])

			obj['before'] = raw_input("Enter End Date: ")
			val_date(obj['before'])
			
			get_user_commits(uri, fetch_type, obj)

		else:
			print('Enter a valid Input')

		print('Perform the operation again?\n1.Yes\n2.No')
		abort = int(raw_input())
		if abort == 2:
			break