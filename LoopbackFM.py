"""
Synthesize percussive sounds using loopback frequency modulation based on the paper "Percussion Synthesis using Loopback Frequency Modulation Oscillators" written by Jennifer S. Hsu and Tamara Smyth.
"""
import sys
import timeit
from math import log, pi
import numpy as np
from scipy.signal import fftconvolve
from scipy.signal import butter
from scipy.signal import sosfilt
from scipy.io import wavfile

# Start timing.
start_time = timeit.default_timer()

# Sample rate and duration.
sr = 48000
samples_du = 0.5
leading_silence_du = 0.5
trailing_silence_du = 0.

# Choose whether or not to use convolution reverb.
use_convolution_reverb = True

# Create leading silence, trailing silence and n array.
if use_convolution_reverb == True:
    leading_silence = np.zeros((int(sr*leading_silence_du), 2)).astype(np.int16)
    trailing_silence = np.zeros((int(sr*trailing_silence_du), 2)).astype(np.int16)
else:
    leading_silence = np.zeros(int(sr*leading_silence_du)).astype(np.int16)
    trailing_silence = np.zeros(int(sr*trailing_silence_du)).astype(np.int16)
n_size = int(sr*samples_du)
n_arr = np.arange(1, n_size+1, 1).astype(np.float32)

# Loopback FM parameters.
f_arr = np.array([250, 500, 750, 1000, 2500], dtype=np.float32)
g = 0.9999
C = 0.

# Envelope parameters
A_arr = np.array([1, 0.75, 0.5, 0.25, 0.25], dtype=np.float32)
τ_arr = np.array([1000, 750, 500, 250, 250], dtype=np.float32)
if f_arr.size == A_arr.size == τ_arr.size:
    f_num = f_arr.size
else:
    print('Error: The sizes of f_arr, A_arr and τ_arr are not equal')
    sys.exit(0)

# Excitation parameters
excitation_type = 1
"""0 represents raised cosine envelopes, 1 represents filtered noise bursts."""
if excitation_type == 0:
    L = 50.
    use_excitation_envelope = False
    A_e = 1.
    τ_e = 10000.
elif excitation_type == 1:
    noise_du = 0.2
    f_low = 250
    f_high = 750
    noise_sr, noise_arr = wavfile.read('./audio_files_input/white_noise_uniform.wav')
    if noise_sr != sr:
        print('Error: The sample rates of direct sound and white noise are not the same.')
        sys.exit(0)
    use_excitation_envelope = True
    A_e = 0.25
    τ_e = 100.
else:
    print('Error: No excitation type.')
    sys.exit(0)

# Reverberation parameters
if use_convolution_reverb == True:
    ir_sr, ir_arr = wavfile.read('./audio_files_input/s1_r1_b.wav')
    if ir_sr != sr:
        print('Error: The sample rates of target output and IR file are not the same.')
        sys.exit(0)
    if ir_arr.ndim != 2:
        print('Error: The IR file is not stereo. The code only supports 2-channel IR files.')
        sys.exit(0)
    if ir_arr.dtype == np.int32:
        ir_max = np.iinfo(np.int32).max
    elif ir_arr.dtype == np.int16:
        ir_max = np.iinfo(np.int16).max
    else:
        print('Error: The bitrate of IR file is not supported. Only 16, 24 or 32 bit integar wav files are supported.')
        sys.exit(0)
    use_ir_envelope = False
    A_ir = 1.
    τ_ir = 20000.

# Loopback FM + Envelope synthesis.
B_arr = np.power(g, n_arr)
arr1 = np.sqrt(1-np.square(B_arr))
b_arr = (arr1-1)/B_arr
ω_c = 0.
A = 0.
τ = 0.
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

# Excitation synthesis
if excitation_type == 0:
    e_size = int(L)
    e_n_arr = np.arange(1, e_size+1, 1).astype(np.float32)
    p_arr1 = 0.5*(1-np.cos((2*pi*e_n_arr)/(L-1)))
    p_arr2 = np.zeros(1).astype(np.float32)
    p_arr2 = np.append(p_arr2, p_arr1[0: e_size-1])
    e_arr = p_arr1-p_arr2
elif excitation_type == 1:
    e_size =int(sr*noise_du)
    e_n_arr = np.arange(1, e_size+1, 1).astype(np.float32)
    noise_arr = noise_arr[0: e_size]
    e_sos_arr = butter(10, (f_low, f_high), btype='bandpass', output='sos', fs=sr)
    e_arr = sosfilt(e_sos_arr, noise_arr)
e_arr_max = max(abs(np.amax(e_arr)), abs(np.amin(e_arr)))
e_arr /= e_arr_max
if use_excitation_envelope == True:
    e_env_arr = A_e*np.exp(-e_n_arr/τ_e)
    e_arr *= e_env_arr

# Reverberation synthesis
if use_convolution_reverb == True:
    ir_arr = (ir_arr/ir_max).astype(np.float32)
    ir_arr_max = max(abs(np.amax(ir_arr)), abs(np.amin(ir_arr)))
    ir_arr /= ir_arr_max
    ir_arr_L = ir_arr[:, 0]
    ir_arr_R = ir_arr[:, 1]
    ir_size = ir_arr_L.size
    if use_ir_envelope == True:
        ir_n_arr = np.arange(1, ir_size+1, 1).astype(np.float32)
        ir_env_arr = A_ir*np.exp(-ir_n_arr/τ_ir)
        ir_arr_L *= ir_env_arr
        ir_arr_R *= ir_env_arr

# Convolve excitation, samples and ir arrays.
samples = fftconvolve(e_arr, m_arr)
samples_max = max(abs(np.amax(samples)), abs(np.amin(samples)))
samples /= samples_max
if use_convolution_reverb == True:
    samples_L = fftconvolve(samples, ir_arr_L)
    samples_R = fftconvolve(samples, ir_arr_R)
    samples = np.stack((samples_L, samples_R), axis=-1)
    samples_max = max(abs(np.amax(samples)), abs(np.amin(samples)))
    samples /= samples_max

# Amplify samples array as integer.
amp_max = 0.9*np.iinfo(np.int16).max
samples = (amp_max*samples).astype(np.int16)

# Concatenate the silence arrays and samples array, and write to wav file.
au = np.concatenate((leading_silence, samples, trailing_silence), axis=0)
wavfile.write('./audio_files_output/perc01.wav', sr, au)

# End timing.
end_time = timeit.default_timer()
running_time = end_time - start_time
print(f'running time: {round(running_time, 4)} seconds')
