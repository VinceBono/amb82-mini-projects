// SPDX-License-Identifier: MIT
// Copyright (c) 2026 Vince Bono
//
// Based on the ObjectDetectionCallback example in the Ameba Arduino SDK (MIT):
// https://github.com/Ameba-AIoT/ameba-arduino-pro2
//
// Runs the stock YOLOv4-tiny detector, draws boxes on the RTSP stream, and prints one
// line per inference frame for logger.py:  FTC,<millis>,<best person score, 0 if none>

#include "WiFi.h"
#include "StreamIO.h"
#include "VideoStream.h"
#include "RTSP.h"
#include "NNObjectDetection.h"
#include "VideoStreamOverlay.h"
#include "secrets.h"    // copy secrets.h.example to secrets.h and fill in your Wi-Fi

#define CHANNEL      0
#define CHANNELNN    3
#define NNWIDTH      576
#define NNHEIGHT     320
#define PERSON_CLASS 0    // index of "person" in the stock 80-class model

VideoSetting config(VIDEO_FHD, 30, VIDEO_H264, 0);
VideoSetting configNN(NNWIDTH, NNHEIGHT, 10, VIDEO_RGB, 0);
NNObjectDetection ObjDet;
RTSP rtsp;
StreamIO videoStreamer(1, 1);
StreamIO videoStreamerNN(1, 1);

char ssid[] = WIFI_SSID;
char pass[] = WIFI_PASS;

void ODPostProcess(std::vector<ObjectDetectionResult> results);

void setup()
{
    Serial.begin(115200);

    int status = WL_IDLE_STATUS;
    while (status != WL_CONNECTED) {
        Serial.print("Connecting to ");
        Serial.println(ssid);
        status = WiFi.begin(ssid, pass);
        delay(2000);
    }

    config.setBitrate(2 * 1024 * 1024);
    Camera.configVideoChannel(CHANNEL, config);
    Camera.configVideoChannel(CHANNELNN, configNN);
    Camera.videoInit();

    rtsp.configVideo(config);
    rtsp.begin();

    ObjDet.configVideo(configNN);
    ObjDet.setResultCallback(ODPostProcess);
    ObjDet.modelSelect(OBJECT_DETECTION, DEFAULT_YOLOV4TINY, NA_MODEL, NA_MODEL);
    ObjDet.begin();

    videoStreamer.registerInput(Camera.getStream(CHANNEL));
    videoStreamer.registerOutput(rtsp);
    if (videoStreamer.begin() != 0) {
        Serial.println("StreamIO link start failed");
    }
    Camera.channelBegin(CHANNEL);

    videoStreamerNN.registerInput(Camera.getStream(CHANNELNN));
    videoStreamerNN.setStackSize();
    videoStreamerNN.setTaskPriority();
    videoStreamerNN.registerOutput(ObjDet);
    if (videoStreamerNN.begin() != 0) {
        Serial.println("StreamIO link start failed");
    }
    Camera.channelBegin(CHANNELNN);

    OSD.configVideo(CHANNEL, config);
    OSD.begin();

    Serial.print("Watch the stream at rtsp://");
    Serial.print(WiFi.localIP());
    Serial.print(":");
    Serial.println(rtsp.getPort());
}

void loop()
{
}

void ODPostProcess(std::vector<ObjectDetectionResult> results)
{
    uint16_t im_h = config.height();
    uint16_t im_w = config.width();
    int best = 0;

    OSD.createBitmap(CHANNEL);
    for (int i = 0; i < ObjDet.getResultCount(); i++) {
        ObjectDetectionResult item = results[i];
        if (item.type() != PERSON_CLASS) {
            continue;
        }
        if (item.score() > best) {
            best = item.score();
        }
        int xmin = (int)(item.xMin() * im_w);
        int xmax = (int)(item.xMax() * im_w);
        int ymin = (int)(item.yMin() * im_h);
        int ymax = (int)(item.yMax() * im_h);
        OSD.drawRect(CHANNEL, xmin, ymin, xmax, ymax, 3, OSD_COLOR_WHITE);
        char text_str[20];
        snprintf(text_str, sizeof(text_str), "person %d", item.score());
        OSD.drawText(CHANNEL, xmin, ymin - OSD.getTextHeight(CHANNEL), text_str, OSD_COLOR_CYAN);
    }
    OSD.update(CHANNEL);

    printf("FTC,%lu,%d\r\n", (unsigned long)millis(), best);
}
