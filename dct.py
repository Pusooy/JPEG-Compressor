"""Implements the DCT."""
import scipy.fftpack


def dct2_scipy(two_d_array):
    """Implements the 2d orthonormal dct using scipy (much quicker)."""
    return scipy.fftpack.dct(scipy.fftpack.dct(two_d_array.T, norm='ortho')
                             .T, norm='ortho')
