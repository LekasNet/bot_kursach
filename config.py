from data import *
import datetime

TOKEN = ''

DATE = int(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).strftime("%d"))

AVAILABLE_TESTS = {"first": words1, "second": words2}