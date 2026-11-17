# Fool the camera

**Status: code written, not yet run on a board.** CI compiles the sketch and tests the logger. Nobody has
flashed it or pointed it at a person yet, so there are no results below.

The AMB82-Mini runs a stock person detector. You try to make it miss you with printed patches, clothing
and lighting. A logger scores each attempt, so "it sort of worked" becomes a number.

## What you need

- AMB82-Mini with its camera, on USB
- Arduino IDE with the AmebaPro2 board package ([getting started](https://ameba-doc-arduino-sdk.readthedocs-hosted.com/en/latest/ameba_pro2/amb82-mini/Getting_Started/index.html))
- Python 3.10+ and `pip install pyserial`
- VLC, to watch the stream

## Run it

1. Copy `fool_the_camera/secrets.h.example` to `fool_the_camera/secrets.h` and fill in your Wi-Fi. Git ignores `secrets.h`.
2. Open `fool_the_camera/fool_the_camera.ino`, pick the AMB82-MINI board, and upload.
3. Open the serial monitor at 115200. It prints an `rtsp://` address; open that in VLC to see the boxes. Close the serial monitor again before step 4.
4. Stand in view and record a baseline, then one run per attack:

```bash
python logger.py baseline --port COM5
python logger.py "paper patch on chest" --port COM5
python logger.py "umbrella" --port COM5 --seconds 30
```

Each run watches for 20 seconds and adds a row to `results.csv`:

```
baseline: person seen in 198/200 frames (99%), mean score 87.4
```

An attack worked if its detection rate is well below the baseline taken in the same spot and light.

## How it works

The sketch is the SDK's `ObjectDetectionCallback` example with one change: for every frame the detector
processes, it prints `FTC,<millis>,<best person score>` on the serial port, with `0` when no person was
found. `logger.py` counts the share of frames with a person.

## Limits

- **One model.** Results apply to the stock YOLOv4-tiny at 576x320. A different model may behave differently.
- **Score scale is unconfirmed.** The SDK prints the score as a whole number; the logger only needs "above zero means detected".
- **Not a controlled experiment.** Distance, light and pose change the result. Take a fresh baseline whenever you move.
- **Own camera only.** Point this at yourself, on your own network.

Back to the [project list](../../README.md).
