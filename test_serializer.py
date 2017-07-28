import csv
import pdb
class Meal:
    def __init__(self, eater, beverage, protein):
        self.eater = eater
        self.beverage = beverage
        self.protein = protein

class Breathatarian:
    def __init__(self, eater):
        self.eater = eater

class Diet(Meal):
    def __init__(self, eater, beverage):
        self.eater = eater
        self.beverage = beverage

class Snack(Meal):
    def __init__(self, eater, beverage, dessert):
        self.eater = eater
        self.beverage = beverage
        self.dessert = dessert

class TastingMenu(Meal):
    def __init__(self, eater, beverage, protein, dessert):
        self.eater = eater
        self.beverage = beverage
        self.protein = protein
        self.dessert = dessert

def serializer(fileobject, meals):
    output = csv.writer(fileobject, delimiter='\t')
    fields = []
    for m in meals:
        
        fields.extend(list(vars(m).keys()))
    
    fieldset = set(fields)
    
    output.writerow(list(fieldset))
    print(list(fieldset))
    for m in meals:
        values = []
        for f in fieldset:
            values.append(getattr(m, f, ""))
        output.writerow(values)
        print(values)
    return fileobject

import io
import unittest

class CsvTest(unittest.TestCase):
    def setUp(self):
        self.file = io.StringIO()
        self.file = serializer(self.file, self.get_meals())
        self.file.seek(0)
        self.header = self.file.readline()

    def test_header(self):
        sorted_header = self.header.split("\t")
        expected_header = sorted(["eater", "beverage", "protein", "dessert"])
        assert self.header == expected_header

    def get_meals(self):
        return []

class CsvTestAnswer(CsvTest):
    def get_meals(self):
        return [Meal("aaron", "grape soda", "lamb?")]

    def test_answer(self):
        assert self.file.read() == "aaron\tgrape soda\tlamb?\t\r\n"

class CsvTestMultipleObjects(CsvTest):
    def get_meals(self):
        meals = [Meal("aaron", "grape soda", "lamb?")]
        meals.append(Meal("rob", "Ginger Ale", "combo"))
        return meals

    def test_multiple_objects(self):
        assert self.file.read() == "aaron\tgrape soda\tlamb?\t\r\nrob\tGinger Ale\tcombo\t\r\n"

class CsvTestMultipleDifferentObjects(CsvTest):
    def get_meals(self):
        meals = [Meal("aaron", "grape soda", "lamb?")]
        meals.append(Meal("rob", "Ginger Ale", "combo"))
        meals.append(Diet("mike", "Water"))
        return meals

    def test_multiple_different_objects(self):
        assert self.file.read() == "aaron\tgrape soda\tlamb?\t\r\nrob\tGinger Ale\tcombo\t\r\nmike\tWater\t\t\r\n"

class CsvTestObjectWithExtraField(CsvTest):
    def get_meals(self):
        return [Snack("adam", "Big Gulp", "reeses")]

    def test_object_with_extra_field(self):
        assert self.file.read() == "adam\tBig Gulp\t\treeses\r\n"

class CsvTestObjectWithIntersectingFields(CsvTest):
    def get_meals(self):
        return [TastingMenu("chrissy", "champagne", "lobster thermidor", "baked alaska")]

    def test_object_with_intersecting_fields(self):
        assert self.file.read() == "chrissy\tchampagne\tlobster thermidor\tbaked alaska\r\n"
