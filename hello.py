import replicate

def get_transcript(audio_file_path):
    try:
        output = replicate.run(
            "nvidia/parakeet-rnnt-1.1b:73ddbebaef172a47c8dfdd79381f110bfdc7691bcc7a4edde82f0a39e380ce50",
            input={
                "audio_file": open(audio_file_path, "rb")
            }
        )
        return(output)

    except Exception as e:
        print(f"Error in transcription: {e}")
    
    
print(get_transcript("recording.wav"))
