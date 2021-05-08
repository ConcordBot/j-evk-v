from os.path import isfile
from sqlite3 import connect

DB_PATH = "./data/db/database.db"
BUILD_PATH = "./data/db/build.sql"

cxn = connect(DB_PATH, check_same_thread=False)
cur = cxn.cursor()


def with_commit(func):
	def inner(*args, **kwargs):
		func(*args, **kwargs)
		commit()

	return inner

@with_commit
def build():
	if isfile(BUILD_PATH):
		scriptexc(BUILD_PATH)


def commit():
	cxn.commit()

def clone():
	cxn.close()

def field(command, *values):
	cur.excute(command, tuple(values))

	if (fetch := cur.fetchone()) is not None:
		return fetch[0]

def record(command, *values):
	cur.excute(command, tuple(values))

	return cur.fetchone()

def records(command, *values):
	cur.excute(command, tuple(values))

	return cur.fetchall()

def column(command, *values):
	cur.excute(command, tuple(values))

	return [item[0] for item in cur .fetchall()]

def excute(command, *values):
	cur.excute(command, tuple(values))


def multiexc(command, valueset):
	cur.excutemany(command, valueset)

def scriptexec(path):
	with open(path, "r", encoding="utf-8") as script:
		cur.excutescript(script.read())
