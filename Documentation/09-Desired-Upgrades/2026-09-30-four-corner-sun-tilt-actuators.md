# Desired upgrade — Four corner actuators for sun tilt

| Field | Value |
| --- | --- |
| **Date (HST)** | 2026-09-30 |
| **Stated by** | Alexander |
| **State** | DESIRED |
| **Grounding** | Channel 1 hourly look on the energy desk (`Security/Cameras/panel_look.py`); Alexander, 2026-09-30 |
| **Related WO** | none yet |

## What is desired

Buy four actuators later, one on each corner of the solar-panel frame, and use them to tilt the array with the sun. The frame may stay wood or be rebuilt in aluminum.

The tilt the actuators would follow is the one already used by hand:

| Part of the day | Position | Notes |
| --- | --- | --- |
| Overnight, and the two hours before sunrise through one hour after | Left side up | Morning prep. It helps early capture. It is not required. Overnight left tilt is the correct prep. Flat is also acceptable. |
| Day, from one hour after sunrise until one hour before sunset | Flat | The day position. |
| Evening, from one hour before sunset until 45 minutes after | Right side up | The evening position. |

Left and right are as channel 1 sees the array: the left end of the panel raised is morning, the right end raised is evening.

## What works today

A person sets the tilt. The array sits on a wood frame. Channel 1 is the panel camera. Once an hour the energy desk looks at the newest channel 1 still, names the weather and the tilt, and asks for a person when the tilt does not match that part of the day. Sunrise and sunset come from `Energy/sun/sun-times-last.json`.

That check stays the record of whether the panels are aimed correctly. It does not move anything.

## What this does not authorize

No purchase, no actuator model, no stroke length, no load rating, no wiring, no frame rebuild, and no control code. The energy desk keeps warning for a person until this upgrade is actually built and signed off.

## Open choices

- Actuator stroke, force, and whether the four corners move as one plane or can be driven separately.
- Power source, and a way to set the tilt by hand if an actuator fails.
- Wood frame kept, or a new aluminum frame.
- Wind and rain hold, so the array is not driven during weather that should leave it down.
