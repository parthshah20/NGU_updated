from flask import Flask, render_template, request
import os
import code_runner
from code_runner import name_dict

def return_filecontent(file_name2, calculate=True):
    file1_content = []
    file2_content = []
    count = 1
    with open(name_dict.return_name(name_dict.show), 'r') as file1:
        temp = file1.readlines()
        for line in temp:
            file1_content.append(str(count) + '. ' + line)
            count += 1
    try:
        print('-----------------Here-------------------')
        if calculate:
            code_runner.run(name_dict.return_name(2), None, 'temp_file.txt')
            code_runner.run(name_dict.return_name(0), 'temp_file.txt', file_name2)
        count = 1
        with open(file_name2, 'r') as file2:
            temp = file2.readlines()
            for line in temp:
                file2_content.append(str(count) + '. ' + line)
                count += 1
    except:
        file2_content = ["Error: please check input files"]
    return file1_content, file2_content


app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    file1_content, file2_content = return_filecontent('_Answers.txt')
    return render_template('index.html', file1=file1_content, file2=file2_content)

@app.route('/update_file', methods=['POST'])
def update_file():
    file1_name = request.form['file1_name']
    temp = file1_name.split('-')[0]
    if temp[0] == 'C' or temp[0] == 'c':
        idx = 2
    else:
        idx = 0
    name = file1_name.split('-')[1]
    name_dict.change_name(int(idx), name)
    name_dict.show = int(idx)
    file1_content, file2_content = return_filecontent('_Answers.txt')
    # Assuming file1 is updated here
    return render_template('index.html', file1=file1_content, file2=file2_content)

@app.route('/append_file1', methods=['POST'])
def append_file1():
    append_text = request.form['append_text']
    with open(name_dict.return_name(name_dict.show), 'a') as file1:
        file1.write('\n' + append_text)
    file1_content, file2_content = return_filecontent('_Answers.txt')
    # Assuming file1 is updated here
    return render_template('index.html', file1=file1_content, file2=file2_content)

@app.route('/delete_line', methods=['POST'])
def delete_line():
    line_number = int(request.form['line_number'])
    with open(name_dict.return_name(name_dict.show), 'r') as file1:
        lines = file1.readlines()
    with open(name_dict.return_name(name_dict.show), 'w') as file1:
        for i, line in enumerate(lines):
            if i != line_number - 1:
                file1.write(line)
    file1_content, file2_content = return_filecontent('_Answers.txt')
    # Assuming file1 is updated here
    return render_template('index.html', file1=file1_content, file2=file2_content)

@app.route('/append_file3', methods=['POST'])
def append_file3():
    file3_name = request.form['file3_name']
    # name_dict.change_name(2, file3_name)
    append_text = request.form['append_text_file3']
    with open(file3_name, 'a') as file3:
        file3.write('\n' + append_text)
    file1_content, file2_content = return_filecontent('_Answers.txt')
    # Assuming file1 is updated here
    return render_template('index.html', file1=file1_content, file2=file2_content)

@app.route('/save', methods=['POST'])
def save_to_file():
    data = request.json
    values = data.get('values', [])
    
    with open(name_dict.return_name(0), 'w') as f:
        for value in values:
            f.write(value + '\n')

    file1_content, file2_content = return_filecontent('_Answers.txt')
    # Assuming file1 is updated here
    return render_template('index.html', file1=file1_content, file2=file2_content)


@app.route('/save_coeff', methods=['POST'])
def save_to_file2():
    data = request.json
    values = data.get('values', [])
    
    with open(name_dict.return_name(2), 'w') as f:
        for value in values:
            f.write(value + '\n')

    file1_content, file2_content = return_filecontent('_Answers.txt')
    # Assuming file1 is updated here
    return render_template('index.html', file1=file1_content, file2=file2_content)

if __name__ == '__main__':
    app.run(debug=True)
