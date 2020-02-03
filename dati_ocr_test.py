from datetime import datetime

from flask import Flask, render_template

from ocr_aws.dati_ocr_new import GeneralOCR

app = Flask(__name__)


# @app.route('/')
# def first():
#     init = datetime.now()
#     abc = GeneralOCR()
#     content = abc.run()
#     time = datetime.now() - init
#     return render_template('index.html', content=content, time=time)
#
#
# if __name__ == '__main__':
#     app.run(debug=True, threaded=False)
if __name__ == '__main__':
    abc = GeneralOCR()
    print(abc.run())