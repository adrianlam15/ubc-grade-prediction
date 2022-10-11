import pandas as pd

path_to_file = "src/CourseSection_Grades_data.csv"
df = pd.read_csv(path_to_file)

print(df.shape)  # (rows, columns) -> (152460, 6)
