# Text-message kill switch

**Status: planned. No code yet, nothing has been run on a board.**

Text STOP and the board sets the kill switch that blocks all agent writes in [mcp-opcua](https://github.com/ustechservice/mcp-opcua). Sender numbers can be faked, so it needs an allowlist plus a code. Simulator only.

- **Needs:** SMS receive, a small agent on the PC that creates the kill-switch file, and a SIM with a data plan

Back to the [project list](../../README.md).
