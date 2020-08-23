
##############################################################################################################################
#                                                       Eigenvalue Analysis                                                  #
##############################################################################################################################
 
 
    set pi [expr 2.0*asin(1.0)];                        # Definition of pi
    set nEigenI 1;                                      # mode i = 1
    set nEigenJ 2;                                      # mode j = 2
    set nEigenK 3;                                      # mode i = 3
    set nEigenL 4;                                      # mode j = 4
    
	
	set lambdaN [eigen [expr $nEigenL]];                # eigenvalue analysis for nEigenJ modes
    foreach lambda $lambdaN {
        # lappend omegalist [expr {sqrt($lambda)}]; # Obtaining angular frequencies
        lappend Tlist [expr {2*$pi/sqrt($lambda)}]; # Obtaining modal periods
    }
    
    # Saving periods
    # Defining mode-shape recorders
    set recorderdir EigenAnalysisOutput; # Recorder folder
    file mkdir $recorderdir; # Creating recorder folder if it doesn't exist
     
	# Record eigen vectors
	for { set k 1 } { $k <= $nEigenL } { incr k } {
		recorder Node -file [format "$recorderdir/Vector%iDirection1.out" $k] -node **EIGENVECTOR_NODE** -dof 1 "eigen $k"
	}
		
    set period_file [open $recorderdir/Periods.out w];
    foreach T $Tlist {
        puts $period_file "$T";
    }
    close $period_file
    
    record
    
    puts "Eigen value analysis succeed"
