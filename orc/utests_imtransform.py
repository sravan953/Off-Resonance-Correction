import unittest

import numpy as np
import math
import matplotlib.pyplot as plt
import ORC

# Cartesian data
ph = np.load('test_data/slph_im.npy').astype(complex)
ph = (ph - np.min(ph)) / (np.max(ph)-np.min(ph))
cart_ksp = np.load('test_data/slph_cart_ksp.npy')


# Non-Cartesian data

ktraj = np.load('test_data/ktraj_noncart.npy')# /80
ktraj_sc = math.pi / abs(np.max(ktraj))
ktraj = ktraj * ktraj_sc
ktraj_dcf = np.load('test_data/ktraj_noncart_dcf.npy').flatten()

noncart_ksp = np.load('test_data/slph_noncart_ksp.npy')
acq_params = {'Npoints': ktraj.shape[0], 'Nshots': ktraj.shape[1], 'N': ph.shape[0], 'dcf': ktraj_dcf}


class TestImageTransformation(unittest.TestCase):
    def test_im2ksp_cart(self):
        ksp = ORC.im2ksp(M=ph, cartesian_opt=1)
        self.assertEqual(ksp.shape, ph.shape) # Dimensions agree
        self.assertEqual(ksp.all(), cart_ksp.all()) # Transformation is correct

    def test_ksp2im_cart(self):
        im = ORC.ksp2im(ksp=cart_ksp, cartesian_opt=1)
        self.assertEqual(im.shape, cart_ksp.shape)  # Dimensions agree
        self.assertEqual(im.all(), ph.all())  # Transformation is correct

    def test_im2ksp_noncart(self):
        nufft_obj = ORC.nufft_init(kt=ktraj, params=acq_params)
        ksp = ORC.im2ksp(M=ph, cartesian_opt=0, NufftObj=nufft_obj, params=acq_params)
        self.assertEqual(ksp.shape, ktraj.shape)

    def test_ksp2im_noncart(self):
        nufft_obj = ORC.nufft_init(kt=ktraj, params=acq_params)
        im = ORC.ksp2im(ksp=noncart_ksp, cartesian_opt=0, NufftObj=nufft_obj, params=acq_params)
        self.assertEqual(im.shape, ph.shape)
        im = (im - np.min(im)) / (np.max(im) - np.min(im))
        self.assertAlmostEqual(im.all(), ph.all())

class TestRaiseErrors(unittest.TestCase):
    def test_cartesian_opt(self):
        with self.assertRaises(ValueError): ORC.im2ksp(M=ph, cartesian_opt=5)
        with self.assertRaises(ValueError): ORC.ksp2im(ksp=cart_ksp, cartesian_opt=100)

    def test_missing_params_Nshots(self):
        params = acq_params
        nufft_obj = ORC.nufft_init(kt=ktraj, params=acq_params)
        del params['Nshots']
        with self.assertRaises(ValueError): ORC.im2ksp(M=ph, cartesian_opt=0, NufftObj=nufft_obj, params=params )

    '''def test_missing_params_Npoints(self):
        params = acq_params
        nufft_obj = ORC.nufft_init(kt=ktraj, params=acq_params)
        del params['Npoints']
        with self.assertRaises(ValueError): ORC.im2ksp(M=ph, cartesian_opt=0, NufftObj=nufft_obj, params=params)'''


if __name__ == "__main__":
    unittest.main()