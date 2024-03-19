@ Deliverable 1: Describe the function of the program.
@ Deliverable 2: Why is "bl fill" the first instruction executed?
@ Deliverable 3: Describe the function of the .space 40 directive.
@ Deliverable 4: Why is #4 added to the registers in the program?



	.data	
a: .space 40
b: .space 40

	.text
	@ ----------------block fill subroutine
fill:	ldr  	r1, =a	@ r1 = ram address pointer
	mov	r0, #10	 	@ counter
	ldr	r2, =0x55555555
l1:	str	r2, [r1]	@ send it to ram
	add	r1, r1, #4	@ r1 = r1 + 4 to increment pointer
	subs	r0, r0, #1	@ r0 = r0 - 1 to decrement counter 

	bne	l1		@ keep doing it until r0 is 0
	bx	lr		@ return to caller

	@ -----------------block copy subroutine
copy:	ldr	r1, =a		@ r1 = ram address pointer (source)
	ldr	r2, =b		@ r2 = ram address pointer (destination)
	mov	r0, #10		@ counter
l2:	ldr	r3, [r1]	@ get from ram1
	str	r3, [r2]	@ send it to ram2
	add	r1, r1, #4	@ r1 = r1 + 4 to increment pointer for ram1
	add	r2, r2, #4	@ r2 = r2 + 4 to increment pointer for ram2
	subs	r0, r0, #1	@ r0 = r0 – 1 for decrementing counter 
	bne	l2		@ keep doing it
	bx	lr		@ return to caller
	
	@ ----------	
	.global _start
_start:
	bl	fill		@ call block fill subroutine
	bl	copy		@ call block transfer subroutine

	mov 	r7, #1
	svc 	0
