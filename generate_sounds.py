import math
import os
import struct
import wave

output_dir = os.path.join('src', 'assets', 'sounds')
os.makedirs(output_dir, exist_ok=True)

sample_rate = 22050
duration = 0.25

for index in range(1, 11):
    path = os.path.join(output_dir, f'message-{index}.wav')
    frames = []

    for t in range(int(sample_rate * duration)):
        if index % 4 == 1:
            freq = 440 + (index * 70) + 110 * math.sin(2 * math.pi * 4 * t / sample_rate)
        elif index % 4 == 2:
            freq = 620 + (index * 55) + 90 * math.sin(2 * math.pi * 6 * t / sample_rate)
        elif index % 4 == 3:
            freq = 760 - (index * 35) + 80 * math.sin(2 * math.pi * 8 * t / sample_rate)
        else:
            freq = 520 + (index * 60) + 70 * math.sin(2 * math.pi * 10 * t / sample_rate)

        if t < sample_rate * 0.05:
            amplitude = 0.25 * (t / (sample_rate * 0.05))
        else:
            amplitude = 0.25

        value = int(32767 * amplitude * math.sin(2 * math.pi * freq * t / sample_rate))
        frames.append(struct.pack('<h', value))

    with wave.open(path, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(b''.join(frames))
