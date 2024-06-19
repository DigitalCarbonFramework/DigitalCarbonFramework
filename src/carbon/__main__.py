from carbon import computation_logger, compute_footprints, logger
from carbon.compute_footprints import Co2Cost
from carbon.digital_carbon_framework import Framework
from carbon.utils import Distribution

if __name__ == "__main__":
    logger.setLevel("INFO")
    computation_logger.setLevel("INFO")

    DEVICES_REPARTITION = {
        "desktop": 60.0,
        "smart_phone": 20.0,
        "tablet": 0.0,
        "connected_tv": 20.0,
    }

    DEVICES = Distribution(weights=DEVICES_REPARTITION)
    campaign = Framework.load()

    results = compute_footprints.impressions_cost(
        campaign,
        nb_impressions=10000,
        creative_type="video",
        allocation="direct",
        creative_size_ko=1200,
        devices_repartition=DEVICES,
        creative_avg_view_s=5,
    )

    print(results.shows())

    results = compute_footprints.impressions_cost(
        campaign,
        nb_impressions=10000,
        creative_type="display",
        allocation="programmatic",
        creative_size_ko=1200,
        devices_repartition=DEVICES,
        creative_avg_view_s=5,
    )
    print(results.shows())

    campaign.change_target_country("DE")  # Changed from France to Germany
    results = compute_footprints.impressions_cost(
        campaign,
        nb_impressions=10000,
        creative_type="display",
        allocation="programmatic",
        creative_size_ko=1200,
        devices_repartition=DEVICES,
        creative_avg_view_s=5,
    )
    print(results.shows())

    test = Co2Cost(use=0.1, manufacturing=0.2)

    a = compute_footprints.bids_cost(campaign, nb_bids=1000)
    print(a.shows())

    a = compute_footprints.adcalls_cost(
        campaign, nb_ad_calls=1000, creative_type="video"
    )

    print(a.shows())
