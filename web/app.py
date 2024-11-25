from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
from OCR_Timetable import TimetableExtractor
import numpy as np

@app.route('/')
def home():
   return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
      # 이미지 처리 함수 호출
      file_data = np.frombuffer(file.read(), np.uint8)

      ext = TimetableExtractor(file_data)
      ext.getlectrue()
      ext.get_time_dictionary()
      ext.save_lecture_data()

      result = ext.result

      return jsonify({'score': result})

if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)