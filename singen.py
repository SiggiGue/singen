"""
This module intends implementation of some signal generators for infinetely generating
audio test signals.
It depends on NumPy and PySoundcard.
An example is given in the __main__ part.
By siegfried Gündert
MIT Licenced
"""

import numpy as np
import pysoundcard as psc


class SineGenerator:
    """
    This Class implements a simple sine generator.
    It contains a playing method for directly playing the sine
    on the systems default soundcard.
    It can be used as a generator by calling the .read() function as well.
    read() returns the next block of the sine signal.
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

    # to stop type: s.stop()

    ## playing a chromatic tone scale:

    import time

    a0 = 0.1
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

    def __init__(self, a0=0.1, f0=1000.0, phi0=0.0,
                 fs=44100, block_len=1024, nchannels=2):
        self._a0 = a0
        self._f0 = f0
        self._phi0 = phi0
        self._fs = fs
        self._counter = 0
        self._block_len = block_len
        self._nblocks = lcm(self.len-1, self.block_len)
        self._nchannels = nchannels

        def callback(output, time, status):
            output[:] = self.read()
            return psc.continue_flag

        default_device = psc.default_output_device()
        self._stream = psc.OutputStream(
            samplerate=self.fs,
            blocksize=self.block_len,
            device=default_device,
            channels=self.nchannels,
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
        """Returns the basic sine function"""
        n = self._ntimes
        phi =  np.linspace(0, n*2*np.pi, n*self._period_len)[:-1]
        return self.a0 * np.sin(phi + self.phi0)

    @property
    def signal(self):
        """Returns the sine signal"""
        return np.tile(self._gensin(), (self.nchannels, 1)).T

    def _nextindex(self):
        self._counter = 1 + self._counter % self._nblocks
        return np.mod(np.arange(self.block_len*(self._counter-1),
                               self._counter*self.block_len),
                     self.len-1).astype(np.int)

    def read(self):
        """Returns the next block of samples"""
        return self.signal[self._nextindex(), :]  # self._signal[idx, :]

    def play(self):
        """Plays the signal on the default sound device"""
        self._stream.start()

    def stop(self):
        """Stops playing of deafult sound device"""
        self._stream.stop()


class LogSweep:
    def __init__(self, a0=0.1, fstart=125, fstop=8000, len_sec=2, pause_sec=0.5,
                 block_len=1024, fs=44100, nchannels=2):
        self._a0 = a0
        self._fstart = float(fstart)
        self._fstop = float(fstop)
        self._len_sec = float(len_sec)
        self._pause_sec = float(pause_sec)
        self._fs = int(fs)

        self._counter = 0
        self._block_len = block_len
        self._nblocks = lcm(self.len-1, self.block_len)
        self._nchannels = nchannels

        def callback(output, time, status):
            output[:] = self.read()
            return psc.continue_flag

        default_device = psc.default_output_device()
        self._stream = psc.OutputStream(
            samplerate=self.fs,
            blocksize=self.block_len,
            device=default_device,
            channels=self.nchannels,
            callback=callback)

    @property
    def a0(self): return self._a0
    @a0.setter
    def a0(self, value): self._a0 = value

    @property
    def fstart(self): return self._fstart
    @fstart.setter
    def fstart(self, value): self._fstart = float(value)

    @property
    def fstop(self): return self._fstop
    @fstop.setter
    def fstop(self, value): self._fstop = float(value)

    @property
    def len_sec(self): return self._len_sec
    @len_sec.setter
    def len_sec(self, value): self._len_sec = float(value)

    @property
    def pause_sec(self): return self._pause_sec
    @pause_sec.setter
    def pause_sec(self, value): self._pause_sec = float(value)

    @property
    def fs(self): return self._fs
    @fs.setter
    def fs(self, value): self._fs = float(value)

    @property
    def block_len(self): return self._block_len
    @block_len.setter
    def block_len(self, value): self._block_len = float(value)

    @property
    def nchannels(self): return self._nchannels
    @nchannels.setter
    def nchannels(self, value): self._nchannels = float(value)

    @property
    def len(self): return int(self.fs * (self.len_sec + self.pause_sec))

    def _gensignal(self):
        sweep = self.a0 * gen_logsweep(self.fstart, self.fstop, self.len_sec, self.fs)[1]
        pause = np.zeros(int(self.pause_sec*self.fs))
        return np.concatenate((sweep, pause))

    @property
    def signal(self):
        return np.tile(self._gensignal(), (self.nchaannels, 1)).T

    def _nextindex(self):
        self._counter = 1 + self._counter % self._nblocks
        return np.mod(np.arange(self.block_len*(self._counter-1),
                               self._counter*self.block_len),
                     self.len-1).astype(np.int)

    def read(self):
        return self.signal[self._nextindex(), :]

    def play(self):
        self._stream.start()

    def stop(self):
        self._stream.stop()


def gen_logsweep(fstart, fstop, len_sec, samplerate):
    ''' Generates an exponential sweep.
    usage:
        t, s = logsweep(fstart, fstop, len_sec, samplerate)
    input:
        fstart: start frequency in Hz
        fstop: stop frequency in Hz
        len_sec: length of the sweep in seconds
        samplerate: frequency of sample points in Hz
    output:
        t: time vector in seconds
        s: exponential sweep signal
    '''
    nsamples = np.round(len_sec * samplerate)
    t = np.arange(nsamples) * (1.0/samplerate)
    w1 = 2*np.pi * fstart
    w2 = 2*np.pi * fstop
    c = np.log(w2 / w1)
    phi = w1 * (len_sec / c) * (np.exp(t*c/len_sec) - 1)
    return t, np.sin(phi)


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

    # play a chromatic scale by changing the f0 of my SineGenerator Object:
    s.play()
    for k in np.arange(13):
        s.f0 = 2**(k/12.0) * f0
        time.sleep(0.15)

    s.stop()

    sl = LogSweep()
    sl.play()

    time.sleep(2.0)

    sl.fstart = 3000
    sl.fstop = 500

    time.sleep(2.0)

    sl.stop()
