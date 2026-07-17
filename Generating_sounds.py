import math
import os
import struct
import wave

# Output folder for generated sounds
OUTPUT_DIR = os.path.join("src", "assets", "sounds")
os.makedirs(OUTPUT_DIR, exist_ok=True)

SAMPLE_RATE = 22050   # samples per second
DURATION = 0.25       # seconds

def generate_tone(index: int) -> bytes:
    """Generate raw audio frames for a given index."""
    frames = []
    total_samples = int(SAMPLE_RATE * DURATION)

    for t in range(total_samples):
        # Pick frequency pattern based on index
        if index % 4 == 1:
            freq = 440 + (index * 70) + 110 * math.sin(2 * math.pi * 4 * t / SAMPLE_RATE)
        elif index % 4 == 2:
            freq = 620 + (index * 55) + 90 * math.sin(2 * math.pi * 6 * t / SAMPLE_RATE)
        elif index % 4 == 3:
            freq = 760 - (index * 35) + 80 * math.sin(2 * math.pi * 8 * t / SAMPLE_RATE)
        else:
            freq = 520 + (index * 60) + 70 * math.sin(2 * math.pi * 10 * t / SAMPLE_RATE)

        # Apply fade‑in for first 5% of samples
        if t < SAMPLE_RATE * 0.05:
            amplitude = 0.25 * (t / (SAMPLE_RATE * 0.05))
        else:
            amplitude = 0.25

        # Calculate sample value (sine wave)
        value = int(32767 * amplitude * math.sin(2 * math.pi * freq * t / SAMPLE_RATE))
        frames.append(struct.pack("<h", value))  # pack as 16‑bit little‑endian

    return b"".join(frames)


def save_wav(index: int, frames: bytes):
    """Save frames to a .wav file."""
    path = os.path.join(OUTPUT_DIR, f"message-{index}.wav")
    with wave.open(path, "wb") as wav_file:
        wav_file.setnchannels(1)        # mono
        wav_file.setsampwidth(2)        # 16‑bit samples
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(frames)


# Generate 10 different tones
for i in range(1, 11):
    frames = generate_tone(i)
    save_wav(i, frames)
