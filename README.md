This is an incomplete python implementation of the paper "Percussion Synthesis using Loopback Frequency Modulation Oscillators" written by Jennifer S. Hsu and Tamara Smyth.

Quote form the paper:
"Copyright: c 2018 Jennifer S. Hsu et al. This is an open-access article distributed under the terms of the Creative Commons Attribution 3.0 Unported License, which permits unrestricted use, distribution, and reproduction in any medium, provided the original author and source are credited."

Impulse response audio file 'DivorceBeach.wav' downloaded from echothief.com ("Copyright 2013-2020 Chris Warren cwarren@sdsu.edu") 

Impulse response audio file 's1_r1_b.wav' downloaded from http://legacy.spa.aalto.fi/projects/poririrs/ ("SIRR processed data are Copyright ©2005 by Helsinki University of Technology (TKK). All other data are Copyright ©2005 by TKK, Akukon Oy Consulting Engineers, and the authors. The data are provided free for noncommercial purposes, provided the authors are cited when the data are used in any research application. Commercial use is prohibited and allowed only by written permission of the copyright owners.")

The code is still under research. I'm still trying to understand how parameters change will affect the final output. Running 'LoopbackFM.py' will generate the 'percussive01.wav' audio example in the 'audio_files_output' folder. You can change the parameters in the code for different sounds. 

If you don't understand the code, you'd better only change the following parameters I'll explain. If you understand my code, you can change and add anything to create something more exciting and share with me.

- All variables with '_arr' in their names are numpy arrays, otherwise they're single-value variables.

- In the 'Sample rate and duration' section, you can sepcify the sample rate, main samples duration and leading and trailing silence duration for better listening experience. Note that the sample rate needs to be the same as the impulse response audio file's sample rate.

- In the 'Choose whether or not to use convolution reverb' section, if you specify 'False', the output will be dry sound.

- In the 'Loopback FM parameters' section, you can specify the basic frequencies in f_arr.

- In the 'Envelope parameters' section, you can specify the envelope amplitude at the beginning in the A_arr and decay rate in τ_arr. They have to have the same sizes as f_arr.

- In the 'Excitation parameters' section, you can specify the L parameter for tonal balance. The bigger the L is, the more bass frequencies and less high frequencies will be generated. You can also choose whether or not to apply an envelope to the excitation array.

- In the 'Reverbration parameters' section, you can copy your own impulse response audio file into the 'audio_files_input' folder and change the wavfile.read file path in the code to convolve your own impulse response. Note that the code only supports 16bit, 24bit or 32bit stereo IR wav files. But surely you can change the settings if you understand my code. You can also choose whether or not to apply an envelope to the impulse response array, which enables you to control how much IR will be convolved (dry/wet degree) by changing the A_ir and τ_ir parameters.

There's a timing section to record the time. It takes 0.01 to 0.05 seconds to run on my windows cpu computer.
