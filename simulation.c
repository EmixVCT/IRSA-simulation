#include <stdio.h>
#include <stdlib.h>

#include "headers/simulation.h"
#include "headers/equipment.h"


void sendPacket(Equipment * equipment, Antenna * antenna, Simulation * simulation);
void answer(Antenna * antenna, Equipment ** equipments, Simulation * simulation);


void initialize(Simulation * simulation){

    //Initialize settings
    simulation->length = 3600000;
    simulation->refreshPeriod = 100;
    simulation->currentTime = 0;

    simulation->nEquipments = 10;
    simulation->transferSpeed = 25;
    simulation->packetSize = 1000;
    simulation->packetDensity = 15;

    simulation->nSuccessfullPackets = 0;
    simulation->nFailedPackets = 0;
    simulation->nCollisions = 0;


    //Initialize antenna
    initAntenna(&(simulation->antenna));


    //Initialize equipments
    simulation->equipments = (Equipment*) malloc(simulation->nEquipments * sizeof(Equipment));
    for(int i=0; i<simulation->nEquipments; i++) {
        initEquipment(&(simulation->equipments[i]), (unsigned int) i);
    }
}


void run(Simulation * simulation) {
    while(simulation->currentTime < simulation->length) {

        //1) Check for new packets
        for(int i=0; i<simulation->nEquipments; i++) {
            sendPacket(&(simulation->equipments[i]), &(simulation->antenna), simulation);
        }

        //2) Answer to current packets
        answer(&(simulation->antenna), &(simulation->equipments), simulation);


        simulation->currentTime += simulation->refreshPeriod;
    }

}


void printResults(Simulation * simulation) {
    printf("nSuccessfullPackets = %d\n", simulation->nSuccessfullPackets);
    printf("nFailedPackets = %d\n", simulation->nFailedPackets);
    printf("nCollisions = %d\n", simulation->nCollisions);
}
