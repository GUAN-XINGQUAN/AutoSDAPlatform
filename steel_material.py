# This file is used to define the class of Building
# Developed by GUAN, XINGQUAN @ UCLA in June 2018
# Updated in Sept. 2018


# #########################################################################
#                     Define a class including steel material property    #
# #########################################################################


class SteelMaterial(object):
    """
    This class is used to define the steel material.
    It includes the following physical quantities:
    (1) Yield stress (Fy)
    (2) Ultimate stress (Fu)
    (3) Young's modulus (E)
    (4) Ry value
    """

    def __init__(self, yield_stress=50, ultimate_stress=65, elastic_modulus=29000, Ry_value=1.1):
        """
        :param yield_stress: Fy of steel material, default value is 50 ksi
        :param elastic_modulus: E of steel material, default value is 29000 ksi
        """
        self.Fy = yield_stress
        self.Fu = ultimate_stress
        self.E = elastic_modulus
        self.Ry = Ry_value