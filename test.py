from gedparse import main, check_divorce_before_death, check_marriage_before_death, check_dates_before_today
from pprint import pprint

marriage_before_death_errors, death_before_marriage_errors, birth_before_death_errors, marriage_before_divorce_errors, dates_before_today_errors= main()

#Lachlan
def mbd1():
	assert "ERROR: FAMILY: US05: 62: @F1@: Married 1994-07-7 after Husband's @I2@ death on 1990-01-1" in marriage_before_death_errors
	print("mbd1 passed")

def mbd2():
	assert "ERROR: FAMILY: US05: 62: @F2@: Married 1970-10-4 after Husband's @I6@ death on 1969-01-1" in marriage_before_death_errors
	print("mbd2 passed")

def mbd3():
	assert "ERROR: FAMILY: US05: 62: @F4@: Married 1993-06-9 after Husband's @I8@ death on 1992-01-1" in marriage_before_death_errors
	print("mbd3 passed")

def dbm1():
	assert "ERROR: FAMILY: US06: 77: @F1@: Divorced 1995-01-1 after Husband's @I2@ death on 1990-01-1" in death_before_marriage_errors
	print("dbm1 passed")

def dbm2():
	assert "ERROR: FAMILY: US06: 77: @F4@: Divorced 1997-01-1 after Husband's @I8@ death on 1992-01-1" in death_before_marriage_errors
	print("dbm2 passed")

def dbm3():
	assert "ERROR: FAMILY: US06: 77: @F4@: Divorced 1997-01-1 after Wife's @I9@ death on 1996-01-1" in death_before_marriage_errors
	print("dbm3 passed")

#Henry
def bbd1():
	assert "ERROR: INDIVIDUAL: US03: 9: @I2@: Died 1990-01-1 before born 2000-08-11" in birth_before_death_errors
	print("bbd1 passed")

def bbd2():
	assert "ERROR: INDIVIDUAL: US03: 9: @I3@: Died 1994-01-1 before born 2000-03-7" in birth_before_death_errors
	print("bbd2 passed")

def bbd3():
	assert "ERROR: INDIVIDUAL: US03: 9: @I6@: Died 1969-01-1 before born 1980-05-2" in birth_before_death_errors
	print("bbd3 passed")

def bbd4():
	assert "ERROR: INDIVIDUAL: US03: 9: @I7@: Died 1969-06-3 before born 1985-06-4" in birth_before_death_errors
	print("bbd4 passed")

def bbd5():
	assert "ERROR: INDIVIDUAL: US03: 9: @I8@: Died 1992-01-1 before born 1996-09-5" in birth_before_death_errors
	print("bbd5 passed")

#Jess
def cd1():
	assert "ERROR: INDIVIDUAL: US01: 9: @I1@: Birthday 2021-02-1 occurs in the future" in dates_before_today_errors
	print("cd1 passed")

def cd2():
	assert "ERROR: INDIVIDUAL: US01: 9: @I4@: Death 2022-01-1 occurs in the future" in dates_before_today_errors
	print("cd2 passed")

def cd3():
	assert "ERROR: FAMILY: US01: 9: @F3@: Marriage 2021-09-7 occurs in the future" in dates_before_today_errors
	print("cd3 passed")

def cd4():
	assert "ERROR: FAMILY: US01: 9: @F3@: Divorce 2022-01-1 occurs in the future" in dates_before_today_errors
	print("cd4 passed")

def cd5():
	assert "ERROR: INDIVIDUAL: US01: 9: @I5@: Birthday 2021-09-5 occurs in the future" in dates_before_today_errors
	print("cd5 passed")



mbd1()
mbd2()
mbd3()
dbm1()
dbm2()
dbm3()
bbd1()
bbd2()
bbd3()
bbd4()
bbd5()
cd1()
cd2()
cd3()
cd4()
cd5()