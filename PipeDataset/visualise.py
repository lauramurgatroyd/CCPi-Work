from ccpi.viewer.iviewer import iviewer
from ccpi.viewer.utils.hdf5_io import HDF5Reader
from ccpi.viewer.utils.conversion import cilHDF5ResampleReader
import vtk


if __name__ == "__main__":
    single_slice = False
    if single_slice:
        reader = HDF5Reader()
        reader.SetFileName(r"D:\rawdata\pco1-105566.hdf")
        reader.SetDatasetName("entry/data/data")
        reader.Update()
    else:
        reader = cilHDF5ResampleReader()
        reader.SetFileName(r"D:\rawdata\pco1-105579.hdf")
        reader.SetDatasetName("entry/data/data")
        reader.SetDatasetName("/entry/instrument/detector/")
        reader.SetIsAcquisitionData(True)
        reader.SetTargetSize(512**3)
        reader.Update()

    err = vtk.vtkFileOutputWindow()
    err.SetFileName("viewer.log")
    vtk.vtkOutputWindow.SetInstance(err)

    image = reader.GetOutput()
    print(image.GetExtent())

    iviewer(reader.GetOutput(), reader.GetOutput())