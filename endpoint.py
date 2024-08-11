from flask import Flask,jsonify
from src.data import load_data
from src.models import util_model
from src.data import util
from pathlib import Path

app = Flask(__name__)

@app.route('/do-ocr', methods=['POST'])
def home():
    dataset_path = "data/raw"
    front_image = "trans020-1" 
    target_image = load_data.read_image(dataset_path, front_image)
    section_dict = util_model.detect_section(target_image)
    processed_sections = util.pre_process(section_dict)
    text_dict = util_model.images_to_texts(processed_sections)
    courses_df = util.make_course(text_dict)
    post_courses_df = util.post_process(courses_df, processed_sections)
    error_df = util.get_error(post_courses_df).reset_index(drop=True)
    export_df = post_courses_df[["id", "name", "unit", "grade"]]
    load_data.export_df_to_csv("data/out/csv", front_image, export_df)
    load_data.csv_to_json("data/out/json", "data/out/csv", front_image)
    return jsonify({"message": "OCR processing complete"})

if __name__ == '__main__':
    app.run(port=5500,debug=True)
