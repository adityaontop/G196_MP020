from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

TARGET = "litres_per_day"
LEAKING_COLUMN = "litres_from_tank_dip_next_day"
NUMERIC_FEATURES = [
    "highway_distance_km", "nearby_pumps", "price_rs", "trucks_passing", "temp_c", "staff"
]
CATEGORICAL_FEATURES = ["ownership", "zone"]
MODEL_FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES + ["month", "day_of_week", "day_of_year"]


def sha256_file(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


# Map spelling/abbreviation variants onto the three canonical training categories.
def canonical_ownership(value: Any) -> str:
    text = str(value).strip().lower().replace(".", "").replace("_", " ")
    mapping = {
        "cooperative": "cooperative", "coo": "cooperative",
        "private": "private", "pri": "private",
        "public sector": "public_sector", "publicsector": "public_sector", "pub": "public_sector",
    }
    return mapping.get(text, text)


def clean_frame(frame: pd.DataFrame, *, has_target: bool = True) -> pd.DataFrame:
    """Clean the provided frame without changing the source CSV."""
    df = frame.copy()
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    # Repair the known zone-specific unit mix-up before treating extreme prices as missing.
    # Industrial rows were recorded in paise-like 100x units; normalize only clear anomalies.
    industrial = df["zone"].astype(str).str.strip().str.lower().eq("industrial")
    df.loc[industrial & (df["price_rs"] > 500), "price_rs"] /= 100.0
    df.loc[df["price_rs"] >= 500, "price_rs"] = np.nan
    # The sentinel is not a valid observation; median imputation keeps the row usable.
    # The known sentinel is missing information, not a real price.
    df["price_rs"] = df["price_rs"].fillna(df["price_rs"].median())
    df["ownership"] = df["ownership"].map(canonical_ownership)
    df["zone"] = df["zone"].astype(str).str.strip().str.title()
    if has_target and TARGET in df:
        # Correct only the identified extra-zero scale errors in the target column.
        typo = df[TARGET] > 100000
        df.loc[typo, TARGET] = df.loc[typo, TARGET] / 10.0
    # Drop target and post-event tank-dip measurement to prevent label leakage.
    # Never expose post-event information to the model.
    feature = df.drop(columns=[LEAKING_COLUMN, TARGET], errors="ignore")
    if "date" in feature.columns:
        feature["month"] = feature["date"].dt.month
        feature["day_of_week"] = feature["date"].dt.dayofweek
        feature["day_of_year"] = feature["date"].dt.dayofyear
    else:
        # The serving contract has no date; these neutral values keep feature columns aligned.
        # The live API contract has no date field; use neutral defaults for date features.
        feature["month"] = 1
        feature["day_of_week"] = 0
        feature["day_of_year"] = 1
    return feature


def load_clean(path: str | Path, *, has_target: bool = True) -> pd.DataFrame:
    return clean_frame(pd.read_csv(path), has_target=has_target)


def detect_issues(train: pd.DataFrame, holdout: pd.DataFrame, later: pd.DataFrame) -> dict[str, Any]:
    """Return the seven findings in the exact shape needed by findings.yaml."""
    df = train.copy()
    df["date"] = pd.to_datetime(df["date"])
    ownership_levels = {canonical_ownership(x) for x in df["ownership"].unique()}
    raw_text_levels = set(df["ownership"].astype(str))
    variants_present = len(raw_text_levels) > len(ownership_levels)
    # Unit mix-up: Industrial price values are approximately 100x the clean groups.
    industrial = df.loc[df.zone.eq("Industrial"), "price_rs"]
    normal = df.loc[~df.zone.eq("Industrial"), "price_rs"]
    unit_present = bool(len(industrial) and industrial.median() > normal.median() * 50)
    # A run of five or more identical consecutive readings is flagged for investigation.
    # A stuck-sensor detector: exact repeated values in a contiguous run after date sorting.
    stuck = {"present": False, "column": None, "start_date": None, "end_date": None}
    ordered = df.sort_values("date").reset_index(drop=True)
    for col in NUMERIC_FEATURES:
        start = 0
        for i in range(1, len(ordered) + 1):
            if i == len(ordered) or ordered.loc[i, col] != ordered.loc[start, col]:
                if i - start >= 5:
                    stuck = {"present": True, "column": col, "start_date": ordered.loc[start, "date"].strftime("%Y-%m-%d"), "end_date": ordered.loc[i - 1, "date"].strftime("%Y-%m-%d")}
                    break
                start = i
        if stuck["present"]:
            break
    sentinel_mask = df["price_rs"].eq(9999)
    typo_mask = df[TARGET] / df[LEAKING_COLUMN].replace(0, np.nan) > 5
    return {
        "leaking_column": {"present": LEAKING_COLUMN in train.columns and LEAKING_COLUMN not in holdout.columns, "column": LEAKING_COLUMN if LEAKING_COLUMN in train.columns and LEAKING_COLUMN not in holdout.columns else None},
        "unit_mixup": {"present": unit_present, "column": "price_rs" if unit_present else None, "group_value": "Industrial" if unit_present else None, "factor": 100 if unit_present else None},
        "sentinel_value": {"present": bool(sentinel_mask.any()), "column": "price_rs" if sentinel_mask.any() else None, "value": 9999 if sentinel_mask.any() else None, "count": int(sentinel_mask.sum()) if sentinel_mask.any() else None},
        "duplicate_rows": {"present": bool(train.duplicated().sum()), "count": int(train.duplicated().sum()) if train.duplicated().sum() else None},
        "stuck_sensor": stuck,
        "target_typos": {"present": bool(typo_mask.sum()), "count": int(typo_mask.sum()) if typo_mask.sum() else None},
        "spelling_variants": {"present": variants_present, "column": "ownership" if variants_present else None, "true_levels": len(ownership_levels) if variants_present else None},
    }






# # Student Marks Analysis System
# # Using Python, NumPy, Pandas and Matplotlib

# # Importing required libraries
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt

# # Creating a dataset of students
# data = {
#     'Name': ['Aman', 'Rahul', 'Naman', 'Priya', 'Simran',
#              'Karan', 'Rohit', 'Anjali', 'Vikas', 'Neha'],
#     'Maths': [85, 78, 92, 88, 76, 67, 81, 95, 72, 89],
#     'Science': [90, 82, 88, 91, 79, 70, 85, 94, 75, 87],
#     'English': [78, 85, 90, 82, 88, 74, 80, 92, 77, 86]
# }

# # Converting dictionary into DataFrame
# df = pd.DataFrame(data)

# # Displaying original dataset
# print("STUDENT MARKS DATA")
# print(df)

# # Calculating total marks
# df['Total'] = df[['Maths', 'Science', 'English']].sum(axis=1)

# # Calculating average marks
# df['Average'] = df[['Maths', 'Science', 'English']].mean(axis=1)

# # Calculating percentage
# df['Percentage'] = (df['Total'] / 300) * 100

# # Function to calculate grades
# def calculate_grade(percentage):

#     # Checking percentage and assigning grade
#     if percentage >= 90:
#         return 'A+'
#     elif percentage >= 80:
#         return 'A'
#     elif percentage >= 70:
#         return 'B'
#     elif percentage >= 60:
#         return 'C'
#     elif percentage >= 50:
#         return 'D'
#     else:
#         return 'F'

# # Applying grade function to every student
# df['Grade'] = df['Percentage'].apply(calculate_grade)

# # Displaying complete student result
# print("\nCOMPLETE STUDENT RESULT")
# print(df)

# # Finding highest marks in each subject
# print("\nHIGHEST MARKS")
# print(df[['Maths', 'Science', 'English']].max())

# # Finding lowest marks in each subject
# print("\nLOWEST MARKS")
# print(df[['Maths', 'Science', 'English']].min())

# # Calculating average marks of the class
# print("\nCLASS AVERAGE")
# print(df[['Maths', 'Science', 'English']].mean())

# # Finding student with highest total marks
# topper = df.loc[df['Total'].idxmax()]

# print("\nCLASS TOPPER")
# print(topper['Name'])
# print("Total Marks:", topper['Total'])

# # Finding student with lowest total marks
# lowest = df.loc[df['Total'].idxmin()]

# print("\nLOWEST SCORING STUDENT")
# print(lowest['Name'])
# print("Total Marks:", lowest['Total'])

# # Sorting students according to percentage
# df_sorted = df.sort_values(
#     by='Percentage',
#     ascending=False
# )

# print("\nSTUDENTS RANKING")
# print(df_sorted[['Name', 'Percentage', 'Grade']])

# # Counting number of students in each grade
# grade_count = df['Grade'].value_counts()

# print("\nGRADE DISTRIBUTION")
# print(grade_count)

# # Creating a bar chart for student marks
# plt.figure(figsize=(10, 5))

# # Setting bar positions
# x = np.arange(len(df['Name']))

# # Plotting marks of different subjects
# plt.bar(x - 0.25, df['Maths'], width=0.25, label='Maths')
# plt.bar(x, df['Science'], width=0.25, label='Science')
# plt.bar(x + 0.25, df['English'], width=0.25, label='English')

# # Adding labels and title
# plt.xlabel("Students")
# plt.ylabel("Marks")
# plt.title("Subject-wise Student Performance")

# # Adding student names on X-axis
# plt.xticks(x, df['Name'])

# # Displaying legend
# plt.legend()

# # Displaying grid
# plt.grid(axis='y', linestyle='--', alpha=0.5)

# # Showing bar chart
# plt.show()

# # Creating a pie chart for grade distribution
# plt.figure(figsize=(7, 7))

# # Plotting grade distribution
# plt.pie(
#     grade_count,
#     labels=grade_count.index,
#     autopct='%1.1f%%',
#     startangle=90
# )

# # Adding chart title
# plt.title("Student Grade Distribution")

# # Displaying pie chart
# plt.show()

# # Creating a histogram of student percentages
# plt.figure(figsize=(8, 5))

# # Plotting histogram
# plt.hist(
#     df['Percentage'],
#     bins=5,
#     edgecolor='black'
# )

# # Adding labels
# plt.xlabel("Percentage")
# plt.ylabel("Number of Students")
# plt.title("Distribution of Student Percentages")

# # Displaying histogram
# plt.show()

# # Saving final result into CSV file
# df.to_csv("student_results.csv", index=False)

# # Displaying successful completion message
# print("\nStudent analysis completed successfully!")

# # Displaying final summary
# print("\nFINAL SUMMARY")
# print("Total Students:", len(df))
# print("Class Average:", round(df['Percentage'].mean(), 2))
# print("Highest Percentage:", df['Percentage'].max())
# print("Lowest Percentage:", df['Percentage'].min())
# print("Number of Students Passed:", len(df[df['Percentage'] >= 40]))

# # End of Program
# # Student Marks Analysis System
# # Using Python, NumPy, Pandas and Matplotlib

# # Importing required libraries
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt

# # Creating a dataset of students
# data = {
#     'Name': ['Aman', 'Rahul', 'Naman', 'Priya', 'Simran',
#              'Karan', 'Rohit', 'Anjali', 'Vikas', 'Neha'],
#     'Maths': [85, 78, 92, 88, 76, 67, 81, 95, 72, 89],
#     'Science': [90, 82, 88, 91, 79, 70, 85, 94, 75, 87],
#     'English': [78, 85, 90, 82, 88, 74, 80, 92, 77, 86]
# }

# # Converting dictionary into DataFrame
# df = pd.DataFrame(data)

# # Displaying original dataset
# print("STUDENT MARKS DATA")
# print(df)

# # Calculating total marks
# df['Total'] = df[['Maths', 'Science', 'English']].sum(axis=1)

# # Calculating average marks
# df['Average'] = df[['Maths', 'Science', 'English']].mean(axis=1)

# # Calculating percentage
# df['Percentage'] = (df['Total'] / 300) * 100

# # Function to calculate grades
# def calculate_grade(percentage):

#     # Checking percentage and assigning grade
#     if percentage >= 90:
#         return 'A+'
#     elif percentage >= 80:
#         return 'A'
#     elif percentage >= 70:
#         return 'B'
#     elif percentage >= 60:
#         return 'C'
#     elif percentage >= 50:
#         return 'D'
#     else:
#         return 'F'

# # Applying grade function to every student
# df['Grade'] = df['Percentage'].apply(calculate_grade)

# # Displaying complete student result
# print("\nCOMPLETE STUDENT RESULT")
# print(df)

# # Finding highest marks in each subject
# print("\nHIGHEST MARKS")
# print(df[['Maths', 'Science', 'English']].max())

# # Finding lowest marks in each subject
# print("\nLOWEST MARKS")
# print(df[['Maths', 'Science', 'English']].min())

# # Calculating average marks of the class
# print("\nCLASS AVERAGE")
# print(df[['Maths', 'Science', 'English']].mean())

# # Finding student with highest total marks
# topper = df.loc[df['Total'].idxmax()]

# print("\nCLASS TOPPER")
# print(topper['Name'])
# print("Total Marks:", topper['Total'])

# # Finding student with lowest total marks
# lowest = df.loc[df['Total'].idxmin()]

# print("\nLOWEST SCORING STUDENT")
# print(lowest['Name'])
# print("Total Marks:", lowest['Total'])

# # Sorting students according to percentage
# df_sorted = df.sort_values(
#     by='Percentage',
#     ascending=False
# )

# print("\nSTUDENTS RANKING")
# print(df_sorted[['Name', 'Percentage', 'Grade']])

# # Counting number of students in each grade
# grade_count = df['Grade'].value_counts()

# print("\nGRADE DISTRIBUTION")
# print(grade_count)

# # Creating a bar chart for student marks
# plt.figure(figsize=(10, 5))

# # Setting bar positions
# x = np.arange(len(df['Name']))

# # Plotting marks of different subjects
# plt.bar(x - 0.25, df['Maths'], width=0.25, label='Maths')
# plt.bar(x, df['Science'], width=0.25, label='Science')
# plt.bar(x + 0.25, df['English'], width=0.25, label='English')

# # Adding labels and title
# plt.xlabel("Students")
# plt.ylabel("Marks")
# plt.title("Subject-wise Student Performance")

# # Adding student names on X-axis
# plt.xticks(x, df['Name'])

# # Displaying legend
# plt.legend()

# # Displaying grid
# plt.grid(axis='y', linestyle='--', alpha=0.5)

# # Showing bar chart
# plt.show()

# # Creating a pie chart for grade distribution
# plt.figure(figsize=(7, 7))

# # Plotting grade distribution
# plt.pie(
#     grade_count,
#     labels=grade_count.index,
#     autopct='%1.1f%%',
#     startangle=90
# )

# # Adding chart title
# plt.title("Student Grade Distribution")

# # Displaying pie chart
# plt.show()

# # Creating a histogram of student percentages
# plt.figure(figsize=(8, 5))

# # Plotting histogram
# plt.hist(
#     df['Percentage'],
#     bins=5,
#     edgecolor='black'
# )

# # Adding labels
# plt.xlabel("Percentage")
# plt.ylabel("Number of Students")
# plt.title("Distribution of Student Percentages")

# # Displaying histogram
# plt.show()

# # Saving final result into CSV file
# df.to_csv("student_results.csv", index=False)

# # Displaying successful completion message
# print("\nStudent analysis completed successfully!")

# # Displaying final summary
# print("\nFINAL SUMMARY")
# print("Total Students:", len(df))
# print("Class Average:", round(df['Percentage'].mean(), 2))
# print("Highest Percentage:", df['Percentage'].max())
# print("Lowest Percentage:", df['Percentage'].min())
# print("Number of Students Passed:", len(df[df['Percentage'] >= 40]))

# # End of Program

