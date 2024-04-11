import pandas as pd
students_df = pd.read_excel('students.xlsx')

subjects_df = pd.read_excel('subjects.xlsx')

subjects_df = subjects_df.sample(frac=1).reset_index(drop=True)

assigned_subjects_df = pd.DataFrame(columns=['First Name', 'Last Name', 'Subjects'])

for index, student in students_df.iterrows():
    remaining_credits = 30
    student_subjects = []

    shuffled_subjects = subjects_df.sample(frac=1).reset_index(drop=True)

    for _, subject in shuffled_subjects.iterrows():
        if remaining_credits >= subject['კრედიტები']:
            student_subjects.append(f"{subject['სასწავლო კომპონენტი']} ({subject['კრედიტები']})")
            remaining_credits -= subject['კრედიტები']
        if remaining_credits == 0:
            break

    assigned_subjects_df = assigned_subjects_df._append({
        'First Name': student['First name'],
        'Last Name': student['Surname'],
        'Subjects': ', '.join(student_subjects)
    }, ignore_index=True)

# Write the assigned subjects to a new Excel file
assigned_subjects_df.to_excel('assigned_subjects.xlsx', index=False)
