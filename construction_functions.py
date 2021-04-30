# This file is used to define functions used to create the column, beam, and connection sets used in "seismic_design.py"
# Developed by GUAN, XINGQUAN @ UCLA in April 2021

import sys

from column_component import Column
from beam_component import Beam
from connection_part import Connection


def create_column_set(building, elastic_demand, steel):
    """
    This function is used to create a set of columns for the entire building.
    :param building: a class defined in "building_information.py" file.
    :param elastic_demand: a class defined in "elastic_output.py" file.
    :param steel: a class defined in "steel_material.py" file.
    :return: a M*N list where M represents the number of story and N represents the number of columns per story.
            Each element is an object of the class Column defined in "column_component.py" file.
    """
    # Check all columns to see whether they have enough strengths
    # Initialize a list to store all column instances
    column_set = []
    not_feasible_column = []  # Used to record which column [story][column_no] is not feasible
    for story in range(building.geometry['number of story']):
        one_story_columns = []
        for column_no in range(building.geometry['number of X bay'] + 1):
            axial_demand = abs(elastic_demand.dominate_load['column axial'][story, 2 * column_no])
            shear_demand = abs(elastic_demand.dominate_load['column shear'][story, 2 * column_no])
            moment_bottom = elastic_demand.dominate_load['column moment'][story, 2 * column_no]
            moment_top = elastic_demand.dominate_load['column moment'][story, 2 * column_no + 1]
            if column_no == 0 or column_no == building.geometry['number of X bay']:
                column_type = 'exterior column'
            else:
                column_type = 'interior column'
            length = (building.geometry['floor height'][story + 1] - building.geometry['floor height'][story]).item()
            # Build instance for each column member
            temp_column = Column(building.member_size[column_type][story], axial_demand, shear_demand, moment_bottom,
                                 moment_top, length, length, steel)
            one_story_columns.append(temp_column)
            # Check the flag of each column
            if not temp_column.check_flag():
                sys.stderr.write('column_%s%s is not feasible!!!\n' % (story, column_no))
                not_feasible_column.append([story, column_no])
        column_set.append(one_story_columns)
    return column_set, not_feasible_column


def create_beam_set(building, elastic_demand, steel):
    """
    This function is used to create a set of beams for the entire building.
    :param building: a class defined in "building_information.py" file.
    :param elastic_demand: a class defined in "elastic_output.py" file.
    :param steel: a class defined in "steel_material.py" file.
    :return: a M*N list where M represents the number of story and N represents the number of bays per story.
            Each element is an object of the class Beam defined in "beam_component.py" file.
    """
    # Initialize a list to store all beam instances
    beam_set = []
    not_feasible_beam = []  # Used to record which beam [story, bay] does not have enough strength.
    for story in range(building.geometry['number of story']):
        one_story_beams = []
        for bay in range(building.geometry['number of X bay']):
            length = building.geometry['X bay width']
            shear_demand = abs(elastic_demand.dominate_load['beam shear'][story, 2 * bay])
            moment_left = elastic_demand.dominate_load['beam moment'][story, 2 * bay]
            moment_right = elastic_demand.dominate_load['beam moment'][story, 2 * bay + 1]
            # Build instance for each beam member
            temp_beam = Beam(building.member_size['beam'][story], length,
                             shear_demand, moment_left, moment_right, steel)
            one_story_beams.append(temp_beam)
            # Check the flag of each beam
            if not temp_beam.check_flag():
                sys.stderr.write('beam_%s%s is not feasible!!!\n' % (story, bay))
                not_feasible_beam.append([story, bay])
        beam_set.append(one_story_beams)
    return beam_set, not_feasible_beam


def create_connection_set(building, column_set, beam_set, steel):
    """
    This function is used to create a set of joint connections for the entire building.
    :param building: a class defined in "building_information.py" file.
    :param column_set: a set of columns with M*N dimensions.
    :param beam_set: a set of beams with M*N dimensions.
    :param steel: a class defined in "steel_material.py" file.
    :return: a M*N list where M represents the number of story and N represents the number of connections per story.
            Each element is an object of the class Connection defined in "connection_part.py" file.
    """
    # Check each beam-column connection to see if they satisfy the AISC/ANSI
    # Initialize a list to store all connection instances
    connection_set = []
    # Record which connection [story#, column#] is not feasible.
    not_feasible_connection = []
    for story in range(building.geometry['number of story']):
        one_story_connection = []
        for connection_no in range(building.geometry['number of X bay']+1):
            dead_load = building.gravity_loads['beam dead load'][story]  # Unit: lb/ft
            live_load = building.gravity_loads['beam live load'][story]  # Unit: lb/ft
            span = building.geometry['X bay width']  # Unit: ft
            # The connection is not on roof
            if story != (building.geometry['number of story'] - 1):
                # The connection is an exterior joint
                if connection_no == 0:
                    temp_connection = Connection('typical exterior', steel, dead_load, live_load, span,
                                                 left_beam=beam_set[story][connection_no],
                                                 right_beam=None,
                                                 top_column=column_set[story + 1][connection_no],
                                                 bottom_column=column_set[story][connection_no])
                # The connection is an exterior joint
                elif connection_no == building.geometry['number of X bay']:
                    temp_connection = Connection('typical exterior', steel, dead_load, live_load, span,
                                                 left_beam=beam_set[story][connection_no-1],
                                                 right_beam=None,
                                                 top_column=column_set[story + 1][connection_no],
                                                 bottom_column=column_set[story][connection_no])
                # The connection is an interior joint
                else:
                    temp_connection = Connection('typical interior', steel, dead_load, live_load, span,
                                                 left_beam=beam_set[story][connection_no - 1],
                                                 right_beam=beam_set[story][connection_no],
                                                 top_column=column_set[story + 1][connection_no],
                                                 bottom_column=column_set[story][connection_no])
            # The connection is not on roof
            else:
                # The connection is an left top exterior joint
                if connection_no == 0:
                    temp_connection = Connection('top exterior', steel, dead_load, live_load, span,
                                                 left_beam=beam_set[story][connection_no],
                                                 right_beam=None,
                                                 top_column=None,
                                                 bottom_column=column_set[story][connection_no])
                # The connection is an right top exterior joint
                elif connection_no == building.geometry['number of X bay']:
                    temp_connection = Connection('top exterior', steel, dead_load, live_load, span,
                                                 left_beam=beam_set[story][connection_no-1],
                                                 right_beam=None,
                                                 top_column=None,
                                                 bottom_column=column_set[story][connection_no])

                # The connection is an top interior joint
                else:
                    temp_connection = Connection('top interior', steel, dead_load, live_load, span,
                                                 left_beam=beam_set[story][connection_no],
                                                 right_beam=beam_set[story][connection_no],
                                                 top_column=None,
                                                 bottom_column=column_set[story][connection_no])
            one_story_connection.append(temp_connection)
            if not temp_connection.check_flag():
                sys.stderr.write('connection_%s%s is not feasible!!!\n' % (story, connection_no))
                not_feasible_connection.append([story, connection_no])
            #   sys.exit(1)
        connection_set.append(one_story_connection)
    return connection_set, not_feasible_connection
