try: import urllib.request as urllib2
except ImportError: import urllib2
import urllib
import os
import pickle
import logging

DATA_PATH = '.\\data\\'

# http://stackoverflow.com/questions/36932/whats-the-best-way-to-implement-an-enum-in-python
def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    reverse = dict((value, key) for key, value in enums.iteritems())
    enums['reverse_mapping'] = reverse
    return type('Enum', (), enums)

def flexfilter(items, key, values):
	if values is None:
		return items
	if type(values) is not list:
		values = [values]
	# TODO: use zip to handle multiple k/v pairs
	return filter(lambda item: getattr(item, key, None) in values, items)

def write_to_file(filename, content, path=DATA_PATH):
	location = path + filename
	logging.debug('Writing to file: {}'.format(location))
	file = open(location, 'w')
	file.write(content)
	file.close()

def read_from_file(filename, path=DATA_PATH):
	location = path + filename
	logging.debug('Reading from file: {}'.format(location))
	file = open(location, 'r')
	contents = file.read()
	return contents

def pickle_it(filename, content, path=DATA_PATH):
	location = path + filename
	logging.debug('Pickling to file: {}'.format(location))
	file = open(location, 'wb')
	pickle.dump(content, file)
	file.close()

def pickle_load(filename, path=DATA_PATH):
	location = path + filename
	logging.debug('Loading pickle from file: {}'.format(location))
	file = open(location, 'rb')
	contents = pickle.load(file)
	file.close()
	return contents

def file_exists(filename, path=DATA_PATH):
	location = path + filename
	logging.debug('Looking up file: {}'.format(location))
	try:
		with open(location, 'r') as f:
			logging.debug('File {} exists.'.format(location))
			return True
	except IOError as e:
		logging.error('File {} does not exist.'.format(location))
		return False

def get_page(url):
	logging.debug('Loading data from {}.'.format(url))
	try:
		request = urllib2.urlopen(url)
		response = str(request.read())
		return response
	except urllib2.URLError as e:
		logging.error('Error accessing web page {}.'.format(url))
		raise e