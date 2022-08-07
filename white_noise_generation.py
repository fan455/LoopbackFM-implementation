"""
White noise generation
"""
import timeit
import numpy as np
from scipy.io import wavfile

# Start timing.
start_time = timeit.default_timer()

# Parameters.
sr = 48000
du = 5.

# Generation.
white_noise_uniform = np.random.uniform(-1, 1, int(sr*du)).astype(np.float32)

# Write to wav file.
wavfile.write('./audio_files_input/white_noise_uniform.wav', sr, white_noise_uniform)

# End timing.
end_time = timeit.default_timer()
running_time = end_time - start_time
print(f'running time: {round(running_time, 4)} seconds')
