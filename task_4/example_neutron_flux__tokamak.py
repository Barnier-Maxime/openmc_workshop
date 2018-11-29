#!/usr/bin/env python3

"""example_isotope_plot.py: plots few 2D views of a simple tokamak geometry with neutron flux."""

__author__      = "Jonathan Shimwell"

import openmc
import matplotlib.pyplot as plt
import os




#MATERIALS#

copper = openmc.Material(name='Copper')
copper.set_density('g/cm3', 8.5)
copper.add_element('Cu', 1.0)
mats.append(copper)

eurofer = openmc.Material(name='EUROFER97')
eurofer.set_density('g/cm3', 7.75)
eurofer.add_element('Fe', 89.067, percent_type='wo')
eurofer.add_element('C', 0.11, percent_type='wo')
eurofer.add_element('Mn', 0.4, percent_type='wo')
eurofer.add_element('Cr', 9.0, percent_type='wo')
eurofer.add_element('Ta', 0.12, percent_type='wo')
eurofer.add_element('W', 1.1, percent_type='wo')
eurofer.add_element('N', 0.003, percent_type='wo')
eurofer.add_element('V', 0.2, percent_type='wo')
mats.append(eurofer)

breeder_material = openmc.Material(1, "PbLi") #Pb84.2Li15.8 with 90% enrichment of Li6
enrichment_fraction = 0.1
breeder_material.add_element('Pb', 84.2,'ao')
breeder_material.add_nuclide('Li6', enrichment_fraction*15.8, 'ao')
breeder_material.add_nuclide('Li7', (1.0-enrichment_fraction)*15.8, 'ao')
# breeder_material.set_density('atom/b-cm',3.2720171e-2)
breeder_material.set_density('g/cm3',11.0)

mats = openmc.Materials([breeder_material, copper, eurofer])



#GEOMETRY#

central_sol_surface = openmc.ZCylinder(R=100)
central_shield_outer_surface = openmc.ZCylinder(R=110)
vessel_inner = openmc.Sphere(R=500)
first_wall_outer_surface = openmc.Sphere(R=510)
breeder_blanket_outer_surface = openmc.Sphere(R=610)


central_sol_region = -central_sol_surface & -vessel_inner
central_sol_cell = openmc.Cell(region=central_sol_region) 
central_sol_cell.fill = copper

central_shield_region = +central_sol_surface & -central_shield_outer_surface & -vessel_inner
central_shield_cell = openmc.Cell(region=central_shield_region) 
central_shield_cell.fill = eurofer

first_wall_region = -first_wall_outer_surface & +vessel_inner
first_wall_cell = openmc.Cell(region=first_wall_region) 
first_wall_cell.fill = eurofer

breeder_blanket_region = +first_wall_outer_surface & -breeder_blanket_outer_surface
breeder_blanket_cell = openmc.Cell(region=breeder_blanket_region) 
breeder_blanket_cell.fill = eurofer

universe = openmc.Universe(cells=[central_sol_cell,central_shield_cell,first_wall_cell, breeder_blanket_cell])






# OpenMC simulation parameters
batches = 1
inactive = 10
particles = 5000

# Instantiate a Settings object
sett = openmc.Settings()
sett.batches = batches
sett.inactive = inactive
sett.particles = particles
sett.run_mode = 'fixed source'

# Create an initial uniform spatial source distribution over fissionable zones
source = openmc.Source()
source.space = openmc.stats.Point((0,0,0))
source.angle = openmc.stats.Isotropic()
source.energy = openmc.stats.Discrete([14e6], [1])
sett.source = source


tallies = openmc.Tallies()


# Create mesh which will be used for tally
mesh = openmc.Mesh()
mesh_height=200
mesh_width = mesh_height
mesh.dimension = [mesh_width, mesh_height]
mesh.lower_left = [-200, -200]
mesh.upper_right = [200, 200]

# Create mesh filter for tally
mesh_filter = openmc.MeshFilter(mesh)
# Create mesh tally to score flux and tritium production rate
mesh_tally = openmc.Tally(1,name='tallies_on_mesh')
mesh_tally.filters = [mesh_filter]
mesh_tally.scores = ['flux','(n,t)']
tallies.append(mesh_tally)



cell_filter = openmc.CellFilter(breeder_blanket_cell)
tbr_tally = openmc.Tally(2,name='TBR')
tbr_tally.filters = [cell_filter]
tbr_tally.scores = ['205']
tallies.append(tbr_tally)

try:
    os.system('rm statepoint.'+str(batches)+'.h5')
except:
    pass

# Run OpenMC! using the python objects instead of the xml files
model = openmc.model.Model(geom, mats, sett, tallies)
model.run()
#openmc.run()

sp = openmc.StatePoint('statepoint.'+str(batches)+'.h5')
#sp = openmc.StatePoint('statepoint.100.h5')

tbr_tally_result = sp.get_tally(name='TBR')
print(tbr_tally_result)
print(tbr_tally_result.sum)



flux_tally = sp.get_tally(scores=['flux'])
flux_slice = flux_tally.get_slice(scores=['flux'])
#flux_slice.std_dev.shape = (mesh_width, mesh_height)
flux_slice.mean.shape = (mesh_width, mesh_height)

fig = plt.subplot()
plt.show(fig.imshow(flux_slice.mean))

print()
absorption_tally = sp.get_tally(scores=['absorption'])
absorption_slice = absorption_tally.get_slice(scores=['absorption'])
#absorption_slice.std_dev.shape = (mesh_width, mesh_height)
absorption_slice.mean.shape = (mesh_width, mesh_height)
#absorption_slice.mean.shape = (100,100)

fig = plt.subplot()
print(fig.imshow(absorption_slice.mean))
plt.show(fig.imshow(absorption_slice.mean))

plt.show(universe.plot(width=(400,400),basis='xz'))
plt.show(universe.plot(width=(400,400),basis='xy'))
plt.show(universe.plot(width=(400,400),basis='yz'))