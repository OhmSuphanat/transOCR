from src.data import preprocess, postprocess
from src.models import util_model
import re
import pandas as pd

def filter_course(text: str):
  text = text.strip()
  pattern = r'[\u0E00-\u0E7F|0-9]{0,1}[0-9]{5}'
  if re.search(pattern, text):
    return text.replace("|", " ")
  return 

def get_courseID(text: str):
  pattern = r'[\u0E00-\u0E7F|0-9]{1}[0-9]{5}'
  result = re.findall(pattern=pattern, string=text)
  if result:
    return postprocess.edit_courseID(result[0])
  print("Error from get_courseID")
  print(text)
  return "999"

def get_course_name(text: str):
  pattern = pattern = r'(?: [\u0E00-\u0E7F|A-z|\/]{3,})+'
  result = re.findall(pattern=pattern, string=text)
  if result:
      return result[0].strip()
  
  print("Error from get_course_name")
  print(text)
  return "999"


def get_numeric(text: str):
  text = postprocess.text_for_numeric(text, get_course_name(text))
  pattern = r'[\s]{2,}.+'
  result = re.findall(pattern=pattern, string=text)
  if result:
    result = result[0]
  else:
    print("Error from get_numeric")
    print(text)
    return "999"
  result = result.replace(".", ".5")
  allowed_chars = "123456 "
  pattern = f"[^{re.escape(allowed_chars)}]"
  result = re.sub(pattern=pattern, repl='', string=result)
  result = result.replace('6', '4')
  return result.strip()

def get_unit(num_list: list):
  return num_list[0]

def get_grade(num_list: list):
  return num_list[1]

def get_unique_characters(text):
    return ''.join(sorted(set(text)))

def get_grade_and_unit(text: str):
  blocks = text.split()
  unit = 999
  grade = 999
  if len(blocks) > 2:
    blocks = blocks[-2:]

  if len(blocks) == 2:
    for idx, block in enumerate(blocks):
      digit = float(get_unique_characters(block))
      if digit > 4:
        digit /= 10
      blocks[idx] = digit
    unit = blocks[0]
    grade = blocks[1]
  return [unit, grade]

def get_cat(text: str):
  for cat in ["ภาษาไทย", "คณิตศาสตร์", "วิทยาศาสตร์", "สังคมศึกษา",
              "สุขศึกษา", "ศิลปะ", "การงานอาชีพ", "ภาษาต่างประเทศ",
              "ศึกษาค้นคว้าด้วยตนเอง", "ผลการเรียน"]:
     if cat in text:
        return text
  return

# def get_subject(text: str):
#    for 
   

def get_GPA(text: str):
   words = pd.Series(text.split('\n'))
   subjects = words.apply(get_cat).dropna()

   return subjects


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
                 }
  return course_dict

def verify_courses(course_dict: dict):
    unique_size = 0
    each_size = 0
    for k, v in course_dict.items():
        each_size = len(v)
        unique_size += each_size
    unique_size /= len(course_dict)
    return True if unique_size == each_size else False

def make_course(text_dict: dict):
    courses_df = pd.DataFrame()
    for idx, text in text_dict.items():
        courses = get_course(text, idx)
        if not verify_courses(courses):
            raise ValueError("Amount Record's not balance.")
        courses_df = pd.concat([courses_df, pd.DataFrame(courses)])
    return courses_df.reset_index(drop=True).sort_values(['section'], ascending=True)

def get_error(df: pd.core.frame.DataFrame):
    return df.loc[(df.id == "999") | (df.name == "999") | (df.unit == 999) | (df.grade == 999)]

def get_non_error(df: pd.core.frame.DataFrame):
    return df.loc[~((df.id == "999") | (df.name == "999") | (df.unit == 999) | (df.grade == 999))]

def get_lines_pos(image):
    data = util_model.get_ocr_data(image)
    line_pos = []
    allow = True
    texts = data.text.to_list()
    pattern = r'[0-9]'
    for idx, text in enumerate(texts):
        if type(text) == float:
            allow = True
        if allow and (type(text) == str):
            if re.findall(pattern, text):
              line_pos.append(data.iloc[idx, [6, 7, 8, 9, 11]].to_dict())
              allow = False
    return line_pos

def pre_process(image_dict):
    for k, v in image_dict.items():
        image_dict[k] = preprocess.pipeline(v)
    return image_dict

def post_process(courses_df: pd.core.frame.DataFrame, image_dict: dict):
   return postprocess.pipeline(courses_df, image_dict)