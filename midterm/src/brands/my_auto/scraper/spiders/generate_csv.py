import json
import csv


# Function to convert JSONL to CSV
def jsonl_to_csv(jsonl_file, csv_file):
    with open(jsonl_file, 'r') as infile, open(csv_file, 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=[
            "Manufacturer", "Model", "Year", "Category", "Mileage", "Fuel type",
            "Engine Volume", "Cylinders", "Gear box type", "Drive wheels", "Doors", "Airbags",
            "Wheel", "Interior material", "Technical inspection", "Catalyst", "Price"
        ])
        writer.writeheader()

        for line in infile:
            data = json.loads(line)
            writer.writerow(data)


# Example usage
jsonl_file_1 = "data_for_model_train.jsonl"
csv_file_1 = "train_data.csv"
jsonl_file_2 = "full_data.jsonl"
csv_file_2 = "full_cars_data.csv"
jsonl_to_csv(jsonl_file_1, csv_file_1)
jsonl_to_csv(jsonl_file_2, csv_file_2)
