from flask import Flask
from server import view
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


app.add_url_rule('/', methods=['GET'], view_func=view.home)
app.add_url_rule('/send_ocr_file', methods=['POST'], view_func=view.convert_file_to_text)
app.add_url_rule('/send_data_selected', methods=['POST'], view_func=view.train_machine_learning)

