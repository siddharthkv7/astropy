from __future__ import division

import numpy as np
from .. import misc


def test_sigma_clip():
    from numpy.random import randn,seed,get_state,set_state
    
    #need to seed the numpy RNG to make sure we don't get some amazingly flukey
    #random number that breaks one of the tests
    
    randstate = get_state()
    try:
        seed(12345)  # Amazing, I've got the same combination on my luggage!
        
        randvar = randn(10000)

        data, mask = misc.sigma_clip(randvar, 1, 2)
        maskedarr = misc.sigma_clip(randvar, 1, 2, maout=True)

        assert sum(mask) > 0
        assert data.size < randvar.size
        assert np.all(mask == ~maskedarr.mask)

        #this is actually a silly thing to do, because it uses the standard
        #deviation as the variance, but it tests to make sure these arguments
        #are actually doing something
        data2, mask2 = misc.sigma_clip(randvar, 1, 2, varfunc=np.std)
        assert not np.all(data == data2)
        assert not np.all(mask == mask2)

        data3, mask3 = misc.sigma_clip(randvar, 1, 2, cenfunc=np.mean)
        assert not np.all(data == data3)
        assert not np.all(mask == mask3)

        #now just make sure the iters=None method works at all.
        maskedarr = misc.sigma_clip(randvar, 3, None, maout=True)
    finally:
        set_state(randstate)