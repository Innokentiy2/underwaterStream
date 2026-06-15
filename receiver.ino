const int sensorPin = A0;

const int BIT_MS = 300;
const int SAMPLES_PER_BIT = 10;

const int FRAME_W = 8;
const int FRAME_H = 8;

byte frame[FRAME_H];

int baseline = 0;
int threshold = 8;

void setup() {
  Serial.begin(9600);

  long sum = 0;
  for (int i = 0; i < 300; i++) {
    sum += analogRead(sensorPin);
    delay(2);
  }
  baseline = sum / 300;
}

byte readBit() {
  long acc = 0;
  for (int i = 0; i < SAMPLES_PER_BIT; i++) {
    acc += analogRead(sensorPin);
    delay(BIT_MS / SAMPLES_PER_BIT);
  }
  int avg = acc / SAMPLES_PER_BIT;
  return (avg > baseline + threshold) ? 1 : 0;
}

byte readByte() {
  byte value = 0;
  for (int i = 0; i < 8; i++) {
    byte b = readBit();
    value |= (b << i);
  }
  return value;
}

void sendFrameToPC() {
  Serial.print("FRAME_BYTES:");
  for (int y = 0; y < FRAME_H; y++) {
    Serial.print(frame[y]);
    if (y < FRAME_H - 1) Serial.print(",");
  }
  Serial.println();
}

void loop() {
  for (int y = 0; y < FRAME_H; y++) {
    frame[y] = readByte();
  }

  sendFrameToPC();
}