from prettytable import PrettyTable
from datetime import datetime, date
from pprint import pprint
from dateutil import relativedelta
import sys

#Stores all tags
ZERO_LEVEL = ["INDI", "FAM", "HEAD", "TRLR", "NOTE"]
ONE_LEVEL = ["NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS", "MARR", "HUSB", "WIFE", \
             "CHIL", "DIV"]
TWO_LEVEL = ["DATE"]

# Variables used to indentify individuals. individuals_list is a list of dictionaries containing the attributes listed in the field names below
individual_table = PrettyTable()
individual_table.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]
individuals_list = []

# Variables used to indentify families. families_list is a list of dictionaries containing the attributes listed in the field names below
families_table = PrettyTable()
families_table.field_names = ["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"]
families_list = []

#Parses the input line and returns output line
def parse_number(line):
    split_line = line.rstrip().split(" ")
    level_number = split_line[0]
    if level_number == "0":
        return handle_0(split_line)
    elif level_number == "1":
        return handle_1(split_line)
    else:
        return handle_2(split_line)

#Handles the line if it is 0th level
def handle_0(line):
    level = line[0]
    if check_format(line) == 1:
        tag = line[1]
        arguments = get_arguments(line)
        return f"<-- {level}|{tag}|Y|{arguments}"
    if check_format(line) == 2:
        tag = line[2]
        arguments = line[1]
        return f"<-- {level}|{tag}|Y|{arguments}"
    tag = line[1]
    arguments = get_arguments(line)
    return f"<-- {level}|{tag}|N|{arguments}"

#Handles the line if it is 1st level
def handle_1(line):
    level = line[0]
    tag = line[1]
    valid = "Y" if line[1] in ONE_LEVEL else "N"
    arguments = get_arguments(line)
    return f"<-- {level}|{tag}|{valid}|{arguments}"

#Handles the line if it is 2nd level
def handle_2(line):
    level = line[0]
    tag = line[1]
    valid = "Y" if line[1] in TWO_LEVEL else "N"
    arguments = get_arguments(line)
    return f"<-- {level}|{tag}|{valid}|{arguments}"

#Gets all of the arguments of a line 
def get_arguments(lst):
    string = ""
    for i in range(2, len(lst)):
        string += lst[i]
        string += " "
    return string

#Used in 0th level check to handle the scenario of the tag being in the 2nd or 3rd slot
def check_format(line):
    if (line[1] == "HEAD" or line[1] == "TRLR") and len(line) == 2:
        return 1
    if line[1] == "NOTE":
        return 1
    if line[2] == "FAM" or line[2] == "INDI":
        return 2
    return 3

#Stores the output lines of the parsed file in a list
def store_parsed_lines(file_content):
    parsed_lines = []
    for line in file_content:
        if line.split(" ")[0] == "<--":
            if line.split("|")[2] == "Y":
                parsed_lines.append(line[4:].rstrip())
    return parsed_lines

#Function to change GED date into formatted date
def parse_date(date_string):
    reference = {"JAN": "01", "FEB":"02", "MAR": "03", "APR": "04", "MAY": "05", "JUN": "06",\
                 "JUL": "07", "AUG": "08", "SEP": "09", "OCT": "10", "NOV": "11", "DEC": "12"}
    parsed = date_string.split(" ")
    day = parsed[0]
    month = reference[parsed[1]]
    year = parsed[2]
    return f"{year}-{month}-{day}"
#Calculate a person's age
def calculate_age(birthday):
    today = datetime.today()
    birthday = datetime.strptime(birthday, '%Y-%m-%d')
    return (today - birthday).days // 365

#Returns one row of an individual
def fill_individuals_table(individual):
    returnlist = []
    returnlist.append(individual["ID"])
    returnlist.append(individual["Name"])
    returnlist.append(individual["Gender"])
    returnlist.append(individual["Birthday"])
    returnlist.append(individual["Age"])
    returnlist.append(individual["Alive"])
    returnlist.append(individual["Death"])
    returnlist.append(individual["Child"])
    returnlist.append(individual["Spouse"])
    return returnlist

def fill_families_table(family):
    returnlist = []
    returnlist.append(family["ID"])
    returnlist.append(family["Married"])
    returnlist.append(family["Divorced"])
    returnlist.append(family["Husband ID"])
    returnlist.append(family["Husband Name"])
    returnlist.append(family["Wife ID"])
    returnlist.append(family["Wife Name"])
    returnlist.append(family["Children"])
    return returnlist

#Date before current date
def check_dates_before_today(arr):
    today = str(date.today())
    for person in individuals_list:
        death = person["Death"]
        birth = person["Birthday"]
        person_id = person["ID"]
        if birth > today:    
            err = f"ERROR: INDIVIDUAL: US01: 9: {person_id}: Birthday {birth} occurs in the future"   
            print(err)
            arr.append(err)    
        elif death == "NA":
            continue
        elif death > today:
            err = f"ERROR: INDIVIDUAL: US01: 9: {person_id}: Death {death} occurs in the future"
            print(err)
            arr.append(err)
    for couple in families_list:
        family_id = couple["ID"]
        marriage = couple["Married"]
        divorce = couple["Divorced"]
        if marriage > today:
            err = f"ERROR: FAMILY: US01: 9: {family_id}: Marriage {marriage} occurs in the future"
            print(err)
            arr.append(err)
        if divorce == "N/A":
            continue
        if divorce > today:
            err = f"ERROR: FAMILY: US01: 9: {family_id}: Divorce {divorce} occurs in the future"
            print(err)
            arr.append(err)
    return arr

#Born before marriage
def check_birth_before_marriage(arr):
	for person in individuals_list:
		birth = person["Birthday"]
		for couple in families_list:
			family_id = couple["ID"]
			marriage = couple["Married"]
			if marriage == "N/A":
				continue
			if person["ID"] == couple["Husband ID"] or person["ID"] == couple["Wife ID"]:
				if marriage < birth:
					err = f"ERROR: FAMILY: US02: 24:{family_id}:  "
					if(person["Gender"] == "M"):
						err = err + f"Husband's birth date {birth} after marriage date {marriage}"
					else:
						err = err + f"Wife's birth date {birth} after marriage date {marriage}"
						print(err)
						arr.append(err)
	return arr

#Birth before death
def check_birth_before_death(arr):
	for person in individuals_list:
		death = person["Death"]
		birth = person["Birthday"]
		person_id = person["ID"]
		if death == "N/A":
			continue
		if death < birth:
			err = f"ERROR: INDIVIDUAL: US03: 9: {person_id}: Died {death} before born {birth}"
			print(err)
			arr.append(err)
	return arr

# Marriage before divorce
def check_marriage_before_divorce(arr):
	for couple in families_list:
		marriage = couple["Married"]
		divorce = couple["Divorced"]
		family_id = couple["ID"]
		if divorce == "N/A":
			continue
		if divorce < marriage:
			err = f"ERROR: FAMILY: US04: 45: {family_id}: Divorced {divorce} before married {marriage}"
			print(err)
			arr.append(err)
	return arr

# Marriage before death
def check_marriage_before_death(arr):
	for person in individuals_list:
		death = person["Death"]
		spouse = person["Spouse"]
		if spouse != "N/A" and death != "N/A":
			for couple in families_list:
				if spouse == couple["ID"]:
					if couple["Married"] > death:
						err = "ERROR: FAMILY: US05: 62: " + couple["ID"] +": Married " + couple["Married"] + " after "
						# ("Husband's " + couple["Husband ID"] + " death on " + death) if (person["Gender"] == "M") else ("Wife's " + couple["Wife ID"] + "death on " + death)
						if(person["Gender"] == "M"):
							err = err + "Husband's " + couple["Husband ID"] + " death on " + death
						else:
							err = err + "Wife's " + couple["Wife ID"] + " death on " + death
						print(err)
						arr.append(err)
	return arr

def check_divorce_before_death(arr):
	for person in individuals_list:
		death = person["Death"]
		spouse = person["Spouse"]
		if spouse != "N/A" and death != "N/A":
			for couple in families_list:
				if spouse == couple["ID"]:
					if couple["Divorced"] != "N/A" and couple["Divorced"] > death:
						err = "ERROR: FAMILY: US06: 77: " + couple["ID"] +": Divorced " + couple["Divorced"] + " after "
						if(person["Gender"] == "M"):
							err = err + "Husband's " + couple["Husband ID"] + " death on " + death
						else:
							err = err + "Wife's " + couple["Wife ID"] + " death on " + death
						print(err)
						arr.append(err)
	return arr

def check_age_less_than_150(arr):
	for person in individuals_list:
		birthday = person["Birthday"]
		birthday = datetime.strptime(birthday, '%Y-%m-%d').date()
		age = (relativedelta.relativedelta(date.today(), birthday)).years
		if(age > 150):
			error_msg = "ERROR: INDIVIDUAL: US07: 90: " + person["ID"] + ": More than 150 years old - Birth date " + person["Birthday"]
			arr.append(error_msg)
			print(error_msg)
	return arr

def check_birth_before_parents_marriage(arr):
	for family in families_list:
		if family["Children"]:
			children = (family["Children"].strip()).split(" ")
			for person in individuals_list:
				if person["ID"] in children:
					childsBirthday = datetime.strptime(person["Birthday"], '%Y-%m-%d').date()
					parentsMarriage = datetime.strptime(family["Married"], '%Y-%m-%d').date()
					if childsBirthday < parentsMarriage:
						error_msg = "ANOMALY: FAMILY: US08: 107: " + family["ID"] + ": Child " + person["ID"] + " born " + person["Birthday"] + " before marriage on " + family["Married"] 
						arr.append(error_msg)
						print(error_msg)
	return arr

def check_birth_before_death_of_parents(arr):
	for family in families_list:
		if family['Children'] != '':
			children = family['Children'].split(' ')
			for child in children:
				for child in children:
					if child != '':
						father = family["Husband Name"]
						mother = family["Wife Name"]
						for person in individuals_list:
							if person["Name"] == father:
								father_death = person["Death"]
							if person["Name"] == mother:
								mother_death = person["Death"]
							if person["ID"] == child:
								child_birth = person["Birthday"]
						if child_birth > father_death:
							err = "ERROR: FAMILY: US09: 80: " + family["ID"] + " Father died before child born"
							print(err)
							arr.append(err)
						if child_birth > mother_death:
							err = "ERROR: FAMILY: US09: 80: " + family["ID"] + " Mother died before child born"
							print(err)
							arr.append(err)
	return arr

def check_marriage_after_14(arr):
	#married after 14 years after birth
	for person in individuals_list:
		birthday = person["Birthday"]
		birthday = datetime.strptime(birthday, '%Y-%m-%d').date()
		age = (relativedelta.relativedelta(date.today(), birthday)).years
		for couple in families_list:
			married = couple["Married"]
			family_id = couple["ID"]

			if age < 14 and married:
				err = "ERROR: COUPLE: US10: 82: @F3@ : Married before 14 years old."
				print(err)
				arr.append(err)
	return arr
						
							
def check_parents_not_too_old(arr):
	for family in families_list:
		if family['Children'] != '':
			children = family['Children'].split(' ')
			for child in children:
				if child != '':
					father_name = family["Husband Name"]
					mother_name = family["Wife Name"]
					for person in individuals_list:
						if person["Name"] == father_name:
							father_age = person["Age"]
						if person["Name"] == mother_name:
							mother_age = person["Age"]
						if person["ID"] == child:
							child_age = person["Age"]
					if father_age - child_age >= 80:
						err = "ERROR: FAMILY: US12: 34: " + family["ID"] + " Father more than 80 years older than child"
						print(err)
						arr.append(err)
					if mother_age - child_age >= 60:
						err = "ERROR: FAMILY: US12: 34: " + family["ID"] + " Mother more than 60 years older than child"
						print(err)
						arr.append(err)
def no_bigamy(arr):
	dont_touch = []
	for family1 in families_list:
		for family2 in families_list:
			if family1["ID"] != family2["ID"] and family1 not in dont_touch:
				if family1["Husband Name"] == family2["Husband Name"] or family1["Wife Name"] == family2["Wife Name"]:

					dont_touch.append(family2)
					family1ID = family1["ID"]
					family2ID = family2["ID"]
					if family1["Divorced"] == "N/A" and family2["Divorced"] == "N/A":
						err = f"ERROR: FAMILY: US13: 32: {family1ID} and {family2ID} has committed bigamy"
						print(err)
						arr.append(err)

def fewer_than_15_siblings():
	arr = []
	for family in families_list:
		num_children = (len(family["Children"].split(" "))) - 1 
		if(num_children > 15):
			familyID = family["ID"]
			err = f"ERROR: FAMILY: US15: 33: {familyID} has more than 15 siblings in the family"
			print(err)
			arr.append(err)
	return arr

def male_last_names():
	arr = []
	for family in families_list:
		husband_ln = family["Husband Name"].split(" ")[1]
		children = family["Children"].split(" ")
		if(len(children) > 1):
			children = children[:-1]
			for child in children:
				for person in individuals_list:
					if(person['ID'] == child and person["Gender"] == 'M'):
						ln = person["Name"].split(" ")[1]
						if(ln != husband_ln):
							err = "ERROR: FAMILY: US16: 35: Male child " + person['ID'] + "'s last name " + ln + " is different from their fathers " + husband_ln
							print(err)
							arr.append(err)
	return arr

def siblings_spacing(arr):
	for family in families_list:
		all_children = []
		children = family["Children"].split(" ")
		for child in children:
			if child != '':
				all_children.append(child)
		if len(all_children) > 1:
			for i in range(len(all_children)):
				for j in range(i+1, len(all_children)):
					for person in individuals_list:
						if person["ID"] == all_children[i]:
							child1 = person["Birthday"]
							child_id1 = all_children[i]
						if person["ID"] == all_children[j]:
							child2 = person["Birthday"]
							child_id2 = all_children[j]
					child1birthday = datetime.strptime(child1, '%Y-%m-%d').date()
					child2birthday = datetime.strptime(child2, '%Y-%m-%d').date()
					if ((relativedelta.relativedelta(child1birthday, child2birthday)).months < 8) and \
						((relativedelta.relativedelta(child1birthday, child2birthday)).days < 1):
						err = f"Error: FAMILY: US13: 15: {child_id1} and {child_id2} born less than 8 months apart"
						print(err)
						arr.append(err)
				
	return arr

def multiple_births(arr):
	for family in families_list:
		all_children = []
		children = family["Children"].split(" ")
		for child in children:
			if child != '':
				all_children.append(child)
	family_id = family["ID"]
	if len(all_children) >= 5:
		multiple = 0
		for i in range(len(all_children)):
			for j in range(i+1, len(all_children)):
				for person in individuals_list:
					if person["ID"] == all_children[i]:
						child1 = person["Birthday"]
						child_id1 = all_children[i]
					if person["ID"] == all_children[j]:
						child2 = person["Birthday"]
						child_id2 = all_children[j]
				child1birthday = datetime.strptime(child1, '%Y-%m-%d').date()
				child2birthday = datetime.strptime(child2, '%Y-%m-%d').date()
				if ((relativedelta.relativedelta(child1birthday, child2birthday)).days < 1):
					multiple += 1
		if multiple >= 5:
			err = f"Error: FAMILY: US14: 44: {family_id} has 5 child born at once"
			print(err)
			arr.append(err)
	return arr

def no_marriages_to_descendants(arr):
	for person in individuals_list:
		spouse = person["Spouse"]
		person_id = person["ID"]
		for family in families_list:
			# print(person["Name"])
			# print(family["Children"])
			if family['Children'] != '' and family["ID"] == person["Spouse"]:
				children = family['Children'].split(' ')
				for child in children:
					father = family["Husband Name"]
					mother = family["Wife Name"]
					if spouse == father or mother:
						err = f"Error: FAMILY: US17: {person_id} can't be married to a decesndant"	
						print(err)		
						arr.append(err)	
	return arr

def no_siblings_marriage(arr):
	for person in individuals_list:
		spouse = person["Spouse"]
		person_id = person["ID"]
		for family in families_list:
			if family['Children'] != '':
				children = family['Children'].split(' ')
				for child in children:
					if spouse == child:
						err = f"Error: FAMILY US18: {person_id} can't be married to it's sibling"
						print(err)
						arr.append(err)
		
				
def check_cousin_marriage():
	arr = []
	for couple in families_list:
		Husband_Grandparent_list = []
		Wife_Grandparent_list = []
		if(couple["Husband ID"] != "N/A"):
			for person in individuals_list:
				if(person["ID"] == couple["Husband ID"]):
					for parentCouple in families_list:
						if(parentCouple["ID"] == person["Child"]):
							if(parentCouple["Husband ID"] != "N/A"):
								for parent in individuals_list:
									if(parent["ID"] == parentCouple["Husband ID"]):
										Husband_Grandparent_list.append(parent["Child"])
							if(parentCouple["Wife ID"] != "N/A"):
								for parent in individuals_list:
									if(parent["ID"] == parentCouple["Wife ID"]):
										Husband_Grandparent_list.append(parent["Child"])
		if(couple["Wife ID"] != "N/A"):
			for person in individuals_list:
				if(person["ID"] == couple["Wife ID"]):
					for parentCouple in families_list:
						if(parentCouple["ID"] == person["Child"]):
							if(parentCouple["Husband ID"] != "N/A"):
								for parent in individuals_list:
									if(parent["ID"] == parentCouple["Husband ID"]):
										Wife_Grandparent_list.append(parent["Child"])
							if(parentCouple["Wife ID"] != "N/A"):
								for parent in individuals_list:
									if(parent["ID"] == parentCouple["Wife ID"]):
										Wife_Grandparent_list.append(parent["Child"])

		Husband_Grandparent_list = list(dict.fromkeys(Husband_Grandparent_list))
		Wife_Grandparent_list = list(dict.fromkeys(Wife_Grandparent_list))
		common_grandparents = set(Husband_Grandparent_list).intersection(Wife_Grandparent_list)
		err = "ERROR: FAMILY: US19: Husband " + couple["Husband ID"] +" and Wife " + couple["Wife ID"] + " are first cousins"
		if(len(common_grandparents) != 0):
			print(err)
			arr.append(err)
		return arr

def check_neice_nephew_aunt_uncle():
	arr = []
	for couple in families_list:
		Husband_Parent_list = []
		Husband_Grandparent_list = []
		Wife_Parent_list = []
		Wife_Grandparent_list = []

		if(couple["Husband ID"] != "N/A"):
			for person in individuals_list:
				if(person["ID"] == couple["Husband ID"]):
					for parentCouple in families_list:
						if(parentCouple["ID"] == person["Child"]):
							Husband_Parent_list.append(person["Child"])
							if(parentCouple["Husband ID"] != "N/A"):
								for parent in individuals_list:
									if(parent["ID"] == parentCouple["Husband ID"]):
										Husband_Grandparent_list.append(parent["Child"])
							if(parentCouple["Wife ID"] != "N/A"):
								for parent in individuals_list:
									if(parent["ID"] == parentCouple["Wife ID"]):
										Husband_Grandparent_list.append(parent["Child"])
		if(couple["Wife ID"] != "N/A"):
			for person in individuals_list:
				if(person["ID"] == couple["Wife ID"]):
					for parentCouple in families_list:
						if(parentCouple["ID"] == person["Child"]):
							Wife_Parent_list.append(person["Child"])
							if(parentCouple["Husband ID"] != "N/A"):
								for parent in individuals_list:
									if(parent["ID"] == parentCouple["Husband ID"]):
										Wife_Grandparent_list.append(parent["Child"])
							if(parentCouple["Wife ID"] != "N/A"):
								for parent in individuals_list:
									if(parent["ID"] == parentCouple["Wife ID"]):
										Wife_Grandparent_list.append(parent["Child"])
										
		Husband_Parent_list = list(dict.fromkeys(Husband_Parent_list))
		Husband_Grandparent_list = list(dict.fromkeys(Husband_Grandparent_list))		
		Wife_Parent_list = list(dict.fromkeys(Wife_Parent_list))
		Wife_Grandparent_list = list(dict.fromkeys(Wife_Grandparent_list))

		if "N/A" in Husband_Parent_list:
			Husband_Parent_list.remove("N/A")
		if "N/A" in Husband_Grandparent_list:
			Husband_Grandparent_list.remove("N/A")
		if "N/A" in Wife_Parent_list:
			Wife_Parent_list.remove("N/A")
		if "N/A" in Wife_Grandparent_list:
			Wife_Grandparent_list.remove("N/A")	

		common_fam1 = set(Husband_Grandparent_list).intersection(Wife_Parent_list)
		common_fam2 = set(Wife_Grandparent_list).intersection(Husband_Parent_list)

		err = "ERROR: FAMILY: US20: Husband " + couple["Husband ID"] +" and Wife " + couple["Wife ID"] + " are Aunt/Uncle married to their Niece/Nephew"
		if(len(common_fam1) != 0 or len(common_fam2) != 0):
			print(err)
			arr.append(err)
	return arr

def error_check_tables():
	cmbd = check_marriage_before_death([])
	cdbf = check_divorce_before_death([])
	cbbd = check_birth_before_death([])
	cmbdv = check_marriage_before_divorce([])
	cdbt = check_dates_before_today([])
	cbbm = check_birth_before_marriage([])
	cbbdop = check_birth_before_death_of_parents([])
	cma14 = check_marriage_after_14([])
	calt150 = check_age_less_than_150([])
	cbbpm = check_birth_before_parents_marriage([])
	cpnto = check_parents_not_too_old([])
	nb = no_bigamy([])
	ft15c = fewer_than_15_siblings()
	mln = male_last_names()
	ss = siblings_spacing([])
	mb = multiple_births([])
	nmtd = no_marriages_to_descendants([])
	nsm = no_siblings_marriage([])
	ccm = check_cousin_marriage()
	cnnau = check_neice_nephew_aunt_uncle()
	return cmbd, cdbf, cbbd, cmbdv, cdbt, cbbm, calt150, cbbpm, cpnto, cbbdop, cma14, ft15c, mln, ss, mb, nmtd, nsm, ccm, cnnau

def main():
	if(len(sys.argv) != 2):
		print("Usage: 'python3 file.ged'")
		return -1

	#Reads GED file and store input
	# with open('testInputSprint3.ged', 'r') as my_file:
	with open(sys.argv[1], 'r') as my_file:
		content = my_file.readlines()
		my_file.close()

	with open('results.txt', 'w') as result_file:
	    for line in content:
	        result_file.write(f"--> {line.rstrip()} \n")
	        result_file.write(parse_number(line) + "\n")
	    result_file.close()

	#Opens and read parsed output file
	with open('results.txt', 'r') as file:
	    lines = file.readlines()
	    file.close()

	parsed_lines = store_parsed_lines(lines)

	#Pretty ugly code to parse string into the individuals table
	parse_birthday = False
	parse_deathdate = False
	current_member = None
	for line in parsed_lines:
	    split_line = line.split("|")
	    if split_line[1] == "INDI":
	        if current_member:
	            individuals_list.append(member_dict)
	        current_member = split_line[3]
	        member_dict = {"ID": current_member}
	        member_dict["Child"] = "N/A"
	        member_dict["Spouse"] = "N/A"
	        
	    if split_line[1] == "NAME":
	        member_dict["Name"] = split_line[3]
	    if split_line[1] == "SEX":
	        member_dict["Gender"] = split_line[3]
	    if split_line[1] == "BIRT":
	        parse_birthday = True
	    if split_line[0] == "2" and split_line[1] == "DATE" and parse_birthday == True:
	        birthdate = parse_date(split_line[3])
	        member_dict["Birthday"] = birthdate
	        member_dict["Age"] = calculate_age(birthdate)
	        parse_birthday = False

	        member_dict["Alive"] = "True"
	        member_dict["Death"] = "NA"
	        
	    if split_line[1] == "DEAT":
	        parse_deathdate = True
	    if split_line[0] == "2" and split_line[1] == "DATE" and parse_deathdate == True:
	        deathdate = parse_date(split_line[3])
	        member_dict["Alive"] = "False"
	        member_dict["Death"] = deathdate
	        parse_deathdate = False
	    if split_line[1] == "FAMC":
	        member_dict["Child"] = split_line[3]
	    if split_line[1] == "FAMS":
	        member_dict["Spouse"] = split_line[3]
	if current_member:
	    individuals_list.append(member_dict)

	#Puts the rows into the individuals table
	for person in individuals_list:
	    individual_table.add_row(fill_individuals_table(person))

	parse_marriage = False
	parse_divorce = False
	current_family = None
	for line in parsed_lines:
	    split_line = line.split("|")
	    if split_line[1] == "FAM":
	        if current_family:
	            families_list.append(family_dict)
	        current_family = split_line[3]
	        family_dict = {"ID": current_family}
	        children_lst = []
	        member_dict["Married"] = "N/A"
	        member_dict["Divorced"] = "N/A"
	    if split_line[1] == "HUSB":
	        family_dict["Husband ID"] = split_line[3]
	        for person in individuals_list:
	            if person["ID"] == split_line[3]:
	                family_dict["Husband Name"] = person["Name"]
	    if split_line[1] == "WIFE":
	        family_dict["Wife ID"] = split_line[3]
	        for person in individuals_list:
	            if person["ID"] == split_line[3]:
	                family_dict["Wife Name"] = person["Name"]
	    if split_line[1] == "CHIL":
	        for person in individuals_list:
	            if person["ID"] == split_line[3]:
	                children_lst.append(person["ID"])
	    if split_line[1] == "MARR":
	        string = ""
	        for child in children_lst:
	            string += child + " "
	        family_dict["Children"] = string
	        parse_marriage = True
	    if split_line[0] == "2" and split_line[1] == "DATE" and parse_marriage == True:
	        marriage = parse_date(split_line[3])
	        family_dict["Married"] = marriage
	        parse_marriage = False
	        family_dict["Divorced"] = "N/A"
	        
	    if split_line[1] == "DIV":
	        parse_divorce = True
	    if split_line[0] == "2" and split_line[1] == "DATE" and parse_divorce == True:
	        divorce = parse_date(split_line[3])
	        family_dict["Divorced"] = divorce
	        parse_divorce = False


	if current_family:
	    families_list.append(family_dict)

	for family in families_list:
	    families_table.add_row(fill_families_table(family))

	with open("tables.txt", "w") as tables:
	    tables.write(str(individual_table))
	    tables.write(str(families_table))
	    tables.close()

	print(individual_table)
	print(families_table)
	error_check_tables()
	# return error_check_tables()

if __name__ == '__main__':	
	main()