import glob
import os
import librosa
import numpy as np
import tensorflow as tf


# We're gonna grab some features from each sound... try some of these
# 1) melspectrogram: Compute a Mel-scaled power spectrogram
# 2) mfcc: Mel-frequency cepstral coefficients
# 3) chorma-stft: chromagram of the waveform
# 4) spectral_contrast: Spectral contrast of the waveform
# 5) tonnetz: Tonal centroid features of the waveform
# 6) tuning: pitch/tuning of the waveform

def extract_feature(file_name):
    X, sample_rate = librosa.load(file_name)
    stft = np.abs(librosa.stft(X))
    mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T,axis=0)
    chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)
    tuning = librosa.estimate_tuning(y=X, sr=sample_rate)
    mel = np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T,axis=0)
    contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T,axis=0)
    tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(X), sr=sample_rate).T,axis=0)
    return mfccs,chroma,mel,contrast,tonnetz,tuning

def parse_audio_files(parent_dir,sub_dirs,file_ext='*.wav'):
    features, labels = np.empty((0,136)), np.empty(0)
    for label, sub_dir in enumerate(sub_dirs):
        for fn in glob.glob(os.path.join(parent_dir, sub_dir, file_ext)):
            mfccs, chroma, mel, contrast,tonnetz, tuning = extract_feature(fn)
            ext_features = np.hstack([mel,contrast, tuning])
            features = np.vstack([features, ext_features])
            labels = np.append(labels, fn.split('/')[2].split('-')[1][:1])
    return np.array(features), np.array(labels, dtype = np.int)

def one_hot_encode(labels):
    n_labels = len(labels)
    n_unique_labels = len(np.unique(labels))
    one_hot_encode = np.zeros((n_labels,n_unique_labels))
    one_hot_encode[np.arange(n_labels), labels] = 1
    return one_hot_encode
