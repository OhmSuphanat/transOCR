import re
import pandas as pd

def filter_course(text: str):
  text = text.strip()
  pattern = r'[\u0E00-\u0E7F|0-9]{0,1}[0-9|๑-๙]{5}'
  if re.search(pattern, text):
    return text.replace("|", " ")
  return 

def get_courseID(text: str):
  pattern = r'[\u0E00-\u0E7F|0-9]{1}[0-9]{5}'
  result = re.findall(pattern=pattern, string=text)
  if result:
    id = result[0]
    if id[0] in ['1']:
      id =  "I" + id[1:]
    if id[0] in ['า', '7']:
      id =  "ว" + id[1:]
    if id[0] in ['ล']:
      id =  "ส" + id[1:]
    return id
  return "999"

def get_course_name(text: str):
  print(text)
  pattern = r'[\u0E00-\u0E7F|A-z|\/]{3,}[\s]{0,1}[0-9]{0,1}'
  result = re.findall(pattern=pattern, string=text)
  return result[0].strip()

def name_case(text: str):
  pattern = r'[\u0E00-\u0E7F]{30,}'
  result = re.findall(pattern=pattern, string=text)
  if result:
    text = re.sub(r'[\u0E00-\u0E7F]', ' ', text)
  return text

def get_numeric(text: str):
  text = name_case(text=text)
  pattern = r'[\s]{2,}.+'
  result = re.findall(pattern=pattern, string=text)
  result = result[0]
  allowed_chars = "12345. "
  pattern = f"[^{re.escape(allowed_chars)}]"
  result = re.sub(pattern=pattern, repl='', string=result)
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
  if len(blocks) == 2:
    for idx, block in enumerate(blocks):
      digit = float(get_unique_characters(block))
      if digit > 4:
        digit /= 10
      blocks[idx] = digit
    unit = blocks[0]
    grade = blocks[1]
  return [unit, grade]
  


