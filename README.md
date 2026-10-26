# Mini-Piano
A PCB with switches and a speaker on it to make notes when the switches are pressed. Also has code for special button sequences, changing octaves, etc.

## Features
- Raspberry Pi Pico 2 SC1631
- Capacitive Touch Sensors for the keys, with a controller to use less pins
- Switches to change octave and mode
- An EC11 rotary encoder to control the volume
- LED's to represent power, mode, and volume, with a level shifter to regulate power
- A piezo buzzer to make the notes

## PCB
This is my PCB. I made it in EasyEda (pro)

Schematic:
![Schematic](<Images\Mini Piano Schematic.png>)

PCB:
![PCB](<Images\Mini Piano PCB.png>)

## 3d Model
I don't have a case for the Mini Piano so it has the PCB looks, so I am just showing the 3d model from EasyEda (pro) and the one I imported into Onshape containing the keycaps I made.

PCB 3d Model:
![PCB 3d Model](<Images\Mini Piano PCB 3d Model.png>)

3d Model with Keycaps:
![3d Model](<Images\Mini Piano 3d Model.png>)

I also included the keycaps at [Keycaps.step](Keycaps.step) and in Onshape [here](https://cad.onshape.com/documents/92bb40b0401efe4351ff9080/w/736b99143a63897fee2c3282/e/aefd495508d0e990bfad80b4?renderMode=0&uiState=6adfe701a4ceaaddce6b25c7).

## Firmware
I used [Micro Python](Modules/.micropico) for all of my code since I was already using the Raspberry Pi Pico and I already knew how to code in python. I used the [Rotary Module](Modules/rotary.py) with [Rotary IRQ (RP2)](Modules/rotary_irq_rp2.py) to control the rotary encoder better.

I made a few test programs to make sure all of the components are working as they should be located in [this folder](Code/Test%20Code).
Here are the ones I made:
- [Buttons Test](Code/Test%20Code/Buttons%20Test.py)
- [Capacitive Touch Sensors Test](Code/Test%20Code/Capacitive%20Touch%20Sensors%20Test.py)
- [LED's Test](Code/Test%20Code/LED's%20Test.py)
- [Piezo Buzzer Test](Code/Test%20Code/Piezo%20Buzzer%20Test.py)
- [Rotary Encoder Test](Code/Test%20Code/Rotary%20Encoder%20Test.py)

And here is the main program:
- [Mini Piano Code](Code/Mini%20Piano%20Code.py)

## BOM
You can view the full [BOM](BOM.csv), or you can see this one with less details but still all of the components:

- 1x Raspberry Pi Pico SC1631
- 3x TE Switches
- 1x EC11 Rotary Encoder
- 1x Piezo Buzzer
- 1x PCB (+ PCBA)
- 3x Surface Mount Neopixel LED's
- 1x AT42 Capacitive Touch Sensor Reader
- 1x Level Shifter (for LED's, included in PCBA if you want)
- 1x 3d Printed Keycaps