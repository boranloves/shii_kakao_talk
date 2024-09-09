from flask import Flask, request, jsonify
import json
from korcen import korcen

no_study_return = "시이는 아무것도 몰라여.."
study_return = "이해 했어요!"

app = Flask(__name__)


def load_bot_info():
    try:
        with open('bot_info.json', 'r', encoding='utf-8') as f:
            bot_info = json.load(f)
    except FileNotFoundError:
        bot_info = {}

    return bot_info


def save_bot_info(bot_info):
    with open('bot_info.json', 'w', encoding='utf-8') as f:
        json.dump(bot_info, f, ensure_ascii=False, indent=4)


def study(keyword: str, description: str):
    '''Teaches the bot to respond to a keyword.'''
    ''':return ex): study_return'''
    bot_info = load_bot_info()
    if 'https://' in description or 'https://' in keyword:
        return "링크를 포함시키지 말아주세요..."
    if 'http://' in description or 'http://' in keyword:
        return "링크를 포함시키지 말아주세요..."
    if 'discord.gg' in description or 'discord.gg' in keyword:
        return "디스코드 서버 초대 링크를 포함시키지 말아주세요..."
    if korcen.check(keyword) or korcen.check(description) or korcen.check(keyword + description) or korcen.check(description + keyword):
        return "그런건... 배우기 싫어여.."
    if keyword not in bot_info:
        bot_info[keyword] = {
            'description': description,
        }
        save_bot_info(bot_info)
        if study_return == None:
          return f"{keyword}를 학습하였습니다."
        else:
          return study_return
    else:
        return f"{keyword}는 이미 알고 있어요!"


def study_say(keyword: str):
    '''Returns the description of the keyword.'''
    ''':return ex): 안녕하세요'''
    bot_info = load_bot_info()
    info = bot_info.get(keyword)

    word = {
          'shii': f"pip install -U shii",
    }

    if keyword in word.keys():
        return f'{word[keyword]}'
    else:
        if info:
            description = info['description']
            return f"{description}"
        else:
          if no_study_return == None:
            return f"{keyword}는 아직 모르겠어요.."
          else:
            return no_study_return


@app.route("/")
def hello():
    return "Hello, World"


@app.route("/say", methods=['POST'])
def say():
    req = request.get_json()

    keywords = req["action"]["detailParams"]["keyword"]["value"]
    print(keywords)
    a = study_say(keywords)
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
def studys():
    req = request.get_json()

    keyword = req["action"]["detailParams"]["keyword"]["value"]
    des = req["action"]["detailParams"]["des"]["value"]

    data = study(keyword, des)

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
