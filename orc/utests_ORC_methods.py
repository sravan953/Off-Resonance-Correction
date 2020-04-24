import unittest

import scipy.io as sio
import numpy as np

import ORC

# Inputs
raw_data = sio.loadmat('test_data/acrph_noncart_ksp')['dat']

ktraj = np.load('test_data/ktraj_noncart.npy')/80
ktraj_dcf = np.load('test_data/ktraj_noncart_dcf.npy').flatten()
t_ro = ktraj.shape[0] * 10e-6
T = np.linspace(4.6e-3, 4.6e-3 + t_ro, ktraj.shape[0]).reshape((ktraj.shape[0], 1))

field_map = np.load('test_data/acrph_df.npy')
acq_params = {'Npoints': ktraj.shape[0], 'Nshots': ktraj.shape[1], 'N': field_map.shape[0], 'dcf': ktraj_dcf, 't_vector': T, 't_readout': t_ro}

print('ok')

class TestfscPR(unittest.TestCase):
    def test_fsCPR_given_rawData(self):
        or_corr_im = ORC.fs_CPR(dataIn=raw_data[:,:,0],dataInType='raw',kt=ktraj,df=field_map,Lx=1,params=acq_params)
        self.assertEqual(or_corr_im.shape, field_map.shape[:-1]) # Dimensions agree

    def test_fsCPR_given_im(self):
        or_corr_im = ORC.fs_CPR(dataIn=raw_data[:,:,0],dataInType='raw',kt=ktraj,df=field_map,Lx=1,params=acq_params)
        or_corr_im2 = ORC.fs_CPR(dataIn=or_corr_im,dataInType='im',kt=ktraj,df=field_map,Lx=1,params=acq_params)
        self.assertEqual(or_corr_im2.shape, field_map.shape[:-1])
        self.assertEqual(or_corr_im2.all(), or_corr_im.all())

    def test_fsCPR_wrongtype(self):
        with self.assertRaises(ValueError): ORC.fs_CPR(dataIn=raw_data[:, :, 0], dataInType='im', kt=ktraj, df=field_map, Lx=1, params=acq_params)
        or_corr_im = ORC.fs_CPR(dataIn=raw_data[:, :, 0], dataInType='raw', kt=ktraj, df=field_map, Lx=1,
                                params=acq_params)
        with self.assertRaises(ValueError): ORC.fs_CPR(dataIn=or_corr_im, dataInType='raw', kt=ktraj,
                                                       df=field_map, Lx=1, params=acq_params)
        with self.assertRaises(ValueError): ORC.fs_CPR(dataIn=raw_data[:, :, 0], dataInType='other', kt=ktraj,
                                                       df=field_map, Lx=1, params=acq_params)

class TestMFI(unittest.TestCase):
    def test_MFI_given_rawData(self):
        or_corr_im = ORC.MFI(dataIn=raw_data[:, :, 0], dataInType='raw', kt=ktraj, df=field_map[:,:,0], Lx=1,
                                params=acq_params)
        self.assertEqual(or_corr_im.shape, field_map.shape[:-1])  # Dimensions agree

    def test_MFI_given_im(self):
        or_corr_im = ORC.MFI(dataIn=raw_data[:, :, 0], dataInType='raw', kt=ktraj, df=field_map[:,:,0], Lx=1,
                                params=acq_params)
        or_corr_im2 = ORC.MFI(dataIn=or_corr_im, dataInType='im', kt=ktraj, df=field_map[:,:,0], Lx=1, params=acq_params)
        self.assertEqual(or_corr_im2.shape, field_map.shape[:-1])
        self.assertEqual(or_corr_im2.all(), or_corr_im.all())

    def test_MFI_wrongtype(self):
        with self.assertRaises(ValueError): ORC.MFI(dataIn=raw_data[:, :, 0], dataInType='im', kt=ktraj,
                                                       df=field_map, Lx=1, params=acq_params)
        or_corr_im = ORC.MFI(dataIn=raw_data[:, :, 0], dataInType='raw', kt=ktraj, df=field_map[:,:,0], Lx=1,
                                params=acq_params)
        with self.assertRaises(ValueError): ORC.MFI(dataIn=or_corr_im, dataInType='raw', kt=ktraj,
                                                       df=field_map, Lx=1, params=acq_params)
        with self.assertRaises(ValueError): ORC.MFI(dataIn=raw_data[:, :, 0], dataInType='other', kt=ktraj,
                                                       df=field_map, Lx=1, params=acq_params)
if __name__ == "__main__":
    unittest.main()