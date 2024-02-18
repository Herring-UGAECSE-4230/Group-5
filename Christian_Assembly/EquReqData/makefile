# Object file names
ZERO = 0_AddressMap.o
ONE = 1_AddInclude.o
TWO = 2_req_p2_2.o
THREE = 3_Indirectp2_3a.o
FOUR = 4_subs_ex2_6.o
FIVE = 5_str_p2_3b.o
SIX = 6_strb_ex2_3.o

# For Debugging
ifdef DEBUG
DEBUGFLGS = -g

else
DEBUGFLGS = 
endif

%.o: %.s
	as $(DEBUGFLGS) $< -o $@

zero: $(ZERO)
	ld -o zero $(ZERO)

one: $(ONE)
	ld -o one $(ONE)

two: $(TWO)
	ld -o two $(TWO)

three: $(THREE)
	ld -o three $(THREE)

four: $(FOUR)
	ld -o four $(FOUR)

five: $(FIVE)
	ld -o five $(FIVE)

six: $(SIX)
	ld -o six $(SIX)

# Deletes all current object files
clean:
	rm *.o zero one two three four five six
