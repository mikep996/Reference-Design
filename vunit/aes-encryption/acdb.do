#------------------------------------------------------------------------------
#-- Subject     : summary VUNIT coverage 
#-- File name   : acdb.do
#-- Date        : 10/16/2024
#-- Developer   : Michal Pacula
#-- Copyright   : (C) 2024 ALDEC Inc. 
#------------------------------------------------------------------------------

package require fileutil
set fileList {}

proc testnameUpdt { FileName testname} {
set data "";
set dataout "";	
set line "";
if {![file exists "$FileName"]} {		
		puts "Error: Cannot find $FileName" 
	} else {
		acdb2xml -i $FileName -o $FileName.xml
		set fi [open "$FileName.xml" r];
		set data [read $fi];	
		close $fi; 
		set fi [open "$FileName.converted" w];
		foreach line [split $data "\n"] { 
			if [string match "*hnode logical_name=*" $line] {
				if [string match "*hnode logical_name=*" $line] {
					regexp {(.*)(logical_name=\")(coverage)(.*)} $line m0 m1 m2 m3 m4 m5;
					puts $fi "$m1$m2$testname$m4";
				} else {
					set firstline $line
				}
			} else {
				puts $fi $line;
			}
		};
	};
	close $fi;
	puts "Converted File:  $FileName.converted";
	xml2acdb -i $FileName.converted -o $FileName
};
# main()

foreach file [fileutil::findByPattern "./vunit_out/test_output" *.acdb] {
	regexp {(./vunit_out/test_output/lib.)(.*)(\.)(.*)(_)(.*)(/rivierapro/coverage.acdb)} $file m0 m1 m2 m3 m4 m5 m6;
	puts $file
	puts $m2
	if [string match "*.*" $m2] {
		regexp {(.*)(\.)(.*)} $m2 l0 l1 l2 l3 ;
		set testbench $l1
		set testname $l3
	} else {
		set testbench $m2
		set testname $m4
	}
	puts $testbench
	puts $testname
    lappend fileList -i $file -path "\/$testbench/enc_inst"
	#testnameUpdt $file $testname
}
#xml2acdb -dataorder id,feature,description,link,type,weight,user,goal -i testplan.xml -o acdb/plan.acdb

acdb merge -associative $fileList -o acdb/results.acdb 
acdb report -html -o acdb/results.html -i acdb/results.acdb
acdb rank -goal 25 -html -i acdb/results.acdb  -o acdb/rank.html

