from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# SQLAlchemy Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://aikane:shojolove@192.168.0.102/flasksurveydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the database model
class Response(db.Model):
    __tablename__ = 'responses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    multiple = db.Column(db.Text, nullable=True)
    japan = db.Column(db.Text, nullable=True)
    china = db.Column(db.Text, nullable=True)
    country = db.Column(db.Text, nullable=True)
    submit_time = db.Column(db.DateTime, default=datetime.utcnow)

# Route for the survey form
@app.route("/", methods=["GET", "POST"])
def survey():
    if request.method == "POST":
        # Get data from form
        name = request.form.get("name")
        email = request.form.get("email")
        multiple = request.form.getlist("multiple")
        japan = request.form.get("japan")
        china = request.form.get("china")
        country = request.form.get("country")

        # Convert list to comma-separated string for storing in a single column
        multiple_str = ",".join(multiple)

        # Create a new response instance and add it to the session
        new_response = Response(
            name=name,
            email=email,
            multiple=multiple_str,
            japan=japan,
            china=china,
            country=country,
            submit_time=datetime.now()
        )

        # Add and commit the response to the database
        db.session.add(new_response)
        db.session.commit()

        # Return a response
        submit_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"Thank you for your response! Submitted on {submit_time}."

    return render_template("survey.html")

if __name__ == "__main__":
    # Create the tables if they don't exist
    with app.app_context():
        db.create_all()
    app.run(debug=True)
