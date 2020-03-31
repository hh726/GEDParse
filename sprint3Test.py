from gedparse import main
from pprint import pprint

marriage_before_death_errors, death_before_marriage_errors, birth_before_death_errors, marriage_before_divorce_errors, dates_before_today_errors, birth_before_marriage, age_less_than_150, birth_before_parents_marriage \
	,parent_not_too_old_errors, birth_before_death_of_parents, marriage_after_14, fewer_than_15_children_errors, male_last_name_errors, sibling_spacing_errors, multiple_birth_errors = main()

def ft15c():
    assert "ERROR: FAMILY: US15: 33: @F1@ has more than 15 siblings in the family" in fewer_than_15_children_errors
    print("Test ft15c passed...")

def mln():
    assert "ERROR: FAMILY: US16: 35: Male child @I8@'s last name /Liu/ is different from their fathers /Smith/" in male_last_name_errors
    print("Test mln passed...")

def sse():
    assert "Error: FAMILY: US13: 15: @I18@ and @I24@ born less than 8 months apart" in sibling_spacing_errors
    print("Test sse passed...")

if __name__ == '__main__':
    ft15c()
    mln()
    sse()
