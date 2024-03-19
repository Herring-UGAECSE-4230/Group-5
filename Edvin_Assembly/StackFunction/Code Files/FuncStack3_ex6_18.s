@ Deliverable 1: Describe how the str instructions work in myFunc.
@ Deliverable 2: Describe how the ldr instructions work in myFunc.
@ Deliverable 3: What are the values of R0, R1, and R2 after the program runs?
@ Deliverable 4: Replace the str and ldr instructions in myFunc with the appropriate (least number) push and pop instructions.  Show your code.

	.text
	.global _start 
_start:
	ldr	r0, =0x125		@ r0 = 0x125
	ldr	r1, =0x144		@ r1 = 0x144
	mov	r2, #0x56		@ r2 = 0x56
	bl	myFunc		@ call a subroutine
	add	r3, r0, r1		@ r3 = r0 + r1 = 0x125 + 0x144 = 0x269
	add	r3, r3, r2		@ r3 = r3 + r2 = 0x269 + 0x56 = 0x2bf
	mov	r7, #1
	svc	0

myFunc:
	@ save r0, r1, and r2 on stack before they are used
	push {r0, r1, r2} @saves registers on a stack
    
	@ -------- modify r0, r1, and r2
	mov	r0, #0	@ r0 = 0
	mov	r1, #0	@ r1 = 0
	mov	r2, #0	@ r2 = 0
	@ --------
    
	@ restore the original registers contents from stack
	pop {r0, r1, r2} @restores registers from stack

	bx	lr			@ return to caller
