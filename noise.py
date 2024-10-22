import noisereduce as nr
import numpy as np
from pydub import AudioSegment

def load_audio(file_path):
    audio = AudioSegment.from_file(file_path)  # Load MP3 or other formats
    audio = audio.set_frame_rate(44100).set_channels(1)  # Convert to 44.1kHz mono
    samples = np.array(audio.get_array_of_samples())
    return samples, audio.frame_rate

def reduce_noise(data, rate):
    noise_sample = data[0:rate*2]  # Use first 2 seconds as noise profile
    reduced_noise_data = nr.reduce_noise(y=data, sr=rate, y_noise=noise_sample)
    return reduced_noise_data

def save_audio(data, file_path, rate):
    audio_segment = AudioSegment(
        data=data.tobytes(),
        sample_width=2,  # 16-bit audio
        frame_rate=rate,
        channels=1
    )
    audio_segment.export(file_path, format='mp3')  # Save as MP3

# Main function
def main():
    input_file = input("Enter the path to the audio file (e.g., music_with_noise.mp3): ")
    output_file = input("Enter the desired output file name (e.g., clean_music.mp3): ")

    data, rate = load_audio(input_file)
    clean_data = reduce_noise(data, rate)
    save_audio(clean_data, output_file, rate)
    print("Noise removed and clear audio saved!")

if __name__ == "__main__":
    main()
