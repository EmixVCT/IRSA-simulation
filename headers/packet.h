#pragma once

typedef struct {
	unsigned int equipmentId;
	unsigned int spreadingFactor;
	unsigned int channel;

	float remainingSize; //bytes
}Packet;
