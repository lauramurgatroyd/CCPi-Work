import h5py
import numpy as np
from cil.io import NXTomoReader, NXTomoWriter
from cil.utilities.display import show2D, show_geometry

# This tells us what datasets are contained in the hdf5 files


def descend_obj(obj, sep='\t'):
    """
    Iterate through groups in a HDF5 file and prints the groups and datasets names and datasets attributes
    """
    if type(obj) in [h5py._hl.group.Group, h5py._hl.files.File]:
        for key in obj.keys():
            print(sep, '-', key, ':', obj[key])
            descend_obj(obj[key], sep=sep+'\t')
    elif type(obj) == h5py._hl.dataset.Dataset:
        for key in obj.attrs.keys():
            print(sep+'\t', '-', key, ':', obj.attrs[key])


def h5dump(path, group='/'):
    """
    print HDF5 file metadata

    group: you can give a specific group, defaults to the root group
    """
    print("dump")
    with h5py.File(path, 'r') as f:
        descend_obj(f[group])

filename = r"D:\rawdata\105564.nxs"
#filename = r"D:\rawdata\pco1-105566.hdf"
filename = r"D:\rawdata\pco1-105579.hdf"

h5dump(filename)

# reader = NXTomoReader(file_name=filename)

# data = reader.get_acquisition_data()
# flat = reader.load_flat()
# dark = reader.load_dark()

# # writer = NXTomoWriter(data = reader.get_acquisition_data(), file_name=r"D:\Images\EPAC\GeminiImaging2019\cat2-take1-CIL-out3.nxs", dark_fields=dark, flat_fields=flat)

# # writer.write()
# print(data)
# show2D(data, slice_list=[('angle',1), ('angle',50), ('angle',100)], fix_range=(200,1000))
