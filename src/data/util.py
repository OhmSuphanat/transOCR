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

def get_partition(n: int):
    result = 1/n
    return [result] * n 

def slice_image(image, n: int):
    vertical_percentages = get_partition(n)
    # Load the image
    width, height = image.size

    # Calculate vertical slice points
    vertical_points = [0] + [int(height * sum(vertical_percentages[:i+1])) for i in range(len(vertical_percentages))]
    
    # Slice the image and store each window
    slices_dict = {}
    for i in range(len(vertical_points) - 1):
        upper = vertical_points[i]
        lower = vertical_points[i + 1]
        slice_img = image.crop((0, upper, width, lower))
        slices_dict[i] = slice_img
    return slices_dict