import pickle
import numpy as np
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Load the trained model
with open('naive.pkl', 'rb') as f:
    model = pickle.load(f)

# HTML template with embedded modern CSS styling
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Employee Prediction Portal</title>
    <style>
        :root {
            --primary: #4f46e5;
            --primary-hover: #4338ca;
            --background: #f8fafc;
            --card-bg: #ffffff;
            --text: #1e293b;
            --text-light: #64748b;
            --border: #cbd5e1;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--background);
            color: var(--text);
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }

        .container {
            background: var(--card-bg);
            padding: 40px;
            border-radius: 16px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 600px;
        }

        h2 {
            margin-top: 0;
            color: var(--primary);
            text-align: center;
            font-size: 26px;
            margin-bottom: 8px;
        }

        p.subtitle {
            text-align: center;
            color: var(--text-light);
            margin-bottom: 30px;
            font-size: 14px;
        }

        .form-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }

        .form-group {
            display: flex;
            flex-direction: column;
        }

        .form-group.full-width {
            grid-column: span 2;
        }

        label {
            font-weight: 600;
            margin-bottom: 8px;
            font-size: 13px;
            color: var(--text);
        }

        input, select {
            padding: 10px 14px;
            border: 1px solid var(--border);
            border-radius: 8px;
            font-size: 14px;
            outline: none;
            transition: border-color 0.2s, box-shadow 0.2s;
            background-color: #fff;
        }

        input:focus, select:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15);
        }

        button {
            grid-column: span 2;
            background-color: var(--primary);
            color: white;
            border: none;
            padding: 12px;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.2s;
            margin-top: 10px;
        }

        button:hover {
            background-color: var(--primary-hover);
        }

        .result-card {
            margin-top: 25px;
            padding: 16px;
            background-color: #e0e7ff;
            border: 1px solid #c7d2fe;
            border-radius: 8px;
            text-align: center;
            font-size: 18px;
            font-weight: bold;
            color: #3730a3;
        }

        @media (max-width: 600px) {
            .form-grid {
                grid-template-columns: 1fr;
            }
            .form-group.full-width {
                grid-column: span 1;
            }
            button {
                grid-column: span 1;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Employee Status Predictor</h2>
        <p class="subtitle">Provide the employee parameters below to run the classification model.</p>
        
        <form method="POST">
            <div class="form-grid">
                <div class="form-group">
                    <label for="Education">Education</label>
                    <select name="Education" id="Education" required>
                        <option value="Bachelors">Bachelors</option>
                        <option value="Masters">Masters</option>
                        <option value="PHD">PHD</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="JoiningYear">Joining Year</label>
                    <input type="number" name="JoiningYear" id="JoiningYear" value="2020" required>
                </div>

                <div class="form-group">
                    <label for="City">City</label>
                    <select name="City" id="City" required>
                        <option value="Bangalore">Bangalore</option>
                        <option value="Pune">Pune</option>
                        <option value="New Delhi">New Delhi</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="PaymentTier">Payment Tier</label>
                    <select name="PaymentTier" id="PaymentTier" required>
                        <option value="1">1</option>
                        <option value="2" selected>2</option>
                        <option value="3">3</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="Age">Age</label>
                    <input type="number" name="Age" id="Age" value="28" required>
                </div>

                <div class="form-group">
                    <label for="Gender">Gender</label>
                    <select name="Gender" id="Gender" required>
                        <option value="Male">Male</option>
                        <option value="Female">Female</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="EverBenched">Ever Benched</label>
                    <select name="EverBenched" id="EverBenched" required>
                        <option value="No">No</option>
                        <option value="Yes">Yes</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="ExperienceInCurrentDomain">Experience in Current Domain</label>
                    <input type="number" name="ExperienceInCurrentDomain" id="ExperienceInCurrentDomain" value="2" required>
                </div>

                <button type="submit">Predict Status</button>
            </div>
        </form>

        {% if prediction is not none %}
        <div class="result-card">
            Prediction Result: {{ prediction }}
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction = None
    if request.method == 'POST':
        try:
            # Extract values from form matching the 8 expected features
            education = request.form['Education']
            joining_year = float(request.form['JoiningYear'])
            city = request.form['City']
            payment_tier = float(request.form['PaymentTier'])
            age = float(request.form['Age'])
            gender = request.form['Gender']
            ever_benched = request.form['EverBenched']
            experience = float(request.form['ExperienceInCurrentDomain'])

            # Package into array shape required by model
            # Note: If your pipeline handles string encoding automatically, pass raw values. 
            # If your model requires encoded numeric values, map them accordingly.
            features = np.array([[education, joining_year, city, payment_tier, age, gender, ever_benched, experience]], dtype=object)
            
            pred = model.predict(features)[0]
            prediction = str(pred)
        except Exception as e:
            prediction = f"Error processing input: {str(e)}"

    return render_template_string(HTML_TEMPLATE, prediction=prediction)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
