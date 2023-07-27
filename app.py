# Import required libraries
import numpy as np
import pyaudio
import time

# Set sample rate either 44100 or 48000
#SAMPLE_RATE = 44100
SAMPLE_RATE = 48000


def generate_sample(freq, duration, volume):

    amplitude = 2000
    total_samples = np.round(SAMPLE_RATE * duration)
    w = 2.0 * np.pi * freq / SAMPLE_RATE
    k = np.arange(0, total_samples)

    return np.round(amplitude * np.sin(k * w))


# Frequency arrary for notes in piano from middle C (C4) to the next C (C5) one octave higher
# The notes is as follows C4, C4#, D4, D4#, E4, F4, F4#, G4, G4#, A4, A4#, B4, C5 
freq_array = np.array([261.6256, 293.6648, 329.6276, 349.2282, 391.9954, 440.0000, 493.8833, 523.2511])

# Frequency arrary for notes in piano from C5 to the middle C one octave lower
# The notes is as follows C5, B4, A4#, A4, G4#, G4, F4#, F4, E4, D4#, D4, C4#, C4
rev_freq = freq_array[::-1] 

tones, tones1 = [], []
 
for freq in freq_array:

    tone = np.array(generate_sample(freq, 2, 1.0), dtype=np.int16)    
    
    # Appending the tones to a list
    tones.append(tone)

for freq in rev_freq:
    tone1 = np.array(generate_sample(freq, 2, 1.0), dtype=np.int16)    
    
    # Appending the tones to a list
    tones1.append(tone1)


def fmain():
    # Instantiate PyAudio and initialize PortAudio system resources
    p = pyaudio.PyAudio()

    # Open stream 
    stream = p.open(format=p.get_format_from_width(width=2), 
                    channels=2, 
                    rate=SAMPLE_RATE,
                    output=True)

    # Play samples from the tones list with a interval of 1 second between successive notes 
    for tone in tones:
        stream.write(tone)
        time.sleep(0.05) # wait for 50 milli seconds between tones

    # Play samples from the tones1 list with a shorter delay between successive notes
    for tone1 in tones1:
        stream.write(tone1)
        time.sleep(0.05) # wait for 50 milli seconds between tones
        
    stream.stop_stream()
    # Close stream 
    stream.close()
    
    # Release PortAudio system resources 
    p.terminate()

# Calling function to play the frequencies converted into tones 
fmain()