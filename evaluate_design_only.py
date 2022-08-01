"""
This file is used to evaluate a given design.

Developed by GUAN, XINGQUAN @ UCLA, April 29 2021
"""

# Please add all the imported modules in the part below
import copy
import numpy as np
import os
import pandas as pd
import pathlib

from building_information import Building
from elastic_analysis import ElasticAnalysis
from elastic_output import ElasticOutput
from global_variables import steel
from global_variables import DRIFT_LIMIT

from design_helper import create_column_set
from design_helper import create_beam_set
from design_helper import create_connection_set
from design_helper import save_all_design_results

##########################################################################
#                         Miscellaneous Input                            #
##########################################################################

# The building folder name
building_id = 'Evaluate_11'
# The directory path where the AutoSDA is.
base_directory = pathlib.Path(os.getcwd())
# Whether the connection is RBS connection: True-> use RBS connection
ADOPT_RBS_CONNECTION = True
# Whether the doubler plate is allowed to be used: True-> permit to use doubler plate.
PERMIT_DOUBLER_PLATE = True


##########################################################################
#                         Prepare the Evaluation                         #
##########################################################################

PASS_ALL_CHECK = True

# Create an instance using "Building" class
building = Building(building_id, base_directory)

# Assign the member sizes from given files
os.chdir(building.directory['building data'])
member_sizes = pd.read_csv('TrialMemberSize.csv', header=0)
building.member_size['exterior column'] = list(member_sizes['exterior column'])
building.member_size['interior column'] = list(member_sizes['interior column'])
building.member_size['beam'] = list(member_sizes['beam'])
building.construction_size = copy.deepcopy(building.member_size)

# Perform the EigenValue Analysis only to obtain the period
_ = ElasticAnalysis(building, for_drift_only=False, for_period_only=True)
building.read_modal_period()

# Compute the seismic story forces based on modal period and CuTa
building.compute_seismic_force()

# Create an elastic analysis model for building instance above using "ElasticAnalysis" class
_ = ElasticAnalysis(building, for_drift_only=False, for_period_only=False)

# Read elastic analysis drift and force demands
building.read_story_drift()
elastic_demand = ElasticOutput(building)

##########################################################################
#                         Check Story Drift                              #
##########################################################################

# Consider the RBS impact on the stiffness
if ADOPT_RBS_CONNECTION:
    RBS_STIFFNESS_FACTOR = 1.10
else:
    RBS_STIFFNESS_FACTOR = 1.0

# Check story drift
drift_check = \
    (np.max(building.elastic_response['story drift']) * building.elf_parameters['Cd'] * RBS_STIFFNESS_FACTOR
     > DRIFT_LIMIT / building.elf_parameters['rho'])


##########################################################################
#                         Check Column Strength                          #
##########################################################################

column_set, not_feasible_column = create_column_set(building, elastic_demand, steel)

##########################################################################
#                         Check Beam Strength                            #
##########################################################################

beam_set, not_feasible_beam = create_beam_set(building, elastic_demand, steel)

##########################################################################
#                         Check Connection Requirements                  #
##########################################################################

connection_set, not_feasible_connection = create_connection_set(building, column_set, beam_set, steel)

##########################################################################
#                         Display Evaluation Results                     #
##########################################################################

# Display the drift check results
print('-----------------------------------------')
if drift_check:
    PASS_ALL_CHECK = False
    print('Story drift is not satisfied:')
    print(building.elastic_response['story drift']*building.elf_parameters['Cd']*RBS_STIFFNESS_FACTOR*100)

# Display the column strength results
print('//////////////////////////////////////////')
for story, connection_no in not_feasible_column:
    PASS_ALL_CHECK = False
    print('Column in Story %i on Line %i has insufficient strength' % (story+1, connection_no))

# Display the beam strength results
print('******************************************')
for story, bay in not_feasible_beam:
    PASS_ALL_CHECK = False
    print('Beam in Floor %i on Bay %i has insufficient strength' % (story+1, bay))

# Display the connection results
print('++++++++++++++++++++++++++++++++++++++++++')
for story in range(building.geometry['number of story']):
    for connection_no in range(building.geometry['number of X bay']+1):
        if (not connection_set[story][connection_no].is_feasible['shear strength']) \
                or (not connection_set[story][connection_no].is_feasible['flexural strength']):
            PASS_ALL_CHECK = False
            print('Connection in Floor %i on Line %i is not OK because of beam' % (story+1, connection_no))
        if not connection_set[story][connection_no].is_feasible['SCWB']:
            PASS_ALL_CHECK = False
            print('Connection in Floor %i on Line %i is not OK because of SCWB: %f'
                  % (story+1, connection_no, connection_set[story+1][connection_no].moment['Mpc']
                     / connection_set[story+1][connection_no].moment['Mpb']))

# Display the constructability
for story in range(0, building.geometry['number of story']):
    for col_no in range(0, building.geometry['number of X bay']+1):
        if column_set[story][col_no].section['bf'] < beam_set[story][0].section['bf']:
            PASS_ALL_CHECK = False
            print('Column width in Story %i on Line %i is less than the corresponding beam' % (story+1, col_no))

if PASS_ALL_CHECK and (not PERMIT_DOUBLER_PLATE):
    # Display the doubler plate thickness
    for story in range(0, building.geometry['number of story']):
        for conn_no in range(0, building.geometry['number of X bay'] + 1):
            if connection_set[story][conn_no].doubler_plate_thickness > 0:
                print('Connection in Story %i on Line %i requires doubler plate' % (story+1, conn_no))
                print(connection_set[story][conn_no].shear_force['Ru'], connection_set[story][conn_no].shear_force['Rn'])


print('##############################################')
print('All evaluation results are displayed')


##########################################################################
#                         Store the Design Results                       #
##########################################################################

if PASS_ALL_CHECK:
    # Change the working directory to building data
    os.chdir(building.directory['building data'])

    # Save all design results.
    save_all_design_results(building, column_set, beam_set, connection_set, True)

# Go back to base directory
os.chdir(base_directory)
