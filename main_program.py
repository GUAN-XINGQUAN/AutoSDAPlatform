# This file is the main file that calls function to perform seismic design, nonlinear model generation and analysis

##########################################################################
#                       Relevant Publications                            #
##########################################################################

# Add relevant publications below
# [1]. Guan, X., Burton, H., and Thomas, S. (2020).
# “Python-based computational platform to automate seismic design,
# nonlinear structural model construction and analysis of steel moment
# resisting frames.” Engineering Structures. (Under Review)

import sys
import time
import os
import pickle

from seismic_design import seismic_design
from global_variables import base_directory

from global_variables import base_directory
from global_variables import SECTION_DATABASE
from global_variables import COLUMN_DATABASE
from global_variables import BEAM_DATABASE
from model_generation import model_generation

# Count the starting time of the main program
start_time = time.time()

# *********************** Design Starts Here *************************
IDs = [0]
for id in IDs:
    building_id = 'Building_' + str(id)
    print("Design for Building ID = ", id)
    seismic_design(building_id, base_directory)
    # ******************* Nonlinear Model Generation Starts Here ******
    print("Model generation for Building ID = ", id)
    model_generation(building_id, base_directory)
    # ******************* Perform Eigen Value Analysis ****************
    print("Eigen Value Analysis for Building ID = ", id)
    analysis_type = 'EigenValueAnalysis'
    target_model = base_directory / 'BuildingNonlinearModels' / building_id / analysis_type
    os.chdir(target_model)
    os.system('OpenSees Model.tcl')
    # ******************* Perform Nonlinear Pushover Analysis *********
    print("Pushover Analysis for Building ID = ", id)
    analysis_type = 'PushoverAnalysis'
    target_model = base_directory / 'BuildingNonlinearModels' / building_id / analysis_type
    os.chdir(target_model)
    os.system('OpenSees Model.tcl')

print("The design, model construction, and analysis for Building ID = %i has been accomplished." % id)

end_time = time.time()
print("Running time is: %s seconds" % round(end_time - start_time, 2))