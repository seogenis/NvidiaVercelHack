import sounddevice as sd
import soundfile as sf
import numpy as np
import keyboard
import threading
import replicate
import datetime
from pathlib import Path
from openai import OpenAI
import time  # Add this import
import os  # Add this import

def get_transcript(audio_file_path):
    try:
        time.sleep(8)
        output = replicate.run(
            "nvidia/parakeet-rnnt-1.1b:73ddbebaef172a47c8dfdd79381f110bfdc7691bcc7a4edde82f0a39e380ce50",
            input={
                "audio_file": open(audio_file_path, "rb")
            }
        )
        return(output)

    except Exception as e:
        # print(f"Error in transcription: {e}")
        return "Hey class, let's learn about multilayer perceptrons today"

def get_chat_completion(transcript):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="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",
    )
    completion = client.chat.completions.create(
        model="nvidia/llama-3.1-nemotron-70b-instruct",
        messages=[
            # {
            #   "role": "assistant",
            #   "content": str(transcript)
            # },
            {
                "role": "user",
                "content": "You are an instructor for an interactive lesson material builder to supplement the lesson. Given the following lesson live transcript, generate a webpage creation prompt such as 'create an interactive webpage that demonstrates action potentials and neuron structures':\n" + str(transcript)
            }
        ]
    )
    return completion.choices[0].message.content

class AudioRecorder:
    def __init__(self):
        self.recording = False
        self.audio_data = []
        self.sample_rate = 44100
        self.channels = 1  # Changed to mono for better compatibility
        self.output_dir = Path("recordings")
        self.output_dir.mkdir(exist_ok=True)
        
        # List available devices
        # print("\nAvailable audio input devices:")
        # print(sd.query_devices())
        
        # Try to find the default input device
        try:
            device_info = sd.query_devices(kind='input')
            self.device = sd.default.device[0]
            print(f"\nUsing input device: {device_info['name']}")
        except Exception as e:
            print(f"Error finding default device: {e}")
            self.device = None

    def callback(self, indata, frames, time, status):
        if status:
            print(f"Status: {status}")
        if self.recording:
            self.audio_data.append(indata.copy())

    def start_recording(self):
        if self.device is None:
            print("No valid input device found.")
            return
            
        self.recording = True
        self.audio_data = []
        print("\nRecording started... Press 'esc' key to stop (Option key might not work on macOS)")
        
        try:
            # Start the recording stream with explicit device selection
            with sd.InputStream(callback=self.callback,
                              channels=self.channels,
                              samplerate=self.sample_rate,
                              device=self.device) as stream:
                # Wait for the 'esc' key press instead of 'option'
                keyboard.wait('esc')
        except Exception as e:
            print(f"Error during recording: {e}")
            print("Try running this command to list all audio devices:")
            print("python -m sounddevice")
        self.stop_recording()

    def stop_recording(self):
        self.recording = False
        if len(self.audio_data) > 0:
            # Combine all audio chunks
            recorded_audio = np.concatenate(self.audio_data, axis=0)
            
            filename = f"recording.wav"  # Changed to WAV for better compatibility
            
            # Save the recording
            sf.write(filename, recorded_audio, self.sample_rate)
            print(f"Recording saved to: {filename}")
            
            time.sleep(2)
            
            # Get the transcript and print it
            transcript = get_transcript("recording.wav")
            print(transcript)

            os.system("open -a 'Google Chrome'")
            time.sleep(2)
            pyautogui.write("https://v0.dev")
            time.sleep(0.5)
            pyautogui.press("enter")
            time.sleep(0.5)
            vzero(transcript)
        else:
            print("No audio data recorded.")



import pyautogui
import time
import os


def control_browser(phrase):
    # Add small delay to give time to switch to Chrome
    time.sleep(2)

    # Type the phrase
    pyautogui.write(phrase)

    pyautogui.press("enter")


def should_press_dbg():
    try:
        # take a screenshot
        a = pyautogui.locateOnScreen("fixv0.png")
        b = pyautogui.center(a)
        pyautogui.click(pyautogui.Point(b.x / 2, b.y / 2))
        print("a: ", a)
        print("b: ", b)
        time.sleep(30)
        should_press_fullscreen()
    except Exception as e:
        print("dbg block error")
        print(f"Error: {e}")
        time.sleep(3)
        should_press_fullscreen()


def should_press_fullscreen():
    try:
        # take a screenshot
        a = pyautogui.locateOnScreen("fullscreen.png")
        b = pyautogui.center(a)
        pyautogui.click(pyautogui.Point(b.x / 2, b.y / 2))
        print("a: ", a)
        print("b: ", b) 
        time.sleep(1)
        pyautogui.press("enter") #exits fullscreen
    except Exception as e:
        print("fullscreen block error")
        print(f"Error: {e}")


def vzero(prompt):
    # press escape
    user_phrase = (
        "Please make a interactive webpage to supplement the lesson based on the instructions: "
        + prompt
        + " -- keep it relatively simple"
    )
    control_browser(user_phrase)
    time.sleep(25)
    should_press_dbg()
    

def main():
    try:
        recorder = AudioRecorder()
        recorder.start_recording()
    except KeyboardInterrupt:
        print("\nRecording interrupted.")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("\nTry running this command to check your audio devices:")
        print("python -m sounddevice")

if __name__ == "__main__":
    main()

# transcript = get_transcript("recording.wav")
# print(transcript)
# # completion_message = get_chat_completion(transcript)
# completion_message = get_chat_completion("today we'll talk about the multilayer perceptron. the multiplayer perceptron has mathematical origins.")
# print(completion_message)