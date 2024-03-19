@ Deliverable 1: Describe what the function of this program?  And, does it end?
@ Deliverable 2: Describe the function of the BL and the BX instructions
@ Deliverable 3: Change the BX instruction to a MOV instruction to peform the same function
@ Deliverable 4: Add appropriate assembly language so that the "again" line is executed 5 times.  Show the complete program with your changes.


	.text
	.global _start	
_start:
	ldr r4, =5 @loads register 4 with decimal 5
again:	mov	r2, #0x55	@ r2 = 0x55
	bl	delay  	@ call delay (r14 = pc of next instruction)
	mov	r2, #0xaa	@ r2 = 0xaa
	bl	delay  	@ call delay
	sub r4, r4, #1 @subtracts 1 from register 4 and loads the remainer
	bne again @branches to again if register 4 is not 0, looping 5 times in total

	mov r7, #1
	svc	0

	@ --------------------delay subroutine
delay:	ldr	r3, =5		@ r3 =5, modify this value for different delay 
l1:	subs	r3, r3, #1	@ r3 = r3 - 1 
	bne	l1
	mov	pc, lr		@ moves the link register to Program Counter, achieving the same effect as bx lr
	@ --------------------end of delay subroutine
