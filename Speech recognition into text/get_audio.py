import pyaudio
import wave
in_path = "./audios/input.wav"

def get_audio(filepath):
    aa = str(input("Start or not？   （y/n）"))
    if aa == str("y") :
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1                # Track number
        RATE = 11025                # Sampling rate
        RECORD_SECONDS = 5          # Recording time
        WAVE_OUTPUT_FILENAME = filepath
        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("*"*5, "Start to Recording", "*"*5)
        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        print("*"*5, "End\n")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
    elif aa == str("否"):
        exit()
    else:
        print("Voice entry failed. Please restart")
        get_audio(in_path)

