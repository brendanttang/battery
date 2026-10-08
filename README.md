>ESC180 Project #1 — Battery Simulator, Fall 2026.

# Project Instructions

Many modern technologies rely on rechargeable batteries, including electric vehicles, e-bikes,
laptops, smartphones, and clean energy systems. As systems transition to renewable energy
sources such as wind and solar power, the need to store energy becomes more crucial. Further,
the electric vehicle industry relies on rechargeable batteries. Research continues to investigate
ways to improve this technology, including improving their performance and extending their
lifetime.

In this project, you will implement a simulator for a rechargeable battery. Note, many aspects of
this assignment are a substantial simplification compared to how batteries actually work but are
inspired by real properties.

The simulation proceeds as a series of operations, which are calls to functions you will define.

The lines of code correspond to different activities (i.e., charging the battery, leaving the battery
idle, using the battery to power some technology), querying for the temperature and charge
status, and querying for the charge time needed for future use.

## The following rules apply to how the battery charge, temperature and health are updated:
- Initial battery charge is set by the initialize() function. Battery begins in good
health, at 50% charge and at 20°C temperature.
- The battery is always charging, being used, or sitting idle.
- Charging can be fast or slow. Fast charging increases the charge by 3% per minute, slow
charging by 1% per minute.
- Fast charging occurs when the temperature is between 0-40°C, battery charge is below
80%, and battery health is good.
- Slow charging increases the temperature by 0.25°C per minute. Fast charging increases
the temperature by 0.5°C per minute.
- If fast charging is possible, it will occur. Charging can switch from fast to slow charging
in a single session.
- Usage discharges the battery by 2% per minute. Temperature increases by 1°C per minute
during usage.
- Sitting idle discharges the battery by 0.5% per minute and decreases the temperature by
1°C per minute. The temperature can never go below 0°C.
- If the battery charge reaches 0% during usage or idling, its temperature will decrease by
1°C per minute that it is dead (not going below 0°C), while the charge does not decrease
past 0%.
- Charging at or past 90% reduces the battery health. If this happens 3 times within 6
hours, the battery is in a bad health state.
- Batteries in bad health state cannot charge past 80%. If the battery initially switches to a
bad health state, it will not charge further until discharged below 80%.
- If the battery charge reaches 100% during charging, its temperature will continue to
increase by 0.25°C per minute, while the charge does not increase past 100%. The same
logic applies to if the battery is in a bad health state and reaches 80% during charging, or
if the battery switches to a bad health state and is at or above 90%: the temperature will
increase by 0.25°C per minute, while the battery charge will not increase further.

## Functions to Implement

**Part (a) get_cur_temp()**\
This function returns the current temperature of the battery, as a float.

**Part (b) get_cur_charge()**\
This function returns the current charge level of the battery, as a float.

**Part (c) get_cur_battery_health()**\
This function returns the health of the battery, as a boolean. It returns True if the battery is in
good health and False if the battery is in bad health.

**Part (d) duration_fast_charge_possible()**\
This function returns the duration for which fast charge is possible based on the current battery
health, temperature, and charge as a starting point.

**Part (e) simulate_activity(activity, duration)**\
This function simulates the battery performing the activity for duration minutes. Assume
duration is a positive int. If the activity is not one of “charge”, “use”, or “idle”, running the
function should have no effect.

**Part (f) charge_time_needed(minutes)**\
This function returns the duration needed for charging to enable use for a specific activity
duration of minutes afterwards. Based on a future journey, how long does the battery need to
charge now to have sufficient battery for minutes use duration? If the battery already has
sufficient charge, return 0. If it is impossible for the battery in its current state to be charged to a
point where usage for minutes duration can be performed, return None.

**Part (g) initialize()**\
This function initializes all the global variables in the program. 

## FAQ

1. The battery can never be below 0% or above 100%
2. The minute the battery charge reaches 90% is the minute that the overcharge has occurred
3. If the battery health is already at or above 90% and an additional charging activity is initiated, it counts as an overcharge
4. If the battery is in a bad health state, it is impossible for it to revert back to a good health state
5. The 6 hour range for overcharging is exclusive
6. Time is continuous, not discrete
