#!/usr/bin/env python3

# This code takes a vtk file as input and generates a 3D model as output

import vtk
from lookuptable import get_lut_1, get_lut_2

# Plot the brain
def map_brain(file_name, min_val, max_val, colors, png_name):
    global count
    print(count)
    count += 1
    # Read the vtk-polydata-file
    reader = vtk.vtkPolyDataReader()
    reader.SetFileName(file_name)
    reader.Update()

    # Get the Lookuptable for colors
    if colors=='redyellowwhitegreenblue':
        colortransfer, lut = get_lut_1(min_val, max_val)
    elif colors=='redwhiteblue':
        colortransfer, lut = get_lut_2(min_val, max_val)

    # Create the mapper
    mapper = vtk.vtkDataSetMapper()
    mapper.SetInputConnection(reader.GetOutputPort())
    mapper.SetLookupTable(lut)
    mapper.SetScalarRange(0, lut.GetNumberOfColors())

    # Actor
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    render_brain(actor, lut, png_name)

# Render the brain and start an interactive window or make a screenshot of the plot
def render_brain(actor, lut, png_name):
    # Create a scalar bar
    if scalarbar:
        scalarBar = vtk.vtkScalarBarActor()
        scalarBar.SetLookupTable(lut)
        scalarBar.SetTitle("score")
        scalarBar.SetNumberOfLabels(5)
        scalarBar.SetMaximumNumberOfColors(200)

    # Renderer
    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
    if scalarbar:
        renderer.AddActor2D(scalarBar)
    renderer.SetBackground(0,0,0) #(0,0,0)=black   #(1,1,1)=white

    # RenderWindow
    renderwindow = vtk.vtkRenderWindow()
    renderwindow.AddRenderer(renderer)
    renderwindow.SetAlphaBitPlanes(1)  # for transparent background in the screenshots

    # Create the RendererWindowInteractor and show the vtk_file
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(renderwindow)

    ## To define the camera position
    # renderer.camera = vtk.vtkCamera()
    # renderer.ResetCamera()
    # camera = renderer.GetActiveCamera()
    # camera.SetThickness(600)
    # camera.SetPosition(50, 150, 150)
    # camera.SetRoll(-90)

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



#############################
count = 0

############################# Variables #############################

## Define the filename of the input file you want to plot
filename = './masks/claustrum_example.vtk'

## Set scalarbar (colorbar) to True or False depending if you want to see a scalarbar on your figure or not.
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

## Set save_mode to True if you want to save an automatic screenshot of the figure. Set it to False if you want to see the image in the 3D interactor without saving.
#save_mode = True
save_mode = False

#############################


if __name__ == "__main__":
    map_brain(file_name=filename, min_val=min_val, max_val=max_val, colors=colors, png_name='Brainplot_vtk.png')