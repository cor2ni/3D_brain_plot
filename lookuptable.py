#!/usr/bin/env python3

# Here is the code for two LookupTables

import vtk
import colorsys

# LookupTable: dark red - orange - white - light green - dark blue
# The input are the minimal and maximal values of the scalar range.
def get_lut_1(min_val, max_val): #e.g. (0, 100)
    dif = max_val - min_val
    lut = vtk.vtkLookupTable()
    lut.SetNumberOfTableValues(max_val)
    lut.SetTableRange(min_val, max_val)
    lut.Build()
    colortransfer = vtk.vtkColorTransferFunction()
    minscalar = int(min_val + 0.05*dif)
    maxscalar = int(max_val - 0.05*dif)
    limitmin = int(min_val + 0.48*dif)
    limitmax = int(max_val - 0.48*dif)
    step = 1

    for i in range(minscalar, limitmin, step):
        hmin=((i-minscalar)/(limitmin-minscalar))*(43/255)    #0 #red   #43/255 #yellow
        smin=1
        l=(((i-minscalar)/(limitmin-minscalar))*0.85)+0.15
        r, g, b = colorsys.hls_to_rgb(h=hmin, s=smin, l=l)
        lut.SetTableValue(i, r, g, b, 1)
        colortransfer.AddRGBPoint(i, r, g, b)

    for i in range(limitmax, maxscalar, step): 
        blue=170/255
        green=85/255
        hmax=(((i-limitmax)/(maxscalar-limitmax))*(blue-green))+green    #85/255 #green    #170/255 #blue
        smax=1
        l=((1-(i-limitmax)/(maxscalar-limitmax))*0.85)+0.15
        r, g, b = colorsys.hls_to_rgb(h=hmax, s=smax, l=l)
        lut.SetTableValue(i, r, g, b, 1)
        colortransfer.AddRGBPoint(i, r, g, b)
    for i in range(limitmin, limitmax, step):
        lut.SetTableValue(i, 1, 1, 1, 1)
        colortransfer.AddRGBPoint(i, 1, 1, 1)
    for i in range(min_val, minscalar, step):
        r, g, b = colorsys.hls_to_rgb(h=0, s=smin, l=0.15)
        lut.SetTableValue(i, r, g, b, 1)
        colortransfer.AddRGBPoint(i, r, g, b)
    for i in range(maxscalar, max_val, step):
        r, g, b = colorsys.hls_to_rgb(h=hmax, s=smax, l=0.15)
        lut.SetTableValue(i, r, g, b, 1)
        colortransfer.AddRGBPoint(i, r, g, b)

    return colortransfer, lut

#LookupTable: dark red - light red - white - light green - dark green
def get_lut_2(min_val, max_val):
    dif = max_val - min_val
    lut = vtk.vtkLookupTable()
    lut.SetNumberOfTableValues(max_val)
    lut.SetTableRange(min_val, max_val)
    lut.Build()
    colortransfer = vtk.vtkColorTransferFunction()
    minscalar = int(min_val + 0.05*dif)
    maxscalar = int(max_val - 0.05*dif)
    limitmin = int(min_val + 0.48*dif)
    limitmax = int(max_val - 0.48*dif)
    step = 1
    for i in range(minscalar, limitmin, step):
        hmin=0 #red
        smin=1
        l=(((i-minscalar)/(limitmin-minscalar))*0.85)+0.15
        r, g, b = colorsys.hls_to_rgb(h=hmin, s=smin, l=l)
        lut.SetTableValue(i, r, g, b, 1)
        colortransfer.AddRGBPoint(i, r, g, b)
    for i in range(limitmax, maxscalar, step): 
        hmax=170/255   #85/255 #green    #170/255 #blue
        smax=1
        l=((1-(i-limitmax)/(maxscalar-limitmax))*0.85)+0.15
        r, g, b = colorsys.hls_to_rgb(h=hmax, s=smax, l=l)
        lut.SetTableValue(i, r, g, b, 1)
        colortransfer.AddRGBPoint(i, r, g, b)
    for i in range(limitmin, limitmax, step):
        lut.SetTableValue(i, 1, 1, 1, 1)
        colortransfer.AddRGBPoint(i, 1, 1, 1)
    for i in range(min_val, minscalar, step):
        r, g, b = colorsys.hls_to_rgb(h=hmin, s=smin, l=0.15)
        colortransfer.AddRGBPoint(i, r, g, b)
        lut.SetTableValue(i, r, g, b, 1)
    for i in range(maxscalar, max_val, step):
        r, g, b = colorsys.hls_to_rgb(h=hmax, s=smax, l=0.15)
        lut.SetTableValue(i, r, g, b, 1)
        colortransfer.AddRGBPoint(i, r, g, b)

    return colortransfer, lut