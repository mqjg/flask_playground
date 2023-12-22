from flask import Flask, render_template, request
from flower_classification.predict import ImageClassifier
import os

uploads_path = 'uploads'
 
# Generate a flask object
app = Flask(__name__)
 
# Add a page to the website and bind a function to it
@app.route('/')
def hello_world():
    return render_template('home.html')
 
# Add a page to the website and bind a function to it
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/print/<string>') 
def print_string(string): 
    return f'{string}'

@app.route('/print_type/<float:value>') 
def print_float(value): 
    return f'{value}'

def another_way():
    return "This is another way to do routing"

# This method is identical to the uncommented on. When enpoint is not specified 
# it defualts to whatever the name of the view_func
# app.add_url_rule('/another_way', endpoint='another_way', view_func=another_way)
app.add_url_rule('/another_way', view_func=another_way)


@app.route('/square', methods=['GET'])
def squarenumber():
    # If method is GET, check if  number is entered 
    # or user has just requested the page.
    # Calculate the square of number and pass it to 
    # answermaths method
    if request.method == 'GET':
   # If 'num' is None, the user has requested page the first time
        if(request.args.get('num') == None):
            return render_template('squarenum.html')
          # If user clicks on Submit button without 
          # entering number display error
        elif(request.args.get('num') == ''):
            return "<html><body> <h1>Invalid number</h1></body></html>"
        else:
          # User has entered a number
          # Fetch the number from args attribute of 
          # request accessing its 'id' from HTML
            number = request.args.get('num')
            sq = int(number) * int(number)
            # pass the result to the answer HTML
            # page using Jinja2 template
            return render_template('answer.html', 
                                   squareofnum=sq, num=number)

@app.route('/square2', methods=['GET', 'POST'])
def squarenumber2():
 # If method is POST, get the number entered by user
 # Calculate the square of number and pass it to answermaths 
    if request.method == 'POST':
        if(request.form['num'] == ''):
            return "<html><body> <h1>Invalid number</h1></body></html>"
        else:
            number = request.form['num']
            sq = int(number) * int(number)
            return render_template('answer.html', 
                            squareofnum=sq, num=number)
    # If the method is GET,render the HTML page to the user
    if request.method == 'GET':
        return render_template("squarenum2.html")

model_path = 'flower_classification/model_0.hdf5'
labels_path = 'flower_classification/model_0_labels.pickle'
model = ImageClassifier(model_path, labels_path)

@app.route('/flower_classification', methods=['GET', 'POST'])
def flower_classification():
 # If method is POST, get the number entered by user
 # Calculate the square of number and pass it to answermaths 
    if request.method == 'POST':
        f = request.files['file'] 
        if not os.path.exists(uploads_path):
            os.makedirs(uploads_path)

        img_path = os.path.join(uploads_path, f.filename)
        f.save(img_path)
        label, score = model.predict(img_path)
        print(f"\nModel predicted \"{label}\" with a confidence of \
               {score: .3f}\n")

        return render_template("image_classification_results.html",
                               name=f.filename, label=label, score=score)  
    # If the method is GET,render the HTML page to the user
    if request.method == 'GET':
        return render_template("upload_file.html")


# main driver function
if __name__ == '__main__':
 
    #start the website
    app.run(debug=True)
