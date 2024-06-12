import sqlite3
import csv

# მონაცემთა ბაზასთან კავშირის დამყარება
conn = sqlite3.connect('employee_satisfaction.db')
cursor = conn.cursor()

# მონაცემთა წაკითხვა და ჩაწერა CSV ფაილებში
def write_to_csv():
    # თანამშრომელთა ცხრილის წაკითხვა და ჩაწერა CSV-ში
    cursor.execute('SELECT * FROM employees')
    employees = cursor.fetchall()
    with open('employees.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['employee_id', 'name', 'department', 'position', 'hire_date'])
        writer.writerows(employees)

    # კმაყოფილების გამოკითხვის ცხრილის წაკითხვა და ჩაწერა CSV-ში
    cursor.execute('SELECT * FROM satisfaction_surveys')
    satisfaction_surveys = cursor.fetchall()
    with open('satisfaction_surveys.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['survey_id', 'employee_id', 'satisfaction_level', 'comments', 'survey_date'])
        writer.writerows(satisfaction_surveys)

    # მოტივაციის გამოკითხვის ცხრილის წაკითხვა და ჩაწერა CSV-ში
    cursor.execute('SELECT * FROM motivation_surveys')
    motivation_surveys = cursor.fetchall()
    with open('motivation_surveys.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['survey_id', 'employee_id', 'motivation_level', 'comments', 'survey_date'])
        writer.writerows(motivation_surveys)

# მონაცემთა CSV ფაილებში ჩაწერა
write_to_csv()

# კავშირის დახურვა
conn.close()
