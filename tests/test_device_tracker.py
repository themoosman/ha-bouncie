"""Tests for device_tracker.py."""
from homeassistant.core import HomeAssistant
from homeassistant.components.device_tracker import DOMAIN as DEVICE_TRACKER_DOMAIN
from homeassistant.helpers import entity_registry as er
from . import setup_platform
from . import const
import homeassistant.util.dt as date_util
from datetime import timedelta
from pytest_homeassistant_custom_component.common import async_fire_time_changed


async def test_device_tracker(hass: HomeAssistant) -> None:
    """Test getting all vehicles."""
    await setup_platform(hass, DEVICE_TRACKER_DOMAIN)
    entity_registry = er.async_get(hass)
    entry = entity_registry.async_get("device_tracker.my_prius")
    assert entry is not None
    state = hass.states.get("device_tracker.my_prius")
    assert state.state == "not_home"
    assert state.attributes["source_type"] == "gps"
    assert (
        state.attributes["latitude"]
        == const.MOCK_VEHICLES_RESPONSE[0]["stats"]["location"]["lat"]
    )
    assert (
        state.attributes["longitude"]
        == const.MOCK_VEHICLES_RESPONSE[0]["stats"]["location"]["lon"]
    )
    assert (
        state.attributes["heading"]
        == const.MOCK_VEHICLES_RESPONSE[0]["stats"]["location"]["heading"]
    )

async def test_device_tracker_update(hass: HomeAssistant) -> None:
    """Test getting updated value."""
    mock_entry, mock_controller = await setup_platform(hass, DEVICE_TRACKER_DOMAIN)
    entity_registry = er.async_get(hass)
    entry = entity_registry.async_get("device_tracker.my_prius")
    assert entry is not None
    state = hass.states.get("device_tracker.my_prius")
    assert state.state == "not_home"
    assert state.attributes["source_type"] == "gps"
    assert (
        state.attributes["latitude"]
        == const.MOCK_VEHICLES_RESPONSE[0]["stats"]["location"]["lat"]
    )
    assert (
        state.attributes["longitude"]
        == const.MOCK_VEHICLES_RESPONSE[0]["stats"]["location"]["lon"]
    )
    assert (
        state.attributes["heading"]
        == const.MOCK_VEHICLES_RESPONSE[0]["stats"]["location"]["heading"]
    )
    instance = mock_controller.return_value
    updated_response = const.MOCK_VEHICLES_RESPONSE
    updated_response[0]["stats"]["location"]["heading"] = 235
    instance.get_all_vehicles.return_value = updated_response
    async_fire_time_changed(hass, date_util.now() + timedelta(seconds=10))
    await hass.async_block_till_done()
    state = hass.states.get("device_tracker.my_prius")
    assert state.state == "not_home"
    assert state.attributes["heading"] == 235
