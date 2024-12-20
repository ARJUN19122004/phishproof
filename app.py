from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import re
from urllib.parse import urlparse
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier


app = Flask(__name__)

# Load dataset and train model
data = pd.read_csv(r"C:\Users\SEC\OneDrive\Documents\phishing_site_urls.csv")
df = pd.DataFrame(data)

# Function to extract features from URL
def extract_features(URL):
    features = []
    parsed_url = urlparse(URL)
    features.append(len(URL))  # Length of URL
    features.append(URL.count('.'))  # Count of '.'
    features.append(int(bool(re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', parsed_url.netloc))))  # IP check
    features.append(URL.count('/'))  # Count of '/'
    features.append(int(parsed_url.scheme == 'https'))  # 'https' check
    return features

df['features'] = df['URL'].apply(extract_features)
X = np.array(df['features'].tolist())
y = np.array(df['Label'])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Function to predict if a URL is phishing or legitimate
def predict_url(url):
    features = np.array(extract_features(url)).reshape(1, -1)
    prediction = model.predict(features)
    return "Phishing Website" if prediction[0] == "bad" else "Legitimate Website"

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for URL prediction
@app.route('/check-url', methods=['POST'])
def check_url():
    url = request.form['url']
    result = predict_url(url)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
