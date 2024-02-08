.global _start

_start:
        @ This code is a simple multiplcation of 20/10 = 2 you can see this in the debugger
        MOV R1, #0x14
        MOV R2, #0xA
        UDIV R0, R1, R2
        MOV R7, #1
        SWI 0