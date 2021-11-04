import pandas as pd
import numpy as np
import json
import sys

path_tests = './Example1/tests.csv'
path_marks = './Example1/marks.csv'
path_students = './Example1/students.csv'
path_courses = './Example1/courses.csv'
path_output = './Example1/output2.json'


# path_tests = sys.argv[3]
# path_marks = sys.argv[4]
# path_students = sys.argv[2]
# path_courses = sys.argv[1]
# path_output = sys.argv[5]

f_tests = pd.read_csv(path_tests)
f_marks = pd.read_csv(path_marks)
f_students = pd.read_csv(path_students)
f_courses = pd.read_csv(path_courses)

f_tests['weight_sum'] = f_tests['weight'].groupby(f_tests['course_id']).transform('sum')

if f_tests['weight_sum'].mean() != 100:
    error = {"error": "Invalid course weights"}
    with open(path_output, 'w', encoding='utf-8') as f:
        json.dump(error, f, ensure_ascii=False, indent=4)

else:
    f1 = f_tests.rename(columns={'id':'test_id'}).merge(f_marks)
    f2 = f1.merge(f_students.rename(columns={'id':'student_id','name':'student_name'}))
    f3 = f2.merge(f_courses.rename(columns={'id':'course_id', 'name':'course_name'}))
    f3['weighted_mark'] = f3['mark']*f3['weight']/100
    f3['courseAverage'] = f3.groupby(['student_id','course_id'])['weighted_mark'].transform('sum').round(2)
    f3['totalAverage'] = f3.groupby(['student_id'])['courseAverage'].transform(np.mean).round(2)
    f3 = f3[['student_id','student_name','totalAverage', 'course_id','course_name','teacher','courseAverage']].drop_duplicates()
    f4 = f3.groupby(['student_id','student_name','totalAverage']).apply(lambda x: x[['course_id','course_name','teacher','courseAverage']].to_dict('records')).reset_index().rename(columns={0:'courses'})
    f4 = f4.rename(columns={'student_id':'id','student_name':'name'})
    f5 = f4[['id','name','totalAverage','courses']].to_dict('records')
    result = {'students':f5}
    with open(path_output, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)


