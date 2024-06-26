# grid_simulator.py
import os
import csv
from datetime import datetime

import simpy
from pyaspg.management import ControlSystem, NetAggregator, UtilityCompany
from pyaspg.communication import SmartMeter, CommunicationNetwork
from pyaspg.prosume import Prosumer
from pyaspg.generation import PowerPlant, SolarPanel, WindTurbine
from pyaspg.distribution import Transmitter, Distributor, Substation
from pyaspg.utils import log_me
from .grid_creator import PyASPGCreator
from .data_log import DataLog

from .connection_handler import (
    GeneratorToTransmitterHandler,
    TransmitterToSubstationHandler,
    SubstationToDistributorHandler,
    DistributorToProsumerHandler,
    ProsumerToSmartMeterHandler,
    SmartMeterToAggregatorHandler,
    AggregatorToUtilityHandler,
)


@log_me
class GridSimulator:
    def __init__(self, creator: PyASPGCreator):
        self.creator = creator
        self.data_log = None        
        self.connection_handlers = {
            'generator_to_transmitter': GeneratorToTransmitterHandler(),
            'transmitter_to_substation': TransmitterToSubstationHandler(),
            'substation_to_distributor': SubstationToDistributorHandler(),
            'distributor_to_prosumer': DistributorToProsumerHandler(),
            'prosumer_to_smart_meter': ProsumerToSmartMeterHandler(),
            'smart_meter_to_aggregator': SmartMeterToAggregatorHandler(),
            'aggregator_to_utility': AggregatorToUtilityHandler()
            # Add other connection handlers here...
        }

    def run_simulation(self, duration, timestep, output_dir):
        self.data_log = DataLog(output_dir)
        env = simpy.Environment()
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        components = self.creator.components
        connections = self.creator.connections

        self._initialize_simlog(output_dir, components)
        start_time = datetime.now()

        # Create a CSV file for each component type
        self.data_log.initialize_files(components, connections)

        def log_and_handle(t):
            for connection_type, connection_list in connections.items():
                handler = self.connection_handlers.get(connection_type)
                if handler:
                    for source, target, params in connection_list:
                        # print(t // timestep, "\nHandle connection\n", source, "\n", target, "\n", params)
                        handler.handle_connection(source, target, params, t // timestep)

            self.data_log.log_data(t, components, connections)

        def run_simulation_step(env):
            while True:                
                log_and_handle(env.now)
                yield env.timeout(timestep)
        
        env.process(run_simulation_step(env))
        env.run(until=duration)
        end_time = datetime.now()

        # Close CSV files
        self.data_log.close_files()

        self._finalize_simlog(output_dir, start_time, end_time, components)

    def _initialize_simlog(self, output_dir, components):
        self.simlog_path = os.path.join(output_dir, 'simlog.txt')
        with open(self.simlog_path, 'w') as log_file:
            log_file.write("Simulation Log\n")
            log_file.write("=============================\n")
            log_file.write(f"Simulation started at: {datetime.now()}\n")
            log_file.write("-----------------------------\n")
            log_file.write("Component Counts:\n")
            for component_type, component_list in components.items():
                log_file.write(f"{component_type.capitalize()}: {len(component_list)}\n")
            log_file.write("=============================\n")

    def _finalize_simlog(self, output_dir, start_time, end_time, components):
        duration = end_time - start_time
        with open(self.simlog_path, 'a') as log_file:
            log_file.write(f"Simulation ended at: {end_time}\n")
            log_file.write(f"Total duration: {duration}\n")
            log_file.write("=============================\n")
