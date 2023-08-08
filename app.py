# importing required libraries
import requests
from feature import FeatureExtraction
from flask import Flask, request, render_template
import numpy as np
import pandas as pd
from sklearn import metrics
import warnings
import pickle
import csv
warnings.filterwarnings('ignore')

# Read the CSV file
#with open('feed.csv', 'r') as file:
    #reader = csv.reader(file)
    #url_list = list(reader)

# Load the trained model
print("started loading the model")
gbc = pickle.load(open("./pickle/XGBoostClassifier.pickle.dat", 'rb'))
print("model loaded succesfully!!")

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    url = request.form["url"]
    # print("This is the url entered: ", url)
    #prediction_text = url+"\n"
    

    # Iterate through the URL list and search for the URL
    # Read the CSV file
    with open('feed.csv', 'r') as file:
        reader = csv.reader(file)
        url_list = list(reader)
    for row in url_list:
        if url in row:
            print("URL found: ", row[0])
            found = True
            prediction_text = 'The url is unsafe as its found in phishing url dataset.'
            return render_template('index.html', prediction_text=prediction_text)

    # If URL not found in the list, print message
    print("URL not found in the dataset.")
    obj = FeatureExtraction(url)
    x = np.array(obj.getFeaturesList()).reshape(1, 30)
    print("Features : ", x)
    print("Feature lenght: ", x.shape)
    y_pred = gbc.predict(x)[0]
    
    
    print("Model output: ", gbc.predict_proba(x))
    y_pro_phishing = gbc.predict_proba(x)[0, 0]
    y_pro_non_phishing = gbc.predict_proba(x)[0, 1]
    # if(y_pred ==1 ):
    # prediction_text = " {0:.2f} percent of safety".format(y_pro_non_phishing*100)+prediction_text
    if (y_pro_non_phishing*100 > 70):
        prediction_text = "It is a safe url"  # safe
    else:
        prediction_text = "It is a Phishing url!!"  # phising
        # Open the CSV file in append mode
        with open('feed.csv', 'a', newline='') as file:
            writer = csv.writer(file)

            # Write the new data to the CSV file
            writer.writerow([url])
    # print(prediction_text)
    return render_template('index.html', prediction_text=f'{prediction_text}')

if __name__ == "__main__":
    app.run(debug=True)
