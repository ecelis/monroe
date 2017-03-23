# monroe

## Parts

* [HC-sr04](https://www.amazon.com/Arrela%C2%AE-Hc-sr04-Ultrasonic-Distance-Measuring/dp/B00KKKT7YK)
* 1 1k Ohm resistor
* 1 2.2k Ohm resistor


## Diagram


    |
    |-GND--------------------------------------------------GPIO GND [Pin 6]
    |                                                   |
    |-ECHO---R1 [1k]--GPIO 26 [Pin 37]---R2 [2Pin 6k]---
    |
    |-TRIG------------GPIO 20 [Pin 38]
    |
    |-Vcc-------------GPIO 5v [Pin 2]
