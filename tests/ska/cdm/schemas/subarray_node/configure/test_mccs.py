"""
Unit tests for the ska.cdm.schemas.subarray_node.configure.mccs module.
"""
import pytest as pytest

from ska.cdm.messages.subarray_node.configure.mccs import MCCSConfiguration
from ska.cdm.messages.subarray_node.configure.mccs import StnConfiguration
from ska.cdm.messages.subarray_node.configure.mccs import SubarrayBeamConfiguration
from ska.cdm.messages.subarray_node.configure.mccs import SubarrayBeamTarget
from ska.cdm.schemas.subarray_node.configure.mccs import MCCSConfigurationSchema
from ska.cdm.schemas.subarray_node.configure.mccs import StnConfigurationSchema
from ska.cdm.schemas.subarray_node.configure.mccs import SubarrayBeamConfigurationSchema
from ska.cdm.schemas.subarray_node.configure.mccs import SubarrayBeamTargetSchema
from ska.cdm.utils import json_is_equal


def test_marshall_subarray_beam_target():
    """Verify that SubarrayBeamTarget is marshalled to json correctly"""
    expected_json = """{
          "system": "HORIZON",
          "name": "DriftScan",
          "az": 180.0,
          "el": 45.0
        }"""
    target = SubarrayBeamTarget(180.0, 45.0, "DriftScan", "HORIZON")
    marshalled = SubarrayBeamTargetSchema().dumps(target)
    assert json_is_equal(expected_json, marshalled)


def test_marshall_stn_configuration():
    """Verify that StnConfiguration is marshalled to json correctly"""
    expected_json = """{"station_id":1}"""
    stn_config = StnConfiguration(1)
    marshalled = StnConfigurationSchema().dumps(stn_config)
    assert json_is_equal(expected_json, marshalled)


def test_marshall_stn_beam_configuration():
    """Verify that SubarrayBeamConfiguration is marshalled to json correctly"""
    expected_json = """
    {
        "subarray_beam_id": 1,
        "station_ids": [1,2],
        "channels": [[1, 2]],
        "update_rate": 0.0,
        "antenna_weights": [1.0, 1.0, 1.0],
        "phase_centre": [0.0, 0.0],
        "target": {
          "system": "HORIZON",
          "name": "DriftScan",
          "az": 180.0,
          "el": 45.0
        }
    }"""
    target = SubarrayBeamTarget(180.0, 45.0, "DriftScan", "HORIZON")
    stn_beam_config = SubarrayBeamConfiguration(
        1, [1, 2], [(1, 2)], 0.0, target,
        [1.0, 1.0, 1.0], [0.0, 0.0]
    )

    marshalled = SubarrayBeamConfigurationSchema().dumps(stn_beam_config)
    assert json_is_equal(expected_json, marshalled)


def test_marshall_mccsconfiguration():
    """
    Verify that MCCSConfiguration is marshalled to json correctly.
    """
    expected_json = """
    {
        "stations": [
            {
                "station_id": 1
            }
        ],
        "subarray_beams": [
            {
                "subarray_beam_id": 1,
                "station_ids": [1,2],
                "channels": [[1, 2]],
                "update_rate": 0.0,
                "antenna_weights": [1.0, 1.0, 1.0],
                "phase_centre": [0.0, 0.0],
                "target": {
                  "system": "HORIZON",
                  "name": "DriftScan",
                  "az": 180.0,
                  "el": 45.0
                }
            }
        ]
    }"""
    stn_config = StnConfiguration(1)
    target = SubarrayBeamTarget(180.0, 45.0, "DriftScan", "HORIZON")
    stn_beam_config = SubarrayBeamConfiguration(
        1, [1, 2], [(1, 2)], 0.0, target,
        [1.0, 1.0, 1.0], [0.0, 0.0]
    )
    config = MCCSConfiguration([stn_config], [stn_beam_config])
    marshalled = MCCSConfigurationSchema().dumps(config)
    assert json_is_equal(expected_json, marshalled)


def test_unmarshall_subarray_beam_target_from_json():
    """
    Verify that SubarrayBeamTarget is unmarshalled correctly from JSON.
    """
    az = 180.0
    el = 45.0
    name = 'DriftScan'
    system = 'HORIZON'
    expected = SubarrayBeamTarget(az, el, name, system)
    valid_json = """{
                  "system": "HORIZON",
                  "name": "DriftScan",
                  "az": 180.0,
                  "el": 45.0
                }"""
    unmarshalled = SubarrayBeamTargetSchema().loads(valid_json)
    assert unmarshalled == expected


def test_unmarshall_stnconfiguration_from_json():
    """
    Verify that StnConfiguration is unmarshalled correctly from JSON.
    """
    expected = StnConfiguration(5)
    valid_json = '{"station_id":5}'
    unmarshalled = StnConfigurationSchema().loads(valid_json)
    assert unmarshalled == expected


@pytest.mark.skip('TBC: Need to check unmarshall')
def test_unmarshall_SubarrayBeamConfiguration_from_json():
    """
    Verify that SubarrayBeamConfiguration is unmarshalled correctly from JSON.
    """
    az = 180.0
    el = 45.0
    name = 'DriftScan'
    system = 'HORIZON'
    target = SubarrayBeamTarget(az, el, name, system)
    subarray_beam_id = 1
    station_ids = [2, 3]
    channels = [(1, 2)]
    update_rate = 0.0
    antenna_weights = [1.0, 1.0, 1.0]
    phase_centre = [0.0, 0.0]

    expected = SubarrayBeamConfiguration(
        subarray_beam_id, station_ids, channels, update_rate, target,
        antenna_weights, phase_centre
    )
    valid_json = """
    {
        "subarray_beam_id": 1,
        "station_ids": [2,3],
        "channels": [[1, 2]],
        "update_rate": 0.0,
        "target": {
          "system": "HORIZON",
          "name": "DriftScan",
          "az": 180.0,
          "el": 45.0
        },
        "antenna_weights": [1.0, 1.0, 1.0],
        "phase_centre": [0.0, 0.0]
    }"""

    unmarshalled = SubarrayBeamConfigurationSchema().loads(valid_json)
    assert unmarshalled == expected


@pytest.mark.skip('TBC: Need to check unmarshall')
def test_unmarshall_mccsconfiguration_from_json():
    """
    Verify that MCCSConfiguration is unmarshalled correctly from JSON.
    """
    stn_config = StnConfiguration(1)
    target = SubarrayBeamTarget(180.0, 45.0, "DriftScan", "HORIZON")
    subarray_beam_config = SubarrayBeamConfiguration(
        1, [2, 3], [(1, 2)], 0.0, target,
        [1.0, 1.0, 1.0], [0.0, 0.0]
    )
    expected = MCCSConfiguration([stn_config], [subarray_beam_config])
    valid_json = """
    {
        "stations": [
            {
                "station_id": 1
            }
        ],
        "subarray_beams": [
            {
                "subarray_beam_id": 1,
                "station_ids": [2,3],
                "channels": [[1, 2]],
                "update_rate": 0.0,
                "target": {
                  "system": "HORIZON",
                  "name": "DriftScan",
                  "az": 180.0,
                  "el": 45.0
                },
                "antenna_weights": [1.0, 1.0, 1.0],
                "phase_centre": [0.0, 0.0]
            }
        ]
    }"""
    unmarshalled = MCCSConfigurationSchema().loads(valid_json)
    assert unmarshalled == expected
