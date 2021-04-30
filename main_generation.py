# This file is the main file that calls functions to generate the nonlinear
# OpenSees models
# Users need to specify the system argument in this file.
# Users also need to specify the variables in "global_variables.py"

# The reason why I create this "redundant" file is to generate nonlinear
# OpenSees models for a bunch of buildings (not a single one)

##########################################################################
#                       Relevant Publications                            #
##########################################################################

# Add relevant publications below

##########################################################################
#                       Load Necessary Packages                          #
##########################################################################

import os
import pickle
import time


from global_variables import base_directory
from global_variables import SECTION_DATABASE
from global_variables import COLUMN_DATABASE
from global_variables import BEAM_DATABASE
from model_generation import model_generation

##########################################################################
#                       Generate Models                                  #
##########################################################################

IDs = [0]
for id in IDs:
    building_id = 'Building_' + str(id)
    print(building_id)
    model_generation(building_id, base_directory)

##########################################################################
#                Run Models in Sequence (not Parallel)                   #
##########################################################################

# # Define building IDs for running analysis
# ID1 = list(range(0, 81, 1))
# ID2 = list(range(81, 566, 3))
# ID3 = list(range(567, 1052, 3))
# ID4 = [1053, 1056, 1059, 1062, 1065, 1068, 1071, 1074, 1080, 1083, 1086, 1089, 1092, 1095, 1098, 1101, 1104, 1107, 1110, 1113, 1116, 1119, 1122, 1125, 1128, 1134, 1137, 1140, 1143, 1146, 1149, 1152, 1155, 1158, 1161, 1164, 1167, 1170, 1173, 1176, 1188, 1191, 1194, 1197, 1200, 1203, 1206, 1209, 1212, 1215, 1218, 1221, 1224, 1227, 1242, 1245, 1248, 1251, 1254, 1257, 1260, 1263, 1266, 1269, 1272, 1275, 1278, 1281, 1284, 1296, 1299, 1302, 1305, 1308, 1311, 1314, 1317, 1320, 1323, 1326, 1329, 1332, 1335, 1338, 1350, 1353, 1356, 1359, 1362, 1365, 1368, 1371, 1374, 1377, 1380, 1383, 1404, 1407, 1410, 1413, 1416, 1419, 1422, 1425, 1428, 1431, 1434, 1437, 1458, 1461, 1464, 1467, 1470, 1473, 1476, 1479, 1482, 1485, 1488, 1491, 1512, 1515, 1518, 1521, 1524, 1527, 1530, 1533]
# ID5 = [1539, 1542, 1566, 1569, 1572, 1575, 1578, 1581, 1584, 1587, 1590, 1593, 1596, 1599, 1620, 1623, 1626, 1629, 1632, 1635, 1638, 1641, 1644, 1647, 1650, 1653, 1674, 1677, 1680, 1683, 1686, 1689, 1692, 1695, 1701, 1704, 1707, 1728, 1731, 1734, 1737, 1740, 1743, 1746, 1749, 1755, 1758, 1761, 1782, 1785, 1788, 1791, 1794, 1797, 1800, 1803, 1809, 1812, 1815, 1836, 1839, 1842, 1845, 1848, 1851, 1863, 1866, 1890, 1893, 1896, 1899, 1902, 1905, 1917, 1920, 1944, 1947, 1950, 1953, 1956, 1959, 1971, 1998, 2001, 2004, 2007, 2010, 2013]
#
# IDs = ID1 + ID2 + ID3 + ID4 + ID5
# # Define the analysis type
# # Options: EigenValueAnalysis, PushoverAnalysis, or DynamicAnalysis
# # DynamicAnalysis is not recommended to run on your own PC as it is better
# # to run a supercomputer.
# analysis_type = 'PushoverAnalysis'
# # Loop over each building model and perform the desired analysis
# for id in IDs:
#     # The folder where models are stored
#     building_id = 'Building_' + str(id)
#     # The target folder for current analysis_type
#     target_model = base_directory / 'BuildingNonlinearModels' / building_id / analysis_type
#     # Change the working directory to that model folder
#     os.chdir(target_model)
#     # Display which model you are analyzing
#     print('Current model is: ', building_id)
#     # Run OpenSees.exe file
#     os.system('OpenSees Model.tcl')