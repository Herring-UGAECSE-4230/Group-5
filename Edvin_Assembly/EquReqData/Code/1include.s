@look at the unistd.s file.  This introduces the .EQU directive which assigns values to variable.
@Deliverable 1: Compile and run the program
@Deliverable 2: Change the last two lines to use meaningful variable names from the classinclude.s file.  Rerun your program.  
@Deliverable 3: What does the .include mean/do in the program?

.include "classinclude.s"

.global _start

_start:
        @This stores 20 in R1 then subtracts 10 from that and stores the remaining amount in R0
        MOV R1, #0x14
        .EQU sys_open, test
        .EQU sys_link, test
        SWI 0
