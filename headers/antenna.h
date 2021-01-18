#pragma once

#include "packet.h"


typedef struct {
	Packet * currentPackets;
	unsigned int nCurrentPackets;
}Antenna;


void initAntenna(Antenna * antenna);
