from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

listofInterestVlrTeams = []
listofInterestLolTeams = []


@app.route("/update-teams", methods=["POST"])
def updateTeams():
    global listofInterestVlrTeams, listofInterestLolTeams

    data = request.json

    listofInterestLolTeams = data.get("lolTeams", [])
    listofInterestVlrTeams = data.get("vlrTeams", [])

    return jsonify({"message": "Teams updated successfuly"}), 200


@app.route("/get-teams", methods=["GET"])
def getTeams():
    return (
        jsonify(
            {
                "vlrTeams": listofInterestVlrTeams,
                "lolTeams": listofInterestLolTeams,
            }
        ),
        200,
    )


if __name__ == "__main__":
    app.run(debug=True)
