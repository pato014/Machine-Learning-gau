import sqlite3
import random
import faker

# მონაცემთა ბაზის შექმნა
conn = sqlite3.connect('employee_satisfaction.db')
cursor = conn.cursor()

# ცხრილების შექმნა
cursor.execute('''
CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY,
    name TEXT,
    department TEXT,
    position TEXT,
    hire_date TEXT
)
''')

cursor.execute('''
CREATE TABLE satisfaction_surveys (
    survey_id INTEGER PRIMARY KEY,
    employee_id INTEGER,
    satisfaction_level INTEGER,
    comments TEXT,
    survey_date TEXT,
    FOREIGN KEY (employee_id) REFERENCES employees (employee_id)
)
''')

cursor.execute('''
CREATE TABLE motivation_surveys (
    survey_id INTEGER PRIMARY KEY,
    employee_id INTEGER,
    motivation_level INTEGER,
    comments TEXT,
    survey_date TEXT,
    FOREIGN KEY (employee_id) REFERENCES employees (employee_id)
)
''')

# მონაცემთა გენერაციის ფუნქცია
def generate_data():
    fake = faker.Faker()
    departments = ['HR', 'Sales', 'Development', 'Marketing', 'Finance']
    positions = ['Manager', 'Senior Developer', 'Junior Developer', 'Salesperson', 'Analyst']

    # თანამშრომელთა მონაცემების გენერაცია
    employees = []
    for _ in range(100):
        employee = (
            fake.name(),
            random.choice(departments),
            random.choice(positions),
            fake.date_between(start_date='-10y', end_date='today')
        )
        employees.append(employee)

    cursor.executemany('''
    INSERT INTO employees (name, department, position, hire_date)
    VALUES (?, ?, ?, ?)
    ''', employees)

    # კმაყოფილების გამოკითხვის მონაცემების გენერაცია
    satisfaction_surveys = []
    for employee_id in range(1, 101):
        for _ in range(random.randint(1, 3)):
            survey = (
                employee_id,
                random.randint(1, 10),
                fake.sentence(),
                fake.date_this_year()
            )
            satisfaction_surveys.append(survey)

    cursor.executemany('''
    INSERT INTO satisfaction_surveys (employee_id, satisfaction_level, comments, survey_date)
    VALUES (?, ?, ?, ?)
    ''', satisfaction_surveys)

    # მოტივაციის გამოკითხვის მონაცემების გენერაცია
    motivation_surveys = []
    for employee_id in range(1, 101):
        for _ in range(random.randint(1, 3)):
            survey = (
                employee_id,
                random.randint(1, 10),
                fake.sentence(),
                fake.date_this_year()
            )
            motivation_surveys.append(survey)

    cursor.executemany('''
    INSERT INTO motivation_surveys (employee_id, motivation_level, comments, survey_date)
    VALUES (?, ?, ?, ?)
    ''', motivation_surveys)

# მონაცემთა გენერაცია
generate_data()

# მონაცემთა ბაზის შენახვა
conn.commit()

# კავშირის დახურვა
conn.close()
