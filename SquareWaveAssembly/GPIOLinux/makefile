OBJS = Linux.o
ifdef DEBUG
DEBUGFLGS = -g
else
DEBUGFLGS =
endif

%.o : %.s
	as $(DEBUGFLGS) $< -o $@
GPIO_ON: $(OBJS)
	gcc -o Linux $(OBJS)

clean:
	rm *.o Linux
