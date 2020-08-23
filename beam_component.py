# This file is used to define the class of beam, which includes the axial, shear, and flexural strengths of column
# Developed by GUAN, XINGQUAN @ UCLA in Apr. 2018
# Updated in Oct. 2018

import numpy as np

from global_variables import SECTION_DATABASE
from help_functions import search_section_property

# #########################################################################
#                           Define a class of beam                        #
# #########################################################################

class Beam(object):
    """
    This class is used to define a beam member, which has the following attributes:
    (1) Beam section, a dictionary including size and associated properties.
    (2) Beam demand, a dictionary including shear and flexural demands.
    (3) Beam strength, a dictionary including shear and flexural strengths.
    (4) Beam flag, a boolean variable with True or False. If it is True, the beam is feasible.
    """

    def __init__(self, section_size, length, shear_demand, moment_demand_left, moment_demand_right, steel):
        """
        This function initializes the attributes of the beam class.
        :param section_size: a string specifying the section size for the beam.
        :param length: a float number denoting the beam length.
        :param shear_demand: a float number denoting the shear demand.
        :param moment_demand_left: a float number denoting the moment demand at right end.
        :param moment_demand_right: a float number denoting the moment demand at left end.
        """
        # Assign the necessary information for column class
        self.section = search_section_property(section_size, SECTION_DATABASE)
        self.demand = {'shear': shear_demand, 'moment left': moment_demand_left, 'moment right': moment_demand_right}
        self.length = length

        # Initialize the following variables
        self.RBS_dimension = {}  # a dictionary used to store the dimensions for reduced beam section
        self.spacing = None  # a scalar indicating the spacing between two lateral supports
        self.strength = {}  # a dictionary used to store the strength of beam component
        self.demand_capacity_ratio = {}  # a dictionary to store the demand to capacity ratio
        self.is_feasible = {}  # a dictionary used to store the failure mode of beam (if any)
        # Define a boolean flag which denotes the overall check results
        self.flag = None

        # Define a hinge dictionary to store all modeling parameters
        self.plastic_hinge = {}

        # Using the following methods to compute strength and check whether strength is sufficient
        self.initialize_reduced_beam_section()
        self.check_flange(steel)
        self.check_web(steel)
        self.determine_spacing_between_lateral_support(steel)
        self.check_shear_strength(steel)
        self.check_flexural_strength(steel)
        self.compute_demand_capacity_ratio()
        self.calculate_hinge_parameters(steel)

    def initialize_reduced_beam_section(self):
        """
        This method is used to initialize RBS dimensions.
        :return: a dictionary including a, b, and c values describing RBS dimensions.
        """
        # Use the lower bound as the initial value for a and b
        self.RBS_dimension['a'] = 0.5 * self.section['bf']
        self.RBS_dimension['b'] = 0.65 * self.section['d']
        #self.RBS_dimension['c'] = 0.1 * self.section['bf']
        self.RBS_dimension['c'] = 0.25 * self.section['bf']

    def check_flange(self, steel):
        """
        This method is used to check whether the flange is satisfied with highly ductile requirement.
        : steel: a class defined in "steel_material.py" file
        : return: a flag (integer) which denotes the flange check result.
        """
        # Calculate equivalent flange width at reduced beam section
        R = (4*self.RBS_dimension['c']**2 + self.RBS_dimension['b']**2)/(8*self.RBS_dimension['c'])
        bf_RBS = 2*(R-self.RBS_dimension['c']) + self.section['bf'] - 2*np.sqrt(R**2-(self.RBS_dimension['b']/3)**2)
        # Compute flange width-to-thickness ratio
        lambda_f = bf_RBS / (2*self.section['tf'])
        # Calculate limit for flange width-to-thickness ratio
        flange_limit = 0.30 * np.sqrt(steel.E/steel.Fy)
        # Check whether the flange satisfies the limit
        if lambda_f <= flange_limit:
            self.is_feasible['flange limit'] = True
        else:
            self.is_feasible['flange limit'] = False

    def check_web(self, steel):
        """
        This method is used to check whether the web is satisfied with highly ductile requirement.
        :param steel: a class defined in "steel_material.py" file.
        :return: a flag (integer) which denotes the web check result.
        """
        # Compute limit for web depth-to-width ratio
        web_limit = 2.45 * np.sqrt(steel.E/steel.Fy)
        # Check whether web is satisfied with the requirement or not
        if self.section['h to tw ratio'] <= web_limit:
            self.is_feasible['web limit'] = True
        else:
            self.is_feasible['web limit'] = False

    def determine_spacing_between_lateral_support(self, steel):
        """
        This method is used to compute the spacing between two lateral supports.
        :param steel: a class defined in "steel_material.py" file.
        :return: a float number indicating the spacing.
        """
        # Compute limit for spacing (Remember to convert from inches to feet)
        spacing_limit = 0.086 * self.section['ry'] * steel.E / steel.Fy * 1/12.0
        # Start with the number of lateral support equal to 1
        # Check whether the current lateral support is enough
        # If it is not sufficient, increase the number of lateral support until the requirement is satisfied
        number_lateral_support = 1
        while self.length/(number_lateral_support+1) > spacing_limit:
            number_lateral_support += 1
        # Check whether the spacing is less than Lp
        # If the spacing greater than Lp, then reduce the spacing such that the flexural strength is governed by
        # plastic yielding.
        Lp = 1.76 * self.section['ry'] * np.sqrt(steel.E/steel.Fy)
        while (self.length/number_lateral_support+1) > Lp:
            number_lateral_support += 1
        self.spacing = self.length/(number_lateral_support+1)

    def check_shear_strength(self, steel):
        """
        This method is used to check whether the shear strength of column is sufficient or not
        :param steel: a class defined in "steel_material.py" file
        :return: a float number denoting the shear strength and a flag denoting whether shear strength is sufficient
        """
        # Compute shear strength of beam
        Cv = 1.0
        Vn = 0.6 * steel.Fy * (self.section['tw'] * self.section['d']) * Cv
        phi = 1.0
        self.strength['shear'] = phi * Vn
        # Check whether shear strength is sufficient
        if self.strength['shear'] >= self.demand['shear']:
            self.is_feasible['shear strength'] = True
        else:
            self.is_feasible['shear strength'] = False

    def check_flexural_strength(self, steel):
        """
        This method is used to check whether the beam has enough flexural strength.
        :return: a float number denoting flexural strength and a flag denoting whether the flexural strength is enough
        """
        # Compute plastic modulus at center of RBS
        Z_RBS = self.section['Zx'] - 2 * self.RBS_dimension['c'] * self.section['tf'] \
                * (self.section['d'] - self.section['tf'])
        # Calculate the moment capacity governed by plastic yielding at RBS
        Mn_RBS = steel.Fy * Z_RBS
        phi = 0.9
        self.strength['flexural RBS'] = phi * Mn_RBS
        # Check whether the flexural strength is sufficient
        M_max = np.max([abs(self.demand['moment right']), abs(self.demand['moment left'])])
        if self.strength['flexural RBS'] >= M_max:
            self.is_feasible['flexural strength'] = True
        else:
            self.is_feasible['flexural strength'] = False

    def check_flag(self):
        """
        This method is used to test whether beam passes all checks.
        :return: a bool variable. True ==> passed
        """
        self.flag = True
        for key in self.is_feasible.keys():
            if self.is_feasible[key] == False:
                self.flag = False
        return self.flag

    def compute_demand_capacity_ratio(self):
        """
        This method is used to compute demand to capacity ratios.
        :return: a dictionary which includes the ratios for shear force and flexural moment.
        """
        self.demand_capacity_ratio['shear'] = self.demand['shear'] / self.strength['shear']
        self.demand_capacity_ratio['flexural'] = max(abs(self.demand['moment left']),
                                                     abs(self.demand['moment right'])) / self.strength['flexural RBS']

    def calculate_hinge_parameters(self, steel):
        """
        This method is used to compute the modeling parameters for plastic hinge using modified IMK material model.
        :return: a dictionary including each parameters required for nonlinear modeling in OpenSees.
        """
        # Following content is based on the following reference:
        # [1] Hysteretic models tha incorporate strength and stiffness deterioration
        # [2] Deterioration modeling of steel components in support of collapse prediction of steel moment frames under
        #     earthquake loading
        # [3] Global collapse of frame structures under seismic excitations
        # [4] Sidesway collapse of deteriorating structural systems under seismic excitations
        # dictionary keys explanations:
        #                              K0: beam stiffness, 6*E*Iz/L
        #                              Myp: bending strength, product of section modulus and material yield strength
        #                              My: effective yield strength, 1.06 * bending strength
        #                              Lambda: reference cumulative plastic rotation
        #                              theta_p: pre-capping plastic rotation
        #                              theta_pc: post-capping plastic rotation
        #                              as: strain hardening before modified by n (=10)
        #                              residual: residual strength ratio, use 0.40 per Lignos' OpenSees example
        #                              theta_u: ultimate rotation, use 0.40 per Lignos' OpenSees example
        # unit: kips, inches
        # beam spacing and length is in feet, remember to convert it to inches
        c1 = 25.4  # c1_unit
        c2 = 6.895  # c2_unit
        McMy = 1.10  # Capping moment to yielding moment ratio. Lignos et al. used 1.05 whereas Prof. Burton used 1.11.
        h = self.section['d'] - 2*self.section['tf']  # Web depth
        self.plastic_hinge['K0'] = 6 * steel.E * self.section['Ix'] / (self.length*12.0)
        self.plastic_hinge['Myp'] = self.section['Zx'] * steel.Fy
        self.plastic_hinge['My'] = 1.00 * self.plastic_hinge['Myp']
        self.plastic_hinge['Lambda'] = 585 * (h/self.section['tw'])**(-1.14) \
                                       * (self.section['bf']/(2*self.section['tf']))**(-0.632) \
                                       * (self.spacing*12.0/self.section['ry'])**(-0.205) \
                                       * (c2*steel.Fy/355)**(-0.391)
        # Pre-capping rotation
        self.plastic_hinge['theta_p'] = 0.19 * (h/self.section['tw'])**(-0.314) \
                                        * (self.section['bf']/(2*self.section['tf']))**(-0.100) \
                                        * (self.spacing*12.0/self.section['ry'])**(-0.185) \
                                        * (self.length*12.0/self.section['d'])**0.113 \
                                        * (c1*self.section['d']/533)**(-0.760) \
                                        * (c2*steel.Fy/355)**(-0.070)
        # Pre-capping rotation is further revised to exclude the elastic deformation
        self.plastic_hinge['theta_p'] = self.plastic_hinge['theta_p'] \
                                        - (McMy - 1.0) * self.plastic_hinge['My'] / self.plastic_hinge['K0']
        # Post-capping rotation
        self.plastic_hinge['theta_pc'] = 9.52 * (h/self.section['tw'])**(-0.513) \
                                         * (self.section['bf']/(2*self.section['tf']))**(-0.863) \
                                         * (self.spacing*12.0/self.section['ry'])**(-0.108) \
                                         * (c2*steel.Fy/355)**(-0.360)
        # Post-capping rotation is further revised to account for elastic deformation
        self.plastic_hinge['theta_y'] = self.plastic_hinge['My'] / self.plastic_hinge['K0']
        self.plastic_hinge['theta_pc'] = self.plastic_hinge['theta_pc'] \
                                         + self.plastic_hinge['theta_y'] \
                                         + (McMy - 1.0) * self.plastic_hinge['My'] / self.plastic_hinge['K0']
        self.plastic_hinge['as'] = (McMy-1.0)*self.plastic_hinge['My']\
                                   /(self.plastic_hinge['theta_p']*self.plastic_hinge['K0'])
        self.plastic_hinge['residual'] = 0.40
        self.plastic_hinge['theta_u'] = 0.20