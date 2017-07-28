import csv
class Meal:
    def __init__(self, eater, beverage, protein):
        self.eater = eater
        self.beverage = beverage
        self.protein = protein

def serializer(fileobject, meals):
    output = csv.writer(fileobject, delimiter='\t')
    output.writerow([meals[0].eater,
        meals[0].beverage,
        meals[0].protein] )
    return fileobject

import io
def test_answer():

    meals = [Meal("aaron", "grape soda", "lamb?")]

    file = io.StringIO()
    file = serializer(file, meals)
    file.seek(0)
    assert file.read() == "aaron\tgrape soda\tlamb\r\n"
