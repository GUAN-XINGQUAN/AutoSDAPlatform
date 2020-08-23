# This file is used to define helpful functions that are used in either main program or user defined class
# Developed by GUAN, XINGQUAN @ UCLA in June 2018
# Updated in Sept. 2018

import numpy as np
import re
import sys

from global_variables import SECTION_DATABASE


def determine_Fa_coefficient(site_class, Ss):
    """
    This function is used to determine Fa coefficient, which is based on ASCE 7-10 Table 11.4-1
    :param Ss: a scalar given in building class
    :param site_class: a string: 'A', 'B', 'C', 'D', or 'E' given in building information
    :return: a scalar which is Fa coefficient
    """
    if site_class == 'A':
        Fa = 0.8
    elif site_class == 'B':
        Fa = 1.0
    elif site_class == 'C':
        if Ss <= 0.5:
            Fa = 1.2
        elif Ss <= 1.0:
            Fa = 1.2 - 0.4*(Ss - 0.5)
        else:
            Fa = 1.0
    elif site_class == 'D':
        if Ss <= 0.25:
            Fa = 1.6
        elif Ss <= 0.75:
            Fa = 1.6 - 0.8*(Ss - 0.25)
        elif Ss <= 1.25:
            Fa = 1.2 - 0.4*(Ss - 0.75)
        else:
            Fa = 1.0
    elif site_class == 'E':
        if Ss <= 0.25:
            Fa = 2.5
        elif Ss <= 0.5:
            Fa = 2.5 - 3.2*(Ss - 0.25)
        elif Ss <= 0.75:
            Fa = 1.7 - 2.0*(Ss - 0.5)
        elif Ss <= 1.0:
            Fa = 1.2 - 1.2*(Ss - 0.75)
        else:
            Fa = 0.9
    else:
        Fa = None
        print("Site class is entered with an invalid value")

    return Fa


def determine_Fv_coefficient(site_class, S1):
    """
    This function is used to determine Fv coefficient, which is based on ASCE 7-10 Table 11.4-2
    :param S1: a scalar given in building class
    :param site_class: a string 'A', 'B', 'C', 'D' or 'E' given in building class
    :return: a scalar which is Fv coefficient
    """
    if site_class == 'A':
        Fv = 0.8
    elif site_class == 'B':
        Fv = 1.0
    elif site_class == 'C':
        if S1 <= 0.1:
            Fv = 1.7
        elif S1 <= 0.5:
            Fv = 1.7 - 1.0*(S1 - 0.1)
        else:
            Fv = 1.3
    elif site_class == 'D':
        if S1 <= 0.1:
            Fv = 2.4
        elif S1 <= 0.2:
            Fv = 2.4 - 4*(S1 - 0.1)
        elif S1 <= 0.4:
            Fv = 2.0 - 2*(S1 - 0.2)
        elif S1 <= 0.5:
            Fv = 1.6 - 1*(S1 - 0.4)
        else:
            Fv = 1.5
    elif site_class == 'E':
        if S1 <= 0.1:
            Fv = 3.5
        elif S1 <= 0.2:
            Fv = 3.5 - 3*(S1 - 0.1)
        elif S1 <= 0.4:
            Fv = 3.2 - 4*(S1 - 0.2)
        else:
            Fv = 2.4
    else:
        Fv = None
        print("Site class is entered with an invalid value")

    return Fv


def calculate_DBE_acceleration(Ss, S1, Fa, Fv):
    """
    This function is used to calculate design spectrum acceleration parameters,
    which is based ASCE 7-10 Section 11.4
    Note: All notations for these variables can be found in ASCE 7-10.
    :param Ss: a scalar given in building information (problem statement)
    :param S1: a scalar given in building information (problem statement)
    :param Fa: a scalar computed from determine_Fa_coefficient
    :param Fv: a scalar computed from determine_Fv_coefficient
    :return: SMS, SM1, SDS, SD1: four scalars which are required for lateral force calculation
    """
    SMS = Fa * Ss
    SM1 = Fv * S1
    SDS = 2/3 * SMS
    SD1 = 2/3 * SM1
    return SMS, SM1, SDS, SD1


def determine_Cu_coefficient(SD1):
    """
    This function is used to determine Cu coefficient, which is based on ASCE 7-10 Table 12.8-1
    Note: All notations for these variables can be found in ASCE 7-10.
    :param SD1: a scalar calculated from funtion determine_DBE_acceleration
    :return: Cu: a scalar
    """
    if SD1 <= 0.1:
        Cu = 1.7
    elif SD1 <= 0.15:
        Cu = 1.7 - 2 * (SD1 - 0.1)
    elif SD1 <= 0.2:
        Cu = 1.6 - 2 * (SD1 - 0.15)
    elif SD1 <= 0.3:
        Cu = 1.5 - 1 * (SD1 - 0.2)
    elif SD1 <= 0.4:
        Cu = 1.4
    else:
        Cu = 1.4

    return Cu


def determine_floor_height(number_of_story, first_story_height, typical_story_height):
    """
    This function is used to calculate the height for each floor level: from ground floor to roof
    Obviously, the height for ground floor level is zero
    Unit: foot (ft)
    :param number_of_story: a scalar which desbribes the number of story for a certain building
    :param first_story_height: a scalar which describes the 1st story height of the building
    :param typical_story_height: a scalar which describes the typical story height for other stories
           except 1st story
    :return: an array which includes the height for each floor level (ground to roof)
    """
    floor_height = np.zeros([number_of_story + 1, 1])
    for level in range(1, number_of_story + 2):
        if level == 1:
            floor_height[level - 1] = 0
        elif level == 2:
            floor_height[level - 1] = 0 + first_story_height
        else:
            floor_height[level - 1] = first_story_height + typical_story_height * (level - 2)

    return floor_height


def calculate_Cs_coefficient(SDS, SD1, S1, T, TL, R, Ie):
    """
    This function is used to calculate the seismic response coefficient based on ASCE 7-10 Section 12.8.1
    Unit: kips, g (gravity constant), second
    Note: All notations for these variables can be found in ASCE 7-10.
    :param SDS: a scalar determined using Equation 11.4-3; output from "calculate_DBE_acceleration" function
    :param SD1: a scalar determined using Equation 11.4-4; output from "calculate_DBE_acceleration" function
    :param S1: a scalar given in building information (problem statement)
    :param T: building period; a scalar determined using Equation 12.8-1 and Cu;
              implemented in "BuildingInformation" object attribute.
    :param TL: long-period transition
    :param R: a scalar given in building information
    :param Ie: a scalar given in building information
    :return: Cs: seismic response coefficient; determined using Equations 12.8-2 to 12.8-6
    """
    # Equation 12.8-2
    Cs_initial = SDS/(R/Ie)

    # Equation 12.8-3 or 12.8-4, Cs coefficient should not exceed the following value
    if T <= TL:
        Cs_upper = SD1/(T * (R/Ie))
    else:
        Cs_upper = SD1 * TL/(T ** 2 * (R/Ie))

    # Equation 12.8-2 results shall be smaller than upper bound of Cs
    if Cs_initial <= Cs_upper:
        Cs = Cs_initial
    else:
        Cs = Cs_upper

    # Equation 12.8-5, Cs shall not be less than the following value
    Cs_lower_1 = np.max([0.044*SDS*Ie, 0.01])

    # Compare the Cs value with lower bound
    if Cs >= Cs_lower_1:
        pass
    else:
        Cs = Cs_lower_1

    # Equation 12.8-6. if S1 is equal to or greater than 0.6g, Cs shall not be less than the following value
    if S1 >= 0.6:
        Cs_lower_2 = 0.5*S1/(R/Ie)
        if Cs >= Cs_lower_2:
            pass
        else:
            Cs = Cs_lower_2
    else:
        pass

    return Cs


def determine_k_coeficient(period):
    """
    This function is used to determine the coefficient k based on ASCE 7-10 Section 12.8.3
    :param period: building period;
    :return: k: a scalar will be used in Equation 12.8-12 in ASCE 7-10
    """
    if period <= 0.5:
        k = 1
    elif period >= 2.5:
        k = 2
    else:
        k = 1 + 0.5*(period - 0.5)

    return k


def calculate_seismic_force(base_shear, floor_weight, floor_height, k):
    """
    This function is used to calculate the seismic story force for each floor level
    Unit: kip, foot
    :param base_shear: a scalar, total base shear for the building
    :param floor_weight: a vector with a length of number_of_story
    :param floor_height: a vector with a length of (number_of_story+1)
    :param k: a scalar given by "determine_k_coefficient"
    :return: Fx: a vector describes the lateral force for each floor level
    """
    # Calculate the product of floor weight and floor height
    # Note that floor height includes ground floor, which will not be used in the actual calculation.
    # Ground floor is stored here for completeness.
    weight_floor_height = floor_weight * floor_height[1:, 0]**k
    # Equation 12.8-12 in ASCE 7-10
    Cvx = weight_floor_height/np.sum(weight_floor_height)
    # Calculate the seismic story force
    seismic_force = Cvx * base_shear
    # Calculate the shear force for each story: from top story to bottom story
    story_shear = np.zeros([len(floor_weight), 1])
    for story in range(len(floor_weight)-1, -1, -1):
        story_shear[story] = np.sum(seismic_force[story:])

    return seismic_force, story_shear


def find_section_candidate(target_depth, section_database):
    """
    This function is used to find all possible section sizes that satisfies the user-specified depth.
    :param target_depth: a string which defines the depth of columns or beams, e.g. W14
    :param section_database: a dataframe read from SMF_Section_Property.csv in Library folder
    :return: a pandas Series of strings which denotes all possible sizes based on depth
    """
    candidate_index = []
    for indx in section_database['index']:
        match = re.search(target_depth, section_database.loc[indx, 'section size'])
        if match:
            candidate_index.append(indx)
    candidates = section_database.loc[candidate_index, 'section size']
    return candidates


def search_member_size(target_name, target_quantity, candidate, section_database):
    """
    This function is used to find an appropriate member size based on a certain section property
    :param target_name: a string which labels the name of target quantity.
                        Options for this string are headers of SMF_Section_Property.csv
    :param target_quantity: a scalar value of the section property, such as the value of Ix or Zx
    :param candidate: a list of strings which defines potential section sizes for beams or columns
    :param section_database: a dataframe read from "Library" SMF_Section_Property.csv
    :return: a string which states the member sizes (e.g., W14X730)
    """
    # Find the index for the candidate
    candidate_index = list(section_database.loc[section_database['section size'].isin(candidate), 'index'])
    # Calculate the difference between target moment of inertia and moment of inertia of each section
    difference = section_database.loc[candidate_index, target_name] - target_quantity
    # Find the index which gives the minimum difference
    min_index = np.where(difference == np.min(difference[difference >= 0]))
    # Note: the minimum value may not be unique. Therefore, use the first element of the min_index
    # I don't know why I need two indices for min_index in the following coding, but this works. T.T
    # Change the two indices into single index does not return pure string for section_size
    # More Info: min_index is a class "tuple". If no difference >= 0 exits, simply using the largest size.
    if not list(min_index[0]):
        section_size = section_database.loc[candidate_index[0], 'section size']
    else:
        section_size = section_database.loc[candidate_index[min_index[0][0]], 'section size']
    return section_size


def search_section_property(target_size, section_database):
    """
    This function is used to obtain the section property when section size is given.
    The output will be stored in a dictionary.
    :param target_size: a string which defines section size, e.g. 'W14X500'
    :param section_database: a dataframe read from SMF_Section_Property.csv in "Library" folder
    :return: section_info: a dictionary which includes section size, index, and associated properties.
    """
    # Loop over the sections in the SMF section database and find the one which matches the target size
    # Then the property of the target section is returned as a dictionary.
    # If target size cannot match any existing sizes in database, a warning message should be given.
    try:
        for indx in np.array(section_database['index']):
            if target_size == section_database.loc[indx, 'section size']:
                section_info = section_database.loc[indx, :]
        return section_info.to_dict()
    except:
        sys.stderr.write('Error: wrong size nominated!\nNo such size exists in section database!')
        sys.exit(1)


def decrease_member_size(candidate, current_size):
    """
    This function is used to decrease the member size one step downward
    :param candidate: a list of strings which defines the possible sizes
    :param current_size: a string which defines current member size
    :return: optimized_size: a string which defines the member size after decrease
    """
    # Find the index of the current section size in candidate pool and move it to the next one
    candidate_pool_index = candidate.index(current_size)
    if candidate_pool_index + 1 > len(candidate):
        # This means the smallest candidate still cannot make design drift close to drift limit,
        # which further means the smallest section candidate is too large.
        sys.stderr.write('The lower bound for depth initialization is too large!\n')
    return candidate[candidate_pool_index + 1]


def extract_depth(size):
    """
    This function is used to extract the depth of a section size when a size string is given.
    :param size: a string denoting a member size, e.g. 'W14X550'
    :return: a integer which denotes the depth of section. e.g. 'W14X550' ==> 14
    """
    # Use Python regular expression to extract the char between 'W' and 'X', which then become depth
    output = re.findall(r'.*W(.*)X.*', size)
    return int(output[0])


def extract_weight(size):
    """
    This function is used to extract the weight of a section size when a size string is given.
    :param size: a string denoting a member size, e.g. 'W14X550'
    :return: a integer which denotes the weight of the section, e.g. 'W14X550' ==> 550
    """
    # Use Python regular expression to extract the char after 'W' to the end of the string,
    # which then becomes weight
    output = re.findall(r'.X(.*)', size)
    return int(output[0])


def constructability_helper(section_size, identical_size_per_story, total_story, sorted_quantity):
    """
    This function is used to make every adjacent N stories have the same size and ensure that the whole list
    is in a descending order.
    :param section_size: a list of strings. e.g. ['W14X500', 'W14X550']
    :param identical_size_per_story: a scalar to denote how many stories are supposed to have same size
    :param total_story: a scalar to denote the total building stories
    :param sorted_quantity：a string to indicate the members are sorted based on which quantity,
           options: 'Ix' or 'Zx'
    :return: a list whose every adjacent N stories have same strings and the whole list is in descending order
    """
    # Determine the number of stories that have the identical member size for constructability
    if identical_size_per_story > total_story:
        per_story = total_story
    else:
        per_story = identical_size_per_story
    # Compute the index where the member size is supposed to be varied
    variation_story = []
    for i in range(0, total_story):
        if i % per_story == 0:
            variation_story.append(i)
    # Pre-process the section size list:
    # Sometimes, we may have the following case for the section list (M < N < K)
    # Story N has larger depth than M and K, but it has smaller Ix or Zx than M.
    # In this case, simply re-assign size for story N such that it has same depth with M
    # and comparable Ix or Zx with old itself.
    i = 0
    while (i < total_story - 1):
        # Find the index [i, j) such that they have same depths (j is exclusive)
        for j in range(i + 1, total_story):
            if (extract_depth(section_size[j]) != extract_depth(section_size[i])):
                break
                # If the current story chunk (with same depth) is not at the beginning nor end.
        if (i > 0 and j < total_story):
            temp_property = []
            # Find the maximum Ix or Zx in current story chunk
            for k in range(i, j):
                temp_property.append(search_section_property(section_size[k], SECTION_DATABASE)[sorted_quantity])
            current_property = max(temp_property)
            # Obtain the Ix or Zx for the stories just below and above the current story chunk.
            lower_property = search_section_property(section_size[i - 1], SECTION_DATABASE)[sorted_quantity]
            upper_property = search_section_property(section_size[j], SECTION_DATABASE)[sorted_quantity]
            # Obtain the depth for stories in current story chunk, below it, and above it.
            current_depth = extract_depth(section_size[i])
            lower_depth = extract_depth(section_size[i - 1])
            upper_depth = extract_depth(section_size[j])
            # Current story chunk has higher depth than the stories below and above
            # current Ix or Zx is less than stories below.
            # Stories below current chunk have the same or greater depth than the stories above current chunk.
            if (current_depth > lower_depth and current_depth > upper_depth and lower_depth >= upper_depth and
                current_property < lower_property and current_property > upper_property):
                # For this case, re-assign the size such that the current chunk has the same depth
                # with stories below.
                # Meanwhile, its Ix or Zx is comparable to the old itself.
                candidates = find_section_candidate('W' + str(lower_depth), SECTION_DATABASE)
                for k in range(i, j):
                    section_size[k] = search_member_size(sorted_quantity, temp_property[k - i], candidates,
                                                         SECTION_DATABASE)
        # Update current index to j
        i = j

    # Process the section list:
    # Make every adjacent N stories have the same member size.
    # It is better to trace the story from top to bottom of the building.
    starting_index = total_story - 1
    ending_index = variation_story[-1]
    while (starting_index > 0):
        # For stories within "identical story block"
        for indx in range(starting_index, ending_index, -1):
            # Only revise those size that are not identical
            if section_size[indx - 1] != section_size[indx]:
                # Obtain Ix or Zx for current story and story below.
                current_property = search_section_property(section_size[indx], SECTION_DATABASE)[sorted_quantity]
                lower_property = search_section_property(section_size[indx - 1], SECTION_DATABASE)[sorted_quantity]
                # Obtain depth for current story and story below.
                current_depth = extract_depth(section_size[indx])
                lower_depth = extract_depth(section_size[indx - 1])
                # Case 1: two depths are the same or lower depth is greater
                if (current_depth <= lower_depth):
                    # Sub-case 1.1: lower member has smaller Ix or Zx ==> change lower size to be equal to current size
                    if (current_property > lower_property):
                        section_size[indx - 1] = section_size[indx]
                    # Sub-case 1.2: lower member has larger Ix or Zx ==> change current size to be equal to lower size
                    else:
                        section_size[indx] = section_size[indx - 1]
                        # Don't forget to trace back because you just change the current story size.
                        # If the story above the current story is still within "identical story block".
                        # Then we need to revise the story above too.
                        for k in range(indx, starting_index + 1, 1):
                            section_size[k] = section_size[indx]
                # Case 2: lower depth is smaller
                else:
                    # Sub-case 2.1: lower member has smaller Zx
                    if (current_property > lower_property):
                        section_size[indx - 1] = section_size[indx]
                    # Sub-case 2.2: lower member has larger Zx
                    else:
                        # We need to change the lower member size such that it has the same depth with current story
                        # and comparable Ix or Zx with old itself.
                        candidates = find_section_candidate('W' + str(current_depth), SECTION_DATABASE)
                        section_size[indx - 1] = search_member_size(sorted_quantity, lower_property, candidates,
                                                                    SECTION_DATABASE)
                        section_size[indx] = section_size[indx - 1]
                        # Don't forget to trace back because you just change the current story size.
                        # If the story above the current story is still within "identical story block".
                        # Then we need to revise the story above too.
                        for k in range(indx, starting_index + 1, 1):
                            section_size[k] = section_size[indx]
        # For stories at the boundary between "identical story block"
        indx = variation_story[-1]
        if indx == 0:
            break
        # We need to make sure the lower block has heavier sections
        # Compute current and lower member property Ix or Zx
        current_property = search_section_property(section_size[indx], SECTION_DATABASE)[sorted_quantity]
        lower_property = search_section_property(section_size[indx - 1], SECTION_DATABASE)[sorted_quantity]
        # Compute the current and lower member depth
        current_depth = extract_depth(section_size[indx])
        lower_depth = extract_depth(section_size[indx - 1])
        # Case 1: lower member has same depth
        if (lower_depth == current_depth):
            # Case 1.1: lower member less Ix or Zx ==> change the lower size to be equal to current
            if (lower_property < current_property):
                section_size[indx - 1] = section_size[indx]
        # Case 2: lower member has smaller depth
        elif (lower_depth < current_depth):
            # Change the lower member such that it has same depth with current and comparable Ix or Zx to old itself.
            candidates = find_section_candidate('W' + str(current_depth), SECTION_DATABASE)
            section_size[indx - 1] = search_member_size(sorted_quantity, lower_property, candidates, SECTION_DATABASE)
        # Case 3: lower member has larger depth
        else:
            # Sub-case 3.1: lower member has smaller Ix or Zx
            if (lower_property < current_property):
                section_size[indx - 1] = section_size[indx]
            # Sub-case 3.2: lower member has larger Ix or Zx
            else:
                pass
        # Update the stating index for next "identical story block"
        starting_index = variation_story[-1] - 1
        if starting_index < 0:
            break
        variation_story.pop()
        # Update the ending index for next "identical story block"
        ending_index = variation_story[-1]
    return section_size

    # # Loop over all stories from top to bottom to consider the constructability
    # starting_story = total_story - 1
    # ending_story = variation_story[-1]
    # while starting_story > 0:
    #     # For stories within "identical story block"
    #     for story in range(starting_story, ending_story, -1):
    #         # Only revise size when adjacent stories have different size
    #         if section_size[story - 1] != section_size[story]:
    #             current_section_property = search_section_property(section_size[story], SECTION_DATABASE)
    #             next_section_property = search_section_property(section_size[story - 1], SECTION_DATABASE)
    #             if current_section_property[sorted_quanity] > next_section_property[sorted_quanity]:
    #                 section_size[story - 1] = section_size[story]
    #             else:
    #                 section_size[story] = section_size[story - 1]
    #
    #     # For stories at the "identical story block boundary"
    #     story = variation_story[-1]
    #     if story == 0:
    #         break
    #     if section_size[story - 1] != section_size[story]:
    #         current_depth = extract_depth(section_size[story])
    #         next_depth = extract_depth(section_size[story - 1])
    #         # Case 1: lower member has same depth but smaller weight
    #         if next_depth == current_depth:
    #             current_weight = extract_weight(section_size[story])
    #             next_weight = extract_weight(section_size[story - 1])
    #             if next_weight < current_weight:
    #                 section_size[story - 1] = section_size[story]
    #         # Case 2: lower member has smaller depth
    #         elif next_depth < current_depth:
    #             section_size[story - 1] = section_size[story]
    #         # Case 3: lower member has larger depth
    #         else:
    #             pass
    #     starting_story = variation_story[-1] - 1
    #     if starting_story < 0:
    #         break
    #     variation_story.pop()
    #     ending_story = variation_story[-1]
    # return section_size


def increase_member_size(candidate, current_size):
    """
    This function is used to increase the member size one step upward
    :param candidate: a list of strings which defines the possible sizes
    :param current_size: a string which denotes current member size
    :return: a string which denotes the member size after one step upward
    """
    # Find the index of current section size in candidate pool and move it to previous one
    candidate_pool_index = candidate.index(current_size)
    if (candidate_pool_index - 1 < 0):  # Make sure the index does not exceed the bound
        # This means the largest candidate still fails to satisfy the requirement
        sys.stderr.write('The upper bound for depth initialization is too small!\n')
    return candidate[candidate_pool_index - 1]
