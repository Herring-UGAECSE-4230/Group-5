.global _start

_start:
        @This stores 20 in R1 then subtracts 10 from that and stores the remaining amount in R0
        MOV R1, #0x14
        SUB R0, R1, #0xA
        MOV R7, #1
        SWI 0