import yaml
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from homeassistant.const import CONF_NAME, CONF_ICON, CONF_ENTITIES, CONF_SCHEDULE_FILE, CONF_SETBACK_TEMPERATURE
from homeassistant.components.climate import PLATFORM_SCHEMA, ClimateDevice
from homeassistant.components.sensor import ENTITY_ID_FORMAT
from homeassistant.core import callback

# Validation schema for the configuration file
CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME): cv.string,
        vol.Optional(CONF_ICON): cv.icon,
        vol.Required(CONF_ENTITIES): vol.All(cv.ensure_list, [cv.string]),
        vol.Required(CONF_SCHEDULE_FILE): cv.string,
        vol.Optional(CONF_SETBACK_TEMPERATURE, default=18): cv.positive_int,
    }
)

# Load the configuration file
def setup_platform(hass, config, add_entities, discovery_info=None):
    name = config[CONF_NAME]
    icon = config.get(CONF_ICON)
    entities = config[CONF_ENTITIES]
    schedule_file = config[CONF_SCHEDULE_FILE]
    setback_temp = config[CONF_SETBACK_TEMPERATURE]

    # Load the YAML file and parse the schedule
    with open(schedule_file) as f:
        schedule = yaml.safe_load(f)
        days = schedule["days"]
        periods = schedule["periods"]

    # Add default schedule between 10pm and 5am
    default_period = {
        "start": "22:00",
        "end": "05:00",
        "temperature": setback_temp
    }
    periods.append(default_period)

    # Create a custom climate device to manage the heating schedule
    climate_device = HeatingSchedule(hass, name, icon, days, periods, entities, setback_temp)
    add_entities([climate_device])

    # Create a text sensor to display the current schedule
    sensor_name = f"{name} Schedule"
    sensor_id = ENTITY_ID_FORMAT.format(sensor_name.lower().replace(" ", "_"))
    sensor = HeatingScheduleSensor(hass, sensor_id, sensor_name, climate_device)
    add_entities([sensor])

    @property
    def name(self):
        return self._name

    @property
    def icon(self):
        return self._icon

    @property
    def current_temperature(self):
        return self._current_temp

    def _calculate_mean_temperature(self):
        # Calculate the mean temperature of the specified entities
        total_temp = 0
        num_entities = len(self._entities)

        for entity in self._entities:
            state = self._hass.states.get(entity)
            total_temp += state.attributes[ATTR_TEMPERATURE]

        return total_temp / num_entities

    @property
    def target_temperature(self):
        # Return the target temperature for the current time period
        now = datetime.now()
        current_day = now.strftime("%A")
        current_time = now.strftime("%H:%M")

        if current_day in self._days:
            for period in self._periods:
                if period["start"] <= current_time <= period["end"]:
                    return period["temperature"]
        else:
            # If it's not a scheduled day, return the setback temperature
            return self._setback_temp

        # If no matching period is found, return the current temperature
        return self._current_temp

    @callback
    def update(self):
        # Update the target temperature for each of the specified entities
        for entity in self._entities:
            self._hass.states.set(entity, self.target_temperature, attributes={ATTR_TEMPERATURE: self.target_temperature})

# Custom sensor to display the current schedule
class HeatingScheduleSensor(Entity):
    def __init__(self, hass, entity_id, name, climate_device):
        self._hass = hass
        self.entity_id = entity_id
        self._name = name
        self._climate_device = climate_device

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        # Return the current schedule as a string
        now = datetime.now()
        current_day = now.strftime("%A")
        current_time = now.strftime("%H:%M")

        if current_day in self._climate_device._days:
            for period in self._climate_device._periods:
                if period["start"] <= current_time <= period["end"]:
                    return f"{period['start']} - {period['end']}: {period['temperature']}°C"
        else:
            # If it's not a scheduled day, return the setback temperature
            return f"{self._climate_device._setback_temp}°C (setback temperature)"

        # If no matching period is found, return "Unscheduled"
        return "Unscheduled"

    @property
    def device_state_attributes(self):
        # Return the full schedule as a dictionary
        schedule = {}
        for day in self._climate_device._days:
            schedule[day] = []
            for period in self._climate_device._periods:
                if period["start"].startswith(day[:2]):
                    schedule[day].append(f"{period['start']} - {period['end']}: {period['temperature']}°C")
        return {"schedule": schedule}


