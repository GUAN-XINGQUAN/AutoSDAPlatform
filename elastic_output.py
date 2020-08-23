# This file is used to define the class of Building
# Developed by GUAN, XINGQUAN @ UCLA in Aug. 2018
# Updated on Sept. 28 2018

import os
import numpy as np

# #########################################################################
#           Define a list of load sequence as global constant             #
# #########################################################################


LOAD_TYPE = ['DeadLoad', 'LiveLoad', 'EarthquakeLoad']


# #########################################################################
#       Define a class to read load output and perform load combination   #
# #########################################################################


class ElasticOutput(object):
    """
    This class is used to the following jobs:
    (1) Read load from OpenSees output files
    (2) Extract axial force, shear force, and moment for columns from matrix read in method (1)
    (3) Extract shear force and moment for beams from matrix read in method (1)
    (4) Perform load combination
        Load combination #1: 1.4D
        Load combination #2: 1.2D + 1.6L
        Load combination #3: (1.2 + 0.2SDS)D + 1.0(0.5)L + rho*E
        Load combination #4: (1.2 + 0.2SDS)D + 1.0(0.5)L - rho*E
        Load combination #5: (0.9 - 0.2SDS)D + rho*E
        Load combination #6: (0.9 - 0.2SDS)D - rho*E
    (5) Determine governing load cases
    """

    def __init__(self, building):
        # Initialize attributes of elastic_output class
        self.raw_column_load = {}
        self.raw_beam_load = {}
        self.dead_load_case = {}
        self.live_load_case = {}
        self.earthquake_load_case = {}
        self.load_combination_1 = {}
        self.load_combination_2 = {}
        self.load_combination_3 = {}
        self.load_combination_4 = {}
        self.load_combination_5 = {}
        self.load_combination_6 = {}
        self.dominate_load = {}

        # Assign the attributes with values using the following methods
        self.read_raw_load(building)
        self.extract_column_load()
        self.extract_beam_load()
        self.perform_load_combination(building)
        self.determine_dominate_load()

    def read_raw_load(self, building):
        """
        This method is used to read the load demand for the structure subjected to certain type of load:
        dead load, live load or earthquake load
        :param building: user-defined class in "building_information.py" file
        :return: a dictionary which contains load demands under three load scenarios
        """
        for load_type in LOAD_TYPE:
            # Define the directory where the column force output is stored
            path_output = building.directory['building elastic model'] / load_type / 'GlobalColumnForces'
            os.chdir(path_output)
            # Initialize a matrix to store all column component forces: axial, shear and moment.
            column_load = np.zeros([building.geometry['number of story'], (building.geometry['number of X bay']+1)*6])
            # Read output txt files
            for story in range(0, building.geometry['number of story']):
                # Define the output txt file name
                file_name = 'GlobalColumnForcesStory' + str(story+1) + '.out'
                read_data = np.loadtxt(file_name)
                column_load[story, :] = read_data[-1, 1:]
            # Store column forces into different load cases
            self.raw_column_load[load_type] = column_load

            # Define the directory where the beam force is stored
            path_output = building.directory['building elastic model'] / load_type / 'GlobalBeamForces'
            os.chdir(path_output)
            #  Initialize a matrix to store all beam component forces: axial, shear and moment
            beam_load = np.zeros([building.geometry['number of story'], building.geometry['number of X bay']*6])
            # Read beam load from output txt files
            for story in range(0, building.geometry['number of story']):
                # Define output txt file name
                file_name = 'GlobalXBeamForcesLevel' + str(story+2) + '.out'
                read_data = np.loadtxt(file_name)
                beam_load[story, :] = read_data[-1, 1:]
            # Store beam forces based on load scenario
            self.raw_beam_load[load_type] = beam_load

    def extract_column_load(self):
        # Extract axial force, shear force, and moment from the variable obtained in the previous step
        # Forces at both ends of columns are stored
        N = self.raw_column_load['DeadLoad'].shape[1]
        axial_index = range(1, N, 3)  # In column matrix, axial force is in column #2, 5, 8, ...
        shear_index = range(0, N, 3)  # In column matrix, shear force is in column #1, 4, 7, ...
        moment_index = range(2, N, 3)  # In column matrix, moment is in column #3, 6, 9, ...

        for load_type in LOAD_TYPE:
            axial_force = self.raw_column_load[load_type][:, axial_index]
            shear_force = self.raw_column_load[load_type][:, shear_index]
            moment = self.raw_column_load[load_type][:, moment_index]
            if load_type == 'DeadLoad':
                self.dead_load_case = {'column axial': axial_force,
                                       'column shear': shear_force,
                                       'column moment': moment}
            elif load_type == 'LiveLoad':
                self.live_load_case = {'column axial': axial_force,
                                       'column shear': shear_force,
                                       'column moment': moment}
            elif load_type == 'EarthquakeLoad':
                self.earthquake_load_case = {'column axial': axial_force,
                                             'column shear': shear_force,
                                             'column moment': moment}

    def extract_beam_load(self):
        # Extract shear and moment from variables obtained in previous step
        # Forces at both ends of beams are stored
        N = self.raw_beam_load['DeadLoad'].shape[1]
        axial_index = range(0, N, 3)  # In beam matrix, axial force is in column #1, 4, 7, ...
        shear_index = range(1, N, 3)  # In beam matrix, shear force is in column #2, 5, 8, ...
        moment_index = range(2, N, 3)  # In beam matrix, moment is in column #3, 6, 9, ...
        # Obtain the forces and store them into existing dictionary
        for load_type in LOAD_TYPE:
            axial_force = self.raw_beam_load[load_type][:, axial_index]
            shear_force = self.raw_beam_load[load_type][:, shear_index]
            moment = self.raw_beam_load[load_type][:, moment_index]
            if load_type == 'DeadLoad':
                self.dead_load_case['beam axial'] = axial_force
                self.dead_load_case['beam shear'] = shear_force
                self.dead_load_case['beam moment'] = moment
            elif load_type == 'LiveLoad':
                self.live_load_case['beam axial'] = axial_force
                self.live_load_case['beam shear'] = shear_force
                self.live_load_case['beam moment'] = moment
            elif load_type == 'EarthquakeLoad':
                self.earthquake_load_case['beam axial'] = axial_force
                self.earthquake_load_case['beam shear'] = shear_force
                self.earthquake_load_case['beam moment'] = moment

    def perform_load_combination(self, building):
        """
        This method is used to perform the load combinations, which will be used to extract the dominate load.
        There are six load combinations in total according to ASCE 7-10.
        :param building: user-defined class in "building_information.py" file
        :return: six dictionaries which individually represents a single load combination result.
        """
        # Load combination 1: 1.4*D
        for force in self.dead_load_case:
            self.load_combination_1[force] = 1.4*self.dead_load_case[force]

        # Load combination 2: 1.2*D + 1.6*L
        for force in self.dead_load_case:
            self.load_combination_2[force] = 1.2*self.dead_load_case[force] + 1.6*self.live_load_case[force]

        # Load combination 3: (1.2*D + 0.2*SDS) + 1.0(0.5)*L + rho*E
        # For Load combination 3 through 6, omega should be used to replace with rho for column axial force
        SDS = building.elf_parameters['SDS']
        rho = 1.0
        omega = 3.0
        for force in self.dead_load_case:
            if force != 'column axial':
                self.load_combination_3[force] = (1.2+0.2*SDS)*self.dead_load_case[force] \
                                                 + 0.5*self.live_load_case[force] \
                                                 + rho*self.earthquake_load_case[force]
            else:
                self.load_combination_3[force] = (1.2+0.2*SDS)*self.dead_load_case[force] \
                                                 + 0.5*self.live_load_case[force] \
                                                 + omega*self.earthquake_load_case[force]

        # Load combination 4: (1.2*D + 0.2*SDS) + 1.0(0.5)*L - rho*E
        for force in self.dead_load_case:
            if force != 'column axial':
                self.load_combination_4[force] = (1.2+0.2*SDS)*self.dead_load_case[force] \
                                                 + 0.5*self.live_load_case[force] \
                                                 - rho*self.earthquake_load_case[force]
            else:
                self.load_combination_4[force] = (1.2+0.2*SDS)*self.dead_load_case[force] \
                                                 + 0.5*self.live_load_case[force] \
                                                 - omega*self.earthquake_load_case[force]

        # Load combination 5: (0.9 - 0.2*SDS) + rho * E
        for force in self.dead_load_case:
            if force != 'column axial':
                self.load_combination_5[force] = (0.9-0.2*SDS)*self.dead_load_case[force] \
                                                 + rho*self.earthquake_load_case[force]
            else:
                self.load_combination_5[force] = (0.9-0.2*SDS)*self.dead_load_case[force] \
                                                 + omega*self.earthquake_load_case[force]

        # Load combination 6: (0.9 - 0.2*SDS) - rho * E
        for force in self.dead_load_case:
            if force != 'column axial':
                self.load_combination_6[force] = (0.9-0.2*SDS)*self.dead_load_case[force] \
                                                 - rho*self.earthquake_load_case[force]
            else:
                self.load_combination_6[force] = (0.9-0.2*SDS)*self.dead_load_case[force] \
                                                 - omega*self.earthquake_load_case[force]

    def determine_dominate_load(self):
        """
        This method is used to determine the governing load for beam and column components.
        :return: a dictionary which includes all six keys and associated matrices.
                 six keys: column axial, column shear, column moment, beam axial, beam shear, beam moment
        """
        dominate_load = {}
        # Find the maximum load demand among six load cases
        for force in self.load_combination_1.keys():
            M, N = self.load_combination_1[force].shape
            dominate_load[force] = np.zeros([M, N])
            for m in range(M):
                for n in range(N):
                    # The demand might be either positive or negative, try to find the one with maximum absolute value
                    temp_1 = np.max([self.load_combination_1[force][m, n], self.load_combination_2[force][m, n],
                                     self.load_combination_3[force][m, n], self.load_combination_4[force][m, n],
                                     self.load_combination_5[force][m, n], self.load_combination_6[force][m, n]])

                    temp_2 = np.min([self.load_combination_1[force][m, n], self.load_combination_2[force][m, n],
                                     self.load_combination_3[force][m, n], self.load_combination_4[force][m, n],
                                     self.load_combination_5[force][m, n], self.load_combination_6[force][m, n]])

                    if (abs(temp_1) > abs(temp_2)):
                        dominate_load[force][m, n] = temp_1
                    else:
                        dominate_load[force][m, n] = temp_2
        self.dominate_load = dominate_load
