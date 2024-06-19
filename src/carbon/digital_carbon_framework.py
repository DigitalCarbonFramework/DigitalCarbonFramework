"""
This is the python implementation of the DigitalCarbonFramework referential to compute the carbon emissions of an advertising campaign.
"""

import os
from typing import Literal

import yaml
from pydantic.dataclasses import dataclass

from carbon import logger
from carbon.compute_footprints import Co2Cost, Distribution


@dataclass
class Device:
    """Represents a target device used in programmatic advertising."""

    name: str
    """Name of the device"""
    average_power_watt: float
    """Average device power in active mode (in watts)"""
    average_lifetime_years: float
    """Average lifetime lifespan (in hours)"""
    average_daily_use_hours_per_day: float
    """Duration of daily device use (in hours)"""
    manufacturing_cost_kgco2: float
    """Average impact of the device, including manufacturing, transport and end of life on its lifespan (excluding use)"""


@dataclass
class Framework:
    """Class representating all the component of the programmatic advertising chain."""

    @dataclass
    class AllocationNetworkUse:
        """Parameters related to the utilization of the network for the Allocation part."""

        nb_requests_per_active_path: int
        """Number of requests per active path"""
        mean_https_request_k0: int
        """Average weight of an HTTP request in kilo bytes"""
        uncertainty_margin: float
        """Uncertainty margin"""
        fixed_network_use: float
        """Average share of fixed network usage in programmatic"""
        energy_efficiency_fixed_network_in_use_kWh_per_kO: float
        """Average energy efficiency of the fixed network in the use phase (kWh/ko)"""
        network_trafic_in_datacenter_country_share: float
        """Share of network traffic in the country of the data center in programmatic"""
        emission_factor_server: float
        """Emission factor for the electricity consumed by the servers (to be adapted depending on the location of the servers) (kgCO2e/kWh)"""

    @dataclass
    class AllocationNetworkManufacturing:
        """Parameters related to the fabrication, utilization and life cycle of the network for the Allocation part."""

        nb_requests_per_active_path: int
        """Number of requests per active path"""
        mean_https_request_k0: int
        """Average weight of an HTTP request in kilo bytes"""
        uncertainty_margin: float
        """Uncertainty margin"""
        fixed_network_use: float
        impact_1ko_transport_on_fixed_network_kgCo2_per_kO: float
        """Impact of transporting 1 KB of data via fixed network including manufacturing, transport and end of life (excluding use) (kgCO2e/ko)"""

    @dataclass
    class AllocationServersUse:
        """Parameters related to the utilization of the servers for the Allocation part."""

        nb_server_requests_per_active_path: int
        """Number of servers requested per active path"""
        server_time_calculation_during_auction_s: float
        """Server calculation time during an auction (hour)"""
        vm_mean_power_in_kW: float
        """Average power of a virtual server (Watt)"""
        pue: float
        """Average PUE of a data center"""
        server_consumption: float
        """Modeling of server consumption linked to uses excluding auctions and distribution (reporting, machine learning, back-end, etc.)"""
        server_share_local: float
        """Share of servers in France"""
        server_share_worldwide: float
        """Share of international servers"""
        emission_factor_country: float
        """Electricity emission factor in target country"""
        emission_factor_worldwide: float
        """International electricity emission factor for IT uses"""

    @dataclass
    class AllocationServersManufacturing:
        """Parameters related to the to the fabrication, utilization and life cycle  of the servers for the Allocation part."""

        nb_server_requests_per_active_path: int
        """Number of servers requested per active path"""
        annual_manufacturing_cost_kgco2: float
        """Server calculation time during an auction (hour)"""
        nb_vm_servers_per_physic_server: int
        """Annual carbon impact - manufacturing and end of life of an average physical server (kgCO2e)"""
        server_time_calculation_during_auction_s: float
        """Number of virtual servers (VMs) per physical server"""
        server_consumption: float
        """Modeling of server consumption linked to uses excluding auctions and distribution (reporting, machine learning, back-end, etc.)"""

    @dataclass
    class AllocationAndServers:
        """Parameters related to the to the fabrication, utilization and life cycle of both network &  servers for the Allocation part."""

        nb_paths_display: int
        """Programmatic - Display - number of potential active paths"""
        nb_paths_video: int
        """Programmatic - Instream video & other modes - number of potential active paths"""
        publisher_activated_paths_share: float
        """Share of potential paths activated at each print (publishers)"""
        ssp_activated_paths_share: float
        """Share of potential paths activated at each print (ssp)"""

    @dataclass
    class DistributionServerUse:
        """Parameters related to the utilization of the server for the distribution part."""

        pue_mean: float
        """Average PUE of a data center"""
        energy_efficiency_server_target_country: float
        """Average energy efficiency of a server the target country (kWh/ko)"""
        energy_efficiency_server_worldwide: float
        """Average energy efficiency of a server worldwide (kWh/ko)"""
        server_share_local: float
        """Share of servers in the target country"""
        server_share_worldwide: float
        """Share of servers worlwide"""
        emission_factor_worldwide: float
        """Electricity emission factor worlwide (kgCO2e/kWh)"""
        emission_factor_target_country: float
        """Electricity emission factor in the target country (kgCO2e/kWh)"""

    @dataclass
    class DistributionServerManufacturing:
        """Parameters related to the fabrication, utilization and life cycle of the server for the distribution part"""

        annual_manufacturing_cost_kgco2: float
        """Average impact of a server reduced to one year of use, including manufacturing, transport and end of life (excluding use) (kgCo2)"""
        bandwidth_server_ko_per_s: float
        """Server bandwidth (Ko/s)"""

    @dataclass
    class DistributionNetworkUse:
        """Parameters related to the utilization of the network for the distribution part."""

        fixed_network_usage_share: float
        """Average share of fixed network usage (wifi)"""
        fixed_mobile_usage_share: float
        """Average share of mobile usage (4G)"""
        server_share_local: float
        """Share of network traffic in the country of content viewing"""
        server_share_datacenter: float
        """Share of network traffic in the datacenter country"""
        energy_efficiency_fixed_network_in_use_kWh_per_kO: float
        """Average energy efficiency of the fixed network in the use phase (kWh/ko)"""
        energy_efficiency_mobile_in_use_kWh_per_kO: float
        """Average energy efficiency of the mobile network in the use phase (kWh/ko)"""
        emission_factor_target_country: float
        """Emission factor of the electricity consumed by the audience (kgCO2e/kWh)"""
        emission_factor_worldwide: float
        """Emission factor of the electricity consumed worldwide  (kgCO2e/kWh)"""

    @dataclass
    class DistributionNetworkManufacturing:
        """Parameters related to the fabrication, utilization and life cycle of the network for the distribution part."""

        fixed_network_usage_share: float
        """Average share of fixed network usage (wifi)"""
        fixed_mobile_usage_share: float
        """Average share of mobile usage (4G)"""
        transport_cost_on_fixed_network_kgCo2_per_kO: float
        """Impact of transporting 1 KB of data via fixed network including manufacturing, transport and end of life (excluding use) (kgCO2e/ko)"""
        transport_cost_on_mobile_kgCo2_per_kO: float
        """Impact of transporting 1 KB of data via mobile network including manufacturing, transport and end of life (excluding use) (kgCO2e/ko)"""

    @dataclass
    class DistributionTerminalUse:
        """Parameters related to the utilization of the terminals for the distribution part."""

        smartphone_usage: Literal["app", "browser"]
        """either 'app' or 'browser'"""
        smart_phone_average_power_watt_app: float
        """Average smartphone power in active mode, for app usage"""
        smart_phone_average_power_watt_browser: float
        """Average smartphone power in active mode, for browser usage"""
        tv_average_power_watt: float
        """Average tv power in active mode"""
        desktop_average_power_watt: float
        """Average computer power in active mode"""
        tablet_average_power_watt: float
        """Average tablet power in active mode"""
        emission_factor_target_country: float
        """Emission factor of the electricity consumed by the audience"""

    @dataclass
    class DistributionTerminalManufacturing:
        """Parameters related to the fabrication, utilization and life cycle of the terminals for the distribution part."""

        desktop_average_lifetime_years: float
        """Average desktop lifespan"""
        desktop_average_daily_use_hours_per_day: float
        """Duration of daily use of a desktop"""
        desktop_manufacturing_cost_kgco2: float
        """Average impact of a desktop, including manufacturing, transport and end of life on its lifespan (excluding use)"""

        tv_average_lifetime_years: float
        """Average connected tv lifespan"""
        tv_average_daily_use_hours_per_day: float
        """Duration of daily use of a connected tv"""
        tv_manufacturing_cost_kgco2: float
        """Average impact of a connected tv, including manufacturing, transport and end of life on its lifespan (excluding use)"""

        tablet_average_lifetime_years: float
        """Average tablet lifespan"""
        tablet_average_daily_use_hours_per_day: float
        """Duration of daily use of a tablet"""
        tablet_manufacturing_cost_kgco2: float
        """Average impact of a tablet, including manufacturing, transport and end of life on its lifespan (excluding use)"""

        smart_phone_average_lifetime_years: float
        """Average smart phone lifespan"""
        smart_phone_average_daily_use_hours_per_day: float
        """Duration of daily use of a smart phone"""
        smart_phone_manufacturing_cost_kgco2: float
        """Average impact of a smart phone, including manufacturing, transport and end of life on its lifespan (excluding use)"""

    @dataclass
    class Server:
        share: float
        emission_factor: float
        energy_efficiency_kwh_per_ko: float = 0.0

    def multiply_attributes(self, Co2Cost_: Co2Cost, factor: float) -> Co2Cost:
        return Co2Cost(
            use=Co2Cost_.use * factor, manufacturing=Co2Cost_.manufacturing * factor
        )

    allocation_network_use: AllocationNetworkUse
    allocation_network_manufacturing: AllocationNetworkManufacturing
    allocation_servers_use: AllocationServersUse
    allocation_servers_manufacturing: AllocationServersManufacturing
    allocation_network_servers: AllocationAndServers

    distribution_server_use: DistributionServerUse
    distribution_server_manufacturing: DistributionServerManufacturing
    distribution_network_use: DistributionNetworkUse
    distribution_network_manufacturing: DistributionNetworkManufacturing
    distribution_terminal_use: DistributionTerminalUse
    distribution_terminal_manufacturing: DistributionTerminalManufacturing

    _emission_factors_dict_iso2 = None
    _emission_factors_dict_iso3 = None

    @classmethod
    def load(cls, config_file: str | None = None):
        logger.info("Starting instanciation of Framework object")
        if config_file is None:
            logger.debug("Loading default config")
            config_file = os.path.join(
                os.path.dirname(__file__), "digital_carbon_framework.yml"
            )

        with open(config_file, "r") as file:
            config_data = yaml.safe_load(file)

        instance = cls(**config_data)
        logger.debug("config file properly loaded")
        logger.info("Framework object generated")
        return instance

    @property
    def hours_in_years(self) -> int:
        return 8766

    @property
    def second_in_years(self) -> float:
        return 24 * 365.25 * 3600

    @property
    def from_kilo(self) -> float:
        return 1 / 1000

    @property
    def seconds_to_hour(self) -> float:
        return 1 / 3600

    @property
    def smart_phone(self) -> Device:
        power = (
            self.distribution_terminal_use.smart_phone_average_power_watt_app
            if self.distribution_terminal_use.smartphone_usage == "app"
            else self.distribution_terminal_use.smart_phone_average_power_watt_browser
        )
        return Device(
            name="smart_phone",
            average_power_watt=power,
            average_lifetime_years=self.distribution_terminal_manufacturing.smart_phone_average_lifetime_years,
            average_daily_use_hours_per_day=self.distribution_terminal_manufacturing.smart_phone_average_daily_use_hours_per_day,
            manufacturing_cost_kgco2=self.distribution_terminal_manufacturing.smart_phone_manufacturing_cost_kgco2,
        )

    @property
    def tv(self) -> Device:
        return Device(
            name="connected_tv",
            average_power_watt=self.distribution_terminal_use.tv_average_power_watt,
            average_lifetime_years=self.distribution_terminal_manufacturing.tv_average_lifetime_years,
            average_daily_use_hours_per_day=self.distribution_terminal_manufacturing.tv_average_daily_use_hours_per_day,
            manufacturing_cost_kgco2=self.distribution_terminal_manufacturing.tv_manufacturing_cost_kgco2,
        )

    @property
    def desktop(self) -> Device:
        return Device(
            name="desktop",
            average_power_watt=self.distribution_terminal_use.desktop_average_power_watt,
            average_lifetime_years=self.distribution_terminal_manufacturing.desktop_average_lifetime_years,
            average_daily_use_hours_per_day=self.distribution_terminal_manufacturing.desktop_average_daily_use_hours_per_day,
            manufacturing_cost_kgco2=self.distribution_terminal_manufacturing.desktop_manufacturing_cost_kgco2,
        )

    @property
    def tablet(self) -> Device:
        return Device(
            name="tablet",
            average_power_watt=self.distribution_terminal_use.tablet_average_power_watt,
            average_lifetime_years=self.distribution_terminal_manufacturing.tablet_average_lifetime_years,
            average_daily_use_hours_per_day=self.distribution_terminal_manufacturing.tablet_average_daily_use_hours_per_day,
            manufacturing_cost_kgco2=self.distribution_terminal_manufacturing.tablet_manufacturing_cost_kgco2,
        )

    @property
    def emission_factors_dict_iso2(self) -> dict:
        if self._emission_factors_dict_iso2 is None:
            with open(
                os.path.join(os.path.dirname(__file__), "iso2.yml"), "r"
            ) as yaml_file:
                self._emission_factors_dict_iso2 = yaml.safe_load(yaml_file)
        else:
            self._emission_factors_dict_iso2 = self._emission_factors_dict_iso2
        return self._emission_factors_dict_iso2

    @property
    def emission_factors_dict_iso3(self) -> dict:
        if self._emission_factors_dict_iso3 is None:
            with open(
                os.path.join(os.path.dirname(__file__), "iso3.yml"), "r"
            ) as yaml_file:
                self._emission_factors_dict_iso3 = yaml.safe_load(yaml_file)
        else:
            self._emission_factors_dict_iso3 = self._emission_factors_dict_iso3
        return self._emission_factors_dict_iso3

    def change_target_country(self, alpha_code: str):
        """
        Set the emission factors of the specified country

        :param alpha_code:  alpha_code of the specified country. Support iso2 & iso3 countries (ex: country: 'France', alpha_code='FR' or alpha_code='FRA' supported)
        :type alpha_code: str

        """
        logger.info(f"Changing Target country to {alpha_code}")

        if len(alpha_code) == 3:
            emission_factors_dict = self.emission_factors_dict_iso3
        elif len(alpha_code) == 2:
            emission_factors_dict = self.emission_factors_dict_iso2
        else:
            raise ValueError(f"Alpha code {alpha_code} not iso2 or iso3 compliant")

        try:
            new_emission_factor = emission_factors_dict[alpha_code]
            self.distribution_server_use.emission_factor_target_country = (
                new_emission_factor
            )
            self.distribution_network_use.emission_factor_target_country = (
                new_emission_factor
            )
            self.distribution_terminal_use.emission_factor_target_country = (
                new_emission_factor
            )
            self.allocation_servers_use.emission_factor_country = new_emission_factor
            logger.info(f"Emission factors changed to {new_emission_factor} ")
        except KeyError:
            logger.error(f"Alpha code {alpha_code} not in database")
            logger.info(f"Emission factors not changed: {alpha_code} not referenced")
            raise

    @property
    def allocation_factor(self) -> float:
        return (
            self.allocation_network_servers.publisher_activated_paths_share
            * self.allocation_network_servers.ssp_activated_paths_share
        )

    @property
    def alloc_servers(self) -> list[Server]:
        """
        :return: a list of two Server classes, associated to the allocation server usage.
        :rtype: list[Server]
        """
        server2 = self.Server(
            share=self.allocation_servers_use.server_share_worldwide,
            emission_factor=self.allocation_servers_use.emission_factor_worldwide,
        )

        server1 = self.Server(
            share=self.allocation_servers_use.server_share_local,
            emission_factor=self.allocation_servers_use.emission_factor_country,
        )
        return [server1, server2]

    @property
    def distrib_servers(self) -> list[Server]:
        """
        :return: a list of two Server classes, associated to the distribution server usage.
        :rtype: list[Server]
        """
        server2 = self.Server(
            share=self.distribution_server_use.server_share_worldwide,
            emission_factor=self.distribution_server_use.emission_factor_worldwide,
            energy_efficiency_kwh_per_ko=self.distribution_server_use.energy_efficiency_server_worldwide,
        )

        server1 = self.Server(
            share=self.distribution_server_use.server_share_local,
            emission_factor=self.distribution_server_use.emission_factor_target_country,
            energy_efficiency_kwh_per_ko=self.distribution_server_use.energy_efficiency_server_target_country,
        )
        return [server1, server2]

    @property
    def kgco2_allocation_server(self) -> Co2Cost:
        return Co2Cost(
            use=(
                self.allocation_servers_use.nb_server_requests_per_active_path
                * self.allocation_servers_use.pue
                * (1 + self.allocation_servers_use.server_consumption)
                * self.allocation_servers_use.server_time_calculation_during_auction_s
                * self.allocation_servers_use.vm_mean_power_in_kW
                * sum(
                    [
                        servers.share * servers.emission_factor
                        for servers in self.alloc_servers
                    ]
                )
            ),
            manufacturing=(
                self.allocation_servers_manufacturing.nb_server_requests_per_active_path
                * self.allocation_servers_manufacturing.annual_manufacturing_cost_kgco2
                / self.allocation_servers_manufacturing.nb_vm_servers_per_physic_server
                * (1 + self.allocation_servers_manufacturing.server_consumption)
                * self.allocation_servers_manufacturing.server_time_calculation_during_auction_s
                / self.hours_in_years
            ),
        )

    @property
    def kgco2_allocation_network(self) -> Co2Cost:
        return Co2Cost(
            use=(
                self.allocation_network_use.nb_requests_per_active_path
                * self.allocation_network_use.mean_https_request_k0
                * (1 + self.allocation_network_use.uncertainty_margin)
                * self.allocation_network_use.fixed_network_use
                * self.allocation_network_use.energy_efficiency_fixed_network_in_use_kWh_per_kO
                * self.allocation_network_use.network_trafic_in_datacenter_country_share
                * self.allocation_network_use.emission_factor_server
            ),
            manufacturing=(
                self.allocation_network_manufacturing.nb_requests_per_active_path
                * self.allocation_network_manufacturing.mean_https_request_k0
                * (1 + self.allocation_network_manufacturing.uncertainty_margin)
                * self.allocation_network_manufacturing.fixed_network_use
                * self.allocation_network_manufacturing.impact_1ko_transport_on_fixed_network_kgCo2_per_kO
            ),
        )

    @property
    def kgco2_distrib_server(self) -> Co2Cost:
        return Co2Cost(
            use=self.distribution_server_use.pue_mean
            * sum(
                [
                    servers.share
                    * servers.emission_factor
                    * servers.energy_efficiency_kwh_per_ko
                    for servers in self.distrib_servers
                ]
            ),
            manufacturing=self.distribution_server_manufacturing.annual_manufacturing_cost_kgco2
            / self.distribution_server_manufacturing.bandwidth_server_ko_per_s
            / self.second_in_years,
        )

    @property
    def kgco2_distrib_network(self) -> Co2Cost:
        return Co2Cost(
            use=(
                self.distribution_network_use.fixed_mobile_usage_share
                * self.distribution_network_use.energy_efficiency_mobile_in_use_kWh_per_kO
                + self.distribution_network_use.fixed_network_usage_share
                * self.distribution_network_use.energy_efficiency_fixed_network_in_use_kWh_per_kO
            )
            * (
                self.distribution_network_use.server_share_local
                * self.distribution_network_use.emission_factor_target_country
                + self.distribution_network_use.server_share_datacenter
                * self.distribution_network_use.emission_factor_worldwide
            ),
            manufacturing=(
                self.distribution_network_manufacturing.fixed_network_usage_share
                * self.distribution_network_manufacturing.transport_cost_on_fixed_network_kgCo2_per_kO
                + self.distribution_network_manufacturing.fixed_mobile_usage_share
                * self.distribution_network_manufacturing.transport_cost_on_mobile_kgCo2_per_kO
            ),
        )

    def kgco2_distrib_terminal(self, devices_repartition: Distribution) -> Co2Cost:
        Co2Cost_terminals = Co2Cost()
        for device in [self.tv, self.desktop, self.tablet, self.smart_phone]:
            kgco2_per_device = self.kgco2_device(device)
            Co2Cost_terminals.use += (
                kgco2_per_device.use * devices_repartition.get_ratio(device.name, -1)
            )
            Co2Cost_terminals.manufacturing += (
                kgco2_per_device.manufacturing
                * devices_repartition.get_ratio(device.name, -1)
            )
        return Co2Cost_terminals

    def kgco2_device(self, specified_device) -> Co2Cost:
        return Co2Cost(
            use=(
                specified_device.average_power_watt
                * self.from_kilo
                * self.distribution_terminal_use.emission_factor_target_country
                * self.seconds_to_hour
            ),
            manufacturing=(
                specified_device.manufacturing_cost_kgco2
                * self.seconds_to_hour
                / (
                    specified_device.average_daily_use_hours_per_day
                    * specified_device.average_lifetime_years
                    * 365
                )
            ),
        )
