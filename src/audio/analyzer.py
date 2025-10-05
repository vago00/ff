# src/audio/analyzer.py
import numpy as np
import sounddevice as sd
import threading
import queue
from src.config import Config

class AudioAnalyzer:
    def __init__(self):
        self.audio_queue = queue.Queue()
        self.volume = 0
        self.is_beat = False
        self.running = True
        
        # Configurações
        self.sample_rate = 44100
        self.block_size = 2048
        self.channels = 1
        
        self._start_audio_thread()
    
    def _start_audio_thread(self):
        self.audio_thread = threading.Thread(target=self._audio_capture)
        self.audio_thread.daemon = True
        self.audio_thread.start()
    
    def _audio_callback(self, indata, frames, time, status):
        self.audio_queue.put(indata.copy())
    
    def _audio_capture(self):
        with sd.InputStream(
            channels=self.channels,
            samplerate=self.sample_rate,
            blocksize=self.block_size,
            callback=self._audio_callback
        ):
            while self.running:
                try:
                    audio_data = self.audio_queue.get(timeout=1.0)
                    self.analyze_audio(audio_data)
                except queue.Empty:
                    continue
    
    def analyze_audio(self, audio_data):
        self.volume = float(np.sqrt(np.mean(audio_data**2)))
        self.is_beat = self.volume > Config.INTENSE_THRESHOLD
    
    def get_state(self):
        if self.volume < Config.VOID_THRESHOLD:
            return "void"
        elif self.volume < Config.INTENSE_THRESHOLD:
            return "ambient"
        else:
            return "intense"
    
    def stop(self):
        self.running = False
        if hasattr(self, 'audio_thread'):
            self.audio_thread.join()