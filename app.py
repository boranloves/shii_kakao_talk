from flask import Flask, request, jsonify
from shii_study import shii

shii.no_study_return_text("시이는 아무것도 몰라여..")
shii.study_return_text("ㅇㅎ")
                          

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, World"


@app.route("/say", methods=['POST'])
def say():
    req = request.get_json()

    keywords = req["action"]["detailParams"]["keyword"]["value"]
    print(keywords)
    a = shii.study_say(keywords)
    b = a

    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": b
                    }
                }
            ]
        }
    }

    return jsonify(res)


@app.route("/study", methods=['POST'])
def study():
    req = request.get_json()

    keyword = req["action"]["detailParams"]["keyword"]["value"]
    des = req["action"]["detailParams"]["des"]["value"]
    user = req["action"]["detailParams"]["user"]["value"]

    data = shii.study(keyword, des, user)

    text = data

    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": text
                    }
                }
            ]
        }
    }

    return jsonify(res)

@app.route("/info", methods=['POST'])
def info():
    text = "made by boran"

    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": text
                    }
                }
            ]
        }
    }

    return jsonify(res)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True)
