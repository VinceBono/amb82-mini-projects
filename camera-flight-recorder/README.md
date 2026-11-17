# Camera with a flight recorder

**Status: planned. No code yet, nothing has been run on a board.**

Every detection is appended to a hash-chained log, so edits to the record can be detected afterwards.

- **Starts from:** `ObjectDetectionCallback`, SD card examples (examples in the [Ameba Arduino SDK](https://github.com/Ameba-AIoT/ameba-arduino-pro2))
- **To add:** The hash-chain writer on the board and a verifier script on the PC.

Back to the [project list](../README.md).
