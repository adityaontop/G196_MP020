
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
