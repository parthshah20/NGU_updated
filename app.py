from flask import Flask, render_template, request
import code_runner

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    first_file = request.form['first_file']
    equations_1 = request.form['equations_1']
    second_file = request.form['second_file']
    equations_2 = request.form['equations_2']

    # Save the data to text files
    with open(f'{first_file}.txt', 'w') as file:
        file.write(f"{equations_1}")

    with open(f'{second_file}.txt', 'w') as file:
        file.write(f"{equations_2}")
        
    code_runner.run(request.form['first_file'], request.form['second_file'], 'answer.txt')

    return 'Form submitted successfully!'

if __name__ == '__main__':
    app.run(debug=True)
