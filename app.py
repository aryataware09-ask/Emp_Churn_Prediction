import pickle
import numpy as np
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Load the trained model
with open('naive.pkl', 'rb') as f:
    model = pickle.load(f)

# HTML template with gorgeous gradient, glassmorphism, and animated styling
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Employee Status Prediction Portal</title>
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #2d3748;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .wrapper {
            width: 100%;
            max-width: 680px;
            animation: fadeIn 0.8s ease-in-out;
        }

        .card {
            background: rgba(255, 255, 255, 0.92);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.4);
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
        }

        .header-title {
            text-align: center;
            font-weight: 700;
            font-size: 28px;
            color: #1a202c;
            margin-bottom: 6px;
            background: linear-gradient(to right, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .subtitle {
            text-align: center;
            color: #718096;
            font-size: 14px;
            margin-bottom: 30px;
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

        label {
            font-weight: 500;
            margin-bottom: 6px;
            font-size: 13px;
            color: #4a5568;
        }

        input, select {
            padding: 12px 16px;
            border: 2px solid #e2e8f0;
            border-radius: 10px;
            font-size: 14px;
            font-family: 'Poppins', sans-serif;
            outline: none;
            transition: all 0.3s ease;
            background-color: #f7fafc;
        }

        input:focus, select:focus {
            border-color: #667eea;
            background-color: #fff;
            box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.15);
        }

        .btn-submit {
            grid-column: span 2;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 14px;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            margin-top: 10px;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }

        .btn-submit:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }

        .result-box {
            margin-top: 25px;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            font-size: 18px;
            font-weight: 600;
            animation: popUp 0.5s ease-out;
        }

        .result-success {
            background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);
            color: #155724;
            border: 1px solid #c3e6cb;
            box-shadow: 0 4px 15px rgba(150, 230, 161, 0.4);
        }

        .result-default {
            background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%);
            color: #0c5460;
            border: 1px solid #bee5eb;
            box-shadow: 0 4px 15px rgba(161, 196, 253, 0.4);
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes popUp {
            0% { transform: scale(0.9); opacity: 0; }
            100% { transform: scale(1); opacity: 1; }
        }

        @media (max-width: 600px) {
            .form-grid {
                grid-template-columns: 1fr;
            }
            .btn-submit {
                grid-column: span 1;
            }
        }
    </style>
</head>
<body>
    <div class="wrapper">
        <div class="card">
            <h1 class="header-title">Employee Predictor</h1>
            <p class="subtitle">Enter the professional metrics to predict employee performance/status.</p>
            
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

                    <button type="submit" class="btn-submit">Run Prediction</button>
                </div>
            </form>

            {% if prediction is not none %}
            <div class="result-box {% if 'Error' in prediction %}result-default{% else %}result-success{% endif %}">
                ✨ Prediction Output: {{ prediction }}
            </div>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction = None
    if request.method == 'POST':
        try:
            # Category mappings adjusted to handle standard numeric conversions safely
            education_map = {'Bachelors': 0, 'Masters': 1, 'PHD': 2}
            city_map = {'Bangalore': 0, 'Pune': 1, 'New Delhi': 2}
            gender_map = {'Male': 0, 'Female': 1}
            benched_map = {'No': 0, 'Yes': 1}

            education = education_map.get(request.form['Education'], 0)
            joining_year = float(request.form['JoiningYear'])
            city = city_map.get(request.form['City'], 0)
            payment_tier = float(request.form['PaymentTier'])
            age = float(request.form['Age'])
            gender = gender_map.get(request.form['Gender'], 0)
            ever_benched = benched_map.get(request.form['EverBenched'], 0)
            experience = float(request.form['ExperienceInCurrentDomain'])

            features = np.array([[education, joining_year, city, payment_tier, age, gender, ever_benched, experience]])
            
            pred = model.predict(features)[0]
            prediction = str(pred)
        except Exception as e:
            prediction = f"Error processing input: {str(e)}"

    return render_template_string(HTML_TEMPLATE, prediction=prediction)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
