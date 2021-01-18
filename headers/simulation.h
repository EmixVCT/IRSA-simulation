#pragma once

#include "antenna.h"
#include "equipment.h"


//Structure containing simulation parameters & current state

typedef struct {
	unsigned int length;	//ms
	unsigned int refreshPeriod;	//ms
	unsigned int currentTime;

	unsigned int nEquipments;
	float transferSpeed;	//byte/s
	unsigned int packetSize;	//byte
	float packetDensity;	//packets/h

	unsigned int nSuccessfullPackets;
	unsigned int nFailedPackets;
	unsigned int nCollisions;

	Antenna antenna;
	Equipment * equipments;
}Simulation;


void initialize(Simulation * simulation);
void run(Simulation * simulation);
void reset(Simulation * simulation);
void printResults(Simulation * simulation);
