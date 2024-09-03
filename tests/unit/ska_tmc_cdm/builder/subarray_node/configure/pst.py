import functools

from ska_tmc_cdm.messages.subarray_node.configure.pst import (
    PSTBeamConfiguration,
    PSTChannelizationStageConfiguration,
    PSTConfiguration,
    PSTScanConfiguration,
    PSTScanCoordinates,
)

PSTScanCoordinatesBuilder = functools.partial(
    PSTScanCoordinates,
    equinox=2000.0,
    ra="19:21:44.815",
    dec="21:53:02.400",
)

PSTChannelizationStageConfigurationBuilder = functools.partial(
    PSTChannelizationStageConfiguration,
    num_filter_taps=1,
    filter_coefficients=(1.0,),
    num_frequency_channels=256,
    oversampling_ratio=(4, 3),
)
PSTScanConfigurationBuilder = functools.partial(
    PSTScanConfiguration,
    activation_time="2022-01-19T23:07:45Z",
    bits_per_sample=32,
    num_of_polarizations=2,
    udp_nsamp=32,
    wt_nsamp=32,
    udp_nchan=24,
    num_frequency_channels=432,
    centre_frequency=200000000.0,
    total_bandwidth=1562500.0,
    observation_mode="VOLTAGE_RECORDER",
    observer_id="jdoe",
    project_id="project1",
    pointing_id="pointing1",
    source="J1921+2153",
    itrf=(5109360.133, 2006852.586, -3238948.127),
    receiver_id="receiver3",
    feed_polarization="LIN",
    feed_handedness=1,
    feed_angle=1.234,
    feed_tracking_mode="FA",
    feed_position_angle=10.0,
    oversampling_ratio=(8, 7),
    coordinates=PSTScanCoordinatesBuilder(),
    max_scan_length=20000.0,
    subint_duration=30.0,
    receptors=("receptor1", "receptor2"),
    receptor_weights=(0.4, 0.6),
    num_channelization_stages=2,
    channelization_stages=(
        PSTChannelizationStageConfigurationBuilder(
            num_frequency_channels=1024,
            oversampling_ratio=(32, 27),
        ),
        PSTChannelizationStageConfigurationBuilder(
            num_frequency_channels=256,
            oversampling_ratio=(4, 3),
        ),
    ),
)


PSTBeamConfigurationBuilder = functools.partial(
    PSTBeamConfiguration, beam_id=1, scan=PSTScanConfigurationBuilder()
)
PSTConfigurationBuilder = functools.partial(
    PSTConfiguration, beams=(PSTBeamConfigurationBuilder(),)
)
