#!/usr/bin/env python3

"""example_isotope_plot.py: plots few 2D views of a simple tokamak geometry ."""

__author__      = "Jonathan Shimwell"

import openmc
import matplotlib.pyplot as plt
import os

mats = openmc.Materials()

natural_lead = openmc.Material(1, "natural_lead")
natural_lead.add_element('Pb', 1,'ao')
mats.append(natural_lead)

natural_copper = openmc.Material(2, "natural_copper") #hint this is an example material you will need another one called natural_tungsten ,density is 19.3
natural_copper.add_element('Cu', 1,'ao')
natural_copper.set_density('g/cm3', 8.96)
mats.append(natural_copper)


shield_material = openmc.Material(3, "mixed_tungsten_water")
shield_material.add_element('W', 0.9, 'ao')
shield_material.add_element('Cu', 0.1, 'ao')
mats.append(shield_material)

mats.export_to_xml()


#example surfaces

surface_sph1 = openmc.Sphere(R=500) #hint, change the radius of this shpere to 500
surface_sph2 = openmc.Sphere(R=600) #hint, change the radius of this shpere to 500+100
surface_sph3=openmc.Sphere(R=480)
surface_cy=openmc.ZCylinder(r=100)
surface_up_zp=openmc.ZPlane(z0=600)
surface_low_zp=openmc.ZPlane(z0=-600)
surface_cy_2=openmc.ZCylinder(r=140)

volume_sph1 = +surface_sph1 & -surface_sph2 # above (+) surface_sph and below (-) surface_sph2
capped_cy= -surface_cy & -surface_up_zp & +surface_low_zp
first_wall= -surface_sph1 & +surface_sph3
shield= -surface_cy_2 & +surface_cy & -surface_up_zp & +surface_low_zp

#hint, add cylindical surfaces here using https://openmc.readthedocs.io/en/stable/usersguide/geometry.html#surfaces-and-regions


#hint, this is an example cell, by default it is filled with a vacuum
cell_1 = openmc.Cell(region=capped_cy)
cell_1.fill = natural_copper #assigning a material to a cell
cell_2 = openmc.Cell(region=first_wall)
cell_2.fill = shield_material
cell_3 = openmc.Cell(region=shield)
cell_3.fill = shield_material
cell_4 = openmc.Cell(region=volume_sph1)
cell_4.fill = natural_lead



#add more cells here

universe = openmc.Universe(cells=[cell_1, cell_2, cell_3, cell_4]) #this list will need to include the new cell



geom = openmc.Geometry(universe)

geom.export_to_xml()

vox_plot = openmc.Plot()
vox_plot.type = 'voxel'
vox_plot.width = (1500., 1500., 1500.)
vox_plot.pixels = (200, 200, 200)
vox_plot.filename = 'plot_3d'
vox_plot.color_by = 'material'
vox_plot.colors = {natural_lead: 'blue'}
plots = openmc.Plots([vox_plot])
plots.export_to_xml()

openmc.plot_geometry()

os.system('openmc-voxel-to-vtk plot_3d.h5 -o plot_3d.vti')
os.system('paraview plot_3d.vti') # or visit might work better
