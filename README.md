# Introduction

This repository contains the drawings, electronics schematics, firmware
and building instructions for a (almost) completely 3D printed robotic
actuator. The actuator is based in a 36 stator poles and 42
rotor/magnetic poles BLCD, whiose output is attached to a 6:1 planetary
gearbox.


# DRIVER


<p align="center">
  <img src="./imgs/Motor_FSM.png" />
</p>


## CAN Protocol

|Frame |Signal|Bit Position|Bit Length|Scale|Offset|Units|Notes                 |
|------|------|------------|----------|-----|------|-----|----------------------|
|0x001 |      |<ul><li>0</li><li>16</li><li>32</li></ul>|<ul><li>16</li><li>16</li><li>16</li></ul>|<ul><li>0.125</li><li>0.125</li><li>0.125</li></ul>|<ul><li>0</li><li>0</li><li>0</li></ul>|<ul><li>-</li><li>-</li><li>-</li></ul>|<ul><li>P value for the PID position control</li><li>I value for the PID position control</li><li>D value for the PID position control</li></ul>|
|0x002 |      |<ul><li>0</li><li>16</li><li>32</li><li>48</li></ul>|<ul><li>16</li><li>16</li><li>16</li><li>16</li></ul>|<ul><li>0.125</li><li>0.125</li><li>0.125</li><li>0.125</li></ul>|<ul><li>0</li><li>0</li><li>0</li><li>0</li><li></ul>|<ul><li>-</li><li>-</li><li>-</li><li>rad/s</li></ul>|<ul><li>P value for the PID speed control</li><li>I value for the PID speed control</li><li>D value for the PID speed control</li><li>Speed limit</li></ul>|
0x003 |      |<ul><li>0</li><li>16</li><li>32</li><li>48</li></ul>|<ul><li>16</li><li>16</li><li>16</li><li>16</li></ul>|<ul><li>0.125</li><li>0.125</li><li>1</li><li>0.125</li></ul>|<ul><li>0</li><li>0</li><li>0</li><li>-4095</li><li></ul>|<ul><li>V</li><li>V</li><li>-</li><li>rad</li></ul>|<ul><li>Voltage limit for motor input</li><li>Voltage limit for aling in calibration</li><li>Calibration (1 skip, o calibrate)</li><li>Electric angle offset </li></ul>|
0x004 |      |<ul><li>0</li><li>16</li><li>32</li><li>48</li></ul>|<ul><li>16</li><li>16</li><li>16</li><li>16</li></ul>|<ul><li>0.125</li><li>0.125</li><li>1</li><li>0.125</li></ul>|<ul><li>-4095</li><li>-4095</li><li>-4095</li><li>-4095</li><li></ul>|<ul><li>V</li><li>V</li><li>I</li><li>rad</li></ul>|<ul><li>Ua component of voltage input</li><li>Ub component of voltage input</li><li>Current drawn by motor</li><li>Electric angle  </li></ul>|
0x005 |      |<ul><li>0</li><li>16</li><li>32</li></ul>|<ul><li>16</li><li>16</li><li>16</li></ul>|<ul><li>0.125</li><li>0.125</li><li>0.125</li></ul>|<ul><li>-4095</li><li>-4095</li><li>-4095</li><li></ul>|<ul><li>rad</li><li>rad</li><li>rad/s</li></ul>|<ul><li>Current mechanical angle</li><li>Mechanical angle setponit</li><li>Shaft speed</li></ul>|
0x006 |      |<ul><li>0</li></ul>|<ul><li>16</li></ul>|<ul><li>1</li></ul>|<ul><li>0</li></ul>|<ul><li>-</li></ul>|<ul><li>Finite State Machine transition</li></ul>|
0x007 |      |<ul><li>0</li></ul>|<ul><li>16</li></ul>|<ul><li>0.125</li></ul>|<ul><li>-4095</li></ul>|<ul><li>rad</li></ul>|<ul><li>Motor set point command</li></ul>|


