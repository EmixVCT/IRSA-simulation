#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

#include "headers/antenna.h"
#include "headers/equipment.h"
#include "headers/simulation.h"


void removePacket(Antenna * antenna, int packetId);
void sendAck(Equipment * equipment, bool value);


void initAntenna(Antenna * antenna) {
    antenna->currentPackets = NULL;
    antenna->nCurrentPackets = 0;
}



void answer(Antenna * antenna, Equipment ** equipments, Simulation * simulation) {
    //Cycle all current packets
    for(int i=0; i<antenna->nCurrentPackets; i++) {
        //If packet transfer is over
        if(antenna->currentPackets[i].remainingSize < simulation->transferSpeed/1000.0 * (float)simulation->refreshPeriod ) {
            //Remove packet form array and send ack
            int equipmentId = antenna->currentPackets[i].equipmentId;

            bool ack = (simulation->equipments[equipmentId].distance >= simulation->equipments[equipmentId].spreadingFactor) ? true : false;

            removePacket(antenna, i);
            i--;

            sendAck(&(simulation->equipments[equipmentId]), ack);

            //Update simulation stats
            if(ack)
                simulation->nSuccessfullPackets++;
            else
                simulation->nFailedPackets++;

        } else {
            antenna->currentPackets[i].remainingSize -= simulation->transferSpeed/1000.0 * (float)simulation->refreshPeriod;
        }
    }
}



void removePacket(Antenna * antenna, int packetId) {
    //Removes the element at rank packetId from current packets array

    Packet* temp = malloc((antenna->nCurrentPackets - 1) * sizeof(Packet));

    if (packetId != 0)
        memcpy(temp, antenna->currentPackets, packetId * sizeof(Packet)); //Copy everything before index

    if (packetId != (antenna->nCurrentPackets - 1))
        memcpy(temp+packetId, antenna->currentPackets+packetId+1, (antenna->nCurrentPackets - packetId - 1) * sizeof(Packet));  //Copy everything after index

    free(antenna->currentPackets);
    antenna->currentPackets = temp;
    antenna->nCurrentPackets--;
}



void sendAck(Equipment * equipment, bool value) {

    //Equipment can increase current spreading factor
    if(value && !equipment->reachedLimit) {
        equipment->spreadingFactor++;
    }
    //Max spreading factor reached
    else if(!equipment->reachedLimit) {
        equipment->reachedLimit = true;
        equipment->spreadingFactor--;
    }
}
