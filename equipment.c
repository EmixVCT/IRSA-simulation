#include <stdio.h>
#include <stdlib.h>

#include "headers/equipment.h"
#include "headers/antenna.h"

#include"headers/simulation.h"

#define MAX(a,b) \
  ({ __typeof__ (a) _a = (a); \
      __typeof__ (b) _b = (b); \
    _a > _b ? _a : _b; })


int checkCollision(Antenna * antenna, int spreadingFactor, int channel);
void removePacket(Antenna * antenna, int packetId);


void initEquipment(Equipment * equipment, unsigned int id)  {
    equipment->id = id;
    equipment->distance = (rand() % 6) + 7;

    equipment->spreadingFactor = 7;
    equipment->reachedLimit = false;

    equipment->timeout = NULL;
    equipment->lastPacket = NULL;
}



void sendPacket(Equipment * equipment, Antenna * antenna, Simulation * simulation) {

    //If equipment had a collision, wait for timeout to end
    if(equipment->timeout != NULL) {
        if(*(equipment->timeout) > simulation->refreshPeriod) {
            *(equipment->timeout) -= simulation->refreshPeriod;
            return;
        } else {
            //Reached end of timeout
            equipment->timeout = NULL;

            antenna->nCurrentPackets++;
            antenna->currentPackets = (Packet*) realloc(antenna->currentPackets, antenna->nCurrentPackets * sizeof(Packet));


            Packet newPacket;
            newPacket.equipmentId = equipment->lastPacket->equipmentId;
            newPacket.spreadingFactor = equipment->lastPacket->spreadingFactor;
            newPacket.channel = equipment->lastPacket->channel;
            newPacket.remainingSize = simulation->packetSize;

            antenna->currentPackets[antenna->nCurrentPackets-1] = newPacket;
            free(equipment->lastPacket);
            free(equipment->timeout);
            return;
        }
    }

    float r = rand() / (float) RAND_MAX;

    //If packet must be sent
    if(r < simulation->packetDensity / (3600000 / simulation->refreshPeriod) ) {

        int spreadingFactor;

        spreadingFactor = equipment->spreadingFactor;

        int channel = rand() % 8;


        int collision = checkCollision(antenna, spreadingFactor, channel);

        if(collision != -1) {
            //Remove conflicting packet
            for(int i=0; i<antenna->nCurrentPackets; i++) {
                if(antenna->currentPackets[i].equipmentId == equipment->id) {
                    unsigned int equipmentId = antenna->currentPackets[i].equipmentId;

                    //Get last packet, then Aloha
                    Packet lastPacket = antenna->currentPackets[i];
                    aloha(equipment, lastPacket, simulation->packetSize);

                    //Get packet to send, then Aloha
                    aloha(&(simulation->equipments[equipmentId]), lastPacket, simulation->packetSize);


                    removePacket(antenna, i);
                    break;
                }
            }



            //Update simulation stats
            simulation->nCollisions ++;

            return;
        }

        //If no collision, send packet
        antenna->nCurrentPackets++;
        antenna->currentPackets = (Packet*) realloc(antenna->currentPackets, antenna->nCurrentPackets * sizeof(Packet));

        Packet newPacket;
        newPacket.equipmentId = equipment->id;
        newPacket.spreadingFactor = spreadingFactor;
        newPacket.channel = channel;
        newPacket.remainingSize = simulation->packetSize;

        antenna->currentPackets[antenna->nCurrentPackets-1] = newPacket;

    }

}



int checkCollision(Antenna * antenna, int spreadingFactor, int channel) {
    //Returns false if no collision

    for(int i=0; i<antenna->nCurrentPackets; i++) {
        if(antenna->currentPackets[i].spreadingFactor == spreadingFactor && antenna->currentPackets[i].channel == channel) {
            return i;
        }
    }

    return -1;
}



void aloha(Equipment * equipment, Packet lastPacket, unsigned int packetSize) {
    //Set timeout
    int r = (rand() % 4) + 1;
    equipment->timeout = (unsigned int*) malloc(sizeof(unsigned int));
    *(equipment->timeout) = 200 * r;

    //Copy last packet to send it later
    equipment->lastPacket = (Packet*) malloc(sizeof(Packet));

    equipment->lastPacket->equipmentId = lastPacket.equipmentId;
    equipment->lastPacket->spreadingFactor = lastPacket.spreadingFactor;
    equipment->lastPacket->channel = lastPacket.channel;

    equipment->lastPacket->remainingSize = packetSize;
}
