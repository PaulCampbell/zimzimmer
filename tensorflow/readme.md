# The tensorflow bit

It's a tensorflow neural network with a couple of layers.

We train it on a bunch of labelled wav files containing peoples voices. We take
those wavs, extract some interesting looking features from them (at time of writing
a combination of mean melspectrogram, mean spectral_contrast and tuning seem to be
getting some good results) and train the nn on those features and labels

Once trained, we can export the model for later use (where it will be loaded into the
[flask app](../site) so that we can chuck sound data at it and find out who it was that was talking)


start a virtual env...

```
virtualenv .
source bin/activate
```


TODO:

[ ] Labels should be names not ints...
[ ] Save exported model

