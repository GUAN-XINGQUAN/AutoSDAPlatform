##############################################################################################################################
# DefineFunctionsAndProcedures                                                                                               #
# This file will be used to define functions and procedures that are used in the rest of the program                         #
# Created based on: Xiaolei Xiong, Tongji University, 2017                                                                   #
# Units: kips, inches, seconds                                                                                               #
##############################################################################################################################


##############################################################################################################################
#          	  				Load Section Database and Create the Section Property		        		    				 #
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
#          	  				       Define rotational springs for leaning column 						    				 #
##############################################################################################################################

proc rotLeaningCol {eleID nodeR nodeC} {

# 	Formal arguments
#       eleID   - unique element ID for this zero length rotational spring
#       nodeR   - node ID which will be retained by the multi-point constraint
#       nodeC   - node ID which will be constrained by the multi-point constraint

	#Spring Stiffness
	set K 1e-9; # k/in

	# Create the material and zero length element (spring)
    uniaxialMaterial Elastic  $eleID  $K	
	element zeroLength $eleID $nodeR $nodeC -mat $eleID -dir 6

	
	# Constrain the translational DOF with a multi-point constraint	
	#   		retained constrained DOF_1 DOF_2
 
	equalDOF    $nodeR     $nodeC     1     2
}



# puts "All Functions and Procedures Defined"