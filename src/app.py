#################################################
# Imports
#################################################
from flask import Flask, jsonify

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# Interface with model.py to get sql session

#################################################
# Flask Routes
#################################################

# Home route
@app.route("/")
def welcome():
    return (
        f"Welcome to the API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/blah"
    )

#################################################
# Flask main method
#################################################
if __name__ == "__main__":
    app.run(debug=True)
