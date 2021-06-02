# This file is used to define the class of Building
# Developed by GUAN, XINGQUAN @ UCLA in June 2018
# Updated in Sept. 2018

import copy
import numpy as np
import os
import pandas as pd

from help_functions import determine_Fa_coefficient
from help_functions import determine_Fv_coefficient
from help_functions import calculate_DBE_acceleration
from help_functions import determine_Cu_coefficient
from help_functions import determine_floor_height
from help_functions import calculate_Cs_coefficient
from help_functions import determine_k_coeficient
from help_functions import calculate_seismic_force
from help_functions import find_section_candidate
from help_functions import search_member_size
from help_functions import search_section_property
from help_functions import decrease_member_size
from help_functions import increase_member_size
from help_functions import constructability_helper
from global_variables import SECTION_DATABASE
from global_variables import COLUMN_DATABASE
from global_variables import BEAM_DATABASE
from global_variables import PERIOD_FOR_DRIFT_LIMIT


# #########################################################################
#                Global Constants Subjected to Revision                   #
# #########################################################################

from global_variables import EXTERIOR_INTERIOR_COLUMN_RATIO
from global_variables import BEAM_TO_COLUMN_RATIO
from global_variables import IDENTICAL_SIZE_PER_STORY

# #########################################################################
#           Open the section database and store it as a global variable   #
# #########################################################################


# # Global constant: SECTION_DATABASE (a panda dataframe read from .csv file)
# with open('AllSectionDatabase.csv', 'r') as file:
#     SECTION_DATABASE = pd.read_csv(file, header=0)


# #########################################################################
#          Define a class including all building information              #
# #########################################################################


class Building(object):
    """
    This class aims to read all the relevant building information from .csv files
    It includes the following methods:
    (1) Define paths to different folders which will be used later
    (2) Read geometry information
    (3) Read load information
    (4) Read equivalent lateral force parameters
    (5) Compute lateral force for the building based on ASCE 7-10
    (6) Determine possible section sizes for columns and beams based on user-specified section depth
    (7) Propose initial beam and column sizes
    """

    def __init__(self, building_id, base_directory):
        """
        This function initializes the attributes of a building instance
        :param building_id: a string that used as a UID to label the building
        :param base_directory:  a string that denotes the path to root folder
        """
        # Assign basic information: unique ID for the building and base path
        self.UID = building_id
        self.base_directory = base_directory

        # Initialize the attributes for the building instance (will be assigned values in the class methods)
        self.directory = {}
        self.geometry = {}
        self.gravity_loads = {}
        self.elf_parameters = {}
        self.seismic_force_for_strength = {}
        self.seismic_force_for_drift = {}
        self.section_depth = {}
        self.element_candidate = {}
        self.member_size = {}
        self.elastic_response = {}
        self.construction_size = {}

        # Call defined methods to achieve the goal of the class
        self.define_directory()
        self.read_geometry()
        self.read_gravity_loads()
        self.read_elf_parameters()
        # self.compute_seismic_force()
        self.determine_member_candidate()
        self.initialize_member()
        # self.initialize_member_v2()

    def define_directory(self):
        # Define all useful paths based on the building UID and path to root folder
        # Define path to folder where the baseline .tcl files for elastic analysis are saved
        baseline_elastic_directory = self.base_directory / 'BaselineTclFiles' / 'ElasticAnalysis'
        # Define path to folder where the baseline .tcl files for nonlinear analysis are stored
        baseline_nonlinear_directory = self.base_directory / 'BaselineTclFiles' / 'NonlinearAnalysis'
        # Define path to folder where the building data (.csv) are saved
        building_data_directory = self.base_directory / 'BuildingData' / self.UID
        # Define path to folder where the generated elastic analysis OpenSees model is saved
        building_elastic_model_directory = self.base_directory / 'BuildingElasticModels' / self.UID
        # Define path to folder where the generated nonlinear analysis OpenSees model is saved
        building_nonlinear_model_directory = self.base_directory / 'BuildingNonlinearModels' / self.UID
        # Store all necessary directories into a dictionary
        self.directory = {'baseline files elastic': baseline_elastic_directory,
                          'baseline files nonlinear': baseline_nonlinear_directory,
                          'building data': building_data_directory,
                          'building elastic model': building_elastic_model_directory,
                          'building nonlinear model': building_nonlinear_model_directory}

    def read_geometry(self):
        """
        This method is used to read the building geometry information from .csv files:
        (1) Change the working directory to the folder where .csv data are stored
        (2) Open the .csv file and save all relevant information to the object itself
        """
        os.chdir(self.directory['building data'])
        with open('Geometry.csv', 'r') as csvfile:
            geometry_data = pd.read_csv(csvfile, header=0)

        # Each variable is a scalar
        number_of_story = geometry_data.loc[0, 'number of story']
        number_of_X_bay = geometry_data.loc[0, 'number of X bay']
        number_of_Z_bay = geometry_data.loc[0, 'number of Z bay']
        first_story_height = geometry_data.loc[0, 'first story height']
        typical_story_height = geometry_data.loc[0, 'typical story height']
        X_bay_width = geometry_data.loc[0, 'X bay width']
        Z_bay_width = geometry_data.loc[0, 'Z bay width']
        number_of_X_LFRS = geometry_data.loc[0, 'number of X LFRS']  # number of lateral resisting frame in X direction
        number_of_Z_LFRS = geometry_data.loc[0, 'number of Z LFRS']  # number of lateral resisting frame in Z direction
        # Call function defined in "help_functions.py" to determine the height for each floor level
        floor_height = determine_floor_height(number_of_story, first_story_height, typical_story_height)
        # Store all necessary information into a dictionary named geometry
        self.geometry = {'number of story': number_of_story,
                         'number of X bay': number_of_X_bay,
                         'number of Z bay': number_of_Z_bay,
                         'first story height': first_story_height,
                         'typical story height': typical_story_height,
                         'X bay width': X_bay_width,
                         'Z bay width': Z_bay_width,
                         'number of X LFRS': number_of_X_LFRS,
                         'number of Z LFRS': number_of_Z_LFRS,
                         'floor height': floor_height}

    def read_gravity_loads(self):
        """
        This method is used to read the load information from .csv files
        (1) Change the directory to the folder where the load data are stored
        (2) Read the .csv files and assign save load values to object values
        """
        os.chdir(self.directory['building data'])
        with open('Loads.csv', 'r') as csvfile:
            loads_data = pd.read_csv(csvfile, header=0)

        # All data is a list (array). Length is the number of story
        # Be cautious about the unit
        floor_weight = loads_data['floor weight']
        floor_dead_load = loads_data['floor dead load']
        floor_live_load = loads_data['floor live load']
        beam_dead_load = loads_data['beam dead load']
        beam_live_load = loads_data['beam live load']
        leaning_column_dead_load = loads_data['leaning column dead load']
        leaning_column_live_load = loads_data['leaning column live load']
        # Store all necessary information into a dictionary named gravity_loads
        self.gravity_loads = {'floor weight': floor_weight,
                              'floor dead load': floor_dead_load,
                              'floor live load': floor_live_load,
                              'beam dead load': beam_dead_load,
                              'beam live load': beam_live_load,
                              'leaning column dead load': leaning_column_dead_load,
                              'leaning column live load': leaning_column_live_load}

    def read_elf_parameters(self):
        """
        This method is used to read equivalent lateral force (in short: elf) parameters and calculate SDS and SD1
        (1) Read equivalent lateral force parameters
        (2) Calculate SMS, SM1, SDS, SD1 values and save them into the attribute
        """
        os.chdir(self.directory['building data'])
        with open('ELFParameters.csv', 'r') as csvfile:
            elf_parameters_data = pd.read_csv(csvfile, header=0)

        # Determine Fa and Fv coefficient based on site class and Ss and S1 (ASCE 7-10 Table 11.4-1 & 11.4-2)
        # Call function defined in "help_functions.py" to calculate two coefficients: Fa and Fv
        Fa = determine_Fa_coefficient(elf_parameters_data.loc[0, 'site class'], elf_parameters_data.loc[0, 'Ss'])
        Fv = determine_Fv_coefficient(elf_parameters_data.loc[0, 'site class'], elf_parameters_data.loc[0, 'S1'])
        # Determine SMS, SM1, SDS, SD1 using the defined function in "help_functions.py"
        SMS, SM1, SDS, SD1 = calculate_DBE_acceleration(elf_parameters_data.loc[0, 'Ss'],
                                                        elf_parameters_data.loc[0, 'S1'], Fa, Fv)
        # Determine Cu using the defined function in "help_functions.py"
        Cu = determine_Cu_coefficient(SD1)

        # Calculate the building period: approximate fundamental period and upper bound period
        approximate_period = elf_parameters_data.loc[0, 'Ct'] \
                             * (self.geometry['floor height'][-1]**elf_parameters_data.loc[0, 'x'])
        upper_period = Cu * approximate_period

        # Save all coefficient into the dictionary named elf_parameters
        self.elf_parameters = {'Ss': elf_parameters_data.loc[0, 'Ss'], 'S1': elf_parameters_data.loc[0, 'S1'],
                               'TL': elf_parameters_data.loc[0, 'TL'], 'Cd': elf_parameters_data.loc[0, 'Cd'],
                               'R': elf_parameters_data.loc[0, 'R'], 'Ie': elf_parameters_data.loc[0, 'Ie'],
                               'rho': elf_parameters_data.loc[0, 'rho'],
                               'site class': elf_parameters_data.loc[0, 'site class'],
                               'Ct': elf_parameters_data.loc[0, 'Ct'], 'x': elf_parameters_data.loc[0, 'x'],
                               'Fa': Fa, 'Fv': Fv, 'SMS': SMS, 'SM1': SM1, 'SDS': SDS, 'SD1': SD1, 'Cu': Cu,
                               'approximate period': approximate_period, 'period': upper_period}

    def compute_seismic_force(self):
        """
        This method is used to calculate the seismic story force using ELF procedure specified in ASCE 7-10 Section 12.8
        (1) Determine the floor level height and save it in a list (array)
        (2) Determine the correct period between first mode period and CuTa
        (3) Determine the Cs coefficient
        (4) Determine the lateral force at each floor level (ground to roof) and save it in an arrary
        """
        # Please note that the period for computing the required strength should be bounded by CuTa
        period_for_strength = min(self.elf_parameters['modal period'], self.elf_parameters['period'])
        # The period used for computing story drift is not required to be bounded by CuTa
        if PERIOD_FOR_DRIFT_LIMIT:
            period_for_drift = min(self.elf_parameters['modal period'], self.elf_parameters['period'])
        else:
            period_for_drift = self.elf_parameters['modal period']
        # Call function defined in "help_functions.py" to determine the seismic response coefficient
        Cs_for_strength = calculate_Cs_coefficient(self.elf_parameters['SDS'], self.elf_parameters['SD1'],
                                                   self.elf_parameters['S1'], period_for_strength,
                                                   self.elf_parameters['TL'], self.elf_parameters['R'],
                                                   self.elf_parameters['Ie'], False)
        Cs_for_drift = calculate_Cs_coefficient(self.elf_parameters['SDS'], self.elf_parameters['SD1'],
                                                self.elf_parameters['S1'], period_for_drift,
                                                self.elf_parameters['TL'], self.elf_parameters['R'],
                                                self.elf_parameters['Ie'], True)
        # Calculate the base shear
        base_shear_for_strength = Cs_for_strength * np.sum(self.gravity_loads['floor weight'])
        base_shear_for_drift = Cs_for_drift * np.sum(self.gravity_loads['floor weight'])
        # Call function defined in "help_functions.py" to compute k coefficient
        k = determine_k_coeficient(self.elf_parameters['period'])
        # Call function defined in "help_functions.py" to determine the lateral force for each floor level
        lateral_story_force_for_strength, story_shear_for_strength \
            = calculate_seismic_force(base_shear_for_strength, self.gravity_loads['floor weight'], \
                                      self.geometry['floor height'], k)
        lateral_story_force_for_drift, story_shear_for_drift \
            = calculate_seismic_force(base_shear_for_drift, self.gravity_loads['floor weight'], \
                                      self.geometry['floor height'], k)
        # Store information into class attribute
        self.seismic_force_for_strength = {'lateral story force': lateral_story_force_for_strength, \
                                           'story shear': story_shear_for_strength, \
                                           'base shear': base_shear_for_strength, 'Cs': Cs_for_strength}
        self.seismic_force_for_drift = {'lateral story force': lateral_story_force_for_drift, \
                                           'story shear': story_shear_for_drift, \
                                           'base shear': base_shear_for_drift, 'Cs': Cs_for_drift}

    def determine_member_candidate(self):
        """
        This method is used to determine all possible member candidates based on the user-specified section depth
        :return: a dictionary which contains the all possible sizes for exterior columns, interior columns, and beams.
        """
        # Read the user-specified depths for interior columns, exterior columns, and beams.
        os.chdir(self.directory['building data'])
        with open('MemberDepth.csv', 'r') as csvfile:
            depth_data = pd.read_csv(csvfile, header=0)
        # Initialize dictionary that will be used to store all possible section sizes for each member (in each story)
        interior_column_candidate = {}
        exterior_column_candidate = {}
        beam_candidate = {}
        # Initialize list that will be used to store section depth for each member (in each story)
        interior_column_depth = []
        exterior_column_depth = []
        beam_depth = []
        for story in range(0, self.geometry['number of story']):  # story number
            # Initialize the Series that will be used to store the member sizes for each single story
            temp_interior_column = pd.Series()
            temp_exterior_column = pd.Series()
            temp_beam = pd.Series()
            # Convert string (read from csv) to list
            interior_column_depth_list = depth_data.loc[story, 'interior column'].split(', ')
            exterior_column_depth_list = depth_data.loc[story, 'exterior column'].split(', ')
            beam_depth_list = depth_data.loc[story, 'beam'].split(', ')
            # Find the section size candidates associated with a certain depth specified by user
            for item in range(0, len(interior_column_depth_list)):
                temp1 = find_section_candidate(interior_column_depth_list[item], COLUMN_DATABASE)
                temp_interior_column = pd.concat([temp_interior_column, temp1])
            for item in range(0, len(exterior_column_depth_list)):
                temp2 = find_section_candidate(exterior_column_depth_list[item], COLUMN_DATABASE)
                temp_exterior_column = pd.concat([temp_exterior_column, temp2])
            for item in range(0, len(beam_depth_list)):
                temp3 = find_section_candidate(beam_depth_list[item], BEAM_DATABASE)
                temp_beam = pd.concat([temp_beam, temp3])
            # Store the section size candidates for each member per story in a dictionary
            # Re-order the Series based on the index (which is further based on descending order of Ix for column
            # and Zx for beam). Convert Series to list.
            interior_column_candidate['story %s' % (story+1)] = list(temp_interior_column.sort_index())
            exterior_column_candidate['story %s' % (story+1)] = list(temp_exterior_column.sort_index())
            beam_candidate['floor level %s' % (story+2)] = list(temp_beam.sort_index())
            # Store the section depth for each member in each story
            interior_column_depth.append(interior_column_depth_list)
            exterior_column_depth.append(exterior_column_depth_list)
            beam_depth.append(beam_depth_list)
        # Summarize all the section candidates to a dictionary
        self.element_candidate = {'interior column': interior_column_candidate,
                                  'exterior column': exterior_column_candidate,
                                  'beam': beam_candidate}
        # Summarize all the section depth to a dictionary
        self.section_depth = {'interior column': interior_column_depth,
                              'exterior column': exterior_column_depth,
                              'beam': beam_depth}

    def initialize_member(self):
        """
        This method is used to initialize the member size
        :return: a dictionary which includes the initial size for interior columns, exterior columns, and beams
        """
        # Define initial sizes for columns and beams
        interior_column = []
        exterior_column = []
        beam = []
        for story in range(0, self.geometry['number of story']):
            # The initial column is selected as the greatest sizes in the candidate pool
            initial_interior = self.element_candidate['interior column']['story %s' % (story+1)][0]
            initial_exterior = self.element_candidate['exterior column']['story %s' % (story+1)][0]
            # Merge initial size of each story together
            interior_column.append(initial_interior)
            exterior_column.append(initial_exterior)
            # Compute the section property of the interior column size
            reference_property = search_section_property(initial_interior, SECTION_DATABASE)
            # Determine the beam size based on beam-to-column section modulus ratio
            beam_size = search_member_size('Zx', reference_property['Zx']*BEAM_TO_COLUMN_RATIO,
                                           self.element_candidate['beam']['floor level %s' % (story+2)],
                                           SECTION_DATABASE)
            # Merge initial beam size of each story together
            beam.append(beam_size)
        # Store all initial member sizes into the dictionary (which will be updated using optimization algorithm later)
        self.member_size = {'interior column': interior_column,
                            'exterior column': exterior_column,
                            'beam': beam}

    def read_modal_period(self):
        """
        This method is used to read the modal period from OpenSees eigen value analysis results and store it in ELF
        parameters.
        :return: the first mode period stored in self.elf_parameters
        """
        # Change the working directory to the folder where the eigen value analysis results are stored
        path_modal_period = self.directory['building elastic model'] / 'EigenAnalysis'
        os.chdir(path_modal_period)
        # Save the first mode period in elf_parameters
        # period = np.loadtxt('Periods.out')
        period = pd.read_csv('Periods.out', header=None)
        self.elf_parameters['modal period'] = np.asscalar((period.iloc[0, 0]))


    def read_story_drift(self):
        """
        This method is used to read the story drifts from OpenSees elastic analysis results and stored it as attribute
        The load case for story drift is the combination of dead, live, and earthquake loads.
        :return: an [story*1] array which includes the story drifts for each story.
        """
        # Change the working directory to the folder where story drifts are stored
        path_story_drift = self.directory['building elastic model'] / 'GravityEarthquake' / 'StoryDrifts'
        os.chdir(path_story_drift)
        # Save all story drifts in an array
        story_drift = np.zeros([self.geometry['number of story'], 1])
        for story in range(self.geometry['number of story']):
            file_name = 'Story' + str(story+1) + '.out'
            read_data = np.loadtxt(file_name)
            story_drift[story] = read_data[-1, -1]
        # Assign the story drifts results into class attribute
        self.elastic_response = {'story drift': story_drift}

    def optimize_member_for_drift(self):
        """
        This method is used to decrease the member size such that the design is most economic.
        :return: update self.member_size
        """
        # Find the story which has the smallest drift
        target_story = np.where(self.elastic_response['story drift'] ==
                                np.min(self.elastic_response['story drift']))[0][0]
        # Update the interior column size in target story
        self.member_size['interior column'][target_story] = \
            decrease_member_size(self.element_candidate['interior column']['story %s' % (target_story+1)],
                                 self.member_size['interior column'][target_story])
        # Compute the section property of the interior column size
        reference_property = search_section_property(self.member_size['interior column'][target_story],
                                                     SECTION_DATABASE)
        # Determine the beam size based on beam-to-column section modulus ratio
        beam_size = search_member_size('Zx', reference_property['Zx'] * BEAM_TO_COLUMN_RATIO,
                                       self.element_candidate['beam']['floor level %s' %(target_story+2)],
                                       SECTION_DATABASE)
        # "Push" the updated beam size back to the class dictionary
        self.member_size['beam'][target_story] = beam_size
        # Determine the exterior column size based on exterior/interior column moment of inertia ratio
        exterior_size = search_member_size('Ix', reference_property['Ix'] * EXTERIOR_INTERIOR_COLUMN_RATIO,
                                           self.element_candidate['exterior column']['story %s' % (target_story+1)],
                                           SECTION_DATABASE)
        self.member_size['exterior column'][target_story] = exterior_size

    def upscale_column(self, target_story, type_column):
        """
        This method is used to increase  column size which might be necessary when column strength is not sufficient
        or strong column weak beam is not satisfied.
        :param target_story: a scalar to denote which story column shall be increased (from 0 to total story # - 1).
        :param type_column: a string denoting whether it is an exterior column or interior column
        :return: update the column size stored in self.member_size
        """
        temp_size = increase_member_size(self.element_candidate[type_column]['story %s' % (target_story+1)],
                                         self.member_size[type_column][target_story])
        self.member_size[type_column][target_story] = temp_size
        # temp_size_2 = increase_member_size(self.element_candidate['exterior column']['story %x' % (target_story+1)],
        #                                    self.member_size['exterior column'][target_story])
        # self.member_size['exterior column'][target_story] = temp_size_2

    def upscale_beam(self, target_floor):
        """
        This method is used to increase beam size which might be necessary when beam strength is not sufficient
        :param target_floor: a scalar to denote which floor beam shall be improved. (from 0 to total story # - 1)
        :return: update the beam size stored in self.member_size
        """
        temp_size = increase_member_size(self.element_candidate['beam']['floor level %s' % (target_floor+2)],
                                         self.member_size['beam'][target_floor])
        self.member_size['beam'][target_floor] = temp_size

    # ************************************* Keep previous version as backup ********************************************
    # def constructability(self):
    #     """
    #     This method is used to update the member size by considering the constructability (ease of construction)
    #     :return: a dictionary which includes the member sizes after consideration of constructability.
    #              Those siezes are considered to be the actual final design.
    #     """
    #     # Make a deep copy of the member sizes and stored them in a new dictionary named construction_size
    #     # Use deep copy to avoid changing the varaiables stored in member size
    #     temp_size = copy.deepcopy(self.member_size)
    #     # Update interior and exterior column size
    #     member = ['interior column', 'exterior column']
    #     for mem in member:
    #         self.construction_size[mem] = constructability_helper(temp_size[mem], IDENTICAL_SIZE_PER_STORY,
    #                                                               self.geometry['number of story'])
    #     # Update beam size using relative ratio between beams and columns
    #     temp_beam = []
    #     for story in range(0, self.geometry['number of story']):
    #         reference_property = search_section_property(self.construction_size['interior column'][story],
    #                                                      SECTION_DATABASE)
    #         beam_size = search_member_size('Zx', reference_property['Zx'] * BEAM_TO_COLUMN_RATIO,
    #                                        self.element_candidate['beam']['floor level %s' % (story + 2)],
    #                                        SECTION_DATABASE)
    #         temp_beam.append(beam_size)
    #     self.construction_size['beam'] = temp_beam
    # ********************************************* Previous version ends here *****************************************

    def constructability_beam(self):
        """
        This method is used to update the beam member size by considering the constructability (ease of construction).
        :return: update the beam sizes stored in self.member_size['beam']
        """
        # Make a deep copy of the member sizes and stored them in a new dictionary named construction_size
        # Use deep copy to avoid changing the variables stored in member size
        temp_size = copy.deepcopy(self.member_size)
        # Update beam size (beam size is updated based on descending order of Zx)
        self.construction_size['beam'] = constructability_helper(temp_size['beam'], IDENTICAL_SIZE_PER_STORY,
                                                                 self.geometry['number of story'], 'Ix')
        # Column sizes here have not been updated (just directly copy)
        self.construction_size['interior column'] = temp_size['interior column']
        self.construction_size['exterior column'] = temp_size['exterior column']

    def constructability_column(self):
        """
        This method is used to update the column member size by considering the constructability (ease of construction).
        :return: update the column sizes stored in self.member_size
        """
        # Make a copy of the member size
        temp_size = copy.deepcopy(self.member_size)
        # Update column sizes based on the sorted Ix
        member_list = ['interior column', 'exterior column']
        for mem in member_list:
            self.construction_size[mem] = constructability_helper(temp_size[mem], IDENTICAL_SIZE_PER_STORY,
                                                                  self.geometry['number of story'], 'Ix')