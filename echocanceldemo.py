# This is a practical demo of Echo Cancellation in audio samples using adaptive filter.  The filter used is adaptfilt from the Python library.
# For more information on adaptfilt, please refer to the source, https://pypi.python.org/pypi/adaptfilt/0.2
# An explainer on the terminologies used in the program: 
# The person in the far-end is "the sender".  The "listener" on the near-end hears the sender and replies to him.  
# However, the sender may get distracted hearing his own voice reflected from the listener's room along with the listener's voice.  
# The coefficients used to simulate the sender's voice getting reflected in the listener's room is the same as those used in the adaptfilt example
# in the above source.
# The purpose of this demo is to illustrate through audio programming, how an adaptive filter can remove the sender's own echo from what he hears.
# NLMS (Normalized Least Means Squares) mode of adaptfilt is used. For the given audio samples, step size of the algorithm is taken to be 0.05, and
# the number of coefficients of the filter to be 50.  These are trial and error values chosen to give the best fidelity.

# The speech content in the audio samples is as follows:
## Sender.wav "Hello there, I am speaking to the person I want to talk to right now."
## Listener.wav "This is the voice of the listener.  And he replies to the person on the other side."

# Processed audio is stored in the file 'output.wav', which is read and played twice by the program.  First it plays the pre-processing scenario.  
# Next it plays the post-processed scenario.
# The audio is kept slightly attenuated, so it is advisable to turn the speaker or headphone volume up to a medium level.

# **** START OF PROGRAM ****

import numpy as np
import matplotlib.pyplot as plt
import adaptfilt as adf
import winsound
from scipy.io import wavfile

waveout = 'output.wav' # Defining the output wave file
step = 0.05 # Step size
M = 50 # Number of filter taps in adaptive filter

# Read the audio files of sender and listener
sfs, u = wavfile.read('sender.wav')
lfs, v = wavfile.read('listener.wav')

u = np.fromstring(u, np.int16)
u = np.float64(u)

v = np.fromstring(v, np.int16)
v = np.float64(v)

# Generate the fedback signal d(n) by a) convolving the sender's voice with randomly chosen coefficients assumed to emulate the listener's room 
# characteristic, and b) mixing the result with listener's voice, so that the sender hears a mix of noise and echo in the reply.

coeffs = np.concatenate(([0.8], np.zeros(8), [-0.7], np.zeros(9), [0.5], np.zeros(11), [-0.3], np.zeros(3),[0.1], np.zeros(20), [-0.05]))
d = np.convolve(u, coeffs)
d = d/20.0
v = v/20.0
d = d[:len(v)] # Trims sender's audio to the same length as that of the listener's in order to mix them
d = d + v - (d*v)/256.0   # Mix with listener's voice.
d = np.round(d,0)

# Hear how the mixed signal sounds before proceeding with the filtering.
dsound = d.astype('int16')
wavfile.write(waveout, lfs, dsound)
winsound.PlaySound(waveout, winsound.SND_ALIAS)

# Apply adaptive filter
y, e, w = adf.nlms(u[:len(d)], d, M, step, returnCoeffs=True)

# The algorithm stores the processed result in the variable 'e', which is the mix of the error signal and the listener's voice.
# Hear how e sounds now.  Ideally we on behalf of the sender, should hear only the listener's voice.  Practically, some echo would still be present.

e = e.astype('int16')
wavfile.write(waveout, lfs, e)
winsound.PlaySound(waveout, winsound.SND_ALIAS)

# Calculate and plot the mean square weight error
mswe = adf.mswe(w, coeffs)
plt.figure()
plt.title('Mean squared weight error')
plt.plot(mswe)
plt.grid()
plt.xlabel('Samples')

plt.show()

# **** PROGRAM END ****

# Copyright (c) 2016 by Varun Chandramohan
