import pychrono.core as chrono
import pychrono.irrlicht as chronoirr
import settings

# This file is used to evaluate the candidate's fitness, along with, along with returning its fitness.
# Fitness is calculated in the later parts of run_sim


chrono.SetChronoDataPath(settings.DATAPATH)


# Traits are in the format of [[block_x, block_z, block_y], ..., mass]
def run_sim(traits, trial_num, gen_num, difficulty_level):
    my_system = chrono.ChSystemNSC()

    # Set the default outward/inward shape margins for collision detection
    chrono.ChCollisionModel.SetDefaultSuggestedEnvelope(0.001)
    chrono.ChCollisionModel.SetDefaultSuggestedMargin(0.001)

    # Sets simulation precision
    my_system.SetMaxItersSolverSpeed(70)

    # Create a contact material (surface property)to share between all objects.
    rollfrict_param = 0.5 / 10.0 * 0.05
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
    block_bodies = []  # visualizes bodies
    block_shapes = []  # geometry purposes
    current_y = 0

    for block_index in range(0, 4):
        size_brick_x = traits[block_index][0]
        size_brick_z = traits[block_index][1]
        size_brick_y = traits[block_index][2]
        if size_brick_y < settings.MIN_DIMENSIONS_THRESHOLD or size_brick_x < settings.MIN_DIMENSIONS_THRESHOLD or size_brick_z < settings.MIN_DIMENSIONS_THRESHOLD:
            return [-50, traits]

        mass_brick = settings.BLOCK_MASS
        inertia_brick_xx = 1 / 12 * mass_brick * (pow(size_brick_z, 2) + pow(size_brick_y, 2))
        inertia_brick_yy = 1 / 12 * mass_brick * (pow(size_brick_x, 2) + pow(size_brick_z, 2))
        inertia_brick_zz = 1 / 12 * mass_brick * (pow(size_brick_x, 2) + pow(size_brick_y, 2))

        body_brick = chrono.ChBody()
        body_brick.SetPos(chrono.ChVectorD(0, current_y + 0.5 * size_brick_y, 0))  # set initial position
        current_y += size_brick_y  # set tower block positions

        # setting mass properties
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

        block_bodies.append(body_brick)
        block_shapes.append(body_brick_shape);
    # Create the room floor
    body_floor = chrono.ChBody()
    body_floor.SetBodyFixed(True)
    body_floor.SetPos(chrono.ChVectorD(0, -2, 0))
    body_floor.SetMaterialSurface(brick_material)

    # Floor's collision shape
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
    # link_shaker.SetMotion_X()
    link_shaker.Initialize(body_table, body_floor, chrono.CSYSNORM)
    my_system.Add(link_shaker)

    # ..create the function for imposed y vertical motion, etc.
    mfunY = chrono.ChFunction_Sine(0, settings.TABLE_FREQ_Y, settings.TABLE_AMP_Y)  # phase, frequency, amplitude
    # ..create the function for imposed z horizontal motion, etc.
    mfunZ = chrono.ChFunction_Sine(0, settings.TABLE_FREQ_Z, settings.TABLE_AMP_Z)  # phase, frequency, amplitude
    # ..create the function for imposed x horizontal motion, etc.
    mfunX = chrono.ChFunction_Sine(2, 0, 0)  # phase, frequency, amplitude
    print("Sim env_level " + str(difficulty_level))
    if difficulty_level == settings.SHAKE_IN_X_AXIS_LEVEL:
        mfunX = chrono.ChFunction_Sine(2, settings.TABLE_FREQ_X, settings.TABLE_AMP_X)  # phase, frequency, amplitude
    elif difficulty_level >= settings.SHAKE_IN_X_AND_Z_AXIS_LEVEL:
        increment = 0.25 * difficulty_level
        mfunX = chrono.ChFunction_Sine(2, settings.TABLE_FREQ_X + increment, settings.TABLE_AMP_X)  # phase, frequency, amplitude
        mfunZ = chrono.ChFunction_Sine(0, settings.TABLE_FREQ_Z + increment, settings.TABLE_AMP_Z)  # phase, frequency, amplitude

    link_shaker.SetMotion_Y(mfunY)
    link_shaker.SetMotion_Z(mfunZ)
    link_shaker.SetMotion_X(mfunX)

    # ---------------------------------------------------------------------
    #
    #  Create an Irrlicht application to visualize the system

    window_name = "Tower Trial: " + str(trial_num) + " Gen: " + str(gen_num)
    if trial_num == -1:
        window_name = "Initializing Population..."
    app = chronoirr.ChIrrApp(my_system, window_name, chronoirr.dimension2du(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    app.AddTypicalSky()
    app.AddTypicalLogo(chrono.GetChronoDataPath() + 'logo_pychrono_alpha.png')
    app.AddTypicalCamera(chronoirr.vector3df(settings.CAMERA_X, settings.CAMERA_Y, settings.CAMERA_Z))

    app.AddLightWithShadow(chronoirr.vector3df(2, 4, 2),  # point
                           chronoirr.vector3df(0, 0, 0),  # aimpoint
                           9,  # radius (power)
                           1, 9,  # near, far
                           30)

    # Committing visualization
    app.AssetBindAll()
    app.AssetUpdateAll();
    app.AddShadowAll();

    # ---------------------------------------------------------------------
    #
    #  Run the simulation. This is where all of the constraints are set
    #

    app.SetTimestep(settings.SPEED)
    app.SetTryRealtime(True)
    app.GetDevice().run()

    fitness = 0
    brick1_init = block_bodies[0].GetPos().y
    brick2_init = block_bodies[1].GetPos().y
    brick3_init = block_bodies[2].GetPos().y
    brick4_init = block_bodies[3].GetPos().y  # Highest
    while True:
        brick1_curr_height = block_bodies[0].GetPos().y
        brick2_curr_height = block_bodies[1].GetPos().y
        brick3_curr_height = block_bodies[2].GetPos().y
        brick4_curr_height = block_bodies[3].GetPos().y  # Highest

        # Break conditions
        if my_system.GetChTime() > settings.SIMULATION_RUNTIME:
            break
        if my_system.GetChTime() > settings.SIMULATION_RUNTIME / 2:
            mfunX = chrono.ChFunction_Sine(2, 0, 0)
            mfunZ = chrono.ChFunction_Sine(2, 0, 0)
            link_shaker.SetMotion_Z(mfunZ)
            link_shaker.SetMotion_X(mfunX)

        # If the blocks fall out of line
        if brick1_init - brick1_curr_height > settings.CANCEL_SIM_THRESHOLD or \
                brick2_init - brick2_curr_height > settings.CANCEL_SIM_THRESHOLD or \
                brick3_init - brick3_curr_height > settings.CANCEL_SIM_THRESHOLD or \
                brick4_init - brick4_curr_height > settings.CANCEL_SIM_THRESHOLD:
            break
        # Record fitness every 1/1000 of the runtime
        if 0.01 > my_system.GetChTime() % ((1 / 1000) * settings.SIMULATION_RUNTIME) > 0:
            if settings.FITNESS_FUNCTION == settings.Fitness.SumLengths:  # Sum of size_y
                fitness += block_shapes[0].GetBoxGeometry().GetLengths().y + \
                           block_shapes[1].GetBoxGeometry().GetLengths().y + \
                           block_shapes[2].GetBoxGeometry().GetLengths().y + \
                           block_shapes[3].GetBoxGeometry().GetLengths().y
            elif settings.FITNESS_FUNCTION == settings.Fitness.MaxPosition:  # Max of y positions
                fitness += max(block_bodies[0].GetPos().y,
                               block_bodies[1].GetPos().y,
                               block_bodies[2].GetPos().y,
                               block_bodies[3].GetPos().y)
            elif settings.FITNESS_FUNCTION == settings.Fitness.MaxPositionSumLengths:  # Max * sum of sizes
                fitness += max(block_bodies[0].GetPos().y,
                               block_bodies[1].GetPos().y,
                               block_bodies[2].GetPos().y,
                               block_bodies[3].GetPos().y) * \
                           block_shapes[0].GetBoxGeometry().GetLengths().y + \
                           block_shapes[1].GetBoxGeometry().GetLengths().y + \
                           block_shapes[2].GetBoxGeometry().GetLengths().y + \
                           block_shapes[3].GetBoxGeometry().GetLengths().y
        app.BeginScene()
        app.DrawAll()
        for substep in range(0, 5):
            app.DoStep()
        app.EndScene()

    app.GetDevice().closeDevice()
    print("Fitness: " + str(fitness) + " Gen: " + str(gen_num))
    return [fitness, traits]
