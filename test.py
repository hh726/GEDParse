from gedparse import main, check_divorce_before_death, check_marriage_before_death
from pprint import pprint

marriage_before_death_errors, death_before_marriage_errors, birth_before_death_errors, marriage_before_divorce_errors = main()

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