"""
Synthesize percussive sound using loopback frequency modulation.
"""
import timeit
from math import log, pi
import numpy as np
from scipy import signal
from scipy.io import wavfile

# Start timing.
start_time = timeit.default_timer()

# Specify sample rate and duration.
sr: np.float32 = 44100
direct_du: np.float32 = 0.5
leading_silence_du: np.float32 = 0.5
trailing_silence_du: np.float32 = 0.5

# Create leading silence, trailing silence, samples and n array.
leading_silence = np.zeros((int(sr*leading_silence_du), 2)).astype(np.int16)
trailing_silence = np.zeros((int(sr*trailing_silence_du), 2)).astype(np.int16)
samples = np.empty(0, dtype=np.float32)
n_size = int(sr*direct_du)
n_arr = np.arange(1, n_size+1, 1).astype(np.float32)

# Loopback FM parameters
f_arr = np.array([250, 500, 750, 1000], dtype=np.float32)
g: np.float32 = 0.9999
C: np.float32 = 0.

# Envelope parameters
A_arr = np.array([1, 0.75, 0.5, 0.25], dtype=np.float32)
τ_arr = np.array([1000, 750, 500, 250], dtype=np.float32)

# Commuted synthesis parameters
L: np.float32 = 50

ir_sr, ir_arr = wavfile.read('Space4ArtGallery.wav')
ir_max_int32 = np.iinfo(np.int32).max
ir_arr = (ir_arr/ir_max_int32).astype(np.float32)
ir_max_abs = max(abs(np.amax(ir_arr)), abs(np.amin(ir_arr)))
ir_arr /= ir_max_abs
ir_arr_L = ir_arr[:, 0]
ir_arr_R = ir_arr[:, 1]
ir_size = ir_arr_L.size
A_ir = 1
τ_ir = 20000

# Check if the sizes of f_arr, A_arr and τ_arr are the same.
if f_arr.size == A_arr.size == τ_arr.size:
    f_num = f_arr.size
else:
    print('Unequal f_arr, A_arr and τ_arr sizes error')
    exit()

# Loopback FM + Envelope synthesis.
B_arr = np.power(g, n_arr)
arr1 = np.sqrt(1-np.square(B_arr))
b_arr = (arr1-1)/B_arr
ω_c: np.float32 = 0.
A: np.float32 = 0.
τ: np.float32 = 0.
m_arr = np.zeros(n_size).astype(np.float32)

for i in range(0, f_num):
    f = f_arr[i]
    ω_c = 2*pi*f
    Θ_arr = (ω_c/log(g))*(arr1-np.arctanh(arr1))+C
    z_r_arr = np.cos(Θ_arr)+(1-np.cos(2*Θ_arr))/(1/b_arr+b_arr+2*np.cos(Θ_arr))
    A = A_arr[i]
    τ = τ_arr[i]
    env_arr = A*np.exp(-n_arr/τ)
    m_arr += z_r_arr*env_arr

# Commuted synthesis
p_split = int(L+1)
p_arr1 = np.append(0.5*(1-np.cos((2*pi*n_arr[0: p_split])/(L-1))), \
                    np.zeros(n_size-p_split))
p_arr2 = np.append(p_arr1[1: n_size], 0.)
e_arr = p_arr1-p_arr2

ir_env_arr = np.arange(1, ir_size+1, 1).astype(np.float32)
ir_env_arr = A_ir*np.exp(-ir_env_arr/τ_ir)
ir_arr_L *= ir_env_arr
ir_arr_R *= ir_env_arr

# Convolution
samples = signal.fftconvolve(e_arr, m_arr)
samples_max_abs = max(abs(np.amax(samples)), abs(np.amin(samples)))
samples /= samples_max_abs
samples_L = signal.fftconvolve(samples, ir_arr_L)
samples_R = signal.fftconvolve(samples, ir_arr_R)
samples = np.stack((samples_L, samples_R), axis=-1)
samples_max_abs = max(abs(np.amax(samples)), abs(np.amin(samples)))
samples /= samples_max_abs

# Amplify samples array as integer.
amp_max = 0.75*np.iinfo(np.int16).max
samples = (amp_max*samples).astype(np.int16)

# Combine the silence array and samples array, and write to wav file.
au = np.concatenate((leading_silence, samples, trailing_silence), axis=0)
wavfile.write('percussive01.wav', sr, au)

# End timing.
end_time = timeit.default_timer()
running_time = end_time - start_time
print(f'running time: {round(running_time, 2)} seconds')
