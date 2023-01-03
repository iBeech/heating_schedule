# Introduction
This is a custom integration for Home Assistant that allows you to specify a heating schedule in a YAML file and apply it to one or more climate entities. The integration also supports the following additional features:

A setback temperature that can be used when the building is not occupied or when the alarm is armed (home).
An optional "occupied" Boolean entity that can be used to override the schedule based on the occupancy status of the building.
An optional alarm control panel entity that can be used to override the schedule when the alarm is armed (home).
Installation
To install this integration, follow these steps:

Add the integration to your Home Assistant instance using HACS.
In your Home Assistant configuration, add the following to your configuration.yaml file:

# Example configuration
```
heating_schedule:
  name: Heating Schedule
  icon: mdi:radiator
  entities:
    - climate.living_room
    - climate.bedroom
  schedule_file: /config/heating_schedule.yaml
  setback_temperature: 18
  occupied_entity: binary_sensor.building_occupied
  alarm_control_panel_entity: alarm_control_panel.alarm
  ```
Create a YAML file for your heating schedule. The file should have the following format:

```
days:
  - Monday
  - Tuesday
  - Wednesday
  - Thursday
  - Friday
periods:
  - start: 07:00
    end: 08:00
    temperature: 20
  - start: 08:00
    end: 09:00
    temperature: 21
  - start: 09:00
    end: 17:00
    temperature: 22
  - start: 17:00
    end: 22:00
    temperature: 21
```
This YAML file specifies that the schedule should be followed on Monday through Friday, with different periods and target temperatures for different times of the day. A default period between 10pm and 5am is added in the code to set the setback temperature.

Restart Home Assistant to apply the changes.
Configuration options
The following options can be added to the configuration.yaml file to customize the integration:

- `name` (required): The name of the custom climate device that will be created.
- `icon` (optional): An icon to display for the custom climate device.
- `entities` (required): A list of climate entities to apply the schedule to.
- `schedule_file` (required): The path to the YAML file containing the schedule.
- `setback_temperature` (optional): The temperature to set when the building is not occupied or when the alarm is armed (home). Default: 18.
- `occupied_entity` (optional): The entity ID of a Boolean entity that represents the occupancy status of the building.
- `alarm_control_panel_entity` (optional): The entity ID of an alarm control panel entity.

# Examples
Here are a few examples of how you might use this integration:
- Set the heating to 20°C from 7am to 8am, 21°C from 8am to 9am, 22°C from 9am to 5pm, and 21°C from 5pm to 10pm on weekdays:

```
days:
  - Monday
  - Tuesday
  - Wednesday
  - Thursday
  - Friday
periods:
  - start: 07:00
    end: 08:00
    temperature: 20
  - start: 08:00
    end: 09:00
    temperature: 21
  - start: 09:00
    end: 17:00
    temperature: 22
  - start: 17:00
    end: 22:00
    temperature: 21
```
Set the heating to 18°C when the building is not occupied, as indicated by the binary_sensor.building_occupied entity:
```
occupied_entity: binary_sensor.building_occupied
Set the heating to 18°C when the alarm is armed (home), as indicated by the alarm_control_panel.alarm entity:
Copy code
alarm_control_panel_entity: alarm_control_panel.alarm
```
# Support
If you have any issues with this integration, please open a GitHub issue.

# Credits
This integration was developed by Tom Beech.
# License
This project is licensed under the MIT License - see the LICENSE file for details.
