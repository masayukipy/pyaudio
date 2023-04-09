import numpy as np
import pyaudio
from tensorflow.keras import models

from recording_helper import record_audio, terminate
from tf_helper import preprocess_audiobuffer
from turtle_helper import move_turtle

commands = ["right", "left", "stop", "up", "yes", "go", "down", "no"]

loaded_model = models.load_model("saved_model")


def callback(in_data, frame_count, time_info, status):  # noqa
    data = np.fromstring(in_data, dtype=np.int16)
    spec = preprocess_audiobuffer(data)
    prediction = loaded_model(spec)
    label_pred = np.argmax(prediction, axis=1)
    command = commands[label_pred[0]]
    move_turtle(command)
    if command == "stop":
        terminate()
    return (in_data, pyaudio.paContinue)


if __name__ == "__main__":
    audio = record_audio()
