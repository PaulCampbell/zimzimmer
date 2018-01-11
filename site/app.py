from flask import Flask, send_from_directory, render_template, request
import numpy as np
from scipy.io.wavfile import write
import os
import tfdeploy as td
import librosa

model = td.Model("model.pkl")
x, y = model.get("input", "output")

print model
print y
print x

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


def extract_feature(X, sample_rate):
    stft = np.abs(librosa.stft(X))
    tuning = librosa.estimate_tuning(y=X, sr=sample_rate)
    mel = np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T,axis=0)
    contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T,axis=0)
    return mel, contrast, tuning


@app.route('/scripts/<path:path>')
def send_js(path):
    return send_from_directory('scripts', path)

@app.route('/assets/<path:path>')
def send_asset(path):
    return send_from_directory('assets', path)

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


@app.route('/predict', methods=['POST'])
def predict():
    content = request.get_json()
    sample_rate = content["sampleRate"]
    data = content["data"]
    data_array = np.array(data, dtype=np.dtype)

    features, labels = np.empty((0,136)), np.empty(0)

    mel, contrast, tuning = extract_feature(data_array.astype(float), sample_rate)
    ext_features = np.hstack([mel,contrast, tuning])
    features = np.vstack([features, ext_features])

    result = y.eval({x: features})
    print "User: {}".format(result[0])
    return ('', 200)

@app.route('/')
def whos_that():
    return render_template('whos_that.html')

if __name__ == '__main__':
    app.run()
