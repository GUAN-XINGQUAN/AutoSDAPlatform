##############################################################################################################################
# DefineFunctionsAndProcedures                                                                                               #
#   This file will be used to define functions and procedures that are used in the rest of the program                       # 
#                                                                                                                            #
# Created by: Henry Burton, Stanford University, 2010                                                                        #
# Revised by: XINGQUAN GUAN, UCLA, 2018
#                                                                                                                            #
# Units: kips, inches, seconds                                                                                               #
##############################################################################################################################

##############################################################################################################################
#                                Load Section Database and Create the Section Property                                       #
##############################################################################################################################

proc SectionProperty { shape } {
    set input_file  [file normalize "Database.csv"];
    set line {}
    set i 0
    if {[catch {set file_in [open $input_file r]} err_msg]} {
    puts "Failed to open the file for reading: $err_msg"
    return
    }
    set content [read $file_in]
    close $file_in
    
    foreach line [split $content "\n"] {
        set propde [split $line ","];
        set name1 [lindex $propde 2];
        set name2 [lindex $propde 80];
        if {[string equal $name1 $shape]} {
            set name [lindex $propde 2];  # lindex 0  AISC shape size
            set d [lindex $propde 6];     # lindex 1  Section Depth: inch
            set A [lindex $propde 5];     # lindex 2  Section Area: inch^2
            set bf [lindex $propde 11];   # lindex 3  Flange width: inch
            set tw [lindex $propde 16];   # lindex 4  Web thickness: inch
            set tf [lindex $propde 19];   # lindex 5  Flange thickness: inch
            set Ix [lindex $propde 38];   # lindex 6  Moment of inertia about major axis: inch^4
            set Iy [lindex $propde 42];   # lindex 7  Moment of inertia about minor axis: inch^4
            set Zx [lindex $propde 39];   # lindex 8  Plastic section modulus about major axis: inch^3
            set Zy [lindex $propde 43];   # lindex 9  Plastic section modulus about minor axis: inch^3
            set ry [lindex $propde 45];   # lindex 10 Radius of gyration about major axis: inch
            set J [lindex $propde 49];    # lindex 11 Torsion constant: inch^4
        }
        if {[string equal $name2 $shape]} {
            set name [lindex $propde 80];                 # lindex 0  
            set d [lindex $propde 83];                    # lindex 1
            set A [lindex $propde 82];                    # lindex 2
            set bf [lindex $propde 88];                   # lindex 3
            set tw [lindex $propde 93];                   # lindex 4
            set tf [lindex $propde 96];                   # lindex 5
            set Ix [expr ([lindex $propde 115])*10**6];   # lindex 6
            set Iy [expr ([lindex $propde 119])*10**6];   # lindex 7
            set Zx [expr ([lindex $propde 116])*10**3];   # lindex 8
            set Zy [expr ([lindex $propde 120])*10**3];   # lindex 9
            set ry [lindex $propde 122];                  # lindex 10
            set J [expr ([lindex $propde 126])*10**3];    # lindex 11
        }
    }
    set Prop [list $name $d $A $bf $tw $tf $Ix $Iy $Zx $Zy $ry $J];
    return $Prop
}

 
##############################################################################################################################
#                                Define Nodes Around Panel Zone for 2D Frame                                                 #
##############################################################################################################################

proc NodesAroundPanelZone {ColPier Level XCoordinate YCoordinate PanelSize MaximumFloor MaximumCol} {
# Input argument explanation:
# Level: the floor level for frame, ground floor is 1.
# ColPier: the column ID, starting from 1 to the number of columns in each frame
# XCoordinate: X coodinate of the column centerline
# YCoordinate: Y coordinate of the beam centerline
# PanelSize: a list with two elements: {a b}:
#            a: the depth of column
#            b: the depth of beam


# Node Label Convention:
# Pier number_Level_Position ID
# Pier number: 1,2,3,4... used to indicate which column pier;
# Level:1,2,3,4... used to indicate the floor level
# Position ID: two digits: 
#                   00: specially used for ground floor
#                   01-12: nodes for Panel Zone
#                   01: top left node
#                   02: top left node
#                   03: top right node
#                   04: top right node
#                   05: bottom right node
#                   06: bottom right node
#                   07: bottom left node
#                   08: bottom left node
#                   09: mid left node
#                   10: top mid node
#                   11: mid right node
#                   12: bottom mid node
#                   13-18: nodes for Plastic Hinge
#                   13: left(negative) beam node
#                   14: Top(positive) column node
#                   15: right(positive) beam node
#                   16: Bottom(negative) column node
if {$Level == 1} {
    node [format %s%s%s $ColPier $Level 10] [expr $XCoordinate] [expr $YCoordinate];
    node [format %s%s%s $ColPier $Level 14] [expr $XCoordinate] [expr $YCoordinate];
} else {
    set dc [expr ([lindex $PanelSize 0]) / 2.0];    
    set db [expr ([lindex $PanelSize 1]) / 2.0];
    
    # define nodes in X direction panel zone 
    node [format %s%s%s $ColPier $Level 01] [expr $XCoordinate - $dc] [expr $YCoordinate + $db];
    node [format %s%s%s $ColPier $Level 02] [expr $XCoordinate - $dc] [expr $YCoordinate + $db];
    node [format %s%s%s $ColPier $Level 03] [expr $XCoordinate + $dc] [expr $YCoordinate + $db];
    node [format %s%s%s $ColPier $Level 04] [expr $XCoordinate + $dc] [expr $YCoordinate + $db];
    node [format %s%s%s $ColPier $Level 05] [expr $XCoordinate + $dc] [expr $YCoordinate - $db];
    node [format %s%s%s $ColPier $Level 06] [expr $XCoordinate + $dc] [expr $YCoordinate - $db];
    node [format %s%s%s $ColPier $Level 07] [expr $XCoordinate - $dc] [expr $YCoordinate - $db];
    node [format %s%s%s $ColPier $Level 08] [expr $XCoordinate - $dc] [expr $YCoordinate - $db];
    node [format %s%s%s $ColPier $Level 09] [expr $XCoordinate - $dc] $YCoordinate;
    node [format %s%s%s $ColPier $Level 11] [expr $XCoordinate + $dc] $YCoordinate;
    node [format %s%s%s $ColPier $Level 10] $XCoordinate [expr $YCoordinate + $db];
    node [format %s%s%s $ColPier $Level 12] $XCoordinate [expr $YCoordinate - $db];
    
    # define nodes for column hinge
    node [format %s%s%s $ColPier $Level 16] $XCoordinate [expr $YCoordinate - $db];
    if {$Level != $MaximumFloor} {
        node [format %s%s%s $ColPier $Level 14] $XCoordinate [expr $YCoordinate + $db];}
        
    # define nodes for xBeam hinge
    if {$ColPier != 1} {
        node [format %s%s%s $ColPier $Level 13] [expr $XCoordinate - $dc] $YCoordinate;}
    if {$ColPier != $MaximumCol} {
        node [format %s%s%s $ColPier $Level 15] [expr $XCoordinate + $dc] $YCoordinate;}
}
}


##############################################################################################################################
#                                    Define Element within Pane Zone for 2D Frame                                            #
##############################################################################################################################

proc elemPanelZone2D {eleID nodeR E VerTransfTag HorTransfTag} {
# elemPanelZone3D.tcl
# Procedure that creates panel zone elements
# 
# The process is based on Gupta 1999
# Reference:  Gupta, A., and Krawinkler, H. (1999). "Seismic Demands for Performance Evaluation of Steel Moment Resisting Frame Structures,"
#            Technical Report 132, The John A. Blume Earthquake Engineering Research Center, Department of Civil Engineering, Stanford University, Stanford, CA.
#
#
# Written by: Dimitrios Lignos
# Date: 11/09/2008
#
# Modified by: Laura Eads
# Date: 1/4/2010
# Modification: changed numbering scheme for panel zone nodes
# 
# Formal arguments
#   eleID     - unique element ID for the zero-length rotational spring
#   nodeR     - node ID for first point (top left) of panel zone --> this node creates all the others
#   E         - Young's modulus
#   G         - Shear modulus
#   S_la      - Large number for J
#   A_PZ      - area of rigid link that creates the panel zone
#   I_PZ      - moment of inertia of Rigid link that creates the panel zone
#   transfTag - geometric transformation

# define panel zone nodes
    set node01 $nodeR;              # top left of joint
    set node02 [expr $node01 + 1];  # top left of joint
    set node03 [expr $node01 + 2];  # top right of joint
    set node04 [expr $node01 + 3];  # top right of joint
    set node05 [expr $node01 + 4];  # btm right of joint
    set node06 [expr $node01 + 5];  # btm right of joint
    set node07 [expr $node01 + 6];  # btm left of joint
    set node08 [expr $node01 + 7];  # btm left of joint
    set node09 [expr $node01 + 8];  # middle left of joint (vertical middle, horizontal left)
    set node10 [expr $node01 + 9];  # top center of joint
    set node11 [expr $node01 + 10]; # middle right of joint (vertical middle, horizontal right)
    set node12 [expr $node01 + 11]; # btm center of joint
    
# create element IDs as a function of first input eleID (8 per panel zone)
    set x1 $eleID;          # left element on top of panel zone
    set x2 [expr $x1 + 1];  # right element on top of panel zone
    set x3 [expr $x1 + 2];  # top element on right side of panel zone
    set x4 [expr $x1 + 3];  # btm element on right side of panel zone
    set x5 [expr $x1 + 4];  # right element on btm of panel zone
    set x6 [expr $x1 + 5];  # left element on btm of panel zone
    set x7 [expr $x1 + 6];  # btm element on left side of panel zone
    set x8 [expr $x1 + 7];  # top element on left side of panel zone
    
    set A_PZ 1.0e12; # area of panel zone element (make much larger than A of frame elements)
    set Ipz 1.0e12;  # moment of intertia of panel zone element (make much larger than I of frame elements)

# create panel zone elements
    #                            tag    ndI     ndJ     A_PZ    E   I_PZ    transfTag
    element elasticBeamColumn    $x1    $node02 $node10 $A_PZ   $E  $Ipz    $HorTransfTag;
    element elasticBeamColumn    $x2    $node10 $node03 $A_PZ   $E  $Ipz    $HorTransfTag;
    element elasticBeamColumn    $x3    $node04 $node11 $A_PZ   $E  $Ipz    $VerTransfTag;
    element elasticBeamColumn    $x4    $node11 $node05 $A_PZ   $E  $Ipz    $VerTransfTag;
    element elasticBeamColumn    $x5    $node06 $node12 $A_PZ   $E  $Ipz    $HorTransfTag;
    element elasticBeamColumn    $x6    $node12 $node07 $A_PZ   $E  $Ipz    $HorTransfTag;
    element elasticBeamColumn    $x7    $node08 $node09 $A_PZ   $E  $Ipz    $VerTransfTag;
    element elasticBeamColumn    $x8    $node09 $node01 $A_PZ   $E  $Ipz    $VerTransfTag;
}


##############################################################################################################################
#                                             Define Rotational Spring in Panel Zone                                         #
##############################################################################################################################

proc rotPanelZone2D {eleID nodeR nodeC E Fy dc bf_c tf_c tp db Ry as} {
# Procedure that creates a rotational spring and constrains the corner nodes of a panel zone
# 
# The equations and process are based on: Krawinkler Model for Panel Zones
# Reference:  Gupta, A., and Krawinkler, H. (1999). "Seismic Demands for Performance Evaluation of Steel Moment Resisting Frame Structures,"
#            Technical Report 132, The John A. Blume Earthquake Engineering Research Center, Department of Civil Engineering, Stanford University, Stanford, CA.
#
#
# Written by: Dimitrios Lignos
# Date: 11/09/2008
#
# Formal arguments
#       eleID   - unique element ID for this zero length rotational spring
#       nodeR   - node ID which will be retained by the multi-point constraint, top right of panel zone
#       nodeC   - node ID which will be constrained by the multi-point constraint, top right of panel zone
#       E       - modulus of elasticity
#       Fy      - yield strength
#       dc      - column depth
#       bf_c    - column flange width
#       tf_c    - column flange thickness
#       tp      - panel zone thickness
#       db      - beam depth
#       Ry      - expected value for yield strength --> Typical value is 1.2
#       as      - assumed strain hardening

# Trilinear Spring
# Yield Shear
    set Vy [expr 0.55 * $Fy * $dc * $tp];
# Shear Modulus
    set G [expr $E/(2.0 * (1.0 + 0.30))]
# Elastic Stiffness
    set Ke [expr 0.95 * $G * $tp * $dc];
# Plastic Stiffness
    set Kp [expr 0.95 * $G * $bf_c * ($tf_c * $tf_c) / $db];

# Define Trilinear Equivalent Rotational Spring
# Yield point for Trilinear Spring at gamma1_y
    set gamma1_y [expr $Vy/$Ke]; set M1y [expr $gamma1_y * ($Ke * $db)];
# Second Point for Trilinear Spring at 4 * gamma1_y
    set gamma2_y [expr 4.0 * $gamma1_y]; set M2y [expr $M1y + ($Kp * $db) * ($gamma2_y - $gamma1_y)];
# Third Point for Trilinear Spring at 100 * gamma1_y
    set gamma3_y [expr 100.0 * $gamma1_y]; set M3y [expr $M2y + ($as * $Ke * $db) * ($gamma3_y - $gamma2_y)];
  
  
# Hysteretic Material without pinching and damage (same mat ID as Ele ID)
    uniaxialMaterial Hysteretic $eleID $M1y $gamma1_y  $M2y $gamma2_y $M3y $gamma3_y [expr -$M1y] [expr -$gamma1_y] [expr -$M2y] [expr -$gamma2_y] [expr -$M3y] [expr -$gamma3_y] 1 1 0.0 0.0 0.0
    
    element zeroLength $eleID $nodeR $nodeC -mat $eleID -dir 6

    equalDOF    $nodeR     $nodeC     1     2
    # Constrain the translational DOF with a multi-point constraint
    # Left Top Corner of PZ
    set nodeR_1 [expr $nodeR - 2];
    set nodeR_2 [expr $nodeR_1 + 1];
    # Right Bottom Corner of PZ
    set nodeR_6 [expr $nodeR + 2];
    set nodeR_7 [expr $nodeR_6 + 1];
    # Left Bottom Corner of PZ
    set nodeL_8 [expr $nodeR + 4];
    set nodeL_9 [expr $nodeL_8 + 1];
    #          retained constrained DOF_1 DOF_2 
    equalDOF    $nodeR_1     $nodeR_2    1     2
    equalDOF    $nodeR_6     $nodeR_7    1     2
    equalDOF    $nodeL_8     $nodeL_9    1     2
}


##############################################################################################################################
#            Define Modified IMK Deterioration Material Model for Beam and Column Plastic Hinges                             #
##############################################################################################################################

proc CreateIMKMaterial {matTag K0 n a_men My Lambda theta_p theta_pc residual theta_u} {
# Input argument explanation:
# matTag: a unique ID to represent the material
# K0: Initial stiffness of beam component before the modification of n
#     i.e., 6*E*Iz/L where E, Iz, and L are Young's modulus, moment of inertia, and length of beam
# n: a coefficient which is equal to 10 based on reference suggestion
# a_men: strain hardening ratio before modification of n
# My: effective yield strength, slightly greater than predicted bending strength, which is Fy*Z.
# Lambda: reference cumulative plastic rotation
# theta_p: pre-capping plastic rotation
# theta_pc: post-capping plastic rotation
# residual: residual strength ratio
# theta_u: ultimate rotation.
# Reference:
#           [1] Ibarra et al. (2005) Hysteretic models that incorporate strength and stiffness deterioration.
#           [2] Ibarra and Krawinkler. (2005)  Global collapse of frame structures under seismic excitation.
#           [3] Lignos (2008) Sidesway collapse of deteriorating structural systems under seismic excitation.
#           [4] Lignos and Krawinkler. (2011) Deterioration modeling of steel component in support of collapse prediction of 
#                                         steel moment frames under earthquake loading.
#			[5] Lignos et al. (2019) Proposed updates to the ASCE 41 nonlinear modeling parameters for wide-flange steel 
#											columns in support performance-based seismic engineering.
  
set Ks  [expr ($n+1.0)*$K0];  # Initial stiffness for rotational spring (hinge)
set asPosScaled [expr ($a_men)/(1.0+$n*(1.0-$a_men))];
set asNegScaled $asPosScaled;
set Lambda_S [expr (0.0+1.0)*$Lambda];  # basic strength deterioration
set Lambda_C [expr (0.0+1.0)*$Lambda];  # post-capping strength deterioration
set Lambda_A [expr (0.0+1.0)*$Lambda];  # accelerated reloading stiffness deterioration (a very large number = no cyclic deterioration)
set Lambda_K [expr (0.0+1.0)*$Lambda];  # unloading stiffness deterioration (a very large number = no cyclic deterioration)

# Built-in command:
# uniaxialMaterial Bilin $matTag $K0 $as_Plus $as_Neg $My_Plus $My_Neg $Lambda_S $Lambda_C $Lambda_A $Lambda_K 
#                       $c_S $c_C $c_A $c_K $theta_p_Plus $theta_p_Neg $theta_pc_Plus $theta_pc_Neg $Res_Pos $Res_Neg 
#                       $theta_u_Plus $theta_u_Neg $D_Plus $D_Neg
# Argument explanation: 
# http://opensees.berkeley.edu/wiki/index.php/Modified_Ibarra-Medina-Krawinkler_Deterioration_Model_with_Bilinear_Hysteretic_Response_(Bilin_Material)

# Create the modified Ibarra-Medina-Krawinkler material model
uniaxialMaterial Bilin $matTag $Ks $asPosScaled $asNegScaled $My [expr -1.0*$My] $Lambda_S $Lambda_C $Lambda_A $Lambda_K 1.0 1.0 1.0 1.0 $theta_p $theta_p $theta_pc $theta_pc $residual $residual $theta_u $theta_u 1.0 1.0;

}


##############################################################################################################################
#                         Define Rotational Spring with Modified IMK Material Models for Plastic Hinges                      #
##############################################################################################################################

proc rotBeamSpring {eleID nodeR nodeC matID stiffMatID} {
# Create a zero length element to represent the beam hinge
# Axial stiffness is extremely large
# Flexural stiffness is defined by Modified IMK material
# Input argument explanation:
# eleID: a unique ID to label the element
# nodeR: master node
# nodeC: slave node
# matID: the associated modified IMK material ID
# stiffMatID: the ID associated with the stiff material (defined in Variables.tcl)

element zeroLength $eleID $nodeR $nodeC -mat $stiffMatID $stiffMatID $matID -dir 1 2 6 -orient 1 0 0 0 1 0;

}

proc rotColumnSpring {eleID nodeR nodeC matID stiffMatID} {
# Create a zero length element to represent the column hinge
# Axial stiffness is extremely large
# Flexural stiffness is defined by Modified IMK material
# Input argument explanation:
# eleID: a unique ID to label the element
# nodeR: master node
# nodeC: slave node
# matID: the associated modified IMK material ID
# stiffMatID: the ID associated with the stiff material (defined in Variables.tcl)

element zeroLength $eleID $nodeR $nodeC -mat $stiffMatID $stiffMatID $matID -dir 1 2 6 -orient 0 1 0 1 0 0;

}


##############################################################################################################################
#                               Define Rotational Spring for Leaning Column Hinges                                           #
##############################################################################################################################

proc rotLeaningCol {eleID nodeR nodeC stiffMatID} {
# Create a zero-stiffness elastic rotational spring for the leaning column
# while constraining the translational DOFs
# Argument explanation:
# eleID: unique element ID for the zero-stiffness rotational spring
# nodeR: ID of node which will be retained by multi-point constraint
# nodeC: ID of node which will be constrained by multi-point constraint

# Spring stiffness: very small number (not using zero) to avoid numerical convergence issue
set K 1e-9;

# Create the material and zero length element (spring)
uniaxialMaterial Elastic $eleID $K;
element zeroLength $eleID $nodeR $nodeC -mat $stiffMatID $stiffMatID $eleID -dir 1 2 6 -orient 0 1 0 1 0 0;

# Constrain the translational DOF with a multi-point constraint
#           retained    constrained DOF1    DOF2
# equalDOF    $nodeR      $nodeC      1       2
}

puts "All Functions and Procedures Have Been Sourced"