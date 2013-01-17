import data
import logging
import pprint
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(data.load(['GOOG', 'YHOO'], '20120101', '20120131').data)