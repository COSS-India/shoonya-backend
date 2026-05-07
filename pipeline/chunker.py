import os
from pydub import AudioSegment
from pydub.silence import split_on_silence


def chunk_audio_to_sentences(input_file, output_folder="audio_chunks"):
    """
    Chunks an audio file into separate sentences using silence detection (VAD).
    """
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    print(f"Loading {input_file}...")
    try:
        audio = AudioSegment.from_file(input_file)
    except Exception as e:
        print(f"Error loading audio: {e}")
        return

    print("Analyzing audio and detecting sentence boundaries...")

    # --- CORE VAD PARAMETERS ---
    # You will likely need to tweak these three numbers based on your specific audio!

    chunks = split_on_silence(
        audio,
        # 1. min_silence_len: How long must the silence be to count as a new sentence?
        # 500ms (half a second) is usually a good baseline for a period/sentence break.
        min_silence_len=500,

        # 2. silence_thresh: How quiet is considered "silence"?
        # audio.dBFS gets the average loudness of the file. We set the threshold
        # to be 16 decibels quieter than the average.
        silence_thresh=audio.dBFS - 16,

        # 3. keep_silence: Leave a little bit of silence at the start/end of the chunk
        # so the audio doesn't sound abruptly cut off.
        keep_silence=250
    )

    print(f"Detected {len(chunks)} sentences. Exporting...")

    # Export each chunk as a new WAV file
    for i, chunk in enumerate(chunks):
        # Format the filename with leading zeros (e.g., sentence_001.wav)
        output_filename = os.path.join(output_folder, f"sentence_{i + 1:03d}.wav")

        print(f"Exporting {output_filename} (Duration: {len(chunk) / 1000:.2f}s)")
        chunk.export(output_filename, format="wav")

    print("Chunking complete!")


# --- Example Usage ---
if __name__ == "__main__":
    # Replace with your actual audio file path (supports wav, mp3, m4a, etc.)
    INPUT_AUDIO = "localtest/garo_test.mp3"

    chunk_audio_to_sentences(INPUT_AUDIO)