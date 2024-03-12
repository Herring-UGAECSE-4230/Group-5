# Object file names
ONE = 1_loop_ex4_1.o
TWO = 2_loop_Prog4_1.o
THREE = 3_loop_Prog4_1.o
FOUR = 4_delay_ex4_3.o
FIVE = 5_div_Prog4_2.o
SIX = 6_count_ex4_15.o

# For Debugging
ifdef DEBUG
DEBUGFLGS = -g

else
DEBUGFLGS = 
endif

%.o: %.s
	as $(DEBUGFLGS) $< -o $@

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
	rm *.o one two three four five six
