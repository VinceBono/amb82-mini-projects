# edge-device-lab

Small projects for cheap connected boards: AI cameras, cellular modems, LoRa radios and ESP32s.

Most of them ask one question: how easy is it to fool, attack, audit or harden a cheap connected device?

> **Status:** this is a plan. Every project below is marked *planned* until its code has run on a
> real board. Nothing here has been tested on hardware yet.

## AMB82-Mini (AI camera)

A $30 Wi-Fi camera board that runs neural networks on the device (RTL8735B, 0.4 TOPS NPU, microphone, Arduino SDK).

### Attacking and securing cheap AI cameras

| Project | What it does | Status |
|---|---|---|
| [Fool the camera](amb82-mini/fool-the-camera/) | Run the stock person detector, then try to make it miss you with printed patches, clothing and lighting. A scoreboard records which attacks worked. | planned |
| [Replay-attack door lock](amb82-mini/replay-attack-door-lock/) | Build the stock face-recognition door unlock, then attack it with a photo, a phone screen and a printed mask, and score each attack. | planned |
| [Camera with a flight recorder](amb82-mini/camera-flight-recorder/) | Every detection is appended to a hash-chained log, so edits to the record can be detected afterwards. | planned |
| [Rogue-camera teardown](amb82-mini/rogue-camera-teardown/) | Treat the board as a cheap IP camera and audit it: what it sends over Wi-Fi, whether the video stream needs a password, what secure boot protects. | planned |
| [Private vision assistant](amb82-mini/private-vision-assistant/) | The board posts a snapshot and a spoken question to a PC on the same network, where a local vision model answers. No frames leave the network. | planned |

### Industrial

| Project | What it does | Status |
|---|---|---|
| [Andon light reader](amb82-mini/andon-light-reader/) | Point the camera at a machine's stack light and publish red, yellow or green over MQTT. Machine status from equipment with no network port. | planned |
| [Analog gauge reader](amb82-mini/gauge-reader/) | Read a needle gauge or a seven-segment display and publish the value. | planned |

### Just for fun

| Project | What it does | Status |
|---|---|---|
| [Bird feeder camera](amb82-mini/bird-feeder-cam/) | Log which birds visit and send a daily digest. | planned |
| [Sound sentry](amb82-mini/sound-sentry/) | Alert on glass breaking, a smoke alarm or a dog barking. Nothing is recorded or uploaded. | planned |

## LTE Cat-1 + ESP32 (cellular)

An ESP32 with a SIMCom A7672G modem and a microSD slot. It works with no Wi-Fi, so it suits alerts and remote monitoring.

| Project | What it does | Status |
|---|---|---|
| [Camera that phones home](lte-cat1-esp32/camera-that-phones-home/) | The AMB82-Mini detects a person and hands the alert to this board, which sends a text over LTE. Cut or jam the Wi-Fi and the alert still arrives. The defence half of [fool-the-camera](amb82-mini/fool-the-camera/). | planned |
| [Text-message kill switch](lte-cat1-esp32/sms-kill-switch/) | Text STOP and the board sets the kill switch that blocks all agent writes in [mcp-opcua](https://github.com/ustechservice/mcp-opcua). Sender numbers can be faked, so it needs an allowlist plus a code. Simulator only. | planned |
| [Out-of-band lab watchdog](lte-cat1-esp32/lab-watchdog/) | Sits on a home lab network, checks that the hypervisor and the internet are alive, and texts when they are not. A relay can power-cycle the router. | planned |
| [Remote equipment monitor](lte-cat1-esp32/remote-equipment-monitor/) | Read a sensor, log to the SD card, and publish over LTE when there is signal, catching up after an outage. Bench only, never plant equipment. | planned |
| [Real phone-call test rig](lte-cat1-esp32/phone-call-test-rig/) | Play real and cloned voice samples through an actual cellular call and record what comes out the other end. Open question: whether this modem variant supports voice calls at all. | planned |
| [Off-grid bird feeder](lte-cat1-esp32/off-grid-bird-feeder/) | The [bird feeder camera](amb82-mini/bird-feeder-cam/) with LTE instead of Wi-Fi, for the back of the yard. | planned |

## On the bench, no projects yet

| Hardware | Likely use |
|---|---|
| Heltec Tracker V2 (ESP32-S3, LoRa SX1262, GPS) | Meshtastic node, off-grid alerts |
| DX-LR02 LoRa kit (ASR6601) | Point-to-point LoRa links |
| Waveshare ESP32-S3 AMOLED touch watch (dual microphones) | Wearable alerts, audio capture |
| ESP32 2.8 inch touch display (ILI9341) | Status panel |
| ESP32 38-pin dev boards and ESP32-S3 breakout | General sensors and glue |
| 8-channel relay module | Switching bench loads |
| USB to RS485/RS422 adapter | Modbus RTU on the bench |
| ESP32 WLED controller with Ethernet | Status lighting |

## Hardware and setup

- AMB82-Mini board: [Seeed Studio](https://www.seeedstudio.com/AMB82-MINI-RTL8735B-IoT-AI-Camera-Dev-Board-p-5584.html)
- AMB82-Mini SDK and examples: [Ameba-AIoT/ameba-arduino-pro2](https://github.com/Ameba-AIoT/ameba-arduino-pro2)
- AMB82-Mini docs: [example guides](https://ameba-doc-arduino-sdk.readthedocs-hosted.com/en/latest/ameba_pro2/amb82-mini/Example_Guides/index.html)

## Ground rules

- Attacks are run against my own board on my own network only.
- Industrial projects are tested on a bench, never on plant equipment.
- This repo does not redistribute Realtek's model files or conversion tools. Flash the stock models
  from the SDK.

## License

MIT. See [LICENSE](LICENSE).
