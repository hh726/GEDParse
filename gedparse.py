from prettytable import PrettyTable
from datetime import datetime
from pprint import pprint

#Reads GED file and store input
with open('family.ged', 'r') as my_file:
    content = my_file.readlines()
    my_file.close()

#Stores all tags
ZERO_LEVEL = ["INDI", "FAM", "HEAD", "TRLR", "NOTE"]
ONE_LEVEL = ["NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS", "MARR", "HUSB", "WIFE", \
             "CHIL", "DIV"]
TWO_LEVEL = ["DATE"]

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

#Writes parsed inputs to a file
with open('results.txt', 'w') as result_file:
    for line in content:
        result_file.write(f"--> {line.rstrip()} \n")
        result_file.write(parse_number(line) + "\n")
    result_file.close()

#Creation of files


#Opens and read parsed output file
with open('results.txt', 'r') as file:
    lines = file.readlines()
    file.close()

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



individual_table = PrettyTable()
individual_table.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]
individuals_list = []
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

#Puts the rows into the individuals table
for person in individuals_list:
    individual_table.add_row(fill_individuals_table(person))

families_table = PrettyTable()
families_table.field_names = ["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"]
families_list = []

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


for family in families_list:
    families_table.add_row(fill_families_table(family))

with open("tables.txt", "w") as tables:
    tables.write(str(individual_table))
    tables.write(str(families_table))

    tables.close()

print(individual_table)
print(families_table)


# Marriage before death
def check_marriage_before_death():
    for person in individuals_list:
        death = person["Death"]
        spouse = person["Spouse"]
        if spouse != "N/A" and death != "N/A":
            for couple in families_list:
                if spouse == couple["ID"]:
                    if couple["Married"] > death:
                        print("ERROR: FAMILY: US05: 62: " + couple["ID"] +": Married " + couple["Married"] + " after " + ("Husband's " + couple["Husband ID"] + " death on " + death) if person["Gender"] == "M" else ("Wife's " + couple["Wife ID"] + "death on " + death))
    return

def check_divorce_before_death():
    for person in individuals_list:
        death = person["Death"]
        spouse = person["Spouse"]
        if spouse != "N/A" and death != "N/A":
            for couple in families_list:
                if spouse == couple["ID"]:
                    # if couple["Divorced"] != "N/A":
                        if couple["Divorced"] > death:
                            print("ERROR: FAMILY: US06: 77: " + couple["ID"] +": Divorced " + couple["Divorced"] + " after " + ("Husband's " + couple["Husband ID"] + " death on " + death) if person["Gender"] == "M" else ("Wife's " + couple["Wife ID"] + "death on " + death))
    return


def error_check_tables():
    check_marriage_before_death()
    check_divorce_before_death()
    return

error_check_tables()