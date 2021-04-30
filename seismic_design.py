"""
This file creates a function that is called by "main_design.py" to perform seismic design

Developed by GUAN, XINGQUAN @ UCLA, March 29 2018
Revised in Feb. 2019
"""

##########################################################################
#                       Load Built-in Packages                           #
##########################################################################

# Please add all the imported modules in the part below
import copy
import numpy as np
import os
import pandas as pd
import pickle
import sys

from building_information import Building
from elastic_analysis import ElasticAnalysis
from elastic_output import ElasticOutput

from global_variables import steel
from global_variables import UPPER_LOWER_COLUMN_Zx
from global_variables import RBS_STIFFNESS_FACTOR
from global_variables import DRIFT_LIMIT

from construction_functions import create_column_set
from construction_functions import create_beam_set
from construction_functions import create_connection_set

##########################################################################
#                         Function Implementation                        #
##########################################################################


def seismic_design(building_id, base_directory):
    # **************** Debug using only **********************************
    # building_id = 'Test3'
    # from global_variables import base_directory
    # ///////////////// Start Seismic Design /////////////////////////////
    # Create an instance using "Building" class
    building_1 = Building(building_id, base_directory)

    # ***************** Debug using only *********************************
    # building_1.member_size['exterior column'] = ['W36X262', 'W36X210', 'W36X210',
    #                                              'W36X232', 'W27X235', 'W27X235',
    #                                              'W24X207', 'W21X182', 'W27X94']
    # building_1.member_size['interior column'] = ['W33X387', 'W36X282', 'W36X282',
    #                                              'W30X357', 'W36X262', 'W36X262',
    #                                              'W36X210', 'W30X191', 'W27X102']
    # # building_1.member_size['interior column'] = ['W14X38', 'W14X38', 'W14X38', 'W14X38', 'W14X38']
    # building_1.member_size['beam'] = ['W24X207', 'W24X207', 'W24X207',
    #                                   'W24X207', 'W24X207', 'W24X207',
    #                                   'W24X207', 'W33X152', 'W21X182']
    # # building_1.member_size['beam'] = ['W21X44', 'W21X44', 'W21X44', 'W21X44', 'W21X44']
    # building_1.member_size['exterior column'] = ['W33X241', 'W36X652', 'W33X241']
    # building_1.member_size['interior column'] = ['36X282', 'W36X652', 'W33X318']
    # building_1.member_size['beam'] = ['W36X210', 'W36X282', 'W36X232']
    # building_1.member_size['exterior column'] = ['W14X426','W14X426','W14X426',
    #                                              'W14X426','W14X426','W14X426',
    #                                              'W14X426','W14X398','W14X370',
    #                                              'W14X370','W14X370','W14X311',
    #                                              'W14X211','W12X170']
    # building_1.member_size['interior column'] = ['W14X426', 'W14X426', 'W14X426',
    #                                              'W14X426', 'W14X426', 'W14X426',
    #                                              'W14X426', 'W14X398', 'W14X370',
    #                                              'W14X370', 'W14X370', 'W14X311',
    #                                              'W14X211', 'W12X170']
    # building_1.member_size['beam'] = ['W24X207', 'W24X207', 'W24X207',
    #                                   'W24X207', 'W24X207', 'W24X207',
    #                                   'W24X207', 'W33X152', 'W21X182',
    #                                   'W21X182', 'W21X182', 'W21X166',
    #                                   'W27X94', 'W21X83']
    # ****************** Debug ends here *********************************

    # Perform EigenValue Analysis only to obtain the period
    _ = ElasticAnalysis(building_1, for_drift_only=False, for_period_only=True)
    building_1.read_modal_period()
    # Compute the seismic story forces based on modal period and CuTa
    building_1.compute_seismic_force()

    # Create an elastic analysis model for building instance above using "ElasticAnalysis" class
    _ = ElasticAnalysis(building_1, for_drift_only=False, for_period_only=False)

    # Read elastic analysis drift
    building_1.read_story_drift()

    # ************************************************************************
    # ///////////////// Optimize Member Size for Drift ///////////////////////
    # ************************************************************************
    # Define iteration index denoting how many iteration it has be performed
    iteration = 0
    # Perform the optimization process
    last_member = copy.deepcopy(building_1.member_size)
    while np.max(building_1.elastic_response['story drift']) * building_1.elf_parameters['Cd'] * RBS_STIFFNESS_FACTOR \
            <= DRIFT_LIMIT/building_1.elf_parameters['rho']:
        print("Member size after optimization %i" % iteration)
        print("Exterior column:", building_1.member_size['exterior column'])
        print("Interior column:", building_1.member_size['interior column'])
        print("Beam:", building_1.member_size['beam'])
        print("Current story drifts: (%)")
        print(building_1.elastic_response['story drift'] * building_1.elf_parameters['Cd'] * RBS_STIFFNESS_FACTOR * 100)
        # Before optimization, record the size in the last step.
        last_member = copy.deepcopy(building_1.member_size)
        # Perform optimization
        building_1.optimize_member_for_drift()
        # Update the design period and thus the design seismic forces
        _ = ElasticAnalysis(building_1, for_drift_only=False, for_period_only=True)
        building_1.read_modal_period()
        building_1.compute_seismic_force()
        # Update the design story drifts
        _ = ElasticAnalysis(building_1, for_drift_only=True, for_period_only=False)
        building_1.read_story_drift()

        iteration = iteration + 1
    # Assign the last member size to building instance
    building_1.member_size = copy.deepcopy(last_member)
    # Add a check here: if the program does not go into previous while loop,
    # probably the initial size is not strong enough ==> not necessary to go into following codes
    if iteration == 0:
        sys.stderr.write("Initial section size is not strong enough!")
        sys.stderr.write("Please increase initial depth!")
        sys.exit(99)

    # *******************************************************************
    # ///////////////// Check Column Strength ///////////////////////////
    # *******************************************************************
    # Create the elastic model using the last member size -> obtain period and seismic force first
    _ = ElasticAnalysis(building_1, for_drift_only=False, for_period_only=True)
    building_1.read_modal_period()
    building_1.compute_seismic_force()
    # Obtain the story drift using the last member size
    _ = ElasticAnalysis(building_1, for_drift_only=False, for_period_only=False)
    building_1.read_story_drift()
    # Extract the load output from elastic analysis and perform load combination
    elastic_demand = ElasticOutput(building_1)
    # Check all columns to see whether they have enough strengths
    # Initialize a list to store all column instances
    column_set, not_feasible_column = create_column_set(building_1, elastic_demand, steel)

    # ********************************** Refactor the codes ************************************************************
    # column_set = [[0] * (building_1.geometry['number of X bay'] + 1)
    #               for story in range(building_1.geometry['number of story'])]
    # not_feasible_column = []  # Used to record which column [story][column_no] is not feasible
    # for story in range(building_1.geometry['number of story']):
    #     for column_no in range(building_1.geometry['number of X bay'] + 1):
    #         axial_demand = abs(elastic_demand.dominate_load['column axial'][story, 2 * column_no])
    #         shear_demand = abs(elastic_demand.dominate_load['column shear'][story, 2 * column_no])
    #         moment_bottom = elastic_demand.dominate_load['column moment'][story, 2 * column_no]
    #         moment_top = elastic_demand.dominate_load['column moment'][story, 2 * column_no + 1]
    #         if column_no == 0 or column_no == building_1.geometry['number of X bay']:
    #             column_type = 'exterior column'
    #         else:
    #             column_type = 'interior column'
    #         length = np.asscalar(
    #             building_1.geometry['floor height'][story + 1] - building_1.geometry['floor height'][story])
    #         # Build instance for each column member
    #         column_set[story][column_no] = Column(building_1.member_size[column_type][story],
    #                                               axial_demand, shear_demand, moment_bottom, moment_top,
    #                                               length, length, steel)
    #         # Check the flag of each column
    #         if not column_set[story][column_no].check_flag():
    #             sys.stderr.write('column_%s%s is not feasible!!!\n' % (story, column_no))
    #             not_feasible_column.append([story, column_no])
    #             # sys.exit(1)
    # ********************************** Refactor Ends **** ************************************************************

    # *******************************************************************
    # ///////// Revise Column to Satisfy Strength Requirement ///////////
    # *******************************************************************
    for story in range(0, building_1.geometry['number of story']):
        for column_no in range(0, building_1.geometry['number of X bay'] + 1):
            while not column_set[story][column_no].check_flag():
                if column_no == 0 or column_no == building_1.geometry['number of X bay']:
                    type_column = 'exterior column'
                else:
                    type_column = 'interior column'
                building_1.upscale_column(story, type_column)
                # Update the modal period and seismic forces
                _ = ElasticAnalysis(building_1, for_drift_only=False, for_period_only=True)
                building_1.read_modal_period()
                building_1.compute_seismic_force()
                # Re-perform the elastic analysis to obtain the updated demand
                _ = ElasticAnalysis(building_1, for_drift_only=False, for_period_only=False)
                building_1.read_story_drift()
                elastic_demand = ElasticOutput(building_1)
                # Re-construct the column objects
                column_set, not_feasible_column = create_column_set(building_1, elastic_demand, steel)

    # ********************************** Refactor the codes ************************************************************
    # for [target_story_index, target_column_no] in not_feasible_column:
    #     while not column_set[target_story_index][target_column_no].check_flag():
    #         # Upscale the unsatisfied column
    #         if target_column_no == 0 or target_column_no == building_1.geometry['number of X bay']:
    #             type_column = 'exterior column'
    #         else:
    #             type_column = 'interior column'
    #         building_1.upscale_column(target_story_index, type_column)
    #         # Update the modal period and seismic forces
    #         model_1 = ElasticAnalysis(building_1, for_drift_only=False, for_period_only=True)
    #         building_1.read_modal_period()
    #         building_1.compute_seismic_force()
    #         # Re-perform the elastic analysis to obtain the updated demand
    #         model_1 = ElasticAnalysis(building_1, for_drift_only=False, for_period_only=False)
    #         building_1.read_story_drift()
    #         elastic_demand = ElasticOutput(building_1)
    #         # Re-construct the column objects (only those revised columns)
    #         for column_no in range(building_1.geometry['number of X bay']+1):
    #             axial_demand = abs(elastic_demand.dominate_load['column axial'][target_story_index, 2 * column_no])
    #             shear_demand = abs(elastic_demand.dominate_load['column shear'][target_story_index, 2 * column_no])
    #             moment_bottom = elastic_demand.dominate_load['column moment'][target_story_index, 2 * column_no]
    #             moment_top = elastic_demand.dominate_load['column moment'][target_story_index, 2 * column_no + 1]
    #             if column_no == 0 or column_no == building_1.geometry['number of X bay']:
    #                 column_type = 'exterior column'
    #             else:
    #                 column_type = 'interior column'
    #             length = np.asscalar(
    #                 building_1.geometry['floor height'][target_story_index + 1]
    #                 - building_1.geometry['floor height'][target_story_index])
    #             # Build instance for each column member
    #             column_set[target_story_index][column_no] =
    #             Column(building_1.member_size[column_type][target_story_index], axial_demand,
    #             shear_demand, moment_bottom, moment_top,
    #             length, length, steel)
    # ********************************** Refactor Ends **** ************************************************************

    # *******************************************************************
    # ///////////////// Check Beam Strength /////////////////////////////
    # *******************************************************************
    # Initialize a list to store all beam instances
    beam_set, not_feasible_beam = create_beam_set(building_1, elastic_demand, steel)

    # ********************************** Refactor the codes ************************************************************
    # beam_set = [[0]*building_1.geometry['number of X bay'] for story in range(building_1.geometry['number of story'])]
    # not_feasible_beam = []  # Used to record which beam [story, bay] does not have enough strength.
    # for story in range(building_1.geometry['number of story']):
    #     for bay in range(building_1.geometry['number of X bay']):
    #         length = building_1.geometry['X bay width']
    #         shear_demand = abs(elastic_demand.dominate_load['beam shear'][story, 2 * bay])
    #         moment_left = elastic_demand.dominate_load['beam moment'][story, 2 * bay]
    #         moment_right = elastic_demand.dominate_load['beam moment'][story, 2 * bay + 1]
    #         beam_set[story][bay] = Beam(building_1.member_size['beam'][story], length,
    #                                     shear_demand, moment_left, moment_right, steel)
    #         # Check the flag of each beam
    #         if not beam_set[story][bay].check_flag():
    #             sys.stderr.write('beam_%s%s is not feasible!!!\n' % (story, bay))
    #             not_feasible_beam.append([story, bay])
    #             # sys.exit(1)
    # ********************************** Refactor Ends **** ************************************************************

    # *******************************************************************
    # ////////// Revise Beam to Satisfy Strength Requirement ////////////
    # *******************************************************************
    for story in range(building_1.geometry['number of story']):
        for bay in range(building_1.geometry['number of X bay']):
            while not beam_set[story][bay].check_flag():
                # Upscale the unsatisfied beam
                building_1.upscale_beam(story)
                # Update modal period and seismic forces
                _ = ElasticAnalysis(building_1, for_drift_only=False, for_period_only=True)
                building_1.read_modal_period()
                building_1.compute_seismic_force()
                # Re-perform the elastic analysis to obtain the updated demand
                _ = ElasticAnalysis(building_1, for_drift_only=False, for_period_only=False)
                building_1.read_story_drift()
                elastic_demand = ElasticOutput(building_1)
                # Re-construct the beam objects
                beam_set, not_feasible_beam = create_beam_set(building_1, elastic_demand, steel)

    # ********************************** Refactor the codes ************************************************************
    # for [target_story_index, bay_no] in not_feasible_beam:
    #     while not beam_set[target_story_index][bay_no].check_flag():
    #         # Upscale the unsatisfied beam
    #         building_1.upscale_beam(target_story_index)
    #         # Update modal period and seismic forces
    #         model_1 = ElasticAnalysis(building_1, for_drift_only=False, for_period_only=True)
    #         building_1.read_modal_period()
    #         building_1.compute_seismic_force()
    #         # Re-perform the elastic analysis to obtain the updated demand
    #         model_1 = ElasticAnalysis(building_1, for_drift_only=False, for_period_only=False)
    #         building_1.read_story_drift()
    #         elastic_demand = ElasticOutput(building_1)
    #         # Re-construct the beam objects (only for those revised by previous upscale activity)
    #         for bay in range(building_1.geometry['number of X bay']):
    #             length = building_1.geometry['X bay width']
    #             shear_demand = abs(elastic_demand.dominate_load['beam shear'][target_story_index, 2 * bay])
    #             moment_left = elastic_demand.dominate_load['beam moment'][target_story_index, 2 * bay]
    #             moment_right = elastic_demand.dominate_load['beam moment'][target_story_index, 2 * bay + 1]
    #             beam_set[target_story_index][bay] = Beam(building_1.member_size['beam'][target_story_index], length,
    #                                                      shear_demand, moment_left, moment_right, steel)
    # ********************************** Refactor Ends **** ************************************************************

    # ********************************************************************
    # ///////////////// Check Beam-Column Connection /////////////////////
    # ********************************************************************

    connection_set, not_feasible_connection = create_connection_set(building_1, column_set, beam_set, steel)

    # ********************************** Refactor the codes ************************************************************
    # # Check each beam-column connection to see if they satisfy the AISC/ANSI
    # # Initialize a list to store all connection instances
    # connection_set = [[0] * (building_1.geometry['number of X bay'] + 1)
    #                   for story in range(building_1.geometry['number of story'])]
    # # Record which connection [story#, column#] is not feasible.
    # not_feasible_connection = []
    # for story in range(building_1.geometry['number of story']):
    #     for connection_no in range(building_1.geometry['number of X bay']+1):
    #         dead_load = building_1.gravity_loads['beam dead load'][story]  # Unit: lb/ft
    #         live_load = building_1.gravity_loads['beam live load'][story]  # Unit: lb/ft
    #         span = building_1.geometry['X bay width']  # Unit: ft
    #         if story != (building_1.geometry['number of story'] - 1):
    #             # The connection is not on roof
    #             if connection_no == 0:
    #                 # The connection is an exterior joint
    #                 connection_set[story][connection_no] = Connection('typical exterior',
    #                                                                   steel, dead_load, live_load, span,
    #                                                                   left_beam=beam_set[story][connection_no],
    #                                                                   right_beam=None,
    #                                                                   top_column=column_set[story + 1][connection_no],
    #                                                                   bottom_column=column_set[story][connection_no])
    #             elif connection_no == building_1.geometry['number of X bay']:
    #                 # The connection is an exterior joint
    #                 connection_set[story][connection_no] = Connection('typical exterior',
    #                                                                   steel, dead_load, live_load, span,
    #                                                                   left_beam=beam_set[story][connection_no-1],
    #                                                                   right_beam=None,
    #                                                                   top_column=column_set[story + 1][connection_no],
    #                                                                   bottom_column=column_set[story][connection_no])
    #             else:
    #                 # The connection is an interior joint
    #                 connection_set[story][connection_no] = Connection('typical interior',
    #                                                                   steel, dead_load, live_load, span,
    #                                                                   left_beam=beam_set[story][connection_no - 1],
    #                                                                   right_beam=beam_set[story][connection_no],
    #                                                                   top_column=column_set[story + 1][connection_no],
    #                                                                   bottom_column=column_set[story][connection_no])
    #         else:
    #             # The connection is not on roof
    #             if connection_no == 0:
    #                 # The connection is an left top exterior joint
    #                 connection_set[story][connection_no] = Connection('top exterior',
    #                                                                   steel, dead_load, live_load, span,
    #                                                                   left_beam=beam_set[story][connection_no],
    #                                                                   right_beam=None,
    #                                                                   top_column=None,
    #                                                                   bottom_column=column_set[story][connection_no])
    #             elif connection_no == building_1.geometry['number of X bay']:
    #                 # The connection is an right top exterior joint
    #                 connection_set[story][connection_no] = Connection('top exterior',
    #                                                                   steel, dead_load, live_load, span,
    #                                                                   left_beam=beam_set[story][connection_no-1],
    #                                                                   right_beam=None,
    #                                                                   top_column=None,
    #                                                                   bottom_column=column_set[story][connection_no])
    #
    #             else:
    #                 # The connection is an top interior joint
    #                 connection_set[story][connection_no] = Connection('top interior',
    #                                                                   steel, dead_load, live_load, span,
    #                                                                   left_beam=beam_set[story][connection_no],
    #                                                                   right_beam=beam_set[story][connection_no],
    #                                                                   top_column=None,
    #                                                                   bottom_column=column_set[story][connection_no])
    #         if not connection_set[story][connection_no].check_flag():
    #             sys.stderr.write('connection_%s%s is not feasible!!!\n' % (story, connection_no))
    #             not_feasible_connection.append([story, connection_no])
    #         #   sys.exit(1)
    # ********************************** Refactor Ends **** ************************************************************

    # ********************************************************************
    # ///////// Revise Member to Satisfy Connection Requirement //////////
    # ********************************************************************
    for story in range(building_1.geometry['number of story']):
        for connection_no in range(building_1.geometry['number of X bay'] + 1):
            while not connection_set[story][connection_no].is_feasible['geometry limits']:
                # This would never be achieved since all beams and columns have been selected from a database that
                # non-prequalified sizes have been removed.
                pass
            # For connection not satisfy the shear or flexural strength requirement -> upscale the beam
            while (not connection_set[story][connection_no].is_feasible['shear strength']) \
                    or (not connection_set[story][connection_no].is_feasible['flexural strength']):
                # Upscale the unsatisfied beam
                building_1.upscale_beam(story)
                # Update the modal period and seismic forces
                _ = ElasticAnalysis(building_1, for_drift_only=False, for_period_only=True)
                building_1.read_modal_period()
                building_1.compute_seismic_force()
                # Re-perform the elastic analysis to obtain the updated demand
                _ = ElasticAnalysis(building_1, for_drift_only=False, for_period_only=False)
                building_1.read_story_drift()
                elastic_demand = ElasticOutput(building_1)
                # Re-construct the beam objects
                beam_set, _ = create_beam_set(building_1, elastic_demand, steel)
                # Re-construct the column objects
                column_set, _ = create_column_set(building_1, elastic_demand, steel)
                # Re-construct the connection objects
                connection_set, _ = create_connection_set(building_1, column_set, beam_set, steel)
            # For connection not satisfy the strong-column-weak beam -> upscale the column
            while not connection_set[story][connection_no].is_feasible['SCWB']:
                # Not feasible connection -> go into loop
                # Determine which story should upscale
                # If it is roof connection which does not satisfy SCWB, we can only upscale top story column
                # because no column exists upper than roof.
                if story == building_1.geometry['number of story'] - 1:
                    target_story = story
                # If it is not roof connection: we need to see whether upper column is significantly smaller than
                # lower column. If that's the case, we should pick up the smaller upper column to upscale.
                else:
                    if (column_set[story + 1][connection_no].section['Zx']
                            < UPPER_LOWER_COLUMN_Zx * column_set[story][connection_no].section['Zx']):
                        target_story = story + 1
                    else:
                        target_story = story
                # Upscale the unsatisfied column on the determined story
                if connection_no == 0 or connection_no == building_1.geometry['number of X bay']:
                    type_column = 'exterior column'
                else:
                    type_column = 'interior column'
                building_1.upscale_column(target_story, type_column)
                # Update modal period and seismic forces
                _ = ElasticAnalysis(building_1, for_drift_only=False, for_period_only=True)
                building_1.read_modal_period()
                building_1.compute_seismic_force()
                # Re-perform the elastic analysis to obtain the updated demand
                _ = ElasticAnalysis(building_1, for_drift_only=False, for_period_only=False)
                building_1.read_story_drift()
                elastic_demand = ElasticOutput(building_1)
                # Re-construct the column objects since the demands are updated and columns are adjusted
                column_set, _ = create_column_set(building_1, elastic_demand, steel)
                # Re-construct the beam objects
                beam_set, _ = create_beam_set(building_1, elastic_demand, steel)
                # Re-construct the connection-objects
                connection_set, _ = create_connection_set(building_1, column_set, beam_set, steel)

    # ********************************** Refactor the codes ************************************************************
    # for [target_story_index, target_connection_no] in not_feasible_connection:
    #     # For connection not satisfy the geometry limit
    #     while not connection_set[target_story_index][target_connection_no].is_feasible['geometry limits']:
    #         # This would never be achieved as all beams and columns have been selected from a database that
    #         non-prequalified
    #         # sizes have been removed.
    #         pass
    #
    #     # For connection not satisfy the shear or flexural strength requirement -> upscale the beam
    #     while (not connection_set[target_story_index][target_connection_no].is_feasible['shear strength']) \
    #         or (not connection_set[target_story_index][target_connection_no].is_feasible['flexural strength']):
    #         # Upscale the unsatisfied beam
    #         building_1.upscale_beam(target_story_index)
    #         # Update the modal period and seismic forces
    #         model_1 = ElasticAnalysis(building_1, for_drift_only=False, for_period_only=True)
    #         building_1.read_modal_period()
    #         building_1.compute_seismic_force()
    #         # Re-perform the elastic analysis to obtain the updated demand
    #         model_1 = ElasticAnalysis(building_1, for_drift_only=False, for_period_only=False)
    #         building_1.read_story_drift()
    #         elastic_demand = ElasticOutput(building_1)
    #         # Re-construct the beam objects (only for those revised by previous upscale activity)
    #         for bay in range(building_1.geometry['number of X bay']):
    #             length = building_1.geometry['X bay width']
    #             shear_demand = abs(elastic_demand.dominate_load['beam shear'][target_story_index, 2 * bay])
    #             moment_left = elastic_demand.dominate_load['beam moment'][target_story_index, 2 * bay]
    #             moment_right = elastic_demand.dominate_load['beam moment'][target_story_index, 2 * bay + 1]
    #             beam_set[target_story_index][bay] = Beam(building_1.member_size['beam'][target_story_index], length,
    #                                                      shear_demand, moment_left, moment_right, steel)
    #         # Re-construct the connection objects (only for those affected by updated beam object)
    #         for story in range(target_story_index, target_story_index+1):
    #             for connection_no in range(building_1.geometry['number of X bay'] + 1):
    #                 # for connection_no in range(1, 2):
    #                 dead_load = building_1.gravity_loads['beam dead load'][story]  # Unit: lb/ft
    #                 live_load = building_1.gravity_loads['beam live load'][story]  # Unit: lb/ft
    #                 span = building_1.geometry['X bay width']  # Unit: ft
    #                 if story != (building_1.geometry['number of story'] - 1):
    #                     # The connection is not on roof
    #                     if connection_no == 0:
    #                         # The connection is an exterior joint
    #                         connection_set[story][connection_no] = Connection('typical exterior',
    #                                                                           steel, dead_load, live_load, span,
    #                                                                           left_beam=beam_set[story][connection_no],
    #                                                                           right_beam=None,
    #                                                                           top_column=column_set[story + 1][
    #                                                                               connection_no],
    #                                                                           bottom_column=column_set[story][
    #                                                                               connection_no])
    #                     elif connection_no == building_1.geometry['number of X bay']:
    #                         # The connection is an exterior joint
    #                         connection_set[story][connection_no] =
    #                         Connection('typical exterior', steel, dead_load, live_load, span,
    #                         left_beam=beam_set[story][connection_no - 1],
    #                         right_beam=None,
    #                         top_column=column_set[story + 1][connection_no],
    #                         bottom_column=column_set[story][connection_no])
    #                     else:
    #                         # The connection is an interior joint
    #                         connection_set[story][connection_no] =
    #                         Connection('typical interior',
    #                         steel, dead_load, live_load, span,
    #                         left_beam=beam_set[story][connection_no - 1],
    #                         right_beam=beam_set[story][connection_no],
    #                         top_column=column_set[story + 1][connection_no],
    #                         bottom_column=column_set[story][connection_no])
    #                 else:
    #                     # The connection is not on roof
    #                     if connection_no == 0:
    #                         # The connection is an left top exterior joint
    #                         connection_set[story][connection_no] = Connection('top exterior',
    #                                                                           steel, dead_load, live_load, span,
    #                                                                           left_beam=beam_set[story][connection_no],
    #                                                                           right_beam=None,
    #                                                                           top_column=None,
    #                                                                           bottom_column=column_set[story][
    #                                                                               connection_no])
    #                     elif connection_no == building_1.geometry['number of X bay']:
    #                         # The connection is an right top exterior joint
    #                         connection_set[story][connection_no] =
    #                         Connection('top exterior',
    #                         steel, dead_load, live_load, span,
    #                         left_beam=beam_set[story][connection_no - 1],
    #                         right_beam=None,
    #                         top_column=None,
    #                         bottom_column=column_set[story][connection_no])
    #
    #                     else:
    #                         # The connection is an top interior joint
    #                         connection_set[story][connection_no] = Connection('top interior',
    #                                                                steel, dead_load, live_load, span,
    #                                                                left_beam=beam_set[story][connection_no],
    #                                                                right_beam=beam_set[story][connection_no],
    #                                                                top_column=None,
    #                                                                bottom_column=column_set[story][
    #                                                                              connection_no])
    #
    #     i = 0
    #     # For connection not satisfy the strong-column-weak beam -> upscale the column
    #     while not connection_set[target_story_index][target_connection_no].is_feasible['SCWB']:
    #         # Not feasible connection -> go into loop
    #         # Determine which story should upscale
    #         # If it is roof connection which does not satisfy SCWB, we can only upscale top story column
    #         # because no column exists upper than roof.
    #         if target_story_index == building_1.geometry['number of story'] - 1:
    #             target_story = target_story_index
    #         # If it is not roof connection: we need to see whether upper column is significantly smaller
    #         than lower column. If that's the case, we should pick up the smaller upper column to upscale.
    #         else:
    #             if (column_set[target_story_index+1][target_connection_no].section['Zx']
    #                 < UPPER_LOWER_COLUMN_Zx*column_set[target_story_index][target_connection_no].section['Zx']):
    #                 target_story = target_story_index + 1
    #             else:
    #                 target_story = target_story_index
    #         # Upscale the unsatisfied column on the determined story
    #         if target_connection_no == 0 or target_connection_no == building_1.geometry['number of X bay']:
    #             type_column = 'exterior column'
    #         else:
    #             type_column = 'interior column'
    #         building_1.upscale_column(target_story, type_column)
    #         # Update modal period and seismic forces
    #         model_1 = ElasticAnalysis(building_1, for_drift_only=False, for_period_only=True)
    #         building_1.read_modal_period()
    #         building_1.compute_seismic_force()
    #         # Re-perform the elastic analysis to obtain the updated demand
    #         model_1 = ElasticAnalysis(building_1, for_drift_only=False, for_period_only=False)
    #         building_1.read_story_drift()
    #
    #
    #         # **************************** Debug Using Only *************************************
    #         i += 1
    #         print("Optimal member size after upscale column%i" % i)
    #         print("Exterior column:", building_1.member_size['exterior column'])
    #         print("Interior column:", building_1.member_size['interior column'])
    #         print("Beam:", building_1.member_size['beam'])
    #         print('After upscale column, current story drift is: ')
    #         print(building_1.elastic_response['story drift'] * 5.5 * 1.1 * 100)
    #         # **************************** Debug Ends Here **************************************
    #
    #
    #         elastic_demand = ElasticOutput(building_1)
    #         # Reconstruct the column objects in the target_story (only update those revised by the previous algorithm)
    #         for column_no in range(building_1.geometry['number of X bay'] + 1):
    #             axial_demand = abs(elastic_demand.dominate_load['column axial'][target_story, 2 * column_no])
    #             shear_demand = abs(elastic_demand.dominate_load['column shear'][target_story, 2 * column_no])
    #             moment_bottom = elastic_demand.dominate_load['column moment'][target_story, 2 * column_no]
    #             moment_top = elastic_demand.dominate_load['column moment'][target_story, 2 * column_no + 1]
    #             if column_no == 0 or column_no == building_1.geometry['number of X bay']:
    #                 column_type = 'exterior column'
    #             else:
    #                 column_type = 'interior column'
    #             length = np.asscalar(
    #                 building_1.geometry['floor height'][target_story + 1]
    #                 - building_1.geometry['floor height'][target_story])
    #             # Build instance for each column member
    #             column_set[target_story][column_no] = Column(building_1.member_size[column_type][target_story],
    #                                                          axial_demand, shear_demand, moment_bottom, moment_top,
    #                                                          length, length, steel)
    #         # Re-construct the connection-objects (only update the joint connections that the column connects)
    #         for story in range(target_story-1 >= 0, target_story+1):
    #             for connection_no in range(building_1.geometry['number of X bay'] + 1):
    #                 dead_load = building_1.gravity_loads['beam dead load'][story]  # Unit: lb/ft
    #                 live_load = building_1.gravity_loads['beam live load'][story]  # Unit: lb/ft
    #                 span = building_1.geometry['X bay width']  # Unit: ft
    #                 if story != (building_1.geometry['number of story'] - 1):
    #                     # The connection is not on roof
    #                     if connection_no == 0:
    #                         # The connection is an exterior joint
    #                         connection_set[story][connection_no] = Connection('typical exterior',
    #                                                                           steel, dead_load, live_load, span,
    #                                                                           left_beam=beam_set[story][connection_no],
    #                                                                           right_beam=None,
    #                                                                           top_column=column_set[story + 1][
    #                                                                               connection_no],
    #                                                                           bottom_column=column_set[story][
    #                                                                               connection_no])
    #                     elif connection_no == building_1.geometry['number of X bay']:
    #                         # The connection is an exterior joint
    #                         connection_set[story][connection_no] = Connection('typical exterior',
    #                                                                     steel, dead_load, live_load, span,
    #                                                                     left_beam=beam_set[story][connection_no - 1],
    #                                                                     right_beam=None,
    #                                                                     top_column=column_set[story + 1][
    #                                                                         connection_no],
    #                                                                     bottom_column=column_set[story][
    #                                                                         connection_no])
    #                     else:
    #                         # The connection is an interior joint
    #                         connection_set[story][connection_no] = Connection('typical interior',
    #                                                                     steel, dead_load, live_load, span,
    #                                                                     left_beam=beam_set[story][connection_no - 1],
    #                                                                     right_beam=beam_set[story][connection_no],
    #                                                                     top_column=column_set[story + 1][
    #                                                                         connection_no],
    #                                                                     bottom_column=column_set[story][
    #                                                                         connection_no])
    #                 else:
    #                     # The connection is not on roof
    #                     if connection_no == 0:
    #                         # The connection is an left top exterior joint
    #                         connection_set[story][connection_no] = Connection('top exterior',
    #                                                                           steel, dead_load, live_load, span,
    #                                                                           left_beam=beam_set[story][connection_no],
    #                                                                           right_beam=None,
    #                                                                           top_column=None,
    #                                                                           bottom_column=column_set[story][
    #                                                                               connection_no])
    #                     elif connection_no == building_1.geometry['number of X bay']:
    #                         # The connection is an right top exterior joint
    #                         connection_set[story][connection_no] = Connection('top exterior',
    #                                                                     steel, dead_load, live_load, span,
    #                                                                     left_beam=beam_set[story][connection_no - 1],
    #                                                                     right_beam=None,
    #                                                                     top_column=None,
    #                                                                     bottom_column=column_set[story][
    #                                                                           connection_no])
    #
    #                     else:
    #                         # The connection is an top interior joint
    #                         connection_set[story][connection_no] = Connection('top interior',
    #                                                                           steel, dead_load, live_load, span,
    #                                                                           left_beam=beam_set[story][connection_no],
    #                                                                           right_beam=beam_set[story][connection_no],
    #                                                                           top_column=None,
    #                                                                           bottom_column=column_set[story][
    #                                                                               connection_no])
    # ********************************** Refactor Ends **** ************************************************************

    # ********************************************************************
    # /////// Revise Beam Member to Consider Constructability ////////////
    # ********************************************************************
    # After performing all checks, finalize the design by considering constructability
    # building_1.constructability()
    # Adjust beam for constructability
    building_1.constructability_beam()
    # Define a new building object to copy the construction size into member size
    building_2 = copy.deepcopy(building_1)
    building_2.member_size = copy.deepcopy(building_1.construction_size)
    # Update modal period and seismic forces
    _ = ElasticAnalysis(building_2, for_drift_only=False, for_period_only=True)
    building_2.read_modal_period()
    building_2.compute_seismic_force()
    # Perform elastic analysis for member sizes after adjustment for constructability
    _ = ElasticAnalysis(building_2, for_drift_only=False, for_period_only=False)
    building_2.read_story_drift()
    # Read elastic analysis results
    elastic_demand_2 = ElasticOutput(building_2)

    # Construct new beam objects after considering constructability
    construction_beam_set, not_feasible_beam = create_beam_set(building_2, elastic_demand_2, steel)

    # Construct new column objects after considering constructability
    construction_column_set, not_feasible_column = create_column_set(building_2, elastic_demand_2, steel)

    # ********************************** Refactor the codes ************************************************************
    # # Construct new beam objects after considering constructability
    # construction_beam_set = [[0] * building_2.geometry['number of X bay']
    #                          for story in range(building_2.geometry['number of story'])]
    # for story in range(building_2.geometry['number of story']):
    #     for bay in range(building_2.geometry['number of X bay']):
    #         length = building_2.geometry['X bay width']
    #         shear_demand = abs(elastic_demand_2.dominate_load['beam shear'][story, 2 * bay])
    #         moment_left = elastic_demand_2.dominate_load['beam moment'][story, 2 * bay]
    #         moment_right = elastic_demand_2.dominate_load['beam moment'][story, 2 * bay + 1]
    #         construction_beam_set[story][bay] = Beam(building_2.member_size['beam'][story], length,
    #                                                  shear_demand, moment_left, moment_right, steel)
    #         # Check the flag of each beam (might not be necessary)
    #         if not construction_beam_set[story][bay].check_flag():
    #             sys.stderr.write('Construction beam_%s%s is not feasible!!!\n' % (story, bay))

    # # Construct new column objects after considering constructability
    # construction_column_set = [[0] * (building_2.geometry['number of X bay'] + 1)
    #                            for story in range(building_2.geometry['number of story'])]
    # for story in range(building_2.geometry['number of story']):
    #     for column_no in range(building_2.geometry['number of X bay'] + 1):
    #         axial_demand = abs(elastic_demand_2.dominate_load['column axial'][story, 2 * column_no])
    #         shear_demand = abs(elastic_demand_2.dominate_load['column shear'][story, 2 * column_no])
    #         moment_bottom = elastic_demand_2.dominate_load['column moment'][story, 2 * column_no]
    #         moment_top = elastic_demand_2.dominate_load['column moment'][story, 2 * column_no + 1]
    #         if column_no == 0 or column_no == building_2.geometry['number of X bay']:
    #             column_type = 'exterior column'
    #         else:
    #             column_type = 'interior column'
    #         length = np.asscalar(
    #             building_2.geometry['floor height'][story + 1] - building_2.geometry['floor height'][story])
    #         # Build instance for each column member
    #         construction_column_set[story][column_no] = Column(building_2.member_size[column_type][story],
    #                                                            axial_demand, shear_demand, moment_bottom, moment_top,
    #                                                            length, length, steel)
    #         # Check the flag of each column (May not be necessary)
    #         if not construction_column_set[story][column_no].check_flag():
    #             sys.stderr.write('Construction column_%s%s is not feasible!!!\n' % (story, column_no))
    # ********************************** Refactor Ends **** ************************************************************

    # ********************************************************************
    # /// Revise Column to SCWB  after Adjusting Beam Constructability ///
    # ********************************************************************

    construction_connection_set, not_feasible_construction_connection = \
        create_connection_set(building_2, construction_column_set, construction_beam_set, steel)

    # Revise column sizes for new construction connection because of SCWB
    for story in range(building_2.geometry['number of story']):
        for connection_no in range(building_1.geometry['number of X bay'] + 1):
            while not construction_connection_set[story][connection_no].is_feasible['geometry limits']:
                # This would never be achieved as all beams and columns have been selected from a database that
                # non-prequalified sizes have been removed.
                pass
            # For connection not satisfy the shear or flexural strength requirement -> upscale the beam
            while ((not construction_connection_set[story][connection_no].is_feasible['shear strength'])
                   or (not construction_connection_set[story][connection_no].is_feasible['flexural strength'])):
                # Upscale the unsatisfied beam
                building_2.upscale_beam(story)
                # Update modal period and seismic forces
                _ = ElasticAnalysis(building_2, for_drift_only=False, for_period_only=True)
                building_2.read_modal_period()
                building_2.compute_seismic_force()
                # Re-perform the elastic analysis to obtain the updated demand
                _ = ElasticAnalysis(building_2, for_drift_only=False, for_period_only=False)
                building_2.read_story_drift()
                elastic_demand_2 = ElasticOutput(building_2)
                # Re-construct the beam objects
                construction_beam_set, _ = create_beam_set(building_2, elastic_demand_2, steel)
                # Re-construct the column objects
                construction_column_set, _ = create_column_set(building_2, elastic_demand_2, steel)
                # Re-construct the connection objects
                construction_connection_set, _ = create_connection_set(building_2, elastic_demand_2, steel)
            # For connection not satisfy the strong-column-weak beam -> upscale the column
            while not construction_connection_set[story][connection_no].is_feasible['SCWB']:
                # Not feasible connection -> go into loop
                # Determine which story should upscale
                # If it is roof connection which does not satisfy SCWB, we can only upscale top story column
                # because no column exists upper than roof.
                if story == building_2.geometry['number of story'] - 1:
                    target_story = story
                # If it is not roof connection: we need to see whether upper column is significantly smaller than lower
                # column. If that's the case, we should pick up the smaller upper column to upscale.
                else:
                    if (column_set[story + 1][connection_no].section['Zx']
                            < UPPER_LOWER_COLUMN_Zx * column_set[story][connection_no].section['Zx']):
                        target_story = story + 1
                    else:
                        target_story = story
                # Upscale the unsatisfied column on the determined story
                if connection_no == 0 or connection_no == building_2.geometry['number of X bay']:
                    type_column = 'exterior column'
                else:
                    type_column = 'interior column'
                building_2.upscale_column(target_story, type_column)
                # Update modal period and seismic forces
                _ = ElasticAnalysis(building_2, for_drift_only=False, for_period_only=True)
                building_2.read_modal_period()
                building_2.compute_seismic_force()
                # Re-perform the elastic analysis to obtain the updated demand
                _ = ElasticAnalysis(building_2, for_drift_only=False, for_period_only=False)
                building_2.read_story_drift()
                elastic_demand_2 = ElasticOutput(building_2)
                # Re-construct the column objects
                construction_column_set, _ = create_column_set(building_2, elastic_demand_2, steel)
                # Re-construct the beam objects
                construction_beam_set, _ = create_beam_set(building_2, elastic_demand_2, steel)
                # Re-construct the connection objects
                construction_connection_set, _ = \
                    create_connection_set(building_2, construction_column_set, construction_beam_set, steel)

    # ********************************** Refactor the codes ************************************************************
    # # Construct new connection objects after considering constructability
    # construction_connection_set = [[0] * (building_2.geometry['number of X bay'] + 1)
    #                                for story in range(building_2.geometry['number of story'])]
    # not_feasible_construction_connection = []
    # for story in range(building_2.geometry['number of story']):
    #     for connection_no in range(building_2.geometry['number of X bay']+1):
    #         dead_load = building_2.gravity_loads['beam dead load'][story]  # Unit: lb/ft
    #         live_load = building_2.gravity_loads['beam live load'][story]  # Unit: lb/ft
    #         span = building_2.geometry['X bay width']  # Unit: ft
    #         if story != (building_2.geometry['number of story'] - 1):
    #             # The connection is not on roof
    #             if connection_no == 0:
    #                 # The connection is an exterior joint
    #                 construction_connection_set[story][connection_no] \
    #                     = Connection('typical exterior', steel, dead_load, live_load, span,
    #                                  left_beam=construction_beam_set[story][connection_no],
    #                                  right_beam=None,
    #                                  top_column=construction_column_set[story + 1][connection_no],
    #                                  bottom_column=construction_column_set[story][connection_no])
    #             elif connection_no == building_2.geometry['number of X bay']:
    #                 # The connection is an exterior joint
    #                 construction_connection_set[story][connection_no] \
    #                     = Connection('typical exterior',
    #                                  steel, dead_load, live_load, span,
    #                                  left_beam=construction_beam_set[story][connection_no-1],
    #                                  right_beam=None,
    #                                  top_column=construction_column_set[story + 1][connection_no],
    #                                  bottom_column=construction_column_set[story][connection_no])
    #             else:
    #                 # The connection is an interior joint
    #                 construction_connection_set[story][connection_no] \
    #                     = Connection('typical interior',
    #                                  steel, dead_load, live_load, span,
    #                                  left_beam=construction_beam_set[story][connection_no - 1],
    #                                  right_beam=construction_beam_set[story][connection_no],
    #                                  top_column=construction_column_set[story + 1][connection_no],
    #                                  bottom_column=construction_column_set[story][connection_no])
    #         else:
    #             # The connection is not on roof
    #             if connection_no == 0:
    #                 # The connection is an left top exterior joint
    #                 construction_connection_set[story][connection_no] \
    #                     = Connection('top exterior',
    #                                  steel, dead_load, live_load, span,
    #                                  left_beam=construction_beam_set[story][connection_no],
    #                                  right_beam=None,
    #                                  top_column=None,
    #                                  bottom_column=construction_column_set[story][connection_no])
    #             elif connection_no == building_2.geometry['number of X bay']:
    #                 # The connection is an right top exterior joint
    #                 construction_connection_set[story][connection_no] \
    #                     = Connection('top exterior',
    #                                  steel, dead_load, live_load, span,
    #                                  left_beam=construction_beam_set[story][connection_no-1],
    #                                  right_beam=None,
    #                                  top_column=None,
    #                                  bottom_column=construction_column_set[story][connection_no])
    #             else:
    #                 # The connection is an top interior joint
    #                 construction_connection_set[story][connection_no] \
    #                     = Connection('top interior',
    #                                  steel, dead_load, live_load, span,
    #                                  left_beam=construction_beam_set[story][connection_no],
    #                                  right_beam=construction_beam_set[story][connection_no],
    #                                  top_column=None,
    #                                  bottom_column=construction_column_set[story][connection_no])
    #         if not construction_connection_set[story][connection_no].check_flag():  # (Might not be necessary)
    #             sys.stderr.write('Construction connection_%s%s is not feasible!!!\n' % (story, connection_no))
    #             not_feasible_construction_connection.append([story, connection_no])

    # # Revise column sizes for new construction connection because of SCWB
    # for [target_story_index, target_connection_no] in not_feasible_construction_connection:
    #     # For connection not satisfy the geometry limit
    #     while not construction_connection_set[target_story_index][target_connection_no].is_feasible['geometry limits']:
    #         # This would never be achieved as all beams and columns have been selected from a database that
    #         on-prequalified sizes have been removed.
    #         pass
    #
    #     # For connection not satisfy the shear or flexural strength requirement -> upscale the beam
    #     while (not construction_connection_set[target_story_index][target_connection_no].is_feasible['shear strength']) \
    #         or (not construction_connection_set[target_story_index][target_connection_no].is_feasible['flexural strength']):
    #         # Upscale the unsatisfied beam
    #         building_2.upscale_beam(target_story_index)
    #         # Update modal period and seismic forces
    #         model_2 = ElasticAnalysis(building_2, for_drift_only=False, for_period_only=True)
    #         building_2.read_modal_period()
    #         building_2.compute_seismic_force()
    #         # Re-perform the elastic analysis to obtain the updated demand
    #         model_2 = ElasticAnalysis(building_2, for_drift_only=False, for_period_only=False)
    #         building_2.read_story_drift()
    #         elastic_demand_2 = ElasticOutput(building_2)
    #         # Re-construct the beam objects (only for those revised by previous upscale activity)
    #         for bay in range(building_2.geometry['number of X bay']):
    #             length = building_2.geometry['X bay width']
    #             shear_demand = abs(elastic_demand_2.dominate_load['beam shear'][target_story_index, 2 * bay])
    #             moment_left = elastic_demand_2.dominate_load['beam moment'][target_story_index, 2 * bay]
    #             moment_right = elastic_demand_2.dominate_load['beam moment'][target_story_index, 2 * bay + 1]
    #             construction_beam_set[target_story_index][bay] =
    #             Beam(building_1.member_size['beam'][target_story_index],
    #                                                                   length, shear_demand,
    #                                                                   moment_left, moment_right, steel)
    #         # Re-construct the connection objects (only for those affected by updated beam object)
    #         for story in range(target_story_index, target_story_index+1):
    #             for connection_no in range(building_2.geometry['number of X bay'] + 1):
    #                 # for connection_no in range(1, 2):
    #                 dead_load = building_2.gravity_loads['beam dead load'][story]  # Unit: lb/ft
    #                 live_load = building_2.gravity_loads['beam live load'][story]  # Unit: lb/ft
    #                 span = building_2.geometry['X bay width']  # Unit: ft
    #                 if story != (building_2.geometry['number of story'] - 1):
    #                     # The connection is not on roof
    #                     if connection_no == 0:
    #                         # The connection is an exterior joint
    #                         construction_connection_set[story][connection_no] \
    #                             = Connection('typical exterior', steel, dead_load, live_load, span,
    #                                          left_beam=construction_beam_set[story][connection_no], right_beam=None,
    #                                          top_column=construction_column_set[story + 1][connection_no],
    #                                          bottom_column=construction_column_set[story][connection_no])
    #                     elif connection_no == building_2.geometry['number of X bay']:
    #                         # The connection is an exterior joint
    #                         construction_connection_set[story][connection_no] \
    #                             = Connection('typical exterior', steel, dead_load, live_load, span,
    #                                          left_beam=construction_beam_set[story][connection_no - 1],
    #                                          right_beam=None,
    #                                          top_column=construction_column_set[story + 1][connection_no],
    #                                          bottom_column=construction_column_set[story][connection_no])
    #                     else:
    #                         # The connection is an interior joint
    #                         construction_connection_set[story][connection_no] \
    #                             = Connection('typical interior', steel, dead_load, live_load, span,
    #                                          left_beam=construction_beam_set[story][connection_no - 1],
    #                                          right_beam=construction_beam_set[story][connection_no],
    #                                          top_column=construction_column_set[story + 1][connection_no],
    #                                          bottom_column=construction_column_set[story][connection_no])
    #                 else:
    #                     # The connection is not on roof
    #                     if connection_no == 0:
    #                         # The connection is an left top exterior joint
    #                         construction_connection_set[story][connection_no] \
    #                             = Connection('top exterior', steel, dead_load, live_load, span,
    #                                          left_beam=construction_beam_set[story][connection_no],
    #                                          right_beam=None,
    #                                          top_column=None,
    #                                          bottom_column=construction_column_set[story][connection_no])
    #                     elif connection_no == building_2.geometry['number of X bay']:
    #                         # The connection is an right top exterior joint
    #                         construction_connection_set[story][connection_no] \
    #                             = Connection('top exterior', steel, dead_load, live_load, span,
    #                                          left_beam=construction_beam_set[story][connection_no - 1],
    #                                          right_beam=None,
    #                                          top_column=None,
    #                                          bottom_column=construction_column_set[story][connection_no])
    #
    #                     else:
    #                         # The connection is an top interior joint
    #                         construction_connection_set[story][connection_no] \
    #                             = Connection('top interior',
    #                                          steel, dead_load, live_load, span,
    #                                          left_beam=construction_beam_set[story][connection_no],
    #                                          right_beam=construction_beam_set[story][connection_no],
    #                                          top_column=None,
    #                                          bottom_column=construction_column_set[story][connection_no])
    #
    #     i = 0
    #     # For connection not satisfy the strong-column-weak beam -> upscale the column
    #     while not construction_connection_set[target_story_index][target_connection_no].is_feasible['SCWB']:
    #         Not feasible connection -> go into loop
    #         # Determine which story should upscale
    #         # If it is roof connection which does not satisfy SCWB, we can only upscale top story column
    #         # because no column exists upper than roof.
    #         if target_story_index == building_2.geometry['number of story'] - 1:
    #             target_story = target_story_index
    #         # If it is not roof connection: we need to see whether upper column is significantly smaller than lower
    #         column. If that's the case, we should pick up the smaller upper column to upscale.
    #         else:
    #             if (column_set[target_story_index+1][target_connection_no].section['Zx']
    #                 < UPPER_LOWER_COLUMN_Zx*column_set[target_story_index][target_connection_no].section['Zx']):
    #                 target_story = target_story_index + 1
    #             else:
    #                 target_story = target_story_index
    #         # Upscale the unsatisfied column on the determined story
    #         if target_connection_no == 0 or target_connection_no == building_2.geometry['number of X bay']:
    #             type_column = 'exterior column'
    #         else:
    #             type_column = 'interior column'
    #         building_2.upscale_column(target_story, type_column)
    #         # Update modal period and seismic forces
    #         model_2 = ElasticAnalysis(building_2, for_drift_only=False, for_period_only=True)
    #         building_2.read_modal_period()
    #         building_2.compute_seismic_force()
    #         # Re-perform the elastic analysis to obtain the updated demand
    #         model_2 = ElasticAnalysis(building_2, for_drift_only=False, for_period_only=False)
    #         building_2.read_story_drift()
    #
    #
    #         # **************************** Debug Using Only *************************************
    #         i += 1
    #         print("Construction#1 member size after upscale column%i" % iteration)
    #         print("Exterior column:", building_1.member_size['exterior column'])
    #         print("Interior column:", building_1.member_size['interior column'])
    #         print("Beam:", building_1.member_size['beam'])
    #         print('After upscale column, current story drift is: ')
    #         print(building_1.elastic_response['story drift'] * 5.5 * 1.1 * 100)
    #         # **************************** Debug Ends Here **************************************
    #
    #
    #
    #         elastic_demand_2 = ElasticOutput(building_2)
    #         # Re-construct the column objects in the target_story (only update those revised by the previous algorithm)
    #         for column_no in range(building_2.geometry['number of X bay'] + 1):
    #             axial_demand = abs(elastic_demand_2.dominate_load['column axial'][target_story, 2 * column_no])
    #             shear_demand = abs(elastic_demand_2.dominate_load['column shear'][target_story, 2 * column_no])
    #             moment_bottom = elastic_demand_2.dominate_load['column moment'][target_story, 2 * column_no]
    #             moment_top = elastic_demand_2.dominate_load['column moment'][target_story, 2 * column_no + 1]
    #             if column_no == 0 or column_no == building_1.geometry['number of X bay']:
    #                 column_type = 'exterior column'
    #             else:
    #                 column_type = 'interior column'
    #             length = np.asscalar(
    #                 building_1.geometry['floor height'][target_story + 1]
    #                 - building_1.geometry['floor height'][target_story])
    #             # Build instance for each column member
    #             construction_column_set[target_story][column_no] \
    #                 = Column(building_2.member_size[column_type][target_story], axial_demand, shear_demand,
    #                          moment_bottom, moment_top, length, length, steel)
    #         # Re-construct the connection-objects (only update the joint connections that the column connects)
    #         for story in range(target_story-1 >= 0, target_story+1):
    #             for connection_no in range(building_2.geometry['number of X bay'] + 1):
    #                 dead_load = building_2.gravity_loads['beam dead load'][story]  # Unit: lb/ft
    #                 live_load = building_2.gravity_loads['beam live load'][story]  # Unit: lb/ft
    #                 span = building_2.geometry['X bay width']  # Unit: ft
    #                 if story != (building_2.geometry['number of story'] - 1):
    #                     # The connection is not on roof
    #                     if connection_no == 0:
    #                         # The connection is an exterior joint
    #                         construction_connection_set[story][connection_no] \
    #                             = Connection('typical exterior',
    #                                          steel, dead_load, live_load, span,
    #                                          left_beam=construction_beam_set[story][connection_no],
    #                                          right_beam=None,
    #                                          top_column=construction_column_set[story + 1][connection_no],
    #                                          bottom_column=construction_column_set[story][connection_no])
    #                     elif connection_no == building_2.geometry['number of X bay']:
    #                         # The connection is an exterior joint
    #                         construction_connection_set[story][connection_no] \
    #                             = Connection('typical exterior', steel, dead_load, live_load, span,
    #                                          left_beam=construction_beam_set[story][connection_no - 1],
    #                                          right_beam=None,
    #                                          top_column=construction_column_set[story + 1][connection_no],
    #                                          bottom_column=construction_column_set[story][connection_no])
    #                     else:
    #                         # The connection is an interior joint
    #                         construction_connection_set[story][connection_no] \
    #                             = Connection('typical interior', steel, dead_load, live_load, span,
    #                                          left_beam=construction_beam_set[story][connection_no - 1],
    #                                          right_beam=construction_beam_set[story][connection_no],
    #                                          top_column=construction_column_set[story + 1][connection_no],
    #                                          bottom_column=construction_column_set[story][connection_no])
    #                 else:
    #                     # The connection is not on roof
    #                     if connection_no == 0:
    #                         # The connection is an left top exterior joint
    #                         connection_set[story][connection_no] \
    #                             = Connection('top exterior', steel, dead_load, live_load, span,
    #                                          left_beam=construction_beam_set[story][connection_no],
    #                                          right_beam=None,
    #                                          top_column=None,
    #                                          bottom_column=construction_column_set[story][connection_no])
    #                     elif connection_no == building_2.geometry['number of X bay']:
    #                         # The connection is an right top exterior joint
    #                         construction_connection_set[story][connection_no] \
    #                             = Connection('top exterior', steel, dead_load, live_load, span,
    #                                          left_beam=construction_beam_set[story][connection_no - 1],
    #                                          right_beam=None,
    #                                          top_column=None,
    #                                          bottom_column=construction_column_set[story][connection_no])
    #                     else:
    #                         # The connection is an top interior joint
    #                         construction_connection_set[story][connection_no] \
    #                             = Connection('top interior', steel, dead_load, live_load, span,
    #                                          left_beam=construction_beam_set[story][connection_no],
    #                                          right_beam=construction_beam_set[story][connection_no],
    #                                          top_column=None,
    #                                          bottom_column=construction_column_set[story][connection_no])
    # ********************************** Refactor Ends **** ************************************************************

    # ********************************************************************
    # ////////////// Revise Column to for Constructability  //////////////
    # ********************************************************************

    # building_1.member_size is optimal design results.
    # building_1.construction_size is after adjusting beam for constructability.
    # building_2.member_size is firstly the same as building_1.construction_size
    # then consider the SCWB requirement to update column based on construction beam
    # building_2.construction_size is consider column constructability, which is construction sizes.
    # To facilitate elastic analysis, building_3 is created.
    # building_3.member_size is final construction results.

    # All construction sizes have been stored in building_3
    building_2.constructability_column()
    building_3 = copy.deepcopy(building_2)
    building_3.member_size = copy.deepcopy(building_2.construction_size)
    # Update modal period and seismic forces
    _ = ElasticAnalysis(building_3, for_drift_only=False, for_period_only=True)
    building_3.read_modal_period()
    building_3.compute_seismic_force()

    # Perform elastic analysis for construction sizes
    _ = ElasticAnalysis(building_3, for_drift_only=False, for_period_only=False)
    building_3.read_story_drift()
    # Obtain the elastic response
    elastic_demand_3 = ElasticOutput(building_3)

    # Re-create column, beam, and connection objects after adjusting the column
    construction_column_set, not_feasible_construction_column = create_column_set(building_3, elastic_demand_3, steel)
    construction_beam_set, not_feasible_construction_beam = create_beam_set(building_3, elastic_demand_3, steel)
    construction_connection_set, not_feasible_construction_connection = \
        create_connection_set(building_3, construction_column_set, construction_beam_set, steel)

    # ********************************** Refactor the codes ************************************************************
    # # Re-create column after adjusting the column
    # for story in range(building_3.geometry['number of story']):
    #     for column_no in range(building_3.geometry['number of X bay'] + 1):
    #         axial_demand = abs(elastic_demand_3.dominate_load['column axial'][story, 2 * column_no])
    #         shear_demand = abs(elastic_demand_3.dominate_load['column shear'][story, 2 * column_no])
    #         moment_bottom = elastic_demand_3.dominate_load['column moment'][story, 2 * column_no]
    #         moment_top = elastic_demand_3.dominate_load['column moment'][story, 2 * column_no + 1]
    #         if column_no == 0 or column_no == building_3.geometry['number of X bay']:
    #             column_type = 'exterior column'
    #         else:
    #             column_type = 'interior column'
    #         length = np.asscalar(
    #             building_3.geometry['floor height'][story + 1] - building_3.geometry['floor height'][story])
    #         # Build instance for each column member
    #         construction_column_set[story][column_no] = Column(building_3.member_size[column_type][story],
    #                                                            axial_demand, shear_demand, moment_bottom, moment_top,
    #                                                            length, length, steel)
    #         # Check the flag of each column (May not be necessary)
    #         if not construction_column_set[story][column_no].check_flag():
    #             sys.stderr.write('Construction column_%s%s is not feasible!!!\n' % (story, column_no))
    #
    # # Re-create connection objects after adjusting column
    # for story in range(building_3.geometry['number of story']):
    #     for column_no in range(building_3.geometry['number of X bay'] + 1):
    #         axial_demand = abs(elastic_demand_3.dominate_load['column axial'][story, 2 * column_no])
    #         shear_demand = abs(elastic_demand_3.dominate_load['column shear'][story, 2 * column_no])
    #         moment_bottom = elastic_demand_3.dominate_load['column moment'][story, 2 * column_no]
    #         moment_top = elastic_demand_3.dominate_load['column moment'][story, 2 * column_no + 1]
    #         if column_no == 0 or column_no == building_3.geometry['number of X bay']:
    #             column_type = 'exterior column'
    #         else:
    #             column_type = 'interior column'
    #         length = np.asscalar(
    #             building_3.geometry['floor height'][story + 1] - building_3.geometry['floor height'][story])
    #         # Build instance for each column member
    #         construction_column_set[story][column_no] = Column(building_3.member_size[column_type][story],
    #                                                            axial_demand, shear_demand, moment_bottom, moment_top,
    #                                                            length, length, steel)
    #         # Check the flag of each column (May not be necessary)
    #         if not construction_column_set[story][column_no].check_flag():
    #             sys.stderr.write('Construction column_%s%s is not feasible!!!\n' % (story, column_no))
    # ********************************** Refactor Ends **** ************************************************************

    # ********************************************************************
    # //////////// Check Column Width Greater than Beam //////////////////
    # ********************************************************************
    for story in range(0, building_3.geometry['number of story']):
        for col_no in range(0, building_3.geometry['number of X bay']+1):
            if construction_column_set[story][col_no].section['bf'] < construction_beam_set[story][0].section['bf']:
                print("Column width in Story %i is less than beam" % story)

    # ********************************************************************
    # ///////////////// Store Design Results /////////////////////////////
    # ********************************************************************
    # building_1: all optimal design results
    # building_3: construction design results

    # Change the working directory to building data
    os.chdir(building_1.directory['building data'])

    # Nonlinear model generation may require information for building, beam/column hinge, and panel zone thickness.
    # Store the building class to "building.pkl"
    with open('optimal_building.pkl', 'wb') as output_file:
        pickle.dump(building_1, output_file)

    with open('construction_building.pkl', 'wb') as output_file:
        pickle.dump(building_3, output_file)

    # Store the beam set to "beam_set.pkl"
    with open('optimal_beam_set.pkl', 'wb') as output_file:
        pickle.dump(beam_set, output_file)

    # Store the column set to "column_set.pkl"
    with open('optimal_column_set.pkl', 'wb') as output_file:
        pickle.dump(column_set, output_file)

    # Store the connection set to "connection_set.pkl"
    with open('optimal_connection_set.pkl', 'wb') as output_file:
        pickle.dump(connection_set, output_file)

    # Store the construction beam set
    with open('construction_beam_set.pkl', 'wb') as output_file:
        pickle.dump(construction_beam_set, output_file)

    # Store the construction column set
    with open('construction_column_set.pkl', 'wb') as output_file:
        pickle.dump(construction_column_set, output_file)

    with open('construction_connection_set.pkl', 'wb') as output_file:
        pickle.dump(construction_connection_set, output_file)

    # Store the member sizes and story drift into csv files.
    optimal_member_size = pd.DataFrame(data=np.column_stack([building_1.member_size['exterior column'],
                                                             building_1.member_size['interior column'],
                                                             building_1.member_size['beam']]),
                                       columns=['exterior column', 'interior column', 'beam'])
    construction_size = pd.DataFrame(data=np.column_stack([building_3.construction_size['exterior column'],
                                                           building_3.construction_size['interior column'],
                                                           building_3.construction_size['beam']]),
                                     columns=['exterior column', 'interior column', 'beam'])
    optimal_drift = pd.DataFrame(data=building_1.elastic_response['story drift'], columns=['story drift'])
    construction_drift = pd.DataFrame(data=building_3.elastic_response['story drift'], columns=['story drift'])
    optimal_member_size.to_csv('OptimalMemberSize.csv', sep=',', index=False)
    construction_size.to_csv('ConstructionSize.csv', sep=',', index=False)
    optimal_drift.to_csv('OptimalStoryDrift.csv', sep=',', index=False)
    construction_drift.to_csv('ConstructionDrift.csv', sep=',', index=False)

    # Store the doubler plate thickness
    header = ['connection %s' % bay for bay in range(building_1.geometry['number of X bay']+1)]
    # Initialize the dataframe to store doubler plate thickness
    optimal_doubler_plate = pd.DataFrame(columns=header)
    construction_doubler_plate = pd.DataFrame(columns=header)
    # Fill this two dataframes
    for row in range(building_1.geometry['number of story']):
        for col in range(building_1.geometry['number of X bay']+1):
            name = header[col]
            optimal_doubler_plate.loc[row, name] = connection_set[row][col].doubler_plate_thickness
            construction_doubler_plate.loc[row, name] = construction_connection_set[row][col].doubler_plate_thickness
    optimal_doubler_plate.to_csv('OptimalDoublerPlate.csv', sep=',', index=False)
    construction_doubler_plate.to_csv('ConstructionDoublerPlate.csv', sep=',', index=False)

    # Store the strong column beam ratio
    header = ['joint %s' % bay for bay in range(building_1.geometry['number of X bay'] + 1)]
    # Initialize the dataframe using the headers defined above
    optimal_column_beam_ratio = pd.DataFrame(columns=header)
    construction_column_beam_ratio = pd.DataFrame(columns=header)
    # Fill this dataframe
    for row in range(building_1.geometry['number of story']):
        for col in range(building_1.geometry['number of X bay'] + 1):
            name = header[col]
            if row == building_1.geometry['number of story'] - 1:
                optimal_column_beam_ratio.loc[row, name] = 'NA'
                construction_column_beam_ratio.loc[row, name] = 'NA'
            else:
                optimal_column_beam_ratio.loc[row, name] = \
                    connection_set[row][col].moment['Mpc'] \
                    / connection_set[row][col].moment['Mpb']
                construction_column_beam_ratio.loc[row, name] = \
                    construction_connection_set[row][col].moment['Mpc'] \
                    / construction_connection_set[row][col].moment['Mpb']
    optimal_column_beam_ratio.to_csv('OptimalColumnBeamRatio.csv', sep=',', index=False)
    construction_column_beam_ratio.to_csv('ConstructionColumnBeamRatio.csv', sep=',', index=False)

    # Store the demand to capacity ratio for columns
    # Define the headers for the columns DC ratio
    header = ['column %s' % bay for bay in range(building_1.geometry['number of X bay'] + 1)]
    force_list = ['axial', 'shear', 'flexural']
    for force in force_list:
        column_DC = [[0] * (building_1.geometry['number of X bay'] + 1)
                     for _ in range(building_1.geometry['number of story'])]
        construction_column_DC = [[0] * (building_1.geometry['number of X bay'] + 1)
                                  for _ in range(building_1.geometry['number of story'])]
        for story in range(0, building_1.geometry['number of story']):
            for bay in range(0, building_1.geometry['number of X bay']+1):
                column_DC[story][bay] = column_set[story][bay].demand_capacity_ratio[force]
                construction_column_DC[story][bay] = construction_column_set[story][bay].demand_capacity_ratio[force]
        file_name = 'OptimalColumn' + force[0].upper() + force[1:] + 'DCRatio.csv'
        (pd.DataFrame(columns=header, data=column_DC)).to_csv(file_name, sep=',', index=False)
        file_name = 'ConstructionColumn' + force[0].upper() + force[1:] + 'DCRatio.csv'
        (pd.DataFrame(columns=header, data=construction_column_DC).to_csv(file_name, sep=',', index=False))

    # Store the demand to capacity ratio for beams
    # Define the headers for the beams DC ratio
    header = ['beam %s' % bay for bay in range(building_1.geometry['number of X bay'])]
    force_list = ['shear', 'flexural']
    for force in force_list:
        beam_DC = [[0] * (building_1.geometry['number of X bay'])
                   for _ in range(building_1.geometry['number of story'])]
        construction_beam_DC = [[0] * (building_1.geometry['number of X bay'])
                                for _ in range(building_1.geometry['number of story'])]
        for story in range(0, building_1.geometry['number of story']):
            for bay in range(0, building_1.geometry['number of X bay']):
                beam_DC[story][bay] = beam_set[story][bay].demand_capacity_ratio[force]
                construction_beam_DC[story][bay] = construction_beam_set[story][bay].demand_capacity_ratio[force]
        file_name = 'OptimalBeam' + force[0].upper() + force[1:] + 'DCRatio.csv'
        (pd.DataFrame(columns=header, data=beam_DC)).to_csv(file_name, sep=',', index=False)
        file_name = 'ConstructionBeam' + force[0].upper() + force[1:] + 'DCRatio.csv'
        (pd.DataFrame(columns=header, data=construction_beam_DC).to_csv(file_name, sep=',', index=False))

    # Go back to base directory
    os.chdir(base_directory)
