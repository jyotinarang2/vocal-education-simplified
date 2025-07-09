import librosa
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.stats import gaussian_kde

def extract_pitch(audio_path, f_ref=440.0):
    y, sr = librosa.load(audio_path)
    f0, _, _ = librosa.pyin(y, fmin=librosa.note_to_hz("C2"), fmax=librosa.note_to_hz("C7"))
    f0 = f0[~np.isnan(f0)]
    cents = 1200 * np.log2(f0 / f_ref)
    return cents

def plot_kde(cents, filename="assets/intonation_kde.png"):
    kde = gaussian_kde(cents)
    x = np.linspace(0, 1200, 1000)
    y = kde(np.mod(x, 1200))  # Wrap to octave

    os.makedirs("assets", exist_ok=True)
    plt.figure(figsize=(8, 4))
    plt.plot(x, y)
    plt.title("Pitch KDE (Cents, wrapped to octave)")
    plt.xlabel("Cents")
    plt.ylabel("Density")
    plt.axvline(0, color='red', linestyle='--', label='Tonic')
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    return filename

def analyze_intonation(audio_path, f_ref=440.0):
    cents = extract_pitch(audio_path, f_ref)
    cents_mod = np.mod(cents, 1200)
    plot_path = plot_kde(cents_mod)
    std_dev = np.std(cents_mod)
    feedback = "✅ Intonation is mostly stable!" if std_dev < 40 else "⚠️ Intonation is unstable. Try again with better pitch control."
    return feedback, plot_path
