from src.data.postprocess import *

def get_course(text: str, idx: int):
  words = pd.Series(text.split('\n'))
  courses = words.apply(filter_course).dropna()
  course_ids = courses.apply(get_courseID).dropna()
  course_names = courses.apply(get_course_name)
  course_numeric = courses.apply(get_numeric)
  course_weight = course_numeric.apply(get_grade_and_unit)
  course_unit = course_weight.apply(get_unit)
  course_grade = course_weight.apply(get_grade)

  course_dict = {"ocr": courses.to_list(),
                 "numeric": course_numeric.to_list(),
                 "section": [f"{idx}{i:02d}" for i in range(courses.shape[0])],
                 "id": course_ids.to_list(),
                 "name": course_names.to_list(),
                 "unit": course_unit.to_list(),
                 "grade": course_grade.to_list(),
                 "weight": course_weight.to_list()
                 }
  return course_dict

def make_course(text_dict: dict):
    courses_df = pd.DataFrame()
    for idx, text in text_dict.items():
        courses = get_course(text, idx)
        print(f"#section{idx}")
        if not get_info(courses):
            raise ValueError("Amount Record's not balance.")
        courses_df = pd.concat([courses_df, pd.DataFrame(courses)])
    return courses_df.reset_index(drop=True).sort_values(['section'], ascending=True)

def get_info(course_dict: dict):
    unique_size = 0
    each_size = 0
    for k, v in course_dict.items():
        each_size = len(v)
        unique_size += each_size
        print(f"{k}: shape(s) = {each_size}")
    unique_size /= len(course_dict)
    return True if unique_size == each_size else False