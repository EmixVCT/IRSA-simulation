#pragma once

#include <stdbool.h>

#include "packet.h"


typedef struct {
	unsigned int id;
	unsigned int distance;

	unsigned int spreadingFactor;
	bool reachedLimit;

		//Used after a collision
	unsigned int * timeout; //ms
	Packet * lastPacket;

}Equipment;


void initEquipment(Equipment * equipment, unsigned int id);
void aloha(Equipment * equipment, Packet lastPacket, unsigned int packetSize);
