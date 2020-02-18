from gedparse import main, check_divorce_before_death, check_marriage_before_death
from pprint import pprint

marriage_errors, death_errors = main()

def mbd1():
	assert "ERROR: FAMILY: US05: 62: @F1@: Married 1994-07-7 after Husband's @I2@ death on 1990-01-1" in marriage_errors

def mbd2():
	assert "ERROR: FAMILY: US05: 62: @F2@: Married 1970-10-4 after Husband's @I6@ death on 1969-01-1" in marriage_errors

def mbd3():
	assert "ERROR: FAMILY: US05: 62: @F4@: Married 1993-06-9 after Husband's @I8@ death on 1992-01-1" in marriage_errors

def dbm1():
	assert "ERROR: FAMILY: US06: 77: @F1@: Divorced 1995-01-1 after Husband's @I2@ death on 1990-01-1" in death_errors

def dbm2():
	assert "ERROR: FAMILY: US06: 77: @F4@: Divorced 1997-01-1 after Husband's @I8@ death on 1992-01-1" in death_errors

def dbm3():
	assert "ERROR: FAMILY: US06: 77: @F4@: Divorced 1997-01-1 after Wife's @I9@ death on 1996-01-1" in death_errors

mbd1()
mbd2()
mbd3()
dbm1()
dbm2()
dbm3()