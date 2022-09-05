"""GE Home Switch Entities"""
import async_timeout
import logging
from typing import Callable

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect


from .entities import GeErdSwitch
from .const import DOMAIN
from .devices import ApplianceApi
from .update_coordinator import GeHomeUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities: Callable):
    """GE Home sensors."""
    _LOGGER.debug('Adding GE Home switches')
    coordinator: GeHomeUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    @callback
    def async_devices_discovered(apis: list[ApplianceApi]):
        _LOGGER.debug(f'Found {len(apis):d} appliance APIs')
        entities = [
            entity
            for api in apis
            for entity in api.entities
            if isinstance(entity, GeErdSwitch) and entity.erd_code in api.appliance._property_cache
        ]
        _LOGGER.debug(f'Found {len(entities):d} switches')
        async_add_entities(entities)

    async_dispatcher_connect(hass, coordinator.signal_ready, async_devices_discovered)
