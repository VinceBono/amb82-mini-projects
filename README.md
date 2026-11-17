# amb82-mini-projects

Small projects for the Seeed Studio / Realtek **AMB82-Mini**, a $30 Wi-Fi camera board that runs
neural networks on the device (RTL8735B, 0.4 TOPS NPU, microphone, Arduino SDK).

Most of them ask one question: how easy is it to fool, attack or audit a cheap AI camera?

> **Status:** this is a plan. Every project below is marked *planned* until its code has run on a
> real board. Nothing here has been tested on hardware yet.

## Attacking and securing cheap AI cameras

| Project | What it does | Status |
|---|---|---|
| [Fool the camera](fool-the-camera/) | Run the stock person detector, then try to make it miss you with printed patches, clothing and lighting. A scoreboard records which attacks worked. | planned |
| [Replay-attack door lock](replay-attack-door-lock/) | Build the stock face-recognition door unlock, then attack it with a photo, a phone screen and a printed mask, and score each attack. | planned |
| [Camera with a flight recorder](camera-flight-recorder/) | Every detection is appended to a hash-chained log, so edits to the record can be detected afterwards. | planned |
| [Rogue-camera teardown](rogue-camera-teardown/) | Treat the board as a cheap IP camera and audit it: what it sends over Wi-Fi, whether the video stream needs a password, what secure boot protects. | planned |
| [Private vision assistant](private-vision-assistant/) | The board posts a snapshot and a spoken question to a PC on the same network, where a local vision model answers. No frames leave the network. | planned |

## Industrial

| Project | What it does | Status |
|---|---|---|
| [Andon light reader](andon-light-reader/) | Point the camera at a machine's stack light and publish red, yellow or green over MQTT. Machine status from equipment with no network port. | planned |
| [Analog gauge reader](gauge-reader/) | Read a needle gauge or a seven-segment display and publish the value. | planned |

## Just for fun

| Project | What it does | Status |
|---|---|---|
| [Bird feeder camera](bird-feeder-cam/) | Log which birds visit and send a daily digest. | planned |
| [Sound sentry](sound-sentry/) | Alert on glass breaking, a smoke alarm or a dog barking. Nothing is recorded or uploaded. | planned |

## Hardware and setup

- Board: [AMB82-Mini](https://www.seeedstudio.com/AMB82-MINI-RTL8735B-IoT-AI-Camera-Dev-Board-p-5584.html)
- SDK and examples: [Ameba-AIoT/ameba-arduino-pro2](https://github.com/Ameba-AIoT/ameba-arduino-pro2)
- Docs: [AMB82-Mini example guides](https://ameba-doc-arduino-sdk.readthedocs-hosted.com/en/latest/ameba_pro2/amb82-mini/Example_Guides/index.html)

## Ground rules

- Attacks are run against my own board on my own network only.
- Industrial projects are tested on a bench, never on plant equipment.
- This repo does not redistribute Realtek's model files or conversion tools. Flash the stock models
  from the SDK.

## License

MIT. See [LICENSE](LICENSE).
