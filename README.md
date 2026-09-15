# Underwater Laser Image Transmission

A prototype optical communication system for transmitting low-resolution images
over a laser link using Raspberry Pi, Arduino, a photodiode, and Python.

> Status: working laboratory prototype in air.  
> Underwater testing is planned as the next stage.

![System architecture](docs/architecture.png)

## Overview

Radio communication performs poorly underwater because electromagnetic waves are
strongly attenuated. Acoustic communication can work over longer distances, but it
usually has lower bandwidth and higher latency.

This project explores an alternative: an optical communication channel based on a
blue laser. The prototype captures an image with a Raspberry Pi camera, converts it
into an 8×8 black-and-white frame, sends the frame bit by bit by modulating a laser
beam, and reconstructs the image on a computer.

## How it works

```text
Raspberry Pi Camera
        ↓
Image processing: grayscale → 8×8 → black/white
        ↓
Laser modulation
        ↓
BPW34 photodiode + amplifier
        ↓
Arduino signal decoding
        ↓
Python/Pygame visualizer
```

## Hardware

- Raspberry Pi with camera
- Blue laser module
- Relay module for the current prototype
- Arduino
- BPW34 photodiode
- Photodiode amplifier
- MOSFET driver planned for the next version

## Software

- Python
- Picamera2
- NumPy
- Pillow
- gpiozero
- Pygame
- Arduino/C++

## Current result

The system can transmit a sequence of 8×8 black-and-white frames over a laser link.
The receiver reconstructs each frame and displays it as a grid of 64 pixels.

This is not yet full-resolution real-time video. The main limitations are the relay
switching speed, simple binary modulation, external light interference, and the need
for precise alignment between the laser and photodiode.

## Challenges

- Accurate laser alignment is required for reliable reception.
- Ambient light can affect the photodiode signal.
- Threshold calibration is needed to distinguish signal from noise.
- The relay limits the switching frequency and data rate.

## Next steps

- Replace the relay with a MOSFET-based laser driver.
- Improve the photodiode amplifier and filtering.
- Add synchronization and frame-integrity checks.
- Add error detection or correction.
- Test the system in water at different distances and turbidity levels.
- Design a waterproof enclosure for the transmitter.

## Repository structure

```text
transmitter/  Raspberry Pi image capture and laser control
receiver/     Arduino receiver firmware
visualizer/   Python/Pygame frame visualizer
hardware/     Components, pinout, and hardware notes
docs/         Schematics, report, and technical documentation
media/        Photos, screenshots, and demo materials
```

## Running the project

### Raspberry Pi transmitter

```bash
pip install -r requirements.txt
python transmitter/image_transmission.py
```

Before running, configure the correct GPIO pin, camera settings, frame size, threshold,
and bit duration in `image_transmission.py`.

### Arduino receiver

Upload `receiver/receiver.ino` to the Arduino board and adjust the following values
if required:

- `sensorPin`
- `BIT_MS`
- `SAMPLES_PER_BIT`
- baseline and threshold parameters

### Visualizer

```bash
pip install pyserial pygame
python visualizer/visualize.py
```

Set the correct serial port in `visualize.py` before launching it.

## Media

Add photos of the transmitter, receiver, laser alignment, and the reconstructed frame
to the `media/` directory. A short demonstration video or GIF is recommended.

## Author

[Your name or GitHub username]

Built as an educational engineering project in 2026.

## License

This project is available under the MIT License.
