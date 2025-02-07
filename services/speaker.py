'''
Module dedicated to audio creation from text and its reproduction. It uses Google Text-to-Speech services.
'''

from services.cloud.google_api import text_to_speech
import simpleaudio as sa

class Speaker:
    def __init__(self, rate = 24000, channels = 1, sample_width = 2):
        self.rate = rate
        self.channels = channels
        self.format = format
        self.sample_width = sample_width
        self.current_playback = None
        
    def speak(self, text):
        audio = text_to_speech(text)
        with open("audio.wav", "wb") as audio_file:
            audio_file.write(audio)
        
        try:
            audio_object = sa.WaveObject.from_wave_file("audio.wav")
            play_object = audio_object.play()
            play_object.wait_done()
        except Exception as e:
            print(f"Error al reproducir el audio: {e}")
              
            
    def play_background_music(self, audio_path):
        try:
            wave_obj = sa.WaveObject.from_wave_file(audio_path)
            self.current_playback = wave_obj.play()
        except Exception as e:
            print(f"Error playing background music: {e}")
        
    def stop_background_music(self):
        if self.current_playback:
            self.current_playback.stop()
            self.current_playback = None  
        