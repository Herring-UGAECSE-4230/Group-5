# Object file names
ONE = 1_flags_ex5_13.o
TWO = 2_flagsfixed_ex5_13.o
THREE = 3_Loopadd_prog5_1.o
FOUR = 4_lowest_prog5_2.o
FIVE = 5_match_ex5_16.o

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


# Deletes all current object files
clean:
	rm *.o one two three four five
