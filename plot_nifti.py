#!/usr/bin/env python3

# This code takes a nifti file as input and generates a 3D model as output

import SimpleITK as sitk
import vtk
from lookuptable import get_lut_1, get_lut_2


# Get vtk-file from nifti-image/numpy array
def get_vtk(data, voxelsize):
    data = data.astype('uint8')
    bytes_data = data.tobytes()

    imageimport = vtk.vtkImageImport()
    imageimport.CopyImportVoidPointer(bytes_data, len(bytes_data))
    imageimport.SetDataSpacing(voxelsize[0],voxelsize[1],voxelsize[2])
    imageimport.SetDataOrigin(0,0,0)
    imageimport.SetDataScalarType(3) #='VTK_UNSIGNED_CHAR'
    imageimport.SetNumberOfScalarComponents(1)
    data_shape = data.shape
    imageimport.SetWholeExtent(0, data_shape[2] - 1, 0, data_shape[1] - 1, 0, data_shape[0]-1)
    imageimport.SetDataExtentToWholeExtent()

    return imageimport

# Plot the brain
def map_brain_surface(data, intensity, voxelsize, min_val, max_val, colors):
    global count
    print(count)
    count += 1

    imageimport = get_vtk(data, voxelsize)

    # Lookuptable for colors
    if colors=='redyellowwhitegreenblue':
        colortransfer, lut = get_lut_1(min_val, max_val)
    elif colors=='redwhiteblue':
        colortransfer, lut = get_lut_2(min_val, max_val)

    contourFilter = vtk.vtkContourFilter()
    contourFilter.SetInputConnection(imageimport.GetOutputPort())
    contourFilter.SetValue(0, intensity)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetLookupTable(colortransfer)
    mapper.SetInputConnection(contourFilter.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    
    return actor, lut

def render_brain(actor, lut, scalarBar, png_name):
    renderer = vtk.vtkRenderer()
    for a in actor:
        renderer.AddActor(a)

    if scalarbar:
        scalarBar = vtk.vtkScalarBarActor()
        scalarBar.SetLookupTable(lut)
        scalarBar.SetTitle("score")
        scalarBar.SetNumberOfLabels(5)
        scalarBar.SetMaximumNumberOfColors(200)

        renderer.AddActor2D(scalarBar)

    renderer.SetBackground(0,0,0) #black   #(1,1,1)=white

    ## Define the camera position
    # renderer.camera = vtk.vtkCamera()
    # renderer.ResetCamera()
    # camera = renderer.GetActiveCamera()
    # camera.SetThickness(600)
    # camera.SetPosition(150, 450, 250)
    # camera.SetRoll(90)

    # RenderWindow
    renderwindow = vtk.vtkRenderWindow()
    renderwindow.AddRenderer(renderer)
    renderwindow.SetAlphaBitPlanes(1)  # for transparent background in the screenshots

    # Create the RendererWindowInteractor and show the vtk_file
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(renderwindow)    

    renderwindow.SetSize(1000,600)
    renderwindow.Render()

    # Get a screenshot with transparent background
    windowtoifilter = vtk.vtkWindowToImageFilter()
    windowtoifilter.SetInput(renderwindow)
    windowtoifilter.SetInputBufferTypeToRGBA()
    windowtoifilter.Update()

    writer = vtk.vtkPNGWriter()
    png_name = './plots/'+png_name
    writer.SetFileName(png_name)    
    writer.SetInputData(windowtoifilter.GetOutput())

    if save_mode:
        writer.Write()
    else:
        interactor.Start()

def main(filename, min_val, max_val, scalarbar, colors, png_name='Brainplot_1.png'):
    img = sitk.ReadImage(filename) # SimpleITK object
    data = sitk.GetArrayFromImage(img).astype('float32') # array
    
    actor_list = []
    count_intensity = 0
    for intensity in range(min_val,max_val,1):
        if intensity in data:
            data_ = (data == intensity).astype(int)
            data_ = data_*intensity
            data_ = data_[::-1] #mirror
            actor, lut = map_brain_surface(data=data_, intensity=intensity, voxelsize=img.GetSpacing(), min_val=min_val, max_val=max_val, colors=colors)
            actor_list.append(actor)
        else:
            count_intensity += 1
    print('Count of intensities not found in the file: ', count_intensity)

    render_brain(actor_list, lut, scalarBar=scalarbar, png_name=png_name)


#############################
count = 0

############################# Variables #############################

## Define the filename of the input file you want to plot
filename = './masks/claustrum_example.nii.gz'

## Set scalarbar (colorbar) to True or False depending if you want to see a scalarbar in your plot or not.
scalarbar = True
#scalarbar = False

## Define the scalar range in your file. As a limitation, the code works best with a minimal value of zero. Both numbers should be integers.
### Hint: negative scores or floats can be encoded in positive integers, e.g. by (value*100)+100 (or +101) for scores between -1 and 1. 
### Thereby, min_val=((-1)*100)+100=0 and max_val=((1)*100)+100=200. The scalarbar has to be adjusted in a post-processing step.
min_val = 0
max_val = 40

## Choose the colors you want to use for your plot. There are two colorscales available. Feel free to adjust them for your own colorsystem.
colors='redyellowwhitegreenblue'
#colors='redwhiteblue'

## Set save_mode to True if you want to save an automatic screenshot of the plot. Set it to False if you want to see the plot in the 3D interactor window without saving.
#save_mode = True
save_mode = False

#############################


if __name__ == "__main__":
    main(filename=filename, min_val=min_val, max_val=max_val, scalarbar=scalarbar, colors=colors, png_name='Brainplot_nifti.png')