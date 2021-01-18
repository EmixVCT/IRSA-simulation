FILES = simulation.o antenna.o equipment.o
FLAGS = -Wall -Werror -g

all: build clean


build: $(FILES)
	gcc main.c $(FILES) $(FLAGS)



simulation.o: headers/simulation.h
	gcc -c simulation.c $(FLAGS)

antenna.o: headers/antenna.h
	gcc -c antenna.c $(FLAGS)

equipment.o: headers/equipment.h
	gcc -c equipment.c $(FLAGS)



clean:
	rm *.o
