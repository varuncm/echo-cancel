# echo-cancel
Demo the principle of Echo Cancellation using simple audio samples.

This is a practical demo of Echo Cancellation in audio samples using adaptive filter.  The filter used is adaptfilt from the Python library. For more information on adaptfilt, please refer to the source, https://pypi.python.org/pypi/adaptfilt/0.2

An explainer on the terminologies used in the program: The person in the far-end is "the sender".  The "listener" on the near-end hears the sender and replies to him.  However, the sender may get distracted hearing his own voice reflected from the listener's room along with the listener's voice.  
The coefficients used to simulate the sender's voice getting reflected in the listener's room is the same as those used in the adaptfilt example in the above source.

The purpose of this demo is to illustrate through audio programming, how an adaptive filter can remove the sender's own echo from what he hears. 
NLMS (Normalized Least Means Squares) mode of adaptfilt is used. For the given audio samples, step size of the algorithm is taken to be 0.05, and the number of coefficients of the filter to be 50.  These are trial and error values chosen to give the best fidelity.

The speech content in the audio samples is as follows:
Sender.wav "Hello there, I am speaking to the person I want to talk to right now."
Listener.wav "This is the voice of the listener.  And he replies to the person on the other side."

Processed audio is stored in the file 'output.wav', which is read and played twice by the program.  First it plays the pre-processing scenario.  Next it plays the post-processed scenario.  The audio is kept slightly attenuated, so it is advisable to turn the speaker or headphone volume up to a medium level.
