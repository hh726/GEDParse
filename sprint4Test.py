from gedparse import main
from pprint import pprint

marriage_before_death_errors, death_before_marriage_errors, birth_before_death_errors, marriage_before_divorce_errors, dates_before_today_errors, birth_before_marriage, age_less_than_150, birth_before_parents_marriage \
	,parent_not_too_old_errors, birth_before_death_of_parents, marriage_after_14, fewer_than_15_children_errors, male_last_name_errors, sibling_spacing_errors, multiple_birth_errors, no_marriages_to_descendants_errors, no_siblings_marriage_errors, check_cousin_marriage_errors, check_neice_nephew_aunt_uncle, check_unique_name_and_birth  = main("Sprint4.ged")

def married_to_cousin():
    assert "ERROR: FAMILY: US19: Husband @I1@ and Wife @I2@ are first cousins" in check_cousin_marriage_errors
    print("Test married_to_cousin passed")

def married_to_aunt_uncle():
    assert "ERROR: FAMILY: US20: Husband @I7@ and Wife @I13@ are Aunt/Uncle married to their Niece/Nephew" in check_neice_nephew_aunt_uncle
    print("Test married_to_aunt_uncle passed")

def unique_name_and_birth():
    assert "ERROR: INDI: US23: @I2@ does not have a unique DOB and Name" in check_unique_name_and_birth
    print("Test unique_name_and_birth passed")

if __name__ == '__main__':
    married_to_cousin()
    married_to_aunt_uncle()
    unique_name_and_birth()
