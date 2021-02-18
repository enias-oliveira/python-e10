import csv


def create_character(filename, name, intelligence, power, strength, agility):

    expected_field_names = [
        "id",
        "name",
        "intelligence",
        "power",
        "strength",
        "agility",
    ]
    with open(filename, "r") as readable_file:
        reader = csv.DictReader(readable_file)

        if reader.fieldnames != expected_field_names:
            raise ValueError("CSV Fieldnames are invalid or dont exist")

        rows = list(reader)
        total_rows = len(rows)

        new_character_id = total_rows + 1

        new_character = {
            "id": new_character_id,
            "name": name,
            "intelligence": intelligence,
            "power": power,
            "strength": strength,
            "agility": agility,
        }

    with open(filename, "a") as writable_file:
        writer = csv.DictWriter(writable_file, fieldnames=expected_field_names)

        writer.writerow(new_character)

    return new_character


def find_character_by_id(filename, character_id):
    def convert_dict_number_values_to_int(dict_):
        number_atributes = ["id", "intelligence", "power", "strength", "agility"]

        return {
            key: (int(value) if (key in number_atributes) else value)
            for key, value in dict_.items()
        }

    with open(filename, "r") as readable_file:
        reader = csv.DictReader(readable_file)

        for row in reader:
            if row["id"] == str(character_id):
                return convert_dict_number_values_to_int(row)

    raise ValueError("Character not found by given id")
