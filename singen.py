import numpy as np
import pysoundcard as psc


class SineGenerator:
    """
    This Class implements a simple sine generator.
    It contains a playing method for directly playing the sine
    on the systems default soundcard.
    It can be used as a generator by calling the .read() function.
    read() returns the next samples of the size block_len.
    You can change the properties a0, f0 and phi0 online.

    parameters:
        a0: amplitude of the signal
        f0: frequency of the sine
        phi0: starting physe of the sine
        fs: sampling frequency
        block_len: length of blocks
        nchannels: number of channels

    returns:
        obj: SineGenerator Object

    important methods:
        obj.read(): yields the next block of samples
        obj.play(): plays on default sound device
        obj.stop(): stops playing

    examples:

    ## playing a sine with 1 kHz

    s = SineGenerator()
    s.play()

    # to stop write: s.stop()

    ## playing a chromatic tone scale:

    import time

    a0 = .1
    f0 = 1000.0
    block_len = 512
    fs = 44100
    s = SineGenerator(a0=a0, f0=f0, block_len=block_len, fs=fs)

    s.play()
    for k in np.arange(13):
        s.f0 = 2**(k/12.0) * f0
        time.sleep(1.0)

    s.stop()

    have fun, siegfried
    """

    def __init__(self, a0=0.5, f0=1000.0, phi0=0.0, fs=44100, block_len=1024, nchannels=2):
        self._a0 = a0
        self._f0 = f0
        self._phi0 = phi0
        self._fs = fs
        self._counter = 0
        self._block_len = block_len
        self._nblocks = lcm(self.len-1, self.block_len)
        self._nchannels = nchannels

        def callback(a, b, c, d):
            return self.read(), psc.continue_flag

        default_device = psc.default_output_device()
        default_device['output channels'] = self.nchannels
        self._stream = psc.Stream(fs=self.fs,
                                  block_length=self.block_len,
                                  output_device=default_device,
                                  input_device=False,
                                  callback=callback)

    @property
    def a0(self): return self._a0
    @a0.setter
    def a0(self, value):
        self._a0 = value

    @property
    def f0(self): return self._f0
    @f0.setter
    def f0(self, value):
        self._f0 = value

    @property
    def phi0(self): return self._phi0
    @phi0.setter
    def phi0(self, value):
        self._phi0 = value

    @property
    def fs(self): return self._fs
    @fs.setter
    def fs(self, value):
        self._fs = value

    @property
    def block_len(self): return self._block_len
    @block_len.setter
    def block_len(self, value):
        self._block_len = value
        self._nblocks = lcm(self.len-1, self.block_len)

    @property
    def nchannels(self): return self._nchannels
    @nchannels.setter
    def nchannels(self, value):
        self._nchannels = value

    @property
    def _period_len(self):
        return int(self.fs / self.f0)

    @property
    def _ntimes(self):
        return np.ceil(self.block_len/float(self._period_len))

    @property
    def len(self):
        return self._period_len*self._ntimes

    def _gensin(self):
        n = self._ntimes
        phi =  np.linspace(0, n*2*np.pi, n*self._period_len)[:-1]
        return self.a0 * np.sin(phi + self.phi0)

    @property
    def signal(self):
        return np.tile(self._gensin(), (2, 1)).T

    def read(self):
        self._counter = 1 + self._counter % self._nblocks
        idx = np.mod(np.arange(self.block_len*(self._counter-1),
                               self._counter*self.block_len),
                     self.len-1).astype(np.int)
        return self.signal[idx, :]  # self._signal[idx, :]

    def play(self):
        """plays the signal on the default sound device"""
        self._stream.start()

    def stop(self):
        self._stream.stop()



def gcd(a, b):
    """Returns greatest common divisor"""
    while b:
        a, b = b, a%b
    return a

def lcm(a, b):
    """Returns the lowest common multiple"""
    return a * b // gcd(a, b)


if __name__=='__main__':
    import time

    a0 = .1
    f0 = 1000.0
    block_len = 512
    fs = 44100
    s = SineGenerator(a0=a0, f0=f0, block_len=block_len, fs=fs)

    s.play()
    for k in np.arange(13):
        s.f0 = 2**(k/12.0) * f0
        time.sleep(0.5)

    s.stop()
