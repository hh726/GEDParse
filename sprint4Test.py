from gedparse import main
from pprint import pprint

marriage_before_death_errors, death_before_marriage_errors, birth_before_death_errors, marriage_before_divorce_errors, dates_before_today_errors, birth_before_marriage, age_less_than_150, birth_before_parents_marriage \
	,parent_not_too_old_errors, birth_before_death_of_parents, marriage_after_14, fewer_than_15_children_errors, male_last_name_errors, sibling_spacing_errors, multiple_birth_errors, no_marriages_to_descendants_errors, \
    no_siblings_marriage_errors, check_cousin_marriage_errors, check_neice_nephew_aunt_uncle, check_unique_name_and_birth, check_unique_spouse_and_marriage_date, correct_gender_for_role  , unique_ids = main("Sprint4.ged")

def married_to_cousin():
    assert "ERROR: FAMILY: US19: Husband @I1@ and Wife @I2@ are first cousins" in check_cousin_marriage_errors
    print("Test married_to_cousin passed")

def married_to_aunt_uncle():
    assert "ERROR: FAMILY: US20: Husband @I7@ and Wife @I13@ are Aunt/Uncle married to their Niece/Nephew" in check_neice_nephew_aunt_uncle
    print("Test married_to_aunt_uncle passed")

def unique_name_and_birth():
    assert "ERROR: INDI: US23: @I2@ does not have a unique DOB and Name" in check_unique_name_and_birth
    print("Test unique_name_and_birth passed")

def unique_spouse_and_marriage_date():
    assert "ERROR: FAM: US24: @F2@ does not have unique spouse names and marriage date" in check_unique_spouse_and_marriage_date
    print("Test unique_spouse_and_marriage_date passed")
def correct_gender_for_role1():
    assert "ERROR: FAM: US21 Lachlan /Mountjoy/ in @F1@family does not have correct gender" in correct_gender_for_role
    print("Test correct_gender_for_role1 passed")

def correct_gender_for_role2():
    assert "ERROR: FAM: US21 Alice /Mountjoy/ in @F7@ family does not have correct gender" in correct_gender_for_role
    print("Test correct_gender_for_role2 passed")


if __name__ == '__main__':
    married_to_cousin()
    married_to_aunt_uncle()
    unique_name_and_birth()
    unique_spouse_and_marriage_date()
    correct_gender_for_role1()
    correct_gender_for_role2()
