# This file is used to define the class of beam-column connection, which includes beam/column depth
# check, RBS dimensions, moment capacity at column face, strong-column-weak-beam check, and panel zone
# thickness (doubler plate)


##########################################################################
#                       Load Built-in Packages                           #
##########################################################################

# Please add all the imported modules in the part below

import copy
import pandas as pd
import sys

##########################################################################
#                  Load User Defined Class and Py Files                  #
##########################################################################

from help_functions import extract_depth
from help_functions import extract_weight

# #########################################################################
#           Open the section database and store it as a global variable   #
# #########################################################################

from global_variables import STRONG_COLUMN_WEAK_BEAM_RATIO

# #########################################################################
#                           Define a class of beam                        #
# #########################################################################

class Connection(object):
    """
    This class is used to define a beam-column connection part, which has the following attributes:
    (1) Check column and beam depth as well as weight per ANSI Section 5.3.1 prequalified connection.
    (2) Extract RBS (reduced beam section) dimension from beam class.
    (3) Compute the probable maximum moment at the center of RBS
    (4) Calculate shear force at the center of RBS
    (5) Compute probable moment at column face
    (6) Compute plastic moment of beam based on expeced yield stress
    (7) Check moment capacity at column face
    (8) Check shear strength of beam
    (9) Check whether strong column weak beam is satisfied
    (10) Calculate doubler plate thickness
    """

    def __init__(self, connection_type, steel, beam_dead_load, beam_live_load, span,
                 left_beam=None, right_beam=None, top_column=None, bottom_column=None):
        """
        This function initializes all attributes of Connection class.
        :param connection_type: a string which denotes the type of beam-column connection.
                                "interior": interior beam-column connection with two beams and two columns
                                "exterior": exterior beam-column connection with one beam and two columns
                                "top exterior": exterior connection at roof with one beam and one column
                                "top interior": interior connection at roof with two beams and one column
        :param steel: a class defined in "steel_material.py" file
        :param beam_dead_load: dead load on beam (unit: lb/ft)
        :param beam_live_load: live load on beam (unit: lb/ft)
        :param span: the length of beam (unit: ft)
        :param left_beam: a class defined in "beam_component.py" file which represents the beam at
                          left side of the connection.
        :param right_beam: a class defined in "beam_component.py" file which represents the beam at
                           right side of the connection.
        :param top_column: a class defined in "column_component.py" file which refers the column in
                           upper story of the connection.
        :param bottom_column: a class defined in "column_component.py" file which refers the column in
                            lower story of the connection.
        """
        self.connection_type = connection_type
        # The dictionary used to store the RBS dimensions
        self.left_RBS_dimension = {}
        self.right_RBS_dimension = {}
        # The dictionary used to store the probable moment
        self.moment = {}
        # The dictionary used to store the shear force
        self.shear_force = {}  # keys:
        # A scalar used to denote the doubler plate thickness
        self.doubler_plate_thickness = 0
        # A dictionary used to store the failure mode (if any)
        self.is_feasible = {}  # keys: 'geometry limit', 'flexural strength', 'shear strength', 'SCWB'
        # Define a boolean flag which denotes the overall check results (True means OK.)
        self.flag = None

        # Call methods to initialize the attributes listed above
        self.check_column_beam(connection_type, left_beam, right_beam, top_column, bottom_column)
        self.extract_reduced_beam_section(connection_type, left_beam, right_beam)
        self.compute_probable_moment_RBS(connection_type, steel, left_beam, right_beam)
        self.compute_shear_force_RBS(connection_type, beam_dead_load, beam_live_load, span, bottom_column)
        self.compute_probable_moment_column_face(connection_type)
        self.compute_plastic_moment(connection_type, steel, left_beam, right_beam)
        self.check_moment_column_face(connection_type)
        self.check_shear_strength(connection_type, beam_dead_load, beam_live_load, left_beam, right_beam)
        self.check_column_beam_relationships(connection_type, steel, left_beam, right_beam, top_column, bottom_column)
        self.determine_doubler_plate(connection_type, steel, left_beam, right_beam, bottom_column, top_column)

    def check_column_beam(self, connection_type, left_beam, right_beam, top_column, bottom_column):
        """
        This method is used to check whether the column and beam depth (weight) is feasible for
        prequalified connection. (step 1 in ANSI Section 5.8)
        The explanations for input arguments are presented in __init__() function.
        :return: a boolean result stored in is_feasible dictionary.
                 Actually, this method should always be true because all beam and column members are selected from a
                 database that non-prequalified sizes have been removed.
        """
        # Extract the beam depth and weight
        if connection_type == 'typical exterior':
            # Connection only has one beam and two columns
            left_beam_depth = extract_depth(left_beam.section['section size'])
            left_beam_weight = extract_weight(left_beam.section['section size'])
            top_column_depth = extract_depth(top_column.section['section size'])
            bottom_column_depth = extract_depth(bottom_column.section['section size'])
            if (left_beam_depth <= 36 and left_beam_weight <= 300
                    and top_column_depth <= 36 and bottom_column_depth <= 36):
                self.is_feasible['geometry limits'] = True
            else:
                sys.stderr.write('Beam and column depth & weight are not acceptable!\n')
                self.is_feasible['geometry limits'] = False
        elif connection_type == 'top exterior':
            # ****************** Debug using only *************************
            # print("top exterior:")
            # print("column size = ", bottom_column.section['section size'])
            # print("beam size = ", left_beam.section['section size'])
            # ****************** Debug ends here **************************
            # Connection only has one beam and one column
            left_beam_depth = extract_depth(left_beam.section['section size'])
            left_beam_weight = extract_weight(left_beam.section['section size'])
            bottom_column_depth = extract_depth(bottom_column.section['section size'])
            if left_beam_depth <= 36 and left_beam_weight <= 300 and bottom_column_depth <= 36:
                self.is_feasible['geometry limits'] = True
            else:
                sys.stderr.write('Beam and column depth & weight are not acceptable!\n')
                self.is_feasible['geometry limits'] = False
        elif connection_type == 'typical interior':
            # Connection has two beams and two columns
            left_beam_depth = extract_depth(left_beam.section['section size'])
            left_beam_weight = extract_weight(left_beam.section['section size'])
            right_beam_depth = extract_depth(right_beam.section['section size'])
            right_beam_weight = extract_weight(right_beam.section['section size'])
            top_column_depth = extract_depth(top_column.section['section size'])
            bottom_column_depth = extract_depth(bottom_column.section['section size'])
            if (left_beam_depth <= 36 and right_beam_depth <= 36
                    and left_beam_weight <= 300 and right_beam_weight <= 300
                    and top_column_depth <= 36 and bottom_column_depth <= 36):
                self.is_feasible['geometry limits'] = True
            else:
                sys.stderr.write('Beam and beam depth & weight are not acceptable!\n')
                self.is_feasible['geometry limits'] = False
        elif connection_type == 'top interior':
            # Connection has two beams and one column
            left_beam_depth = extract_depth(left_beam.section['section size'])
            left_beam_weight = extract_weight(left_beam.section['section size'])
            right_beam_depth = extract_depth(right_beam.section['section size'])
            right_beam_weight = extract_weight(right_beam.section['section size'])
            bottom_column_depth = extract_depth(bottom_column.section['section size'])
            if (left_beam_depth <= 36 and right_beam_depth <= 36
                    and left_beam_weight <= 300 and right_beam_weight <= 300
                    and bottom_column_depth <= 36):
                self.is_feasible['geometry limits'] = True
            else:
                sys.stderr.write('Beam and beam depth & weight are not acceptable!\n')
                self.is_feasible['geometry limits'] = False
        else:
            sys.stderr.write('Error: wrong type of connection specified!\n No such keyword for connection exists!\n')
            sys.exit(2)

    def extract_reduced_beam_section(self, connection_type, left_beam, right_beam):
        """
        This method is used to extract the RBS dimensions into one (or two) dictionary.
        The explanations for input arguments are presented in __init__() function.
        :return: one (two) dictionary which contains the RBS dimensions.
        """
        if connection_type == 'typical exterior' or connection_type == 'top exterior':
            # The connection only has one beam in this case
            self.left_RBS_dimension = copy.deepcopy(left_beam.RBS_dimension)
        elif connection_type == 'typical interior' or connection_type == 'top interior':
            # The connection has two beams at both sides
            self.left_RBS_dimension = copy.deepcopy(left_beam.RBS_dimension)
            self.right_RBS_dimension = copy.deepcopy(right_beam.RBS_dimension)
        else:
            sys.stderr.write('Error: wrong type of connection specified!\nNo such keyword for connection exists!\n')
            sys.exit(2)

    def compute_probable_moment_RBS(self, connection_type, steel, left_beam, right_beam):
        """
        This method is used to compute section modulus at RBS center (step 2 and 3 in ANSI Section 5.8)
        :return: a dictionary which includes the probable moment at RBS center
        """
        Cpr = (steel.Fy+steel.Fu) / (2*steel.Fy)
        if Cpr >= 1.2:
            Cpr = 1.2
        if connection_type == 'typical exterior' or connection_type == 'top exterior':
            left_Z_RBS = left_beam.section['Zx'] - 2 * left_beam.RBS_dimension['c'] * left_beam.section['tf'] \
                    * (left_beam.section['d'] - left_beam.section['tf'])
            self.moment['Mpr1'] = Cpr * steel.Ry * steel.Fy * left_Z_RBS
        elif connection_type == 'typical interior' or connection_type == 'top interior':
            left_Z_RBS = left_beam.section['Zx'] - 2 * left_beam.RBS_dimension['c'] * left_beam.section['tf'] \
                    * (left_beam.section['d'] - left_beam.section['tf'])
            self.moment['Mpr1'] = Cpr * steel.Ry * steel.Fy * left_Z_RBS
            right_Z_RBS = right_beam.section['Zx'] - 2 * right_beam.RBS_dimension['c'] * right_beam.section['tf'] \
                    * (right_beam.section['d'] - right_beam.section['tf'])
            self.moment['Mpr2'] = Cpr * steel.Ry * steel.Fy * right_Z_RBS
        else:
            sys.stderr.write('Error: wrong type of connection specified!\nNo such keyword for connection exists!')
            sys.exit(2)

    def compute_shear_force_RBS(self, connection_type, beam_dead_load, beam_live_load, span, bottom_column):
        """
        This method calculates the shear force at the center of RBS (step 4 in ANSI Section 5.8)
        :return: a dictionary which includes the shear forces
        """
        # Be cautious: beam_dead_load read here is in the unit of lb/ft
        # The unit should be converted from lb/ft to kips/inch
        wu = 1.2*(beam_dead_load*0.001/12) + 0.5*(beam_live_load*0.001/12) + 0.2*0
        Sh = self.left_RBS_dimension['a'] + self.left_RBS_dimension['b']/2
        Lh = span*12.0 - 2 * bottom_column.section['d'] - 2 * Sh
        if connection_type == 'typical exterior' or connection_type == 'top exterior':
            self.shear_force['VRBS1'] = 2*self.moment['Mpr1']/Lh + wu*Lh/2
        elif connection_type == 'typical interior' or connection_type == 'top interior':
            self.shear_force['VRBS1'] = 2 * self.moment['Mpr1'] / Lh + wu * Lh / 2
            self.shear_force['VRBS2'] = 2 * self.moment['Mpr2'] / Lh - wu * Lh / 2
        else:
            sys.stderr.write('Error: wrong type of connection specified!\nNo such keyword for connection exists!\n')
            sys.exit(2)

    def compute_probable_moment_column_face(self, connection_type):
        """
        This method calculates the probable maximum moment at the face of the column. (step 5 in ANSI Section 5.8)
        :return: Store probable maximum moment at column face into the dictionary
        """
        Sh = self.left_RBS_dimension['a'] + self.left_RBS_dimension['b']/2
        if connection_type == 'typical exterior' or connection_type == 'top exterior':
            self.moment['Mf1'] = self.moment['Mpr1'] + self.shear_force['VRBS1']*Sh
        elif connection_type == 'typical interior' or connection_type == 'top interior':
            self.moment['Mf1'] = self.moment['Mpr1'] + self.shear_force['VRBS1']*Sh
            self.moment['Mf2'] = self.moment['Mpr2'] + self.shear_force['VRBS2']*Sh
        else:
            sys.stderr.write('Error: wrong type of connection specified!\nNo such keyword for connection exists!\n')
            sys.exit(2)

    def compute_plastic_moment(self, connection_type, steel, left_beam, right_beam):
        """
        This method calculates the plastic moment of the beam based on expected yield stress.
        (step 6 in ANSI Section 5.8)
        :return: Store the plastic moment to the dictionary.
        """
        if connection_type == 'typical exterior' or connection_type == 'top exterior':
            self.moment['Mpe1'] = steel.Ry * steel.Fy * left_beam.section['Zx']
        elif connection_type == 'typical interior' or connection_type == 'top interior':
            self.moment['Mpe1'] = steel.Ry * steel.Fy * left_beam.section['Zx']
            self.moment['Mpe2'] = steel.Ry * steel.Fy * right_beam.section['Zx']
        else:
            sys.stderr.write('Error: wrong type of connection specified!\nNo such keyword for connection exists!\n')
            sys.exit(2)

    def check_moment_column_face(self, connection_type):
        """
        This method checks whether the plastic moment is greater than the actual moment at column face.
        (step 7 in ANSI Section 5.8)
        :return: boolean result stored in is_feasible dictionary.
        """
        phi_d = 1.0
        if connection_type == 'typical exterior' or connection_type == 'top exterior':
            if phi_d*self.moment['Mpe1'] >= self.moment['Mf1']:
                self.is_feasible['flexural strength'] = True
            else:
                sys.stderr.write('Plastic moment at column face is not sufficient!\n')
                self.is_feasible['flexural strength'] = False
        elif connection_type == 'typical interior' or connection_type == 'top interior':
            if (phi_d*self.moment['Mpe1'] >= self.moment['Mf1']
                    and phi_d*self.moment['Mpe2'] >= self.moment['Mf2']):
                self.is_feasible['flexural strength'] = True
            else:
                sys.stderr.write('Plastic moment at column face is not sufficient!\n')
                self.is_feasible['flexural strength'] = False
        else:
            sys.stderr.write('Error: wrong type of connection specified!\nNo such keyword for connection exists!\n')
            sys.exit(2)

    def check_shear_strength(self, connection_type, beam_dead_load, beam_live_load, left_beam, right_beam):
        """
        This method checks whether the beam shear strength is sufficient for the required shear strength.
        (step 8 in ANSI Section 5.8)
        :return: boolean result stored in is_feasible dictionary.
        """
        wu = 1.2 * (beam_dead_load * 0.001 / 12) + 0.5 * (beam_live_load * 0.001 / 12) + 0.2 * 0
        Sh = self.left_RBS_dimension['a'] + self.left_RBS_dimension['b'] / 2
        if connection_type == 'typical exterior' or connection_type == 'top exterior':
            self.shear_force['Vu1'] = self.shear_force['VRBS1'] + wu*Sh
            if left_beam.strength['shear'] >= self.shear_force['Vu1']:
                self.is_feasible['shear strength'] = True
            else:
                sys.stderr.write('Shear strength is not sufficient!\n')
                self.is_feasible['shear strength'] = False
        elif connection_type == 'typical interior' or connection_type == 'top interior':
            self.shear_force['Vu1'] = self.shear_force['VRBS1'] + wu * Sh
            self.shear_force['Vu2'] = self.shear_force['VRBS2'] + wu * Sh
            if (left_beam.strength['shear'] >= self.shear_force['Vu1']
                    and right_beam.strength['shear'] >= self.shear_force['Vu2']):
                self.is_feasible['shear strength'] = True
            else:
                sys.stderr.write('Shear strength is not sufficient!\n')
                self.is_feasible['shear strength'] = False
        else:
            sys.stderr.write('Error: wrong type of connection specified!\nNo such keyword for connection exists!\n')
            sys.exit(2)

    def check_column_beam_relationships(self, connection_type, steel, left_beam, right_beam, top_column, bottom_column):
        """
        This method examines whether the "strong-column-weak-beam" criteria is satisfied.
        (step 11 in ANSI Section 5.8)
        :return: boolean result stored in is_feasible dictionary.
        """
        if connection_type == 'top exterior':
            # For column in one-story building or top story:
            # Strong column weak beam is exempted if the column axial load ratio < 0.3 for all load combinations except
            # those using amplified seismic load.
            # If not the case, still need to check the Mpc/Mpb ratio.
            if bottom_column.demand['axial']/bottom_column.strength['axial'] < 0.3:
                self.is_feasible['SCWB'] = True
            else:
                Puc_bot = bottom_column.demand['axial']
                Ag_bot = bottom_column.section['A']
                ht_bot = bottom_column.unbraced_length['x']*12.2  # Be cautious: convert the unit from ft to inch
                Zx_bot = bottom_column.section['Zx']
                db = left_beam.section['d']
                # Compute the moment summation for column
                self.moment['Mpc'] = Zx_bot * (steel.Fy-Puc_bot/Ag_bot) * (ht_bot/(ht_bot-db/2))
                # Compute the moment summation for beam
                self.moment['Muv'] = self.shear_force['VRBS1'] * (self.left_RBS_dimension['a']
                                                                  + self.left_RBS_dimension['b']/2
                                                                  + bottom_column.section['d']/2)
                self.moment['Mpb'] = self.moment['Mpr1'] + self.moment['Muv']
                # Perform the strong column weak beam check
                if self.moment['Mpc']/self.moment['Mpb'] >= STRONG_COLUMN_WEAK_BEAM_RATIO:
                    self.is_feasible['SCWB'] = True
                else:
                    sys.stderr.write('Strong column weak beam (top exterior) is not satisfied!\n')
                    self.is_feasible['SCWB'] = False
        elif connection_type == 'top interior':
            # For column in one-story building or top story:
            # Strong column weak beam is exempted if the column axial load ratio < 0.3 for all load combinations except
            # those using amplified seismic load.
            # If not the case, still need to check the Mpc/Mpb ratio.
            if bottom_column.demand['axial']/bottom_column.strength['axial'] < 0.3:
                self.is_feasible['SCWB'] = True
            else:
                Puc_bot = bottom_column.demand['axial']
                Ag_bot = bottom_column.section['A']
                h_bot = bottom_column.unbraced_length['x']*12.0  # Be cautious: convert the unit from ft to inch
                Zx_bot = bottom_column.section['Zx']
                # Generally the left and right beams have the identical beam sizes
                db = (left_beam.section['d'] + right_beam.section['d']) / 2
                # Compute the moment summation for column
                self.moment['Mpc'] = Zx_bot * (steel.Fy-Puc_bot/Ag_bot) * (h_bot/(h_bot-db/2))
                # Compute the moment summation for beam
                self.moment['Muv'] = (self.shear_force['VRBS1']+self.shear_force['VRBS2']) \
                                     * (self.left_RBS_dimension['a']+self.left_RBS_dimension['b']/2
                                        +bottom_column.section['d']/2)
                self.moment['Mpb'] = self.moment['Mpr1'] + self.moment['Mpr2'] + self.moment['Muv']
                # Perform the strong column weak beam check
                if self.moment['Mpc']/self.moment['Mpb'] >= STRONG_COLUMN_WEAK_BEAM_RATIO:
                    self.is_feasible['SCWB'] = True
                else:
                    sys.stderr.write('Strong column weak beam (top interior) is not satisfied!\n')
                    self.is_feasible['SCWB'] = False
        elif connection_type == 'typical exterior':
            # This connection has two columns and one beam
            Puc_top = top_column.demand['axial']
            Puc_bot = bottom_column.demand['axial']
            Ag_top = top_column.section['A']
            Ag_bot = bottom_column.section['A']
            ht_top = top_column.unbraced_length['x']*12.0  # Be cautious: convert the unit from ft to inch
            ht_bot = bottom_column.unbraced_length['x']*12.0  # Be cautious: convert the unit from ft to inch
            Zx_top = top_column.section['Zx']
            Zx_bot = bottom_column.section['Zx']
            db = left_beam.section['d']
            # Compute the moment summation for column
            self.moment['Mpc'] = Zx_top * (steel.Fy-Puc_top/Ag_top) * (ht_top/(ht_top-db/2)) \
                                 + Zx_bot * (steel.Fy-Puc_bot/Ag_bot) * (ht_bot/(ht_bot-db/2))
            # Compute the moment summation for beam
            self.moment['Muv'] = self.shear_force['VRBS1'] * (self.left_RBS_dimension['a']
                                                              + self.left_RBS_dimension['b']/2
                                                              + bottom_column.section['d']/2)
            self.moment['Mpb'] = self.moment['Mpr1'] + self.moment['Muv']
            # Perform the strong column weak beam check
            if self.moment['Mpc']/self.moment['Mpb'] >= STRONG_COLUMN_WEAK_BEAM_RATIO:
                self.is_feasible['SCWB'] = True
            else:
                sys.stderr.write('Strong column weak beam is not satisfied!\n')
                self.is_feasible['SCWB'] = False
        elif connection_type == 'typical interior':
            # This connection has two columns and two beams
            Puc_top = top_column.demand['axial']
            Puc_bot = bottom_column.demand['axial']
            Ag_top = top_column.section['A']
            Ag_bot = bottom_column.section['A']
            h_top = top_column.unbraced_length['x']*12.0  # Be cautious: convert the unit from ft to inch
            h_bot = bottom_column.unbraced_length['x']*12.0  # Be cautious: convert the unit from ft to inch
            Zx_top = top_column.section['Zx']
            Zx_bot = bottom_column.section['Zx']
            # Generally the left and right beams have the identical beam sizes
            db = (left_beam.section['d'] + right_beam.section['d']) / 2
            # Compute the moment summation for column
            self.moment['Mpc'] = Zx_top * (steel.Fy - Puc_top / Ag_top) * (h_top / (h_top - db / 2)) \
                                 + Zx_bot * (steel.Fy - Puc_bot / Ag_bot) * (h_bot / (h_bot - db / 2))
            # Compute the moment summation for beam
            self.moment['Muv'] = (self.shear_force['VRBS1']+self.shear_force['VRBS2']) \
                                 * (self.left_RBS_dimension['a']+self.left_RBS_dimension['b']/2
                                    + bottom_column.section['d']/2)
            self.moment['Mpb'] = self.moment['Mpr1'] + self.moment['Mpr2'] + self.moment['Muv']
            # Perform the strong column weak beam check
            if self.moment['Mpc'] / self.moment['Mpb'] >= STRONG_COLUMN_WEAK_BEAM_RATIO:
                self.is_feasible['SCWB'] = True
            else:
                sys.stderr.write('Strong column weak beam is not satisfied!\n')
                self.is_feasible['SCWB'] = False
        else:
            sys.stderr.write('Error: wrong type of connection specified!\nNo such keyword for connection exists!\n')
            sys.exit(2)

    def determine_doubler_plate(self, connection_type, steel, left_beam, right_beam, bottom_column, top_column):
        """
        This method determines the panel zone thickness (doubler plates).
        :return: a scalar which denotes the doubler plate thickness.
        """
        if connection_type == 'top exterior':
            # Connection has one left beam and one bottom column
            h_bot = bottom_column.unbraced_length['x']*12.0  # Be cautious: convert the unit from ft to inch
            db = left_beam.section['d']
            tf = left_beam.section['tf']
            self.shear_force['Vc'] = (self.moment['Mf1']+0) / (h_bot/2+0)
            self.shear_force['Ru'] = (self.moment['Mf1']+0)/(db-tf) - self.shear_force['Vc']
        elif connection_type == 'typical exterior':
            # Connection has one left beam and two columns
            h_bot = bottom_column.unbraced_length['x']*12.0  # Be cautious: convert the unit from ft to inch
            h_top = top_column.unbraced_length['x']*12.0  # Be cautious: convert the unit from ft to inch
            db = left_beam.section['d']
            tf = left_beam.section['tf']
            self.shear_force['Vc'] = (self.moment['Mf1']+0) / (h_bot/2+h_top/2)
            self.shear_force['Ru'] = (self.moment['Mf1']+0)/(db-tf) - self.shear_force['Vc']
        elif connection_type == 'top interior':
            # Connection has two beams and one bottom column
            h_bot = bottom_column.unbraced_length['x']*12.0  # Be cautious: convert the unit from ft to inch
            # Actually left and right beams have the identical sizes
            db = (left_beam.section['d'] + right_beam.section['d'])/2
            tf = (left_beam.section['tf'] + right_beam.section['tf'])/2
            self.shear_force['Vc'] = (self.moment['Mf1']+self.moment['Mf2']) / (h_bot/2)
            self.shear_force['Ru'] = (self.moment['Mf1']+self.moment['Mf2'])/(db-tf) - self.shear_force['Vc']
        elif connection_type == 'typical interior':
            # Connection has two beams and two columns
            h_bot = bottom_column.unbraced_length['x']*12.0  # Be cautious: convert the unit from ft to inch
            h_top = top_column.unbraced_length['x']*12.0  # Be cautious: convert the unit from ft to inch
            db = (left_beam.section['d'] + right_beam.section['d']) / 2
            tf = (left_beam.section['tf'] + right_beam.section['tf']) / 2
            self.shear_force['Vc'] = (self.moment['Mf1']+self.moment['Mf2']) / (h_bot/2+h_top/2)
            self.shear_force['Ru'] = (self.moment['Mf1']+self.moment['Mf2'])/(db-tf) - self.shear_force['Vc']
        else:
            sys.stderr.write('Error: wrong type of connection specified!\nNo such keyword for connection exists!\n')
            sys.exit(2)
        # Compute the shear strength of the panel zone
        phi = 1.0
        dc = bottom_column.section['d']
        tw = bottom_column.section['tw']
        bcf = bottom_column.section['bf']
        tcf = bottom_column.section['tf']
        db = left_beam.section['d']
        self.shear_force['Rn'] = 0.60 * steel.Fy * dc * tw * (1+(3*bcf*tcf**2)/(db*dc*tw))
        # Compute the doubler plate thickness
        if phi*self.shear_force['Rn'] >= self.shear_force['Ru']:
            # Panel zone shear strength is sufficient ==> no need for doubler plate
            self.doubler_plate_thickness = 0
        else:
            # Panel zone shear strength is not sufficient ==> need doubler plate
            required_tp = (self.shear_force['Ru'] - 0.60*steel.Fy*(3*bcf*tcf**2)/db) / (0.60*steel.Fy*dc)
            tp = 0.25  # Assumed doubler plate thickness
            while tp < required_tp:
                tp += 0.25  # Update the thickness at an increment of 0.25 until it reaches the requirement
            self.doubler_plate_thickness = tp

    def check_flag(self):
        """
        This method is used to test whether the connection passed all checks.
        :return: a boolean variable indicating the connection is feasible or note.
        """
        # Loop over each checking result to see if it is feasible or not
        self.flag = True
        for key in self.is_feasible.keys():
            if self.is_feasible[key] == False:
                self.flag = False
        return self.flag
