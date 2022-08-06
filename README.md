This is a imcomplete python implementation of the paper "Percussion Synthesis using Loopback Frequency Modulation Oscillators" written by Jennifer S. Hsu and Tamara Smyth.

Quote form the paper:
"Copyright: c 2018 Jennifer S. Hsu et al. This is an open-access article distributed under the terms of the Creative Commons Attribution 3.0 Unported License, which permits unrestricted use, distribution, and reproduction in any medium, provided the original author and source are credited."

Impulse response audio 'Space4ArtGallery.wav' downloaded from echothief.com (Copyright 2013-2020 Chris Warren cwarren@sdsu.edu).

The code is still under development. Running 'LoopbackFM.py' will generate the 'percussive01.wav' audio example.

You can change the parameters in the code for different sound. I'm still trying to understand how parameters change will affect the final output. 

If you don't understand the code, you'd better only change the following parameters I'll explain. If you understand my code, you can change and add anything to create something more exciting and share with me.

- In the 'Specify sample rate and duration' section, you can sepcify the sample rate, main samples duration and leading and trailing silence duration for better listening experience. Note that the sample rate needs to be the same as the impulse response audio file's sample rate.

- In the 'Loopback FM parameters' section, you can specify the basic frequencies in f_arr.

- In the 'Envelope parameters' section, you can specify the envelope amplitude at the beginning in the A_arr and decay rate in τ_arr. They have to have the same sizes as f_arr.

- In the 'Commuted synthesis parameters' section, you can specify the L parameter for tonal balance. The bigger L is, the more bass frequencies will be generated. This probably has the most impact on the output. You can also copy your own impulse response audio into the 'impulse_response' folder to convolve your own impulse response. Note that the code only supports 44.1kHz 24bit or 32bit IR audio files. But surely you can change the settings if you understand my code. Like the above envelope, I've created an envelope array for impulse response so you can control how much IR will be convolved (dry/wet degree) by changing the A_ir and τ_ir parameters (this time they're single values rather than arrays).

There's a timing section to record the time. It takes 0.03 to 0.04 seconds to run on my windows cpu computer.
