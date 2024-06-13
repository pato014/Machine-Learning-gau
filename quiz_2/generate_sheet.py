import pandas as pd
import numpy as np

num_interns = 70
num_days = 30
codes = [f"{i:05d}" for i in range(num_interns)]

hr_scores = np.random.randint(0, 101, size=(num_interns, num_days)).astype(float)
mask_hr = np.random.rand(num_interns, num_days) < 0.20
hr_scores[mask_hr] = np.nan

it_scores = np.random.randint(0, 101, size=(num_interns, num_days)).astype(float)
mask_it = np.random.rand(num_interns, num_days) < 0.25
it_scores[mask_it] = np.nan

with pd.ExcelWriter('interns.xlsx') as writer:
    df_sheet1 = pd.DataFrame(hr_scores, columns=[f'Day{i + 1}' for i in range(num_days)])
    df_sheet1.insert(0, 'Intern Code', codes)
    df_sheet1.to_excel(writer, sheet_name='Sheet1', index=False)

    df_sheet2 = pd.DataFrame(it_scores, columns=[f'Day{i + 1}' for i in range(num_days)])
    df_sheet2.insert(0, 'Intern Code', codes)
    df_sheet2.to_excel(writer, sheet_name='Sheet2', index=False)
