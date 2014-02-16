# Generate Sine Singnals with infinite duration and play them on your sound device

This module intends to implements a sine signal generator for infinetely playing on your audio
device with the module PySoundcard.

It can be used as a signal block yielder as well for generating more complex test signals of infenite length.
When playing the signal on the soundcard the user is able to change the parameters of the signal generator online! And you can play the signal as long as you want.

It depends on NumPy and PySoundcard.

## Examples

*Play a sine with initial parameters (a0=0.1, f0=1000):*
```python
    s = SineGenerator()
    s.play()

    # to stop write: s.stop()

```


*Play a chromatic scale:*
```python
    a0 = .1
    f0 = 1000.0
    block_len = 512
    fs = 44100
    s = SineGenerator(a0=a0, f0=f0, block_len=block_len, fs=fs)

    # play a chromatic scale by changing the f0 of my SineGenerator Object:
    s.play()
    for k in np.arange(13):
        s.f0 = 2**(k/12.0) * f0
        time.sleep(0.5)

    s.stop()

```

*Play with exponentially swept sine:*
```python

    sl = LogSweep()
    sl.play()

    time.sleep(2.0)

    sl.fstart = 3000
    sl.fstop = 500

    time.sleep(2.0)

    sl.stop()

```
