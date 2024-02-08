.global _start

_start:
        @ This code is a simple multiplcation of 10 x 20 = 200 you can see this in the debugger
        MOV R1, #0x14
        MOV R2, #0xA
        MUL R0, R1, R2
        MOV R7, #1
        SWI 0