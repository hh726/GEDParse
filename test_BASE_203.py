from gedparse import main, check_divorce_before_death, check_marriage_before_death, check_dates_before_today
from pprint import pprint

marriage_before_death_errors, death_before_marriage_errors, birth_before_death_errors, marriage_before_divorce_errors, dates_before_today_errors, birth_before_marriage, age_less_than_150, birth_before_parents_marriage = main()

#Lachlan
def mbd1():
	assert "ERROR: FAMILY: US05: 62: @F1@: Married 1994-07-7 after Husband's @I2@ death on 1990-01-1" in marriage_before_death_errors

def mbd2():
	assert "ERROR: FAMILY: US05: 62: @F2@: Married 1970-10-4 after Husband's @I6@ death on 1969-01-1" in marriage_before_death_errors

def mbd3():
	assert "ERROR: FAMILY: US05: 62: @F4@: Married 1993-06-9 after Husband's @I8@ death on 1992-01-1" in marriage_before_death_errors

def dbm1():
	assert "ERROR: FAMILY: US06: 77: @F1@: Divorced 1995-01-1 after Husband's @I2@ death on 1990-01-1" in death_before_marriage_errors

def dbm2():
	assert "ERROR: FAMILY: US06: 77: @F4@: Divorced 1997-01-1 after Husband's @I8@ death on 1992-01-1" in death_before_marriage_errors

def dbm3():
	assert "ERROR: FAMILY: US06: 77: @F4@: Divorced 1997-01-1 after Wife's @I9@ death on 1996-01-1" in death_before_marriage_errors

#Henry
def bbd1():
	assert "ERROR: INDIVIDUAL: US03: 9: @I2@: Died 1990-01-1 before born 2000-08-11" in birth_before_death_errors

def bbd2():
	assert "ERROR: INDIVIDUAL: US03: 9: @I3@: Died 1994-01-1 before born 2000-03-7" in birth_before_death_errors

def bbd3():
	assert "ERROR: INDIVIDUAL: US03: 9: @I6@: Died 1969-01-1 before born 1980-05-2" in birth_before_death_errors

def bbd4():
	assert "ERROR: INDIVIDUAL: US03: 9: @I7@: Died 1969-06-3 before born 1985-06-4" in birth_before_death_errors

def bbd5():
	assert "ERROR: INDIVIDUAL: US03: 9: @I8@: Died 1992-01-1 before born 1996-09-5" in birth_before_death_errors

#Jess
def cd1():
	assert "ERROR: INDIVIDUAL: US01: 9: @I1@: Birthday 2021-02-1 occurs in the future" in dates_before_today_errors
def cd2():
	assert "ERROR: INDIVIDUAL: US01: 9: @I4@: Death 2022-01-1 occurs in the future" in dates_before_today_errors
def cd3():
	assert "ERROR: FAMILY: US01: 9: @F3@: Marriage 2021-09-7 occurs in the future" in dates_before_today_errors
def cd4():
	assert "ERROR: FAMILY: US01: 9: @F3@: Divorce 2022-01-1 occurs in the future" in dates_before_today_errors
def cd5():
	assert "ERROR: INDIVIDUAL: US01: 9: @I5@: Birthday 2021-09-5 occurs in the future" in dates_before_today_errors

# -------------------------------------- Sprint 2 ------------------------------------------- #

#Lachlan

def ca1501():
	assert "ERROR: INDIVIDUAL: US07: 86: @I3@: More than 150 years old - Brith date 1771-03-7" in age_less_than_150

def ca1502():
	assert "ERROR: INDIVIDUAL: US07: 90: @I9@: More than 150 years old - Birth date 1270-08-4" in age_less_than_150

def ca1503():
	assert "ERROR: INDIVIDUAL: US07: 90: @I1@: More than 150 years old - Birth date 1859-02-1" in age_less_than_150

def bbm1():
	"ANOMALY: FAMILY: US08: 107: @F1@: Child @I1@ born 1859-02-1 before marriage on 1994-07-7" in birth_before_parents_marriage

def bbm2():
	"ANOMALY: FAMILY: US08: 107: @F2@: Child @I3@ born 1771-03-7 before marriage on 1970-10-4" in birth_before_parents_marriage



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
ca1501()
ca1502()
ca1503()
bbm1()
bbm2()