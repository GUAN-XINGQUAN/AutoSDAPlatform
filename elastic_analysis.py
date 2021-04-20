# This file is used to include all user defined classes and functions
# Developed by GUAN, XINGQUAN @ UCLA in June 2018
# Updated in Sept. 2018

import os
import shutil

from global_variables import ACCIDENTAL_TORSION

# #########################################################################
#              Generate OpenSees model (write .tcl files)                 #
# #########################################################################

class ElasticAnalysis(object):
    """
    This class generates the .tcl files required for elastic analysis. It includes .tcl files for the following modules:
    (1) OpenSees nodes
    (2) boundary condition
    (3) floor constraint
    (4) beam component
    (5) column component
    (6) leaning column spring
    (7) mass
    (8) all recorders
    (9) story drift recorder
    (10) node displacement recorder
    (11) beam force recorder
    (12) column force recorder
    (13) gravity dead load
    (14) gravity live load
    (15) earthquake load
    (16) gravity and earthquake loads combination
    (17) copy baseline .tcl files
    (18) run OpenSees.exe
    """

    def __init__(self, building, for_drift_only=False, for_period_only=False):
        """
        This function is used to call all methods to write .tcl files required for an elastic analysis OpenSees model.
        :param building: a class defined in "building_information.py" file
        :param for_drift_only: a boolean variable.
                               True means we only perform the elastic analysis under GravityEarthquake loads.
                               Otherwise, all load types (dead, live, earthquake) will be considered.
        :param for_period_only: a boolean variable.
                                True means we only perform the eigen value analysis to obtain the period
                                Otherwise, all load types will be considered.
        """
        # Change the working directory to folder where .tcl files will be saved
        if not os.path.exists(building.directory['building elastic model']):
            os.makedirs(building.directory['building elastic model'])
        os.chdir(building.directory['building elastic model'])

        # Call methods to write .tcl files for the building
        self.write_nodes(building)
        self.write_fixities(building)
        self.write_floor_constraint(building)
        self.write_beam(building)
        self.write_column(building)
        self.write_leaning_column_spring(building)
        self.write_mass(building)
        self.write_all_recorder()
        if not for_period_only:
            self.write_story_drift_recorder(building)
            self.write_node_displacement_recorder(building)
            self.write_beam_force_recorder(building)
            self.write_column_force_recorder(building)
            self.write_gravity_dead_load(building)
            self.write_gravity_live_load(building)
            self.write_earthquake_load(building)
            self.write_gravity_earthquake_load(building)
        self.copy_baseline_files(building, for_drift_only, for_period_only)

        # Call method to run OpenSees.exe for performing elastic analysis
        self.run_OpenSees_program()

    def write_nodes(self, building):
        # Create a .tcl file and write the node information
        with open('DefineNodes2DModel.tcl', 'w') as tclfile:
            tclfile.write("# This file will be used to define all nodes \n")  # Introduce the file usage
            tclfile.write("# Units: inch \n\n\n")  # Explain the units

            tclfile.write("# Set bay width and story height \n")
            tclfile.write("set\tBayWidth\t[expr %.2f*12]; \n" % (building.geometry['X bay width']))
            tclfile.write("set\tFirstStory\t[expr %.2f*12]; \n" % (building.geometry['first story height']))
            tclfile.write("set\tTypicalStory\t[expr %.2f*12]; \n\n\n" % (building.geometry['typical story height']))

            # Write the nodes at beam column intersection points
            tclfile.write("# Define nodes at corner of frames \n")
            for i in range(1, building.geometry['number of story']+2):  # i is floor level number
                tclfile.write("# Level %i \n" % i)
                for j in range(1, building.geometry['number of X bay']+2):  # j is column label
                    tclfile.write("node\t%i%i%i" % (j, i, 1))  # Node label
                    tclfile.write("\t[expr %i*$BayWidth]" % (j - 1))  # X coordinate
                    if i <= 2:
                        tclfile.write("\t[expr %i*$FirstStory];" % (i - 1))  # Y coordinate
                        tclfile.write("\t # Column #%i \n" % j)  # Comments to explain the column label
                    else:
                        tclfile.write("\t[expr 1*$FirstStory+%i*$TypicalStory];" % (i - 2))
                        tclfile.write("\t # Column #%i \n" % j)
                tclfile.write("\n")
            tclfile.write("# puts \"Nodes at frame corner defined\" \n\n")

            # Write the nodes for leaning column
            tclfile.write("# Define nodes for leaning column \n")
            for i in range(1, building.geometry['number of story']+2):
                tclfile.write("node\t%i%i" % (building.geometry['number of X bay']+2, i))  # Node label
                tclfile.write("\t[expr %i*$BayWidth]" % (building.geometry['number of X bay']+1))  # X coordinate
                if i <= 2:
                    tclfile.write("\t[expr %i*$FirstStory]; " % (i-1))  # Y coordinate
                    tclfile.write("\t# Level %i\n" % i)  # Comments to explain floor level
                else:
                    tclfile.write("\t[expr 1*$FirstStory+%i*$TypicalStory];" % (i-2))
                    tclfile.write("\t# Level %i\n" % i)
            tclfile.write("\n")
            tclfile.write("# puts \"Nodes for leaning column defined\" \n\n")

            # Write the extra nodes for leaning column springs
            tclfile.write("# Define extra nodes needed to define leaning column springs \n")
            for i in range(2, building.geometry['number of story']+2):
                # The node below floor level
                tclfile.write("node\t%i%i%i" % (building.geometry['number of X bay']+2, i, 2))  # Node label
                tclfile.write("\t[expr %i*$BayWidth]" % (building.geometry['number of X bay'] + 1))  # X coordinate
                tclfile.write("\t[expr 1*$FirstStory+%i*$TypicalStory];" % (i-2))  # Y coordinate
                tclfile.write("\t# Node below floor level %i\n" % i)

                # If it's top story, node above roof is not needed
                # because no leaning column above roof
                if i < building.geometry['number of story']+1:
                    # The node above floor level
                    tclfile.write("node\t%i%i%i" % (building.geometry['number of X bay']+2, i, 4))  # Nodel label
                    tclfile.write("\t[expr %i*$BayWidth]" % (building.geometry['number of X bay']+1))  # X coordinate
                    tclfile.write("\t[expr 1*$FirstStory+%i*$TypicalStory];" % (i-2))  # Y coordinate
                    tclfile.write("\t# Node above floor level %i\n" % i)
                else:
                    pass
            tclfile.write("\n")
            tclfile.write("# puts \"Extra nodes for leaning column springs defined\"\n")

    def write_fixities(self, building):
        # Create a .tcl file to write boundary for the model
        with open('DefineFixities2DModel.tcl', 'w') as tclfile:
            tclfile.write("# This file will be used to define the fixity at all column bases \n\n\n")
            tclfile.write("# Defining fixity at column base \n")
            for j in range(1, building.geometry['number of X bay']+2):
                tclfile.write("fix\t%i%i%i\t1\t1\t1; \n" % (j, 1, 1))
            # Leaning column base
            tclfile.write("fix\t%i%i\t1\t1\t0; \n\n" % (building.geometry['number of X bay']+2, 1))
            tclfile.write("# puts \"All column base fixities have been defined\"")

    def write_floor_constraint(self, building):
        # Create a .tcl file to write floor constrain, i.e., equal DOF
        with open('DefineFloorConstraint2DModel.tcl', 'w') as tclfile:
            tclfile.write("# This file will be used to define floor constraint \n\n")
            tclfile.write("set\tConstrainDOF\t1;\t# Nodes at same floor level have identical lateral displacement \n\n")
            # Constraint starts from floor level 2
            for i in range(2, building.geometry['number of story']+2):
                tclfile.write("# Level %i \n" % i)
                for j in range(2, building.geometry['number of X bay']+2):
                    tclfile.write("equalDOF\t%i%i%i\t%i%i%i\t$ConstrainDOF;" % (1, i, 1, j, i, 1))
                    tclfile.write("\t# Pier 1 to Pier %i\n" % j)
                # Include the leaning column nodes to floor constrain
                tclfile.write("equalDOF\t%i%i%i\t%i%i\t$ConstrainDOF;"
                              % (1, i, 1, building.geometry['number of X bay']+2, i))
                tclfile.write("\t# Pier 1 to Leaning column\n\n")
            tclfile.write("# puts \"Floor constraint defined\"")

    def write_beam(self, building):
        # Create a .tcl file to write beam elements
        with open('DefineBeams2DModel.tcl', 'w') as tclfile:
            tclfile.write("# This file will be used to define beam elements \n\n\n")
            tclfile.write("# Define beam section sizes \n")
            for i in range(2, building.geometry['number of story']+2):
                tclfile.write("set\tBeamLevel%i\t[SectionProperty %s]; \n" % (i, building.member_size['beam'][i-2]))
            tclfile.write("\n\n# Define beams \n")
            for i in range(2, building.geometry['number of story']+2):
                tclfile.write("# Level %i\n" % i)
                # Beam elements in frame
                for j in range(1, building.geometry['number of X bay']+1):
                    tclfile.write("element\telasticBeamColumn")  # elastic beam-column command
                    tclfile.write("\t%i%i%i%i%i%i%i" % (2, j, i, 1, j+1, i, 1))  # Beam element tag
                    tclfile.write("\t%i%i%i" % (j, i, 1))  # Starting node
                    tclfile.write("\t%i%i%i" % (j+1, i, 1))  # Ending node
                    tclfile.write("\t[lindex $BeamLevel%i 2]" % i)  # Area of beam section
                    tclfile.write("\t$Es")  # Young's modulus of steel material
                    tclfile.write("\t[lindex $BeamLevel%i 6]" % i)  # Moment of inertia of beam section
                    tclfile.write("\t$LinearTransf; \n")  # Geometric transformation

                # Beam elements connection frame and leaning column
                tclfile.write("element\ttruss")  # elastic beam-column command
                tclfile.write("\t%i%i%i%i%i%i" % (2, building.geometry['number of X bay']+1, i, 1,
                                                  building.geometry['number of X bay']+2, i))
                tclfile.write("\t%i%i%i" % (building.geometry['number of X bay']+1, i, 1))  # Starting node in frame
                tclfile.write("\t%i%i" % (building.geometry['number of X bay']+2, i))  # Ending node in leaning column
                tclfile.write("\t$AreaRigid\t$TrussMatID; \n")  # Large area and truss element material
                tclfile.write("\n")
            tclfile.write("# puts \"Beams defined\"")

    def write_column(self, building):
        # Create a .tcl file to define all column elements
        with open('DefineColumns2DModel.tcl', 'w') as tclfile:
            tclfile.write("# This file will be used to define columns \n\n\n")

            # Define exterior column sizes
            tclfile.write("# Define exterior column section sizes \n")
            for i in range(1, building.geometry['number of story']+1):
                tclfile.write("set\tExteriorColumnStory%i\t[SectionProperty %s]; \n"
                              % (i, building.member_size['exterior column'][i-1]))

            tclfile.write("\n\n")

            # Define interior column sizes
            tclfile.write("# Define interior column section sizes \n")
            for i in range(1, building.geometry['number of story']+1):
                tclfile.write("set\tInteriorColumnStory%i\t[SectionProperty %s]; \n"
                              % (i, building.member_size['interior column'][i-1]))

            tclfile.write("\n\n# Define columns\n")
            for i in range(1, building.geometry['number of story']+1):
                tclfile.write("# Story %i \n" % i)
                # Columns in frame
                for j in range(1, building.geometry['number of X bay']+2):
                    tclfile.write("element\telasticBeamColumn")  # element command
                    tclfile.write("\t%i%i%i%i%i%i%i" % (3, j, i, 1, j, i+1, 1))  # element tag
                    tclfile.write("\t%i%i%i" % (j, i, 1))  # Starting node
                    tclfile.write("\t%i%i%i" % (j, i+1, 1))  # Ending node
                    # Determine whether the column is interior or exterior column
                    # This would affect the column section size
                    if 1 < j < building.geometry['number of X bay'] + 1:
                        tclfile.write("\t[lindex $InteriorColumnStory%i 2]" % i)  # Area of section
                        tclfile.write("\t$Es")  # Young's modulus of steel material
                        tclfile.write("\t[lindex $InteriorColumnStory%i 6]" % i)  # Moment of inertia of column section
                    else:
                        tclfile.write("\t[lindex $ExteriorColumnStory%i 2]" % i)  # Area of section
                        tclfile.write("\t$Es")
                        tclfile.write("\t[lindex $ExteriorColumnStory%i 6]" % i)  # Moment of inertia of column section
                    tclfile.write("\t$PDeltaTransf; \n")  # Geometric transformation

                # Leaning column elements
                tclfile.write("element\telasticBeamColumn")  # element command
                if i == 1:
                    tclfile.write("\t%i%i%i%i%i%i" % (3, building.geometry['number of X bay']+2, i,
                                                      building.geometry['number of X bay']+2, i+1, 2))
                    tclfile.write("\t%i%i" % (building.geometry['number of X bay']+2, i))
                    tclfile.write("\t%i%i%i" % (building.geometry['number of X bay']+2, i+1, 2))
                else:
                    tclfile.write("\t%i%i%i%i%i%i%i" % (3, building.geometry['number of X bay']+2, i, 4,
                                                        building.geometry['number of X bay']+2, i+1, 2))
                    tclfile.write("\t%i%i%i" % (building.geometry['number of X bay']+2, i, 4))
                    tclfile.write("\t%i%i%i" % (building.geometry['number of X bay']+2, i+1, 2))
                tclfile.write("\t$AreaRigid\t$Es\t$IRigid\t$PDeltaTransf; \n\n")
            tclfile.write("# puts \"Columns defined\"")

    def write_leaning_column_spring(self, building):
        # Create a .tcl file to write all rotational springs for leaning column
        with open('DefineLeaningColumnSpring.tcl', 'w') as tclfile:
            tclfile.write("# This file will be used to define column hinges \n\n")
            for i in range(2, building.geometry['number of story']+2):
                # Spring below the floor level i
                tclfile.write("rotLeaningCol")  # rotLeaningCol is user-defined process in OpenSees
                tclfile.write("\t%i%i%i%i%i" % (building.geometry['number of X bay']+2, i,
                                                building.geometry['number of X bay']+2, i, 2))  # Spring tag
                tclfile.write("\t%i%i" % (building.geometry['number of X bay']+2, i))  # Node at floor level
                tclfile.write("\t%i%i%i;" % (building.geometry['number of X bay']+2, i, 2))  # Node below floor level
                tclfile.write("\t# Spring below floor level %i \n" % i)

                # Spring above floor level i
                # If it's roof, no rotational spring exists above roof
                if i < building.geometry['number of story']+1:
                    tclfile.write("rotLeaningCol")  # rotLeaningCol is user-defined process in OpenSees
                    tclfile.write("\t%i%i%i%i%i" % (building.geometry['number of X bay']+2, i,
                                                    building.geometry['number of X bay'], i, 4))  # Spring tag
                    tclfile.write("\t%i%i" % (building.geometry['number of X bay']+2, i))  # Node at floor level
                    # Node above floor level
                    tclfile.write("\t%i%i%i;" % (building.geometry['number of X bay']+2, i, 4))
                    tclfile.write("\t# Spring above floor level %i \n" % i)
                else:
                    pass
            tclfile.write("\n")
            tclfile.write("# puts \"Leaning column springs defined\"")

    def write_mass(self, building):
        # Create a .tcl file to write nodal mass
        with open('DefineMasses2DModel.tcl', 'w') as tclfile:
            tclfile.write("# This file will be used to define all nodal masses \n\n")

            # Write values for floor weights, tributary mass ratio, and nodal mass
            tclfile.write("# Define floor weights and each nodal mass \n")
            for i in range(2, building.geometry['number of story']+2):
                tclfile.write("set\tFloor%iWeight\t%.2f; \n" % (i, building.gravity_loads['floor weight'][i-2]))
            tclfile.write("set\tFrameTributaryMassRatio\t%s; \n" % (1.0 / building.geometry['number of X LFRS']))
            tclfile.write("set\tTotalNodesPerFloor\t%i; \n" % (building.geometry['number of X bay']+1))
            for i in range(2, building.geometry['number of story']+2):
                tclfile.write("set\tNodalMassFloor%i" % i)
                tclfile.write("\t[expr $Floor%iWeight*$FrameTributaryMassRatio/$TotalNodesPerFloor/$g]; \n" % i)
            tclfile.write("\n\n")

            # Write nodal masses for each floor level
            for i in range(2, building.geometry['number of story']+2):
                tclfile.write("# Level %i \n" % i)
                for j in range(1, building.geometry['number of X bay']+2):
                    tclfile.write("mass\t%i%i%i" % (j, i, 1))  # Nodal mass command and node tag
                    tclfile.write("\t$NodalMassFloor%i" % i)  # Mass along X direction
                    tclfile.write("\t$Negligible\t$Negligible\n")  # Mass along Y and RotZ doesn't matter
                tclfile.write("\n")
            tclfile.write("# puts \"Nodal mass defined\"")  # Write puts command which denotes the ending of the .tcl file

    def write_all_recorder(self):
        # Create a .tcl file to write all recorders for output
        with open('DefineAllRecorders2DModel.tcl', 'w') as tclfile:
            tclfile.write("# This file will be used to define all recorders \n\n\n")  # File explanation
            tclfile.write("# Setting up main folders for different load scenarios\n")
            tclfile.write("set\tbaseDir\t[pwd]\n")  # OpenSees base directory
            tclfile.write("set\tdataDir\t$LoadType\n")  # OpenSees output data folder, based on type of applied load
            tclfile.write("file\tmkdir\t$dataDir\n")  # Create the data folder
            tclfile.write("cd\t$baseDir/$dataDir\n\n")  # Go to data folder

            tclfile.write("# Creating all the sub-folders for different quantities\n")
            tclfile.write("file\tmkdir\tStoryDrifts\n")
            tclfile.write("file\tmkdir\tNodeDisplacements\n")
            tclfile.write("file\tmkdir\tGlobalBeamForces\n")
            tclfile.write("file\tmkdir\tGlobalColumnForces\n\n")

            tclfile.write("# Source all the tcl files that define the output\n")
            tclfile.write("cd\t$baseDir\n")
            tclfile.write("source\tDefineStoryDriftRecorders2DModel.tcl\n\n")

            tclfile.write("cd\t$baseDir\n")
            tclfile.write("source\tDefineNodeDisplacementRecorders2DModel.tcl\n\n")

            tclfile.write("cd\t$baseDir\n")
            tclfile.write("source\tDefineGlobalBeamForceRecorders2DModel.tcl\n\n")

            tclfile.write("cd\t$baseDir\n")
            tclfile.write("source\tDefineGlobalColumnForceRecorders2DModel.tcl\n\n")

            tclfile.write("cd\t$baseDir\n")
            tclfile.write("# puts \"All recorders defined\"")

    def write_story_drift_recorder(self, building):
        # Create a .tcl file to write story drift recorder for output
        with open('DefineStoryDriftRecorders2DModel.tcl', 'w') as tclfile:
            tclfile.write("# Define story drift recorders\n\n\n")
            tclfile.write("cd\t$baseDir/$dataDir/StoryDrifts\n\n")

            # Write the story drift recorder for each story
            for i in range(1, building.geometry['number of story']+1):
                tclfile.write("recorder\tDrift\t-file")
                tclfile.write("\t$baseDir/$dataDir/StoryDrifts/Story%i.out" % i)
                # Always use nodes on column #1 to calculate story drift
                tclfile.write("\t-time\t-iNode\t%i%i%i" % (1, i, 1))  # node at bottom of current story
                tclfile.write("\t-jNode\t%i%i%i" % (1, i+1, 1))  # node at top of current story
                tclfile.write("\t-dof\t1\t-perpDirn\t2; \n")

            # Write the story drift recorder for roof
            tclfile.write("recorder\tDrift\t-file")
            tclfile.write("\t$baseDir/$dataDir/StoryDrifts/Roof.out")
            tclfile.write("\t-time\t-iNode\t%i%i%i" % (1, 1, 1))
            tclfile.write("\t-jNode\t%i%i%i" % (1, building.geometry['number of story']+1, 1))
            tclfile.write("\t-dof\t1\t-perpDirn\t2; \n")

    def write_node_displacement_recorder(self, building):
        # Create a .tcl file to write node displacement recorder for output
        with open('DefineNodeDisplacementRecorders2DModel.tcl', 'w') as tclfile:
            tclfile.write("# Define node displacement recorders\n\n\n")
            tclfile.write("cd\t$baseDir/$dataDir/NodeDisplacements\n\n")
            # Write the node displacement recorder for node at each floor level
            for i in range(1, building.geometry['number of story']+2):
                tclfile.write("recorder\tNode\t-file")
                tclfile.write("\tNodeDisplacementLevel%i.out" % i)
                tclfile.write("\t-time\t-node")
                for j in range(1, building.geometry['number of X bay']+2):
                    tclfile.write("\t%i%i%i" % (j, i, 1))
                tclfile.write("\t-dof\t1\t2\t3\tdisp; \n")

    def write_beam_force_recorder(self, building):
        # Create a .tcl file to write beam force recorder for output
        with open('DefineGlobalBeamForceRecorders2DModel.tcl', 'w') as tclfile:
            tclfile.write("# Define global beam force recorders\n\n\n")
            tclfile.write("cd\t$baseDir/$dataDir/GlobalBeamForces\n\n")

            tclfile.write("# Beam element global force recorders\n")
            for i in range(2, building.geometry['number of story']+2):
                tclfile.write("recorder\tElement\t-file\tGlobalXBeamForcesLevel%i.out" % i)
                tclfile.write("\t-time\t-ele")
                for j in range(1, building.geometry['number of X bay']+1):
                    tclfile.write("\t%i%i%i%i%i%i%i" % (2, j, i, 1, j+1, i, 1))
                tclfile.write("\tforce; \n")

    def write_column_force_recorder(self, building):
        # Create a .tcl file to write column force recorder for output
        with open('DefineGlobalColumnForceRecorders2DModel.tcl', 'w') as tclfile:
            tclfile.write("# Define global column force recorders\n\n\n")
            tclfile.write("cd\t$baseDir/$dataDir/GlobalColumnForces\n\n")

            tclfile.write("# X-Direction frame column element global force recorders\n")
            for i in range(1, building.geometry['number of story']+1):
                tclfile.write("recorder\tElement\t-file\tGlobalColumnForcesStory%i.out" % i)
                tclfile.write("\t-time\t-ele")
                for j in range(1, building.geometry['number of X bay']+2):
                    tclfile.write("\t%i%i%i%i%i%i%i" % (3, j, i, 1, j, i+1, 1))
                tclfile.write("\tforce;\n")

    def write_gravity_dead_load(self, building):
        # Create a .tcl file that writes the gravity dead load on the model
        with open('DefineGravityDeadLoads2DModel.tcl', 'w') as tclfile:
            tclfile.write("# Define gravity dead loads\n\n\n")

            # Assign the beam dead load values
            tclfile.write("# Assign uniform beam dead load values (kip/inch)\n")
            for i in range(2, building.geometry['number of story']+2):
                # Be cautious: convert the unit from lb/ft to kip/inch
                tclfile.write("set\tBeamDeadLoadFloor%i\t%f; \n"
                              % (i, building.gravity_loads['beam dead load'][i-2]*0.001/12))
            tclfile.write("\n")

            # Assign the beam live load values
            tclfile.write("# Assign uniform beam live load values (kip/inch)\n")
            for i in range(2, building.geometry['number of story']+2):
                # Be cautious: convert the unit from lb/ft to kip/inch
                tclfile.write("set\tBeamLiveLoadFloor%i\t%f; \n"
                              % (i, building.gravity_loads['beam live load'][i-2]*0.001/12))
            tclfile.write("\n")

            # Assign the values for point dead load acting on leaning column
            tclfile.write("# Assign point dead load values on leaning column: kip\n")
            for i in range(2, building.geometry['number of story']+2):
                tclfile.write("set\tLeaningColumnDeadLoadFloor%i\t%f; \n"
                              % (i, building.gravity_loads['leaning column dead load'][i-2]))
            tclfile.write("\n")

            # Assign the values for point live load acting on leaning column
            tclfile.write("# Assign point live load values on leaning column (kip)\n")
            for i in range(2, building.geometry['number of story']+2):
                tclfile.write("set\tLeaningColumnLiveLoadFloor%i\t%f; \n"
                              % (i, building.gravity_loads['leaning column live load'][i-2]))
            tclfile.write("\n")

            # Assign the lateral load values caused by earthquake
            # Please note this is used to verify the strength -> use seismic_force_for_strength
            tclfile.write("# Assign lateral load values caused by earthquake (kip)\n")
            tclfile.write("set\tLateralLoad\t[list")
            for i in range(building.geometry['number of story']):
                tclfile.write("\t%f"
                              % (building.seismic_force_for_strength['lateral story force'][i] \
                                 /building.geometry['number of X LFRS'] * ACCIDENTAL_TORSION))
            tclfile.write("];\n\n\n")

            # Define the load pattern in OpenSees
            tclfile.write("# Define uniform loads on beams\n")
            tclfile.write("# Load combinations:\n")
            tclfile.write("# 101 Dead load only\n")
            tclfile.write("# 102 Live load only\n")
            tclfile.write("# 103 Earthquake load only\n")
            tclfile.write("# 104 Gravity and earthquake (for calculation of drift)\n")
            tclfile.write("pattern\tPlain\t101\tConstant\t{")
            # Dead loads on beam
            for i in range(2, building.geometry['number of story']+2):
                tclfile.write("# Level%i\n" % i)
                for j in range(1, building.geometry['number of X bay']+1):
                    tclfile.write("eleLoad\t-ele")
                    tclfile.write("\t%i%i%i%i%i%i%i" % (2, j, i, 1, j+1, i, 1))
                    tclfile.write("\t-type\t-beamUniform\t[expr -1*$BeamDeadLoadFloor%i]; \n" % i)
                tclfile.write("\n")
            tclfile.write("\n\n")
            # Dead loads on leaning column
            tclfile.write("# Define point loads on leaning column\n")
            for i in range(2, building.geometry['number of story']+2):
                tclfile.write("load\t%i%i\t0\t[expr -1*$LeaningColumnDeadLoadFloor%i]\t0; \n"
                              %(building.geometry['number of X bay']+2, i, i))
            tclfile.write("\n}\n")

            tclfile.write("# puts \"Dead load defined\"")

    def write_gravity_live_load(self, building):
        # Create a .tcl file to write live load
        with open('DefineGravityLiveLoads2DModel.tcl', 'w') as tclfile:
            tclfile.write("# Define gravity live loads\n\n\n")

            # Assign the beam dead load values
            tclfile.write("# Assign uniform beam dead load values (kip/inch)\n")
            for i in range(2, building.geometry['number of story']+2):
                # Be cautious: convert the unit from lb/ft to kip/inch
                tclfile.write("set\tBeamDeadLoadFloor%i\t%f; \n"
                              % (i, building.gravity_loads['beam dead load'][i-2]*0.001/12))
            tclfile.write("\n")

            # Assign the beam live load values
            tclfile.write("# Assign uniform beam live load values (kip/inch)\n")
            for i in range(2, building.geometry['number of story']+2):
                # Be cautious: convert the unit from lb/ft to kip/inch
                tclfile.write("set\tBeamLiveLoadFloor%i\t%f; \n"
                              % (i, building.gravity_loads['beam live load'][i-2]*0.001/12))
            tclfile.write("\n")

            # Assign the values for point dead load acting on leaning column
            tclfile.write("# Assign point dead load values on leaning column: kip\n")
            for i in range(2, building.geometry['number of story']+2):
                tclfile.write("set\tLeaningColumnDeadLoadFloor%i\t%f; \n"
                              % (i, building.gravity_loads['leaning column dead load'][i-2]))
            tclfile.write("\n")

            # Assign the values for point live load acting on leaning column
            tclfile.write("# Assign point live load values on leaning column (kip)\n")
            for i in range(2, building.geometry['number of story']+2):
                tclfile.write("set\tLeaningColumnLiveLoadFloor%i\t%f; \n"
                              %(i, building.gravity_loads['leaning column live load'][i-2]))
            tclfile.write("\n")

            # Assign the lateral load values caused by earthquake
            # This is used to compute the required strength -> use seismic_force_for_strength
            tclfile.write("# Assign lateral load values caused by earthquake (kip)\n")
            tclfile.write("set\tLateralLoad\t[list")
            for i in range(building.geometry['number of story']):
                tclfile.write("\t%f"
                              % (building.seismic_force_for_strength['lateral story force'][i]
                                 / building.geometry['number of X LFRS'] * ACCIDENTAL_TORSION))
            tclfile.write("];\n\n\n")

            # Define the load pattern in OpenSees
            tclfile.write("# Define uniform loads on beams\n")
            tclfile.write("# Load combinations:\n")
            tclfile.write("# 101 Dead load only\n")
            tclfile.write("# 102 Live load only\n")
            tclfile.write("# 103 Earthquake load only\n")
            tclfile.write("# 104 Gravity and earthquake (for calculation of drift)\n")
            tclfile.write("pattern\tPlain\t102\tConstant\t{")
            # Dead loads on beam
            for i in range(2, building.geometry['number of story']+2):
                tclfile.write("# Level%i\n" % i)
                for j in range(1, building.geometry['number of X bay']+1):
                    tclfile.write("eleLoad\t-ele")
                    tclfile.write("\t%i%i%i%i%i%i%i" % (2, j, i, 1, j+1, i, 1))
                    tclfile.write("\t-type\t-beamUniform\t[expr -1*$BeamLiveLoadFloor%i]; \n" % i)
                tclfile.write("\n")
            tclfile.write("\n\n")
            # Dead loads on leaning column
            tclfile.write("# Define point loads on leaning column\n")
            for i in range(2, building.geometry['number of story']+2):
                tclfile.write("load\t%i%i\t0\t[expr -1*$LeaningColumnLiveLoadFloor%i]\t0; \n"
                              % (building.geometry['number of X bay']+2, i, i))
            tclfile.write("\n}\n")

            tclfile.write("# puts \"Live load defined\"")

    def write_earthquake_load(self, building):
        # Create a .tcl file to write earthquake load
        with open('DefineEarthquakeLaterLoads2DModel.tcl', 'w') as tclfile:
            tclfile.write("# Define gravity live loads\n\n\n")

            # Assign the beam dead load values
            tclfile.write("# Assign uniform beam dead load values (kip/inch)\n")
            for i in range(2, building.geometry['number of story']+2):
                # Be cautious: convert the unit from lb/ft to kip/inch
                tclfile.write("set\tBeamDeadLoadFloor%i\t%f; \n"
                              % (i, building.gravity_loads['beam dead load'][i-2]*0.001/12))
            tclfile.write("\n")

            # Assign the beam live load values
            tclfile.write("# Assign uniform beam live load values (kip/inch)\n")
            for i in range(2, building.geometry['number of story']+2):
                # Be cautious: convert the unit from lb/ft to kip/inch
                tclfile.write("set\tBeamLiveLoadFloor%i\t%f; \n"
                              % (i, building.gravity_loads['beam live load'][i-2]*0.001/12))
            tclfile.write("\n")

            # Assign the values for point dead load acting on leaning column
            tclfile.write("# Assign point dead load values on leaning column: kip\n")
            for i in range(2, building.geometry['number of story']+2):
                tclfile.write("set\tLeaningColumnDeadLoadFloor%i\t%f; \n"
                              % (i, building.gravity_loads['leaning column dead load'][i-2]))
            tclfile.write("\n")

            # Assign the values for point live load acting on leaning column
            tclfile.write("# Assign point live load values on leaning column (kip)\n")
            for i in range(2, building.geometry['number of story']+2):
                tclfile.write("set\tLeaningColumnLiveLoadFloor%i\t%f; \n"
                              % (i, building.gravity_loads['leaning column live load'][i-2]))
            tclfile.write("\n")

            # Assign the lateral load values caused by earthquake
            # This is used to compute the required strength -> use seismic_force_for_strength
            tclfile.write("# Assign lateral load values caused by earthquake (kip)\n")
            tclfile.write("set\tLateralLoad\t[list")
            for i in range(building.geometry['number of story']):
                tclfile.write("\t%f"
                              % (building.seismic_force_for_strength['lateral story force'][i]
                                 / building.geometry['number of X LFRS'] * ACCIDENTAL_TORSION))
            tclfile.write("];\n\n\n")

            # Define the load pattern in OpenSees
            tclfile.write("# Define uniform loads on beams\n")
            tclfile.write("# Load combinations:\n")
            tclfile.write("# 101 Dead load only\n")
            tclfile.write("# 102 Live load only\n")
            tclfile.write("# 103 Earthquake load only\n")
            tclfile.write("# 104 Gravity and earthquake (for calculation of drift)\n")
            tclfile.write("pattern\tPlain\t103\tLinear\t{")
            tclfile.write("\n\n")
            for i in range(2, building.geometry['number of story']+2):
                tclfile.write("load\t%i%i%i\t[lindex $LateralLoad %i] 0.0 0.0;\t# Level%i\n" % (1, i, 1, i-2, i))
            tclfile.write("\n}\n")
            tclfile.write("# puts \"Earthquake load defined\"")

    def write_gravity_earthquake_load(self, building):
        # Create a .tcl file to write the combination of earthquake and gravity loads
        # This load case is used to calculate story drift
        with open('DefineGravityEarthquakeLoads2DModel.tcl', 'w') as tclfile:
            tclfile.write("# Define gravity live loads\n\n\n")

            # Assign the beam dead load values
            tclfile.write("# Assign uniform beam dead load values (kip/inch)\n")
            for i in range(2, building.geometry['number of story']+2):
                # Be cautious: convert the unit from lb/ft to kip/inch
                tclfile.write("set\tBeamDeadLoadFloor%i\t%f; \n"
                              % (i, building.gravity_loads['beam dead load'][i-2]*0.001/12))
            tclfile.write("\n")

            # Assign the beam live load values
            tclfile.write("# Assign uniform beam live load values (kip/inch)\n")
            for i in range(2, building.geometry['number of story']+2):
                # Be cautious: convert the unit from lb/ft to kip/inch
                tclfile.write("set\tBeamLiveLoadFloor%i\t%f; \n"
                              % (i, building.gravity_loads['beam live load'][i-2]*0.001/12))
            tclfile.write("\n")

            # Assign the values for point dead load acting on leaning column
            tclfile.write("# Assign point dead load values on leaning column: kip\n")
            for i in range(2, building.geometry['number of story']+2):
                tclfile.write("set\tLeaningColumnDeadLoadFloor%i\t%f; \n"
                              % (i, building.gravity_loads['leaning column dead load'][i-2]))
            tclfile.write("\n")

            # Assign the values for point live load acting on leaning column
            tclfile.write("# Assign point live load values on leaning column (kip)\n")
            for i in range(2, building.geometry['number of story']+2):
                tclfile.write("set\tLeaningColumnLiveLoadFloor%i\t%f; \n"
                              % (i, building.gravity_loads['leaning column live load'][i-2]))
            tclfile.write("\n")

            # Assign the lateral load values caused by earthquake
            tclfile.write("# Assign lateral load values caused by earthquake (kip)\n")
            tclfile.write("set\tLateralLoad\t[list")
            for i in range(building.geometry['number of story']):
                tclfile.write("\t%f"
                              % (building.seismic_force_for_drift['lateral story force'][i]
                                 / building.geometry['number of X LFRS'] * ACCIDENTAL_TORSION))
            tclfile.write("];\n\n\n")

            # Define the load pattern in OpenSees
            tclfile.write("# Load combinations:\n"
                          "# 101 Dead load only\n")
            tclfile.write("# 102 Live load only\n")
            tclfile.write("# 103 Earthquake load only\n")
            tclfile.write("# 104 Gravity and earthquake (for calculation of drift)\n")
            tclfile.write("pattern\tPlain\t104\tConstant\t{")
            # Gravity load on beam
            tclfile.write("# Define uniform loads on beams\n\n")
            for i in range(2, building.geometry['number of story']+2):
                tclfile.write("# Level%i\n" % i)
                for j in range(1, building.geometry['number of X bay']+1):
                    tclfile.write("eleLoad\t-ele")
                    tclfile.write("\t%i%i%i%i%i%i%i" % (2, j, i, 1, j+1, i, 1))
                    tclfile.write("\t-type\t-beamUniform"
                                  "\t[expr -(1.2+0.2*%.2f)*$BeamDeadLoadFloor%i - "
                                  "0.5*$BeamLiveLoadFloor%i]; \n"
                                  % (building.elf_parameters['SDS'], i, i))
                tclfile.write("\n")
            tclfile.write("\n")
            # Gravity load on leaning column
            tclfile.write("# Define point loads on leaning column\n")
            for i in range(2, building.geometry['number of story']+2):
                tclfile.write("load\t%i%i\t0\t[expr -(1.2+0.2*%.2f)*$LeaningColumnDeadLoadFloor%i -"
                              "0.5*$LeaningColumnLiveLoadFloor%i]\t0;\n"
                              % (building.geometry['number of X bay']+2, i,
                                 building.elf_parameters['SDS'], i, i))
            tclfile.write("\n")
            # Earthquake lateral load
            tclfile.write("# Define earthquake lateral loads\n")
            for i in range(2, building.geometry['number of story']+2):
                tclfile.write("load\t%i%i%i\t[lindex $LateralLoad %i]\t0.0\t0.0;\t# Level%i\n" % (1, i, 1, i-2, i))
            tclfile.write("\n\n}\n")

            tclfile.write("# puts \"Gravity and earthquake loads defined\"")

    def copy_baseline_files(self, building, for_drift_only, for_period_only):
        """
        Some .tcl files are fixed, i.e., no need to change for different OpenSees models.
        Therefore, just copy these .tcl files from the baseline folder
        """
        # define a list which includes all baseline files' names
        file_list = ['Database.csv', 'DefineFunctionsAndProcedures.tcl', 'DefineVariables.tcl',
                     'EigenValueAnalysis.tcl', 'Model.tcl', 'PerformLoadsAnalysis.tcl']
        # Change the working directory to the folder where baseline .tcl files are stored
        os.chdir(building.directory['baseline files elastic'])
        # Copy all baseline .tcl files to building model directory
        for file in file_list:
            target_file = building.directory['building elastic model'] / file
            shutil.copyfile(file, target_file)
        # Remember to change the working directory to building model directory
        os.chdir(building.directory['building elastic model'])
        # Revise "Model.tcl" file if we only want to obtain drifts
        # Firstly read all content in "Model.tcl", then revise the content, and store it back to "Model.tcl"
        old_string = '[list EigenValue DeadLoad LiveLoad EarthquakeLoad GravityEarthquake]'
        new_string_for_drift = '[list GravityEarthquake]'
        if for_drift_only:
            with open('Model.tcl', 'r') as file:
                content = file.read()
            new_content = content.replace(old_string, new_string_for_drift)
            with open('Model.tcl', 'w') as file:
                file.write(new_content)
        # Revise "Model.tcl" file if we only want to obtain period
        new_string_for_period = '[list EigenValue]'
        if for_period_only:
            with open('Model.tcl', 'r') as file:
                content = file.read()
            new_content = content.replace(old_string, new_string_for_period)
            with open('Model.tcl', 'w') as file:
                file.write(new_content)


    def run_OpenSees_program(self):
        # This method is used to run the "RunModel.bat" file. OpenSees.exe program is thus run.
        os.system('OpenSees Model.tcl')