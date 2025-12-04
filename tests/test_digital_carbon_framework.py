import unittest

from carbon import digital_carbon_framework
from carbon.compute_footprints import Co2Cost, impressions_cost

DEVICES_REPARTITION = digital_carbon_framework.Distribution(
    weights={
        "desktop": 10,
        "smart_phone": 20,
        "tablet": 5,
        "connected_tv": 20,
    }
)


class DigitalCarbonTest(unittest.TestCase):
    def test_co2_full_direct(self):
        campaign = digital_carbon_framework.Framework.load()
        self.assertAlmostEqual(
            impressions_cost(
                campaign,
                nb_impressions=10000,
                creative_type="video",
                allocation="direct",
                creative_size_ko=1200,
                devices_repartition=DEVICES_REPARTITION,
                creative_avg_view_s=5,
            ).overall.total,
            Co2Cost(use=0.2562733391548535, manufacturing=0.5793029714657473).total,
        )

    def test_co2_full_programmatic(self):
        campaign = digital_carbon_framework.Framework.load()
        self.assertAlmostEqual(
            impressions_cost(
                campaign,
                nb_impressions=10000,
                creative_type="display",
                allocation="programmatic",
                creative_size_ko=1200,
                devices_repartition=DEVICES_REPARTITION,
                creative_avg_view_s=5,
            ).overall.total,
            Co2Cost(use=7.323631186960354, manufacturing=3.2045569703363834).total,
        )

    def test_change_target_country(self):
        campaign = digital_carbon_framework.Framework.load()
        campaign.change_target_country(alpha_code="DEU")
        self.assertAlmostEqual(
            impressions_cost(
                campaign,
                nb_impressions=10000,
                creative_type="display",
                allocation="programmatic",
                creative_size_ko=1200,
                devices_repartition=DEVICES_REPARTITION,
                creative_avg_view_s=5,
            ).overall.total,
            Co2Cost(use=7.83829675080798, manufacturing=3.2045569703363834).total,
        )

    def test_cant_construct_distrib_with_null_weights(self):
        with self.assertRaises(ValueError):
            digital_carbon_framework.Distribution(weights={"desktop": 0})

    def test_cant_construct_distrib_with_negative_weights(self):
        with self.assertRaises(ValueError):
            digital_carbon_framework.Distribution(weights={"desktop": -1})

    def test_compute_distrib_terminal(self):
        all_devices = digital_carbon_framework.Distribution(weights={'smart_phone': 1.0, 'tablet': 0.0, 'desktop': 0.0, 'connected_tv':1})
        carbon_all_devices = impressions_cost( digital_carbon_framework.Framework.load(),
                    creative_type='video', nb_impressions=1000,
                    allocation='direct', creative_size_ko=5000,
                    devices_repartition=all_devices, creative_avg_view_s=3)
        
        limited_devices = digital_carbon_framework.Distribution(weights={'smart_phone': 1.0, 'connected_tv':1})
        carbon_limited_devices = impressions_cost( digital_carbon_framework.Framework.load(),
                    creative_type='video', nb_impressions=1000,
                    allocation='direct', creative_size_ko=5000,
                    devices_repartition=limited_devices, creative_avg_view_s=3)
        self.assertEqual(carbon_all_devices.kgco2_distrib_terminal.total
                            , carbon_limited_devices.kgco2_distrib_terminal.total) 
