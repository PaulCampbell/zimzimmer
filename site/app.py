from flask import Flask, send_from_directory, render_template, request
import numpy as np
from scipy.io.wavfile import write
import os

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/scripts/<path:path>')
def send_js(path):
    return send_from_directory('scripts', path)


@app.route('/get_voice')
def get_voices():
    return render_template('get_voice.html')


@app.route('/voices', methods=['POST'])
def save_voices():
    content = request.get_json()
    name = content["name"]
    sample_rate = int(content["sampleRate"])
    for entry in content["sentences"]:
        file_name = '{}-{}.wav'.format(entry["fileName"], name)
        data_array = np.array(entry["data"], dtype=np.dtype)
        write(os.path.join(os.getcwd(), 'voices', file_name), sample_rate, data_array.astype(float))
    return ('', 201)


@app.route('/')
def whos_that():
    return render_template('whos_that.html')


if __name__ == '__main__':
    app.run()
