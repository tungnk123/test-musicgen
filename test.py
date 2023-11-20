from pydub import AudioSegment

def duplicate_and_crossfade(audio1, audio2, num_duplicates, crossfade_duration, trim_duration):
    # Load audio files
    audio_file1 = AudioSegment.from_file(audio1)
    audio_file2 = AudioSegment.from_file(audio2)

    # Ensure both audio files have the same sample width and frame rate
    audio_file1 = audio_file1.set_sample_width(2)
    audio_file2 = audio_file2.set_sample_width(2)

    audio_file1 = audio_file1.set_frame_rate(44100)
    audio_file2 = audio_file2.set_frame_rate(44100)

    # Trim 1 second from the beginning and end of each audio clip
    audio_file1 = audio_file1[1000:-1000]
    audio_file2 = audio_file2[1000:-1000]

    # Duplicate each audio clip
    duplicated_audio1 = audio_file1 * num_duplicates
    duplicated_audio2 = audio_file2 * num_duplicates

    # Initialize the crossfaded audio
    crossfaded_audio = AudioSegment.silent(duration=0)

    # Crossfade the duplicated audio clips
    for i in range(num_duplicates):
        start_time = i * len(audio_file1)
        end_time = (i + 1) * len(audio_file1)

        # Extract the corresponding segments from each duplicated audio clip
        segment1 = duplicated_audio1[start_time:end_time - trim_duration * 1000]
        segment2 = duplicated_audio2[start_time:end_time - trim_duration * 1000]

        # Apply fade in and fade out to achieve a crossfade effect
        crossfaded_segment = segment1.fade_out(crossfade_duration * 1000).overlay(segment2.fade_in(crossfade_duration * 1000))

        # Append the crossfaded segment to the result
        crossfaded_audio = crossfaded_audio + crossfaded_segment

    return crossfaded_audio

# Paths to your audio files
audio_file1 = "12.mp4"

# Number of duplicates, crossfade duration, and trim duration
num_duplicates = 5
crossfade_duration = 3  # seconds
trim_duration = 2  # seconds

# Create the crossfaded audio
crossfaded_audio = duplicate_and_crossfade(audio_file1, audio_file1, num_duplicates, crossfade_duration, trim_duration)

# Export the crossfaded audio to a new file
output_path = "crossfaded_output.mp4"
crossfaded_audio.export(output_path, format="mp4")
