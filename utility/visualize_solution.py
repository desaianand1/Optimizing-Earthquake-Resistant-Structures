import pychrono.core as chrono
import pychrono.irrlicht as chronoirr
import settings as set
import re
import csv
import os

# Set trial and file to read and show solution for
trial = 1
file = str(set.EXP_NAME) + '_' + str(set.FITNESS_FUNCTION)
folder = ''
parent_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Set whether or not to show the shaking table
showShakingTable = False
# Get the best Tower from the selected CSV file
traits = []
with open(parent_path + '/data/' + folder + file + '_best_trait_' + str(trial) + '.csv', newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    # next(csvfile)
    for row in reversed(list(csvreader)):
        for char in row:
            matches = re.findall("[+-]?\d+\.\d+", char)
            traits.append(matches)
        break
    print(*traits, sep='\n')

# Get the fitness for this tower:
fitness = ""
with open(parent_path + '/data/' + folder + file + '_trial_' + str(trial) + '.csv', newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    # next(csvfile)
    for row in reversed(list(csvreader)):
        fitness = row[-1]
        break

print(fitness)

chrono.SetChronoDataPath(set.DATAPATH)

my_system = chrono.ChSystemNSC()

# Set the default outward/inward shape margins for collision detection,
# this is especially important for very large or very small objects.
chrono.ChCollisionModel.SetDefaultSuggestedEnvelope(0.001)
chrono.ChCollisionModel.SetDefaultSuggestedMargin(0.001)

# Maybe you want to change some settings for the solver. For example you
# might want to use SetMaxItersSolverSpeed to set the number of iterations
# per timestep, etc.

# my_system.SetSolverType(chrono.ChSolver.Type_BARZILAIBORWEIN) # precise, more slow
my_system.SetMaxItersSolverSpeed(70)

rollfrict_param = 0.5 / 10.0 * 0.05
# Create a contact material (surface property)to share between all objects.
# The rolling and spinning parameters are optional - if enabled they double
# the computational time.
brick_material = chrono.ChMaterialSurfaceNSC()
brick_material.SetFriction(0.5)
brick_material.SetDampingF(0.2)
brick_material.SetCompliance(0.0000001)
brick_material.SetComplianceT(0.0000001)
brick_material.SetRollingFriction(rollfrict_param)
brick_material.SetSpinningFriction(0.00000001)
brick_material.SetComplianceRolling(0.0000001)
brick_material.SetComplianceSpinning(0.0000001)

# Create the set of bricks in a vertical stack, along Y axis
brick_bodies = []
brick_shapes = []
current_y = 0

for block_index in range(0, 4):
    size_brick_x = float(traits[block_index][0])
    size_brick_z = float(traits[block_index][1])
    size_brick_y = float(traits[block_index][2])
    pos_brick_x = size_brick_x / 2 * -1
    pos_brick_z = size_brick_z / 2 * -1

    mass_brick = set.BLOCK_MASS
    # inertia_brick = 2 / 5 * (pow(size_brick_x, 2)) * mass_brick  # to do: compute separate xx,yy,zz inertias
    inertia_brick_xx = 1 / 12 * mass_brick * (pow(size_brick_z, 2) + pow(size_brick_y, 2))
    inertia_brick_yy = 1 / 12 * mass_brick * (pow(size_brick_x, 2) + pow(size_brick_z, 2))
    inertia_brick_zz = 1 / 12 * mass_brick * (pow(size_brick_x, 2) + pow(size_brick_y, 2))
    # create it
    body_brick = chrono.ChBody()
    # set initial position
    body_brick.SetPos(chrono.ChVectorD(0, current_y + 0.5 * size_brick_y, 0))
    current_y += size_brick_y
    # set mass properties
    body_brick.SetMass(mass_brick)
    body_brick.SetInertiaXX(chrono.ChVectorD(inertia_brick_xx, inertia_brick_yy, inertia_brick_zz))
    # set collision surface properties
    body_brick.SetMaterialSurface(brick_material)

    # Collision shape
    body_brick.GetCollisionModel().ClearModel()
    body_brick.GetCollisionModel().AddBox(size_brick_x / 2, size_brick_y / 2,
                                          size_brick_z / 2)  # must set half sizes
    body_brick.GetCollisionModel().BuildModel()
    body_brick.SetCollide(True)

    # Visualization shape, for rendering animation
    body_brick_shape = chrono.ChBoxShape()
    body_brick_shape.GetBoxGeometry().Size = chrono.ChVectorD(size_brick_x / 2, size_brick_y / 2,
                                                              size_brick_z / 2)

    if block_index % 2 == 0:
        body_brick_shape.SetColor(chrono.ChColor(0.65, 0.65, 0.6))  # set gray color only for odd bricks

    body_brick.GetAssets().push_back(body_brick_shape)
    my_system.Add(body_brick)

    brick_bodies.append(body_brick)
    brick_shapes.append(body_brick_shape);
# Create the room floor: a simple fixed rigid body with a collision shape
# and a visualization shape
body_floor = chrono.ChBody()
body_floor.SetBodyFixed(True)
body_floor.SetPos(chrono.ChVectorD(0, -2, 0))
body_floor.SetMaterialSurface(brick_material)

# Collision shape
body_floor.GetCollisionModel().ClearModel()
body_floor.GetCollisionModel().AddBox(3, 1, 3)  # hemi sizes  default: 3,1,3
body_floor.GetCollisionModel().BuildModel()
body_floor.SetCollide(True)

# Visualization shape
body_floor_shape = chrono.ChBoxShape()
body_floor_shape.GetBoxGeometry().Size = chrono.ChVectorD(3, 1, 3)
body_floor.GetAssets().push_back(body_floor_shape)

body_floor_texture = chrono.ChTexture()
# body_floor_texture.SetTextureFilename(chrono.GetChronoDataPath() + 'concrete.jpg')
body_floor.GetAssets().push_back(body_floor_texture)

my_system.Add(body_floor)

# Create the shaking table, as a box
size_table_x = 1
size_table_y = 0.2
size_table_z = 1

body_table = chrono.ChBody()
body_table.SetPos(chrono.ChVectorD(0, -size_table_y / 2, 0))
body_table.SetMaterialSurface(brick_material)

# Collision shape
body_table.GetCollisionModel().ClearModel()
body_table.GetCollisionModel().AddBox(size_table_x / 2, size_table_y / 2, size_table_z / 2)  # hemi sizes
body_table.GetCollisionModel().BuildModel()
body_table.SetCollide(True)

# Visualization shape
body_table_shape = chrono.ChBoxShape()
body_table_shape.GetBoxGeometry().Size = chrono.ChVectorD(size_table_x / 2, size_table_y / 2, size_table_z / 2)
body_table_shape.SetColor(chrono.ChColor(0.4, 0.4, 0.5))
body_table.GetAssets().push_back(body_table_shape)

body_table_texture = chrono.ChTexture()
# body_table_texture.SetTextureFilename(chrono.GetChronoDataPath() + 'concrete.jpg')
body_table.GetAssets().push_back(body_table_texture)

my_system.Add(body_table)

# Makes the table shake
link_shaker = chrono.ChLinkLockLock()
link_shaker.Initialize(body_table, body_floor, chrono.CSYSNORM)
my_system.Add(link_shaker)

if showShakingTable:
    # ..create the function for imposed x horizontal motion, etc.
    mfunY = chrono.ChFunction_Sine(0, set.TABLE_FREQ, set.TABLE_AMP)  # phase, frequency, amplitude
    link_shaker.SetMotion_Y(mfunY)

    # ..create the function for imposed y vertical motion, etc.
    mfunZ = chrono.ChFunction_Sine(0, 1.5, 0.12)  # phase, frequency, amplitude
    link_shaker.SetMotion_Z(mfunZ)

# Note that you could use other types of ChFunction_ objects, or create
# your custom function by class inheritance (see demo_python.py), or also
# set a function for table rotation , etc.

# ---------------------------------------------------------------------
#
#  Create an Irrlicht application to visualize the system

window_name = "Tower Trial: " + str(trial) + " Fitness: " + str(fitness)
app = chronoirr.ChIrrApp(my_system, window_name, chronoirr.dimension2du(set.SCREEN_WIDTH, set.SCREEN_HEIGHT))
# app = chronoirr.ChIrrApp(my_system)
app.AddTypicalSky()
app.AddTypicalLogo(chrono.GetChronoDataPath() + 'logo_pychrono_alpha.png')
app.AddTypicalCamera(chronoirr.vector3df(set.CAMERA_X, set.CAMERA_Y, set.CAMERA_Z))

app.AddLightWithShadow(chronoirr.vector3df(2, 4, 2),  # point
                       chronoirr.vector3df(0, 0, 0),  # aimpoint
                       9,  # radius (power)
                       1, 9,  # near, far
                       30)

app.AssetBindAll()

# ==IMPORTANT!== Use this function for 'converting' into Irrlicht meshes the assets
# that you added to the bodies into 3D shapes, they can be visualized by Irrlicht!

app.AssetUpdateAll();

# If you want to show shadows because you used "AddLightWithShadow()'
# you must remember this:
app.AddShadowAll();

# ---------------------------------------------------------------------
#
#  Run the simulation
#

app.SetTimestep(set.SPEED)
app.SetTryRealtime(True)
app.GetDevice().run()
while my_system.GetChTime() < set.DISPLAY_TIME:
    app.BeginScene()
    app.DrawAll()
    for substep in range(0, 5):
        app.DoStep()
    app.EndScene()

# time = my_system.GetChTime()
app.GetDevice().closeDevice()
