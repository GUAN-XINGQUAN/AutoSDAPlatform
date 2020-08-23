# This file is used to include all user defined classes and functions
# Developed by GUAN, XINGQUAN @ UCLA in Dec 2018

import numpy as np
import os
import sys
import shutil

# #########################################################################
#              Generate Nonlinear OpenSees model (write .tcl files)       #
# #########################################################################


class NonlinearAnalysis(object):
    """
    This class generates the .tcl files required for nonlinear analysis. It includes the following methods:
    (1) OpenSees nodes
    (2) boundary condition
    (3) floor constraint
    (4) beam hinge material
    (5) column hinge material
    (6) beam elements
    (7) column elements
    (8) beam hinge springs
    (9) column hinge springs
    (10) mass on each floor distributed at each node
    (11) panel zone elements
    (12) panel zone springs
    (13) gravity loads
    (14) copy baseline files and revise if necessary
    (15) define various recorders for output
    (16) define pushover loading pattern
    """

    def __init__(self, building, column_set, beam_set, connection_set, analysis_type):
        """
        This function is used to call all methods to write .tcl files required for nonlinear analysis OpenSees model
        :param building: a class defined in "building_information.py" file
        :param column_set: a two-dimensional list[x][y] and each element is a column object defined in "column_component
                           x: from 0 to (story number-1)
                           y: from 0 to (bay number+1)
        :param beam_set: a two-dimensional list[x][z] and each element is a beam object defined in "beam_component"
                           x: from 0 to (story number-1)
                           z: from 0 to (bay number)
        :param connection_set: a two-dimensional list[x][y] and each element is a connection object defined in
                               "connection_part.py" file
                               x: from 0 to (story number-1)
                               y: from 0 to (bay number+1)
        :param analysis_type: a string specifies which analysis type the current model is for
                              options: 'EigenValueAnalysis', 'PushoverAnalysis', 'DynamicAnalysis'
        """
        # User-hints: if wrong analysis_type is input
        if analysis_type != 'EigenValueAnalysis' and analysis_type != 'PushoverAnalysis' \
                and analysis_type != 'DynamicAnalysis':
            sys.stderr.write('Wrong analysis type input. Please input one of the followings:\n')
            sys.stderr.write('EigenValueAnalys, PushoverAnalysis, DynamicAnalysis')
            sys.exit(99)

        # Change the working directory to the target building folder
        if not os.path.exists(building.directory['building nonlinear model']):
            os.makedirs(building.directory['building nonlinear model'])
        os.chdir(building.directory['building nonlinear model'])
        # Change the working directory to the desired folder (EigenValueAnalysis, PushoverAnalysis, or DynamicAnalysis)
        target_folder = building.directory['building nonlinear model'] / analysis_type
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
        os.chdir(target_folder)

        # Call methods to write .tcl files for the building
        # Nonlinear model for different purpose might require different .tcl files (different methods)
        self.write_nodes(building, column_set, beam_set)
        self.write_fixities(building)
        self.write_floor_constraint(building)
        self.write_beam_hinge_material(building, beam_set)
        self.write_column_hinge_material(building, column_set)
        self.write_beam(building)
        self.write_column(building)
        self.write_beam_hinge(building)
        self.write_column_hinge(building)
        self.write_mass(building)
        self.write_panel_zone_elements(building)
        self.write_panel_zone_springs(building, column_set, beam_set, connection_set)
        self.write_gravity_load(building)
        self.copy_baseline_eigen_files(building, analysis_type)
        if analysis_type == 'PushoverAnalysis':
            self.write_base_reaction_recorder(building)
            self.write_beam_hinge_recorder(building)
            self.write_column_hinge_recorder(building)
            self.write_beam_force_recorder(building)
            self.write_column_force_recorder(building)
            self.write_node_displacement_recorder(building)
            self.write_story_drift_recorder(building, analysis_type)
            self.write_pushover_loading(building)
        if analysis_type == 'DynamicAnalysis':
            self.write_story_drift_recorder(building, analysis_type)
            self.write_node_acceleration_recorder(building)
            self.write_damping(building)
            self.write_dynamic_analysis_parameters(building)

    def write_nodes(self, building, column_set, beam_set):
        """
        Create a .tcl file to write node tags and coordinates for nonlinear analysis model
        :param building: a class defined in "building_information.py"
        :param column_set: a list[x][y] and each element is a class defined in "column_component.py"
        :param beam_set: a list[x][z] and each element is a class defined in "beam_component.py"
        :return: a .tcl file
        """
        with open('DefineNodes2DModel.tcl', 'w') as tclfile:
            tclfile.write("# This file will be used to define all nodes \n")  # Introduce the file usage
            tclfile.write("# Units: inch\n\n\n")  # Explain the units

            tclfile.write("# Set bay width and story height\n")
            tclfile.write("set\tBayWidth\t[expr %.2f*12]; \n" % (building.geometry['X bay width']))
            tclfile.write("set\tFirstStory\t[expr %.2f*12]; \n" % (building.geometry['first story height']))
            tclfile.write("set\tTypicalStory\t[expr %.2f*12]; \n\n" % (building.geometry['typical story height']))

            # Define the panel sizes before building the node coordinates
            tclfile.write("# Set panel zone size as column depth and beam depth\n")
            for i in range(1, building.geometry['number of story']+2):  # i is floor level number (1 for ground floor)
                    tclfile.write("# Level %i \n" % i)
                    for j in range(1, building.geometry['number of X bay']+2):  # j is column number (1 for leftmost)
                        if i == 1:
                            tclfile.write("set\tPanelSizeLevel%iColumn%i\t[list %i %i];"
                                          "# No panel zone on ground floor so using [0, 0] is okay\n"
                                          % (i, j, 0, 0))
                        else:
                            # Note that beam size is identical in one floor level.
                            # Therefore second index for beam_set doesn't need to be changed.
                            tclfile.write("set\tPanelSizeLevel%iColumn%i\t[list %.1f %.1f];\n"
                                          % (i, j, column_set[i-2][j-1].section['d'], beam_set[i-2][0].section['d']))
            tclfile.write("\n")

            # Write nodes for frame using pre-defined tcl proc "NodesAroundPanelZone".
            tclfile.write("# Set max number of columns (excluding leaning column) and floors (counting 1 for ground)\n")
            tclfile.write("set\tMaximumFloor\t%i; \n" % (building.geometry['number of story']+1))
            tclfile.write("set\tMaximumCol\t%i; \n\n" % (building.geometry['number of X bay']+1))

            tclfile.write("# Define nodes for the frame \n")
            for i in range(1, building.geometry['number of story']+2):  # i is floor level number
                tclfile.write("# Level %i \n" % i)
                for j in range(1, building.geometry['number of X bay']+2):  # j is column label
                    tclfile.write("NodesAroundPanelZone\t%i\t%i\t[expr %i*$BayWidth]"
                                  % (j, i, j-1))
                    if i <= 2:
                        tclfile.write("\t[expr %i*$FirstStory+0*$TypicalStory]" % (i-1))
                    else:
                        tclfile.write("\t[expr 1*$FirstStory+%i*$TypicalStory]" % (i-2))
                    tclfile.write("\t$PanelSizeLevel%iColumn%i" % (i, j))
                    tclfile.write("\t$MaximumFloor\t$MaximumCol; \n")
            tclfile.write("\n")
            tclfile.write("puts \"Nodes for frame defined\" \n\n")

            # Write the nodes for leaning column
            tclfile.write("# Define nodes for leaning column \n")
            for i in range(1, building.geometry['number of story']+2):
                tclfile.write("node\t %i%i" % (building.geometry['number of X bay']+2, i))  # Node label
                tclfile.write("\t[expr %i*$BayWidth]" % (building.geometry['number of X bay']+1))  # X coordinate
                if i <= 2:
                    tclfile.write("\t[expr %i*$FirstStory+0*$TypicalStory];" % (i-1))  # Y coordinate
                    tclfile.write("\t#Level %i\n" % i)  # Comments to explain floor level
                else:
                    tclfile.write("\t[expr 1*$FirstStory+%i*$TypicalStory];" % (i-2))
                    tclfile.write("\t# Level %i\n" % i)
            tclfile.write("\n")
            tclfile.write("puts \"Nodes for leaning column defined\" \n\n")

            # Write extra nodes for leaning column springs
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
            tclfile.write("puts \"Extra nodes for leaning column springs defined\"\n")

    def write_fixities(self, building):
        """
        Create a .tcl file to write boundary for the model
        :param building: a class defined in "building_information.py"
        :return: a .tcl file
        """
        with open('DefineFixities2DModel.tcl', 'w') as tclfile:
            tclfile.write("# This file will be used to define the fixity at all column bases \n\n\n")
            tclfile.write("# Defining fixity at column base \n")
            for j in range(1, building.geometry['number of X bay']+2):
                tclfile.write("fix\t%i%i%i%i\t1\t1\t1; \n" % (j, 1, 1, 0))
            # Leaning column base
            tclfile.write("fix\t%i%i\t1\t1\t0; \n\n" % (building.geometry['number of X bay']+2, 1))
            tclfile.write("puts \"All column base fixities have been defined\"")

    def write_floor_constraint(self, building):
        """
        Create a .tcl file to write floor constraint, i.e., equal DOF
        :param building: a class defined in "building_information.py"
        :return: a .tcl file
        """
        # Create a .tcl file to write floor constraint, i.e., equal DOF
        with open('DefineFloorConstraint2DModel.tcl', 'w') as tclfile:
            tclfile.write("# This file will be used to define floor constraint \n")
            tclfile.write("# Nodes at same floor level have identical lateral displacement\n")
            tclfile.write("# Select mid right node of each panel zone as the constrained node\n\n")
            tclfile.write("set\tConstrainDOF\t1;  # X-direction\n\n")
            # Constraint starts from level 2
            for i in range(2, building.geometry['number of story']+2):  # i is floor level
                tclfile.write("# Level %i \n" % i)
                for j in range(2, building.geometry['number of X bay']+2):  # j is bay number
                    tclfile.write("equalDOF\t%i%i11\t%i%i11\t$ConstrainDOF;" % (1, i, j, i))
                    tclfile.write("\t# Pier 1 to Pier %i\n" % j)
                # Include the leaning column nodes to floor constraint
                tclfile.write("equalDOF\t%i%i%i%i\t%i%i\t$ConstrainDOF;"
                              % (1, i, 1, 1,
                                 building.geometry['number of X bay']+2, i))
                tclfile.write("\t#Pier 1 to Leaning column\n\n")
            tclfile.write("puts \"Floor constraint defined\"")

    def write_beam_hinge_material(self, building, beam_set):
        """
        Create a .tcl file to define all beam plastic hinge materials using Modified IMK material model
        :param building: a class defined in "building_information.py"
        :param beam_set: a list[x][z] and each element is a class defined in "beam_component.py"
        :return: a .tcl file
        """
        material_tag = 70001
        with open('DefineBeamHingeMaterials2DModel.tcl', 'w') as tclfile:
            tclfile.write("# This file will be used to define beam hinge material models\n\n\n")
            for i in range(2, building.geometry['number of story']+2):  # i is floor level number (no beam on ground)
                for j in range(1, building.geometry['number of X bay']+1):  # j is bay number (1 for leftmost bay)
                    tclfile.write("# Level%iBay%i\n" % (i, j))
                    tclfile.write("set\tBeamHingeMaterialLevel%iBay%iTag\t%i;\n" % (i, j, material_tag))
                    tclfile.write("set\tBeamHingeMaterialLevel%iBay%iK0\t%.4f;\n"
                                  % (i, j, (beam_set[i-2][j-1].plastic_hinge['K0'])))
                    tclfile.write("set\tBeamHingeMaterialLevel%iBay%iAs\t%.4f;\n"
                                  % (i, j, (beam_set[i-2][j-1].plastic_hinge['as'])))
                    tclfile.write("set\tBeamHingeMaterialLevel%iBay%iMy\t%.4f;\n"
                                  % (i, j, (beam_set[i-2][j-1].plastic_hinge['My'])))
                    tclfile.write("set\tBeamHingeMaterialLevel%iBay%iLambda\t%.4f;\n"
                                  % (i, j, (beam_set[i-2][j-1].plastic_hinge['Lambda'])))
                    tclfile.write("set\tBeamHingeMaterialLevel%iBay%iThetaP\t%.4f;\n"
                                  % (i, j, (beam_set[i-2][j-1].plastic_hinge['theta_p'])))
                    tclfile.write("set\tBeamHingeMaterialLevel%iBay%iThetaPc\t%.4f;\n"
                                  % (i, j, (beam_set[i-2][j-1].plastic_hinge['theta_pc'])))
                    tclfile.write("set\tBeamHingeMaterialLevel%iBay%iResidual\t%.4f;\n"
                                  % (i, j, (beam_set[i-2][j-1].plastic_hinge['residual'])))
                    tclfile.write("set\tBeamHingeMaterialLevel%iBay%iThetaU\t%.4f;\n"
                                  % (i, j, (beam_set[i-2][j-1].plastic_hinge['theta_u'])))
                    tclfile.write("CreateIMKMaterial\t$BeamHingeMaterialLevel%iBay%iTag" % (i, j))
                    tclfile.write("\t$BeamHingeMaterialLevel%iBay%iK0" % (i, j))
                    tclfile.write("\t$n")
                    tclfile.write("\t$BeamHingeMaterialLevel%iBay%iAs" % (i, j))
                    tclfile.write("\t$BeamHingeMaterialLevel%iBay%iMy" % (i, j))
                    tclfile.write("\t$BeamHingeMaterialLevel%iBay%iLambda" % (i, j))
                    tclfile.write("\t$BeamHingeMaterialLevel%iBay%iThetaP" % (i, j))
                    tclfile.write("\t$BeamHingeMaterialLevel%iBay%iThetaPc" % (i, j))
                    tclfile.write("\t$BeamHingeMaterialLevel%iBay%iResidual" % (i, j))
                    tclfile.write("\t$BeamHingeMaterialLevel%iBay%iThetaU;\n\n" % (i, j))
                    material_tag += 1
            tclfile.write("\n\nputs \"Beam hinge materials defined\"")

    def write_column_hinge_material(self, building, column_set):
        """
        Create a .tcl file to define all column plastic hinge materials using modified IMK material model
        :param building: a class defined in "building_information.py"
        :param column_set: a list[x][y] and each element is a class defined in "column_component.py" file
        :return: a .tcl file
        """
        material_tag = 60001
        with open('DefineColumnHingeMaterials2DModel.tcl', 'w') as tclfile:
            tclfile.write("# This file will be used to define column hinge material models\n\n\n")
            for i in range(1, building.geometry['number of story']+1):  # i is story number (from 1)
                for j in range(1, building.geometry['number of X bay']+2):  # j is pier number (1 for leftmost pier)
                    tclfile.write("# Story%iPier%i\n" % (i, j))
                    tclfile.write("set\tColumnHingeMaterialStory%iPier%iTag\t%i;\n" % (i, j, material_tag))
                    tclfile.write("set\tColumnHingeMaterialStory%iPier%iK0\t%.4f;\n"
                                  % (i, j, (column_set[i-1][j-1].plastic_hinge['K0'])))
                    tclfile.write("set\tColumnHingeMaterialStory%iPier%iAs\t%.4f;\n"
                                  % (i, j, (column_set[i-1][j-1].plastic_hinge['as'])))
                    tclfile.write("set\tColumnHingeMaterialStory%iPier%iMy\t%.4f;\n"
                                  % (i, j, (column_set[i-1][j-1].plastic_hinge['My'])))
                    tclfile.write("set\tColumnHingeMaterialStory%iPier%iLambda\t%.4f;\n"
                                  % (i, j, (column_set[i-1][j-1].plastic_hinge['Lambda'])))
                    tclfile.write("set\tColumnHingeMaterialStory%iPier%iThetaP\t%.4f;\n"
                                  % (i, j, (column_set[i-1][j-1].plastic_hinge['theta_p'])))
                    tclfile.write("set\tColumnHingeMaterialStory%iPier%iThetaPc\t%.4f;\n"
                                  % (i, j, (column_set[i-1][j-1].plastic_hinge['theta_pc'])))
                    tclfile.write("set\tColumnHingeMaterialStory%iPier%iResidual\t%.4f;\n"
                                  % (i, j, (column_set[i-1][j-1].plastic_hinge['residual'])))
                    tclfile.write("set\tColumnHingeMaterialStory%iPier%iThetaU\t%.4f;\n"
                                  % (i, j, (column_set[i-1][j-1].plastic_hinge['theta_u'])))
                    tclfile.write("CreateIMKMaterial\t$ColumnHingeMaterialStory%iPier%iTag" % (i, j))
                    tclfile.write("\t$ColumnHingeMaterialStory%iPier%iK0" % (i, j))
                    tclfile.write("\t$n")
                    tclfile.write("\t$ColumnHingeMaterialStory%iPier%iAs" % (i, j))
                    tclfile.write("\t$ColumnHingeMaterialStory%iPier%iMy" % (i, j))
                    tclfile.write("\t$ColumnHingeMaterialStory%iPier%iLambda" % (i, j))
                    tclfile.write("\t$ColumnHingeMaterialStory%iPier%iThetaP" % (i, j))
                    tclfile.write("\t$ColumnHingeMaterialStory%iPier%iThetaPc" % (i, j))
                    tclfile.write("\t$ColumnHingeMaterialStory%iPier%iResidual" % (i, j))
                    tclfile.write("\t$ColumnHingeMaterialStory%iPier%iThetaU;\n\n" % (i, j))
                    material_tag += 1
            tclfile.write("\n\nputs \"Column hinge materials defined\"")

    def write_beam(self, building):
        """
        Create a .tcl file to define the beam element
        :param building: a class defined in "building_information.py" file
        :return: a .tcl file
        """
        with open('DefineBeams2DModel.tcl', 'w') as tclfile:
            tclfile.write("# This file will be used to define beam elements \n\n\n")
            tclfile.write("# Define beam section sizes \n")
            for i in range(2, building.geometry['number of story']+2):  # i is the floor level (from 2)
                tclfile.write("set\tBeamLevel%i\t[SectionProperty %s];\n" % (i, building.member_size['beam'][i-2]))
            tclfile.write("\n\n# Define beams \n")
            for i in range(2, building.geometry['number of story']+2):  # i is the floor level (from 2)
                tclfile.write("# Level%i\n" % i)
                # Beam elements in frame
                for j in range(1, building.geometry['number of X bay']+1):  # j is the bay number
                    tclfile.write("element\telasticBeamColumn")  # elastic beam-column command
                    tclfile.write("\t%i%i%i%i%i%i%i" % (2, j, i, 1, j+1, i, 1))  # Beam element tag
                    tclfile.write("\t%i%i%i%i" % (j, i, 1, 5))  # Starting node
                    tclfile.write("\t%i%i%i%i" % (j+1, i, 1, 3))  # Ending node
                    tclfile.write("\t[lindex $BeamLevel%i 2]" % i)  # Area of beam section
                    tclfile.write("\t$Es")  # Young's modulus of steel material
                    tclfile.write("\t[expr ($n+1.0)/$n*[lindex $BeamLevel%i 6]]" % i)  # Modified moment of inertia
                    tclfile.write("\t$LinearTransf; \n")  # Geometric transformation

                # Truss elements connecting frame and leaning column
                tclfile.write("element\ttruss")  # elastic beam-column command
                tclfile.write("\t%i%i%i%i%i%i" % (2, building.geometry['number of X bay']+1, i, 1,
                                                  building.geometry['number of X bay']+2, i))
                tclfile.write("\t%i%i%i%i" % (building.geometry['number of X bay']+1, i, 1, 1))  # Start node in frame
                tclfile.write("\t%i%i" % (building.geometry['number of X bay']+2, i))  # Ending node in leaning column
                tclfile.write("\t$AreaRigid\t$TrussMatID; \n")  # Large area and truss element material
                tclfile.write("\n")
            tclfile.write("puts \"Beams defined\"")

    def write_column(self, building):
        """
        Create a .tcl file to define column element
        :param building: a class defined in "building_information.py" file
        :return: a .tcl file
        """
        with open('DefineColumns2DModel.tcl', 'w') as tclfile:
            tclfile.write("# This file will be used to define columns \n\n\n")

            # Define exterior column sizes
            tclfile.write("# Define exterior column section sizes \n")
            for i in range(1, building.geometry['number of story']+1):  # i is story number
                tclfile.write("set\tExteriorColumnStory%i\t[SectionProperty %s];\n"
                              % (i, building.member_size['exterior column'][i-1]))
            tclfile.write("\n\n")

            # Define interior column sizes
            tclfile.write("# Define interior column section sizes \n")
            for i in range(1, building.geometry['number of story']+1):  # i is story number
                tclfile.write("set\tInteriorColumnStory%i\t[SectionProperty %s];\n"
                              % (i, building.member_size['interior column'][i-1]))

            tclfile.write("\n\n# Define columns\n")
            for i in range(1, building.geometry['number of story']+1):  # i is story number
                tclfile.write("# Story %i \n" % i)
                # Columns in frame
                for j in range(1, building.geometry['number of X bay']+2):  # j is bay number
                    tclfile.write("element\telasticBeamColumn")  # element command
                    tclfile.write("\t%i%i%i%i%i%i%i" % (3, j, i, 1, j, i+1, 1))  # element tag
                    tclfile.write("\t%i%i%i%i" % (j, i, 1, 4))  # starting node
                    tclfile.write("\t%i%i%i%i" % (j, i+1, 1, 6))  # ending node
                    # Determine whether the column is interior or exterior column
                    # this would affect the column section size
                    if 1 < j < building.geometry['number of X bay']+1:
                        tclfile.write("\t[lindex $InteriorColumnStory%i 2]" % i)  # Area of section
                        tclfile.write("\t$Es")  # Young's modulus of steel material
                        tclfile.write("\t[expr ($n+1.0)/$n*[lindex $InteriorColumnStory%i 6]]" % i)  # Modified inertia
                    else:
                        tclfile.write("\t[lindex $ExteriorColumnStory%i 2]" % i)  # Area of section
                        tclfile.write("\t$Es")  # Young's modulus of steel material
                        tclfile.write("\t[expr ($n+1.0)/$n*[lindex $ExteriorColumnStory%i 6]]" % i)  # Modified inertia
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
            tclfile.write("puts \"Columns defined\"")

    def write_beam_hinge(self, building):
        """
        Create a .tcl file to define beam hinge element (rotational spring)
        :param building: a class defined in "building_information.py" file
        :return: a .tcl file
        """
        with open('DefineBeamHinges2DModel.tcl', 'w') as tclfile:
            tclfile.write("# This file will be used to define beam hinges \n\n\n")

            tclfile.write("# Define beam hinges using rotational spring with modified IMK material\n")
            for i in range(2, building.geometry['number of story']+2):  # i is the floor level (from 2)
                tclfile.write("# Level%i\n" % i)
                for j in range(1, building.geometry['number of X bay'] + 1):  # j is the bay number
                    tclfile.write("rotBeamSpring\t%i%i%i%i%i%i%i" % (7, j, i, 1, 1, 1, 5))  # element ID
                    tclfile.write("\t%i%i%i%i" % (j, i, 1, 1))  # node on mid right of panel zone
                    tclfile.write("\t%i%i%i%i" % (j, i, 1, 5))  # node on left end of beam element
                    tclfile.write("\t$BeamHingeMaterialLevel%iBay%iTag" % (i, j))  # associated modified IMK material
                    tclfile.write("\t$StiffMatID;\n")  # stiff material ID

                    tclfile.write("rotBeamSpring\t%i%i%i%i%i%i%i" % (7, j+1, i, 0, 9, 1, 3))  # element ID
                    tclfile.write("\t%i%i%i%i" % (j+1, i, 0, 9))  # node on mid left of panel zone
                    tclfile.write("\t%i%i%i%i" % (j+1, i, 1, 3))  # node on right end of beam element
                    tclfile.write("\t$BeamHingeMaterialLevel%iBay%iTag" % (i, j))  # associated modified IMK material
                    tclfile.write("\t$StiffMatID;\n\n")  # stiff material ID

            tclfile.write("puts \"Beam hinges defined\"")

    def write_column_hinge(self, building):
        """
        Create a .tcl file to define column hinge element (rotational spring)
        :param building: a class defined in "building_information.py" file
        :return: a .tcl file
        """
        with open('DefineColumnHinges2DModel.tcl', 'w') as tclfile:
            tclfile.write("# This file wil be used to define column hinges\n\n\n")
            for i in range(1, building.geometry['number of story']+1):  # i refers the story number
                    tclfile.write("# Column hinges at bottom of story%i\n" % i)
                    for j in range(1, building.geometry['number of X bay']+2):  # j refers the column number
                        tclfile.write("rotColumnSpring\t%i%i%i%i%i%i%i" % (6, j, i, 1, 0, 1, 4))  # element ID
                        tclfile.write("\t%i%i%i%i" % (j, i, 1, 0))  # Node on the ground
                        tclfile.write("\t%i%i%i%i" % (j, i, 1, 4))  # Node at the bottom of column element
                        tclfile.write("\t$ColumnHingeMaterialStory%iPier%iTag" % (i, j))  # associated modified IMK
                        tclfile.write("\t$StiffMatID;\n")  # stiff material
                    tclfile.write("\n")
                    tclfile.write("# Column hinges at top of story%i\n" % i)
                    for j in range(1, building.geometry['number of X bay']+2):  # j refers the column number
                        tclfile.write("rotColumnSpring\t%i%i%i%i%i%i%i" % (6, j, i+1, 1, 2, 1, 6))  # element ID
                        tclfile.write("\t%i%i%i%i" % (j, i+1, 1, 2))  # Node on the ground
                        tclfile.write("\t%i%i%i%i" % (j, i+1, 1, 6))  # Node at the bottom of column element
                        tclfile.write("\t$ColumnHingeMaterialStory%iPier%iTag" % (i, j))  # associated modified IMK
                        tclfile.write("\t$StiffMatID;\n")  # stiff material
                    tclfile.write("\n")
            tclfile.write("# Rotational springs for leaning column\n")
            for i in range(2, building.geometry['number of story']+2):  # i refers to the floor level number
                # Write the springs below floor level i
                tclfile.write("rotLeaningCol")  # procedure command to create rotational spring of leaning column
                tclfile.write("\t%i%i%i%i%i%i" % (6, building.geometry['number of X bay']+2, i,
                                                  building.geometry['number of X bay']+2, i, 2))  # spring ID
                tclfile.write("\t%i%i" % (building.geometry['number of X bay']+2, i))  # node at floor level
                tclfile.write("\t%i%i%i\t$StiffMatID;"
                              % (building.geometry['number of X bay']+2, i, 2))  # node below floor level
                tclfile.write("\t# Spring below floor level %i \n" % i)  # comment to explain the location of the sprubg

                # Write the springs above floor level i
                # If it is roof, no springs above the roof
                if i < building.geometry['number of story']+1:
                    tclfile.write("rotLeaningCol")  # rotLeaningCol is user-defined process in OpenSees
                    tclfile.write("\t%i%i%i%i%i%i" % (6, building.geometry['number of X bay']+2, i,
                                                      building.geometry['number of X bay'], i, 4))  # Spring tag
                    tclfile.write("\t%i%i" % (building.geometry['number of X bay']+2, i))  # Node at floor level
                    # Node above floor level
                    tclfile.write("\t%i%i%i\t$StiffMatID;" % (building.geometry['number of X bay']+2, i, 4))
                    tclfile.write("\t# Spring above floor level %i \n" % i)
                else:
                    pass
            tclfile.write("\n")
            tclfile.write("puts \"Column hinge defined\"")

    def write_mass(self, building):
        """
        Create a .tcl file which defines the mass of each floor at each node
        :param building: a class defined in "building_information.py" file
        :return: a .tcl file
        """
        with open('DefineMasses2DModel.tcl', 'w') as tclfile:
            tclfile.write("# This file will be used to define all nodal masses \n\n")

            # Write values for floor weights, tributary mass ratio, and nodal mass
            tclfile.write("# Define floor weights and each nodal mass \n")
            for i in range(2, building.geometry['number of story']+2):
                tclfile.write("set\tFloor%iWeight\t%.2f; \n" % (i, building.gravity_loads['floor weight'][i-2]))
            tclfile.write("set\tFrameTributaryMassRatio\t%s; \n" % (1.0 / building.geometry['number of X LFRS']))
            tclfile.write("set\tTotalNodesPerFloor\t%i; \n" % (building.geometry['number of X bay'] + 2))
            for i in range(2, building.geometry['number of story'] + 2):
                tclfile.write("set\tNodalMassFloor%i" % i)
                tclfile.write("\t[expr $Floor%iWeight*$FrameTributaryMassRatio/$TotalNodesPerFloor/$g]; \n" % i)
            tclfile.write("\n\n")

            # Write nodal masses for each floor level
            for i in range(2, building.geometry['number of story']+2):
                tclfile.write("# Level%i \n" % i)
                for j in range(1, building.geometry['number of X bay']+3):
                    if j < building.geometry['number of X bay']+2:
                        # Write mass for nodes in structural columns
                        tclfile.write("mass\t%i%i%i%i" % (j, i, 1, 1))  # Nodal mass command and node tag
                    else:
                        # Write mass for nodes in leaning column
                        tclfile.write("mass\t%i%i" % (j, i))  # Nodal mass command (leaning column)
                    tclfile.write("\t$NodalMassFloor%i" % i)  # Mass along X direction
                    tclfile.write("\t$Negligible\t$Negligible \n")  # Mass along Y and RotZ doesn't matter
                tclfile.write("\n")
            tclfile.write("puts \"Nodal mass defined\"")

    def write_panel_zone_elements(self, building):
        """
        Create a .tcl file that defines the elements in panel zone
        :param building: a class defined in "building_information.py" file
        :return: a .tcl file
        """
        with open('DefinePanelZoneElements.tcl', 'w') as tclfile:
            tclfile.write("# This file will be used to define elements in panel zones \n\n")
            tclfile.write("# Procedure used to produce panel zone elements:\n")
            for i in range(2, building.geometry['number of story']+2):  # i refers to the floor level number
                tclfile.write("# Level%i \n" % i)
                for j in range(1, building.geometry['number of X bay']+2):  # j refers to the column number
                    tclfile.write("elemPanelZone2D\t%i%i%i%i%i%i" % (8, 0, 0, j, i, 1))  # panel zone starting element tag
                    tclfile.write("\t%i%i%i%i" % (j, i, 0, 1))  # first node in panel zone (top left corner)
                    tclfile.write("\t$Es\t$PDeltaTransf\t$LinearTransf;  \n")
                tclfile.write("\n")
            tclfile.write("puts \"Panel zone elements defined\"")

    def write_panel_zone_springs(self, building, column_set, beam_set, connection_set):
        # Create a .tcl file that defines the springs involved in panel zones
        with open('DefinePanelZoneSprings.tcl', 'w') as tclfile:
            tclfile.write("# This file will be used to define springs in panel zone \n\n")
            tclfile.write("# Procedure command:\n")
            tclfile.write("# rotPanelZone2D\teleID\tnodeR\tnodeC\tE\tFy\tdc\tbf_c\ttf_c\ttp\tdb\tRy\tas\n\n")
            for i in range(2, building.geometry['number of story']+2):  # i refers to the floor level number
                tclfile.write("# Level%i\n" % i)
                for j in range(1, building.geometry['number of X bay']+2):  # j refers to the column number
                    tclfile.write("rotPanelZone2D\t%i%i%i%i%i%i" % (9, j, i, 1, 0, 0))  # panel zone spring tag
                    tclfile.write("\t%i%i%i%i" % (j, i, 0, 3))  # node tag at top right corner of panel zone
                    tclfile.write("\t%i%i%i%i" % (j, i, 0, 4))  # node tag at top right corner of panel zone
                    tclfile.write("\t$Es\t$Fy")  # Young's modulus and Yielding stress
                    tclfile.write("\t%.2f" % column_set[i-2][j-1].section['d'])  # column depth
                    tclfile.write("\t%.2f" % column_set[i-2][j-1].section['bf'])  # column flange width
                    tclfile.write("\t%.2f" % column_set[i-2][j-1].section['tf'])  # column flange thickness
                    # Use actual panel zone thickness rather than the assumed column web thickness
                    tclfile.write("\t%.2f" % (column_set[i-2][j-1].section['tw']
                                              + connection_set[i-2][j-1].doubler_plate_thickness))  # panel zone thickness
                    if j != building.geometry['number of X bay']+1:
                        # note that j is the column number.
                        # the number of beam at each floor level is one less than that of columns
                        tclfile.write("\t%.2f" % beam_set[i-2][j-1].section['d'])  # beam depth
                    else:
                        tclfile.write("\t%.2f" % beam_set[i-2][-1].section['d'])  # beam depth
                    tclfile.write("\t1.1\t0.03; \n")  # Ry value and as value (both of them are constant)
                tclfile.write("\n")
            tclfile.write("puts \"Panel zone springs defined\"")

    def write_gravity_load(self, building):
        # Create a .tcl file to write gravity load: 1.00 DL + 0.25 LL
        with open('DefineGravityLoads2DModel.tcl', 'w') as tclfile:
            tclfile.write("# Define expected gravity loads\n\n\n")

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

            # Assign the point dead load acting on leaning column
            tclfile.write("# Assign point dead load values on leaning column: kip\n")
            for i in range(2, building.geometry['number of story']+2):
                tclfile.write("set\tLeaningColumnDeadLoadFloor%i\t%f; \n"
                              % (i, building.gravity_loads['leaning column dead load'][i-2]))
            tclfile.write("\n")

            # Assign the point live load acting on leaning column
            tclfile.write("# Assign point live load values on leaning column: kip\n")
            for i in range(2, building.geometry['number of story']+2):
                tclfile.write("set\tLeaningColumnLiveLoadFloor%i\t%f; \n"
                              % (i, building.gravity_loads['leaning column live load'][i-2]))
            tclfile.write("\n")

            # Define the load pattern in OpenSees
            tclfile.write("# Define uniform loads on beams\n")
            tclfile.write("# Load combinations:\n")
            tclfile.write("# 104 Expected gravity loads: 1.05 DL + 0.25 LL\n")
            tclfile.write("pattern\tPlain\t104\tConstant\t{\n\n")
            # Dead loads on beam
            for i in range(2, building.geometry['number of story']+2):
                tclfile.write("# Level%i\n" % i)
                for j in range(1, building.geometry['number of X bay']+1):
                    tclfile.write("eleLoad\t-ele")
                    tclfile.write("\t%i%i%i%i%i%i%i" % (2, j, i, 1, j + 1, i, 1))  # Beam element tag
                    tclfile.write("\t-type\t-beamUniform")
                    tclfile.write("\t[expr -1.05*$BeamDeadLoadFloor%i - 0.25*$BeamLiveLoadFloor%i];\n"
                                  % (i, i))
                tclfile.write("\n")
            tclfile.write("\n")
            # Gravity load on leaning column
            tclfile.write("# Define point loads on leaning column\n")
            for i in range(2, building.geometry['number of story']+2):
                tclfile.write("load\t%i%i\t0\t[expr -1*$LeaningColumnDeadLoadFloor%i - "
                              "0.25*$LeaningColumnLiveLoadFloor%i]\t0;\n"
                              % (building.geometry['number of X bay']+2, i, i, i))
            tclfile.write("\n}\n")

            tclfile.write("puts \"Expected gravity loads defined\"")

    def write_pushover_loading(self, building):
        # Create a .tcl file to write lateral pushover loading
        with open('DefinePushoverLoading2DModel.tcl', 'w') as tclfile:
            tclfile.write("# Define pushover loading\n\n\n")
            tclfile.write("pattern\tPlain\t200\tLinear\t{\n\n")
            tclfile.write("# Pushover pattern\n")
            for i in range(2, building.geometry['number of story']+2):  # Floor level
                tclfile.write("# Level%i\n" % i)
                for j in range(1, building.geometry['number of X bay']+2):  # Column number
                    load = building.seismic_force_for_strength['lateral story force'][i-2]\
                           / np.sum(building.seismic_force_for_strength['lateral story force'])
                    tclfile.write("load\t%i%i%i%i\t%.3f\t0\t0;\n" % (j, i, 1, 1, load))
                tclfile.write("\n")
            tclfile.write("}")

    def write_base_reaction_recorder(self, building):
        # Create a .tcl file to write the recorders for base reactions
        with open('DefineBaseReactionRecorders2DModel.tcl', 'w') as tclfile:
            tclfile.write("# Define base node reaction recorders\n\n\n")
            tclfile.write("cd\t$baseDir/$dataDir/BaseReactions\n\n")

            # Record vertical reactions
            tclfile.write("# Vertical reactions\n")
            tclfile.write("recorder\tNode\t-file\tVerticalReactions.out\t-time\t-node")
            for j in range(1, building.geometry['number of X bay']+2):
                tclfile.write("\t%i%i%i%i" % (j, 1, 1, 0))
            tclfile.write("\t%i%i" % (building.geometry['number of X bay']+2, 1))
            tclfile.write("\t-dof\t2\treaction;\n\n")

            # Record horizontal reactions
            tclfile.write("# X-Direction reactions\n")
            tclfile.write("recorder\tNode\t-file\tXReactions.out\t-time\t-node")
            for j in range(1, building.geometry['number of X bay']+2):
                tclfile.write("\t%i%i%i%i" % (j, 1, 1, 0))
            tclfile.write("\t%i%i" % (building.geometry['number of X bay']+2, 1))
            tclfile.write("\t-dof\t1\treaction;\n\n")

    def write_beam_hinge_recorder(self, building):
        # Create a .tcl file to record beam hinge forces and deformation
        with open('DefineBeamHingeRecorders2DModel.tcl', 'w') as tclfile:
            tclfile.write("# Define beam hinge force-deformation recorders\n\n\n")
            tclfile.write("cd\t$baseDir/$dataDir/BeamHingeMoment\n\n")

            # Define output files to record beam hinge element forces
            tclfile.write("# X-Direction beam hinge element force recorders\n")
            for i in range(2, building.geometry['number of story']+2):
                tclfile.write("recorder\tElement\t-file\tBeamHingeForcesLevel%i.out\t-time\t-ele" % i)
                for j in range(1, building.geometry['number of X bay']+1):
                    tclfile.write("\t%i%i%i%i%i%i%i" % (7, j, i, 1, 1, 1, 5))
                    tclfile.write("\t%i%i%i%i%i%i%i" % (7, j+1, i, 0, 9, 1, 3))
                tclfile.write("\tforce;\n")
            tclfile.write("\n")

            tclfile.write("cd\t$baseDir/$dataDir/BeamHingeDeformations\n\n")
            # Define output files to record beam hinge element deformations
            tclfile.write("# X-Direction beam hinge deformation recorders\n")
            for i in range(2, building.geometry['number of story']+2):
                tclfile.write("recorder\tElement\t-file\tBeamHingeForcesLevel%i.out\t-time\t-ele" % i)
                for j in range(1, building.geometry['number of X bay']+1):
                    tclfile.write("\t%i%i%i%i%i%i%i" % (7, j, i, 1, 1, 1, 5))
                    tclfile.write("\t%i%i%i%i%i%i%i" % (7, j+1, i, 0, 9, 1, 3))
                tclfile.write("\tdeformation;\n")
            tclfile.write("\n")

    def write_column_hinge_recorder(self, building):
        # Create a .tcl file to record column hinge forces and deformations
        with open('DefineColumnHingeRecorders2DModel.tcl', 'w') as tclfile:
            tclfile.write("# Define column hinge force-deformation recorders\n\n\n")
            tclfile.write("cd\t$baseDir/$dataDir/ColumnHingeMoment\n\n")

            # Define output files to record column hinge forces
            tclfile.write("# Column hinge element force recorders\n")
            for i in range(1, building.geometry['number of story']+1):
                tclfile.write("recorder\tElement\t-file\tColumnHingeForcesStory%i.out\t-time\t-ele" % i)
                for j in range(1, building.geometry['number of X bay']+2):
                    tclfile.write("\t%i%i%i%i%i%i%i" % (6, j, i, 1, 0, 1, 4))
                    tclfile.write("\t%i%i%i%i%i%i%i" % (6, j, i+1, 1, 2, 1, 6))
                tclfile.write("\tforce;\n")
            tclfile.write("\n")

            # Define output files to record column hinge deformations
            tclfile.write("cd\t$baseDir/$dataDir/ColumnHingeDeformations\n\n")
            tclfile.write("# Column hinge element deformation recorders\n")
            for i in range(1, building.geometry['number of story']+1):
                tclfile.write("recorder\tElement\t-file\tColumnHingeForcesStory%i.out\t-time\t-ele" % i)
                for j in range(1, building.geometry['number of X bay']+2):
                    tclfile.write("\t%i%i%i%i%i%i%i" % (6, j, i, 1, 0, 1, 4))
                    tclfile.write("\t%i%i%i%i%i%i%i" % (6, j, i+1, 1, 2, 1, 6))
                tclfile.write("\tdeformation;")
            tclfile.write("\n")

    def write_beam_force_recorder(self, building):
        # Create a .tcl file to write beam element forces recorder for output
        with open('DefineGlobalBeamForceRecorders2DModel.tcl', 'w') as tclfile:
            tclfile.write("# Define global beam force recorders\n\n\n")
            tclfile.write("cd\t$baseDir/$dataDir/GlobalBeamForces\n\n")
            tclfile.write("# X-Direction beam element global force recorders\n")
            for i in range(2, building.geometry['number of story']+2):
                tclfile.write("recorder\tElement\t-file\tGlobalXBeamForcesLevel%i.out\t-time\t-ele" % i)
                for j in range(1, building.geometry['number of X bay']+1):
                    tclfile.write("\t%i%i%i%i%i%i%i" % (2, j, i, 1, j+1, i, 1))
                tclfile.write("\tforce\n")

    def write_column_force_recorder(self, building):
        # Create a .tcl file to write column element forces recorder for output
        with open('DefineGlobalColumnForceRecorders2DModel.tcl', 'w') as tclfile:
            tclfile.write("# Define global column force recorders\n\n\n")
            tclfile.write("cd\t$baseDir/$dataDir/GlobalBeamForces\n\n")
            tclfile.write("# Column element global force recorders\n")
            for i in range(1, building.geometry['number of story']+1):  # i is story number
                tclfile.write("recorder\tElement\t-file\tGlobalColumnForcesStory%i.out\t-time\t-ele" % i)
                for j in range(1, building.geometry['number of X bay']+2):
                    tclfile.write("\t%i%i%i%i%i%i%i" % (3, j, i, 1, j, i+1, 1))
                tclfile.write("\tforce;\n")
            tclfile.write("\n")

    def write_node_displacement_recorder(self, building):
        # Create a .tcl file to write the node displacements recorder for output
        with open('DefineNodeDisplacementRecorders2DModel.tcl', 'w') as tclfile:
            tclfile.write("# Define node displacement recorders\n\n\n")
            tclfile.write("cd\t$baseDir/$dataDir/NodeDisplacements\n\n")
            for i in range(1, building.geometry['number of story']+2):
                tclfile.write("recorder\tNode\t-file\tNodeDispLevel%i.out\t-time\t-node" % i)
                for j in range(1, building.geometry['number of X bay']+2):
                    if i == 1:
                        tclfile.write("\t%i%i%i%i" % (j, i, 1, 0))
                    else:
                        tclfile.write("\t%i%i%i%i" % (j, i, 1, 1))
                tclfile.write("\t-dof\t1\tdisp;\n")

    def write_story_drift_recorder(self, building, analysis_type):
        # Create a .tcl file to write story drift recorder for output
        with open('DefineStoryDriftRecorders2DModel.tcl', 'w') as tclfile:
            tclfile.write("# Define story drift recorders\n\n\n")

            if analysis_type == 'PushoverAnalysis':
                tclfile.write("cd\t$baseDir/$dataDir/StoryDrifts\n\n")
            if analysis_type == 'DynamicAnalysis':
                tclfile.write("cd\t$baseDir/$dataDir/EQ_$eqNumber/Scale_$scale/StoryDrifts\n\n")
            # Write the story drift recorder for each story
            for i in range(1, building.geometry['number of story']+1):
                tclfile.write("recorder\tDrift\t-file")
                if analysis_type == 'PushoverAnalysis':
                    tclfile.write("\t$baseDir/$dataDir/StoryDrifts/Story%i.out" % i)
                if analysis_type == 'DynamicAnalysis':
                    tclfile.write("\t$baseDir/$dataDir/EQ_$eqNumber/Scale_$scale/StoryDrifts/Story%i.out" % i)
                # Always use nodes on column #1 to calculate story drift
                if i == 1:
                    # Node tag at ground floor is different from those on upper stories
                    tclfile.write("\t-time\t-iNode\t%i%i%i%i" % (1, i, 1, 0))  # Node at bottom of current story
                else:
                    tclfile.write("\t-time\t-iNode\t%i%i%i%i" % (1, i, 1, 1))  # Node at bottom of current story
                tclfile.write("\t-time\t-jNode\t%i%i%i%i" % (1, i+1, 1, 1))  # Node at top of current story
                tclfile.write("\t-dof\t1\t-perpDirn\t2; \n")

            # Write the story drift recorder for roof
            tclfile.write("recorder\tDrift\t-file")
            if analysis_type == 'PushoverAnalysis':
                tclfile.write("\t$baseDir/$dataDir/StoryDrifts/Roof.out")
            if analysis_type == 'DynamicAnalysis':
                tclfile.write("\t$baseDir/$dataDir/EQ_$eqNumber/Scale_$scale/StoryDrifts/Roof.out")
            tclfile.write("\t-time\t-iNode\t%i%i%i%i" % (1, 1, 1, 0))
            tclfile.write("\t-jNode\t%i%i%i%i" % (1, building.geometry['number of story']+1, 1, 1))
            tclfile.write("\t-dof\t1\t-perpDirn\t2; \n")

    def write_node_acceleration_recorder(self, building):
        # Create a .tcl file to record absolute node acceleration
        with open('DefineNodeAccelerationRecorders2DModel.tcl', 'w') as tclfile:
            tclfile.write("# Define node acceleration recorders\n\n\n")
            tclfile.write("cd $baseDir/$dataDir/EQ_$eqNumber/Scale_$scale/NodeAccelerations\n\n")
            for i in range(1, building.geometry['number of story']+2):
                tclfile.write("recorder\tNode\t-file\tNodeAccLevel%i.out\t-timeSeries\t2\t-time\t-node" % i)
                for j in range(1, building.geometry['number of X bay']+2):
                    if i == 1:
                        tclfile.write("\t%i%i%i%i" % (j, i, 1, 0))
                    else:
                        tclfile.write("\t%i%i%i%i" % (j, i, 1, 1))
                tclfile.write("\t-dof\t1\taccel;\n")

    def write_damping(self, building):
        # Create a .tcl file to define damping for dynamic analysis
        with open('DefineDamping2DModel.tcl', 'w') as tclfile:
            tclfile.write("# This file will be used to define damping\n\n")

            tclfile.write("# A damping ratio of 2% is used for steel buildings\n")
            tclfile.write("set\tdampingRatio\t0.02;\n")

            tclfile.write("# Define the value for pi\n")
            tclfile.write("set\tpi\t[expr 2.0*asin(1.0)];\n\n")

            tclfile.write("# Defining damping parameters\n")
            tclfile.write("set\tomegaI\t[expr (2.0*$pi) / $periodForRayleighDamping_1];\n")
            tclfile.write("set\tomegaJ\t[expr (2.0*$pi) / $periodForRayleighDamping_2];\n")
            tclfile.write("set\talpha0\t[expr ($dampingRatio*2.0*$omegaI*$omegaJ) / ($omegaI+$omegaJ)];\n")
            tclfile.write("set\talpha1\t[expr ($dampingRatio*2.0) / ($omegaI+$omegaJ) * ($n+1.0) / $n];")
            tclfile.write("\t # (n+1.0)/n factor is because stiffness for elastic elements have been modified\n\n")

            tclfile.write("# Assign damping to beam elements\n")
            tclfile.write("region\t1\t-ele")
            for i in range(2, building.geometry['number of story']+2):  # i is the floor level (from 2)
                for j in range(1, building.geometry['number of X bay']+1):  # j is the bay number
                    tclfile.write("\t%i%i%i%i%i%i%i" % (2, j, i, 1, j+1, i, 1))  # Beam element tag
            tclfile.write("\t-rayleigh\t0.0\t0.0\t$alpha1\t0.0;\n")

            tclfile.write("# Assign damping to column elements\n")
            tclfile.write("region\t2\t-ele")
            for i in range(1, building.geometry['number of story']+1):  # i is story number
                for j in range(1, building.geometry['number of X bay']+2):  # j is bay number
                    tclfile.write("\t%i%i%i%i%i%i%i" % (3, j, i, 1, j, i+1, 1))  # element tag
            tclfile.write("\t-rayleigh\t0.0\t0.0\t$alpha1\t0.0;\n")

            tclfile.write("# Assign damping to nodes\n")
            tclfile.write("region\t3\t-node")
            for i in range(2, building.geometry['number of story']+2):
                for j in range(1, building.geometry['number of X bay']+3):
                    if j == building.geometry['number of X bay']+2:
                        tclfile.write("\t%i%i" % (j, i))
                    else:
                        tclfile.write("\t%i%i%i%i" % (j, i, 1, 1))
            tclfile.write("\t-rayleigh\t$alpha0\t0.0\t0.0\t0.0;\n\n")
            tclfile.write("puts \"Rayleigh damping defined\"")

    def write_dynamic_analysis_parameters(self, building):
        # Create a .tcl file to define all parameters pertinent to dynamic analysis solver
        with open('DefineDynamicAnalysisParameters2DModel.tcl', 'w') as tclfile:
            tclfile.write("# This file will be used to define analysis parameters relevant to dynamic solver\n\n\n")
            tclfile.write("set\tNStories\t%i; \n" % building.geometry['number of story'])
            # The height shall be converted from ft to inch
            tclfile.write("set\tHTypicalStory\t%.2f; \n" % (building.geometry['typical story height']*12.0))
            tclfile.write("set\tHFirstStory\t%.2f; \n" % (building.geometry['first story height']*12.0))
            tclfile.write("set\tFloorNodes\t[list")
            for i in range(1, building.geometry['number of story']+2):
                if i == 1:
                    tclfile.write("\t1110")
                else:
                    tclfile.write("\t%i%i%i%i" % (1, i, 1, 1))
            tclfile.write("];\n\n")
            tclfile.write("puts \"Dynamic analysis parameters defined\"")

    def copy_baseline_eigen_files(self, building, analysis_type):
        """
        Some .tcl files are fixed, i.e., no need to change for different OpenSees models.
        Therefore, just copy those .tcl files from the baseline folder
        :param building: a class defined in "building_information.py"
        :param analysis_type: a string specifies the analysis type that the current nonlinear model is for
                              options: 'EigenValueAnalysis', 'PushoverAnalysis', 'DynamicAnalysis'
        :return:
        """
        # Change the working directory to the folder where baseline .tcl files are stored
        source_dir = building.directory['baseline files nonlinear'] / analysis_type
        os.chdir(source_dir)
        # Copy all baseline .tcl files to building model directory
        for _, _, files in os.walk(source_dir):
            for file in files:
                target_file = building.directory['building nonlinear model'] / analysis_type / file
                shutil.copy(file, target_file)
        # Remember to change the working directory to building model directory
        os.chdir(building.directory['building nonlinear model'] / analysis_type)

        # Update necessary information in .tcl files for different analysis
        if analysis_type == 'EigenValueAnalysis':
            old_mode = 'set nEigenL 4'
            new_mode = 'set nEigenL 4'
            # Revise the baseline file: EigenValueAnalysis.tcl if building has less than four stories.
            # Default EigenValueAnalysis.tcl file analyzes four modes.
            # For buildings which have three stories or below, they might only have 1st mode, 2nd mode, and 3rd mode.
            if building.geometry['number of story'] <= 3:
                # This is to change the number of desired mode
                new_mode = 'set nEigenL 3'
                # Releast the equal DOF constraints for buildings with less than 3 stories
                with open('Model.tcl', 'r') as file:
                    content = file.read()
                new_content = content.replace('source DefineFloorConstraint2DModel.tcl',
                                              '# source DefineFloorConstraint2DModel.tcl')
                with open('Model.tcl', 'w') as file:
                    file.write(new_content)
            # This is to change the node tag to record eigen vector
            old_string = '**EIGENVECTOR_NODE**'
            new_string = '1110'
            for floor in range(1, building.geometry['number of story']+1):
                new_string += (' %i%i%i%i' % (1, floor+1, 1, 1))
            with open('EigenValueAnalysis.tcl', 'r') as file:
                content = file.read()
            new_content = content.replace(old_mode, new_mode)
            new_content = new_content.replace(old_string, new_string)
            with open('EigenValueAnalysis.tcl', 'w') as file:
                file.write(new_content)

            # Perform Eigen Analysis to obtain the periods which will be necessary for raleigh damping in dynamic part
            os.system('OpenSees Model.tcl')

        # Update pushover parameters contained Model.tcl when performing pushover analysis
        elif analysis_type == 'PushoverAnalysis':
            # This is to update the pushover analysis parameters
            old_string = ['**ControlNode**', '**ControlDOF**', '**DisplacementIncrement**', '**DisplacementMaximum**']
            new_string = ['%i%i%i%i' % (1, building.geometry['number of story']+1, 1, 1), '%i' % 1, '0.01',
                          '%.2f' % (0.1*building.geometry['floor height'][-1]*12)]  # DisplamentMaximum should be in inch.
            with open('Model.tcl', 'r') as file:
                content = file.read()
            for indx in range(len(old_string)):
                content = content.replace(old_string[indx], new_string[indx])
            with open('Model.tcl', 'w') as file:
                file.write(content)

        # Update Model.tcl and RunIDA2DModel.tcl files for dynamic analysis
        elif analysis_type == 'DynamicAnalysis':
            # This is to update periods for rayleigh damping
            old_periods = ['**firstModePeriod**', '**thirdModePeriod**']
            # The path to Eigen value analysis results
            periods_dir = building.directory['building nonlinear model'] / 'EigenValueAnalysis' / 'EigenAnalysisOutput'
            # Read the periods from .out files generated by Eigen value analysis
            os.chdir(periods_dir)
            periods = np.loadtxt('Periods.out')
            # Update period variables in Model.tcl
            os.chdir(building.directory['building nonlinear model'] / analysis_type)
            with open('Model.tcl', 'r') as file:
                content = file.read()
            content = content.replace(old_periods[0], str(periods[0]))  # First-mode period
            content = content.replace(old_periods[1], str(periods[2]))  # Third-mode period
            # Write the updated content into Model.tcl
            with open('Model.tcl', 'w') as file:
                file.write(content)
            # Update dynamic parameters in RunIDA2DModel.tcl
            with open('RunIDA2DModel.tcl', 'r') as file:
                content = file.read()
            old_string = ['**NumberOfGroundMotions**', '**IntensityScales**', '**MCEScaleFactor**']
            new_string = [240, 100, 1.0]
            for indx in range(len(old_string)):
                content = content.replace(old_string[indx], str(new_string[indx]))
            # Write the new content back into RunIDA2DModel.tcl
            with open('RunIDA2DModel.tcl', 'w') as file:
                file.write(content)