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
import sys

from building_information import Building
from elastic_analysis import ElasticAnalysis
from elastic_output import ElasticOutput

from global_variables import steel
from global_variables import UPPER_LOWER_COLUMN_Zx
from global_variables import RBS_STIFFNESS_FACTOR
from global_variables import DRIFT_LIMIT

from design_helper import create_column_set
from design_helper import create_beam_set
from design_helper import create_connection_set
from design_helper import save_all_design_results

##########################################################################
#                         Function Implementation                        #
##########################################################################


def seismic_design(building_id, base_directory):
    # ************************************************************************
    # ///////////////// Start Seismic Design /////////////////////////////////
    # ************************************************************************
    # Create an instance using "Building" class
    building_1 = Building(building_id, base_directory)


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


    # *******************************************************************
    # ///////////////// Check Beam Strength /////////////////////////////
    # *******************************************************************
    # Initialize a list to store all beam instances
    beam_set, not_feasible_beam = create_beam_set(building_1, elastic_demand, steel)


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


    # ********************************************************************
    # ///////////////// Check Beam-Column Connection /////////////////////
    # ********************************************************************
    connection_set, not_feasible_connection = create_connection_set(building_1, column_set, beam_set, steel)

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

    # Change the working directory to building data
    os.chdir(building_1.directory['building data'])

    save_all_design_results(building_1, column_set, beam_set, connection_set, False)
    save_all_design_results(building_3, construction_column_set, construction_beam_set, construction_connection_set,
                            True)

    # Go back to base directory
    os.chdir(base_directory)
