from flask import Flask

app = Flask(__name__)


@app.route('/', methods=['GET'])
def token_required(request):
    return "Test", request


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
