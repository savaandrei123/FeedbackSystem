#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <NTPClient.h>
#include <WiFiUdp.h>
#include <DebouncedSwitch.h>

#define BUTTON1 D2
#define BUTTON2 D3
#define BUTTON3 D4
#define BUTTON4 D5
#define BUTTON5 D6

DebouncedSwitch sw1(BUTTON1);
DebouncedSwitch sw2(BUTTON2);
DebouncedSwitch sw3(BUTTON3);
DebouncedSwitch sw4(BUTTON4);
DebouncedSwitch sw5(BUTTON5);

const char* ssid = "Sava-2.4G";
const char* password = "parolaNoua";

const long utcOffsetInSeconds = 7200;

WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org", utcOffsetInSeconds);

const char* serverName = "http://192.168.1.131:5000/insert";



String printLocalTime();
void sendRating(int rating);

void setup() {
  Serial.begin(115200);

  pinMode(BUTTON1, INPUT_PULLUP);
  pinMode(BUTTON2, INPUT_PULLUP);
  pinMode(BUTTON3, INPUT_PULLUP);
  pinMode(BUTTON4, INPUT_PULLUP);
  pinMode(BUTTON5, INPUT_PULLUP);

  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());

  timeClient.begin();
}

unsigned long lastTime = 0;
unsigned long timerDelay = 3000;
void loop() {
  
    if (WiFi.status() == WL_CONNECTED) {

      sw1.update();
      sw2.update();
      sw3.update();
      sw4.update();
      sw5.update();
    if ((millis() - lastTime) > timerDelay) {
      if (sw1.isChanged()) {
        if (!sw1.isDown()) {
          sendRating(1);
          Serial.println("BTN1 press");
          lastTime = millis();
        }
      }
    }
if ((millis() - lastTime) > timerDelay) {
      if (sw2.isChanged()) {
        if (!sw2.isDown()) {
          sendRating(2);
          Serial.println("BTN2 press");
          lastTime = millis();
        }
      }
}
if ((millis() - lastTime) > timerDelay) {

      if (sw3.isChanged()) {
        if (!sw3.isDown()) {
          sendRating(3);
          Serial.println("BTN3 press");
          lastTime = millis();
        }
      }}

if ((millis() - lastTime) > timerDelay) {
      if (sw4.isChanged()) {
        if (!sw4.isDown()) {
          sendRating(4);
          Serial.println("BTN4 press");
          lastTime = millis();
        }
      }
}
if ((millis() - lastTime) > timerDelay) {
      if (sw5.isChanged()) {
        if (!sw5.isDown()) {
          sendRating(5);
          Serial.println("BTN5 press");
          lastTime = millis();
        }
      }
    }
    } 
    else {
      Serial.println("WiFi Disconnected");
    }
  }



void sendRating(int rating) {
  WiFiClient client;
  HTTPClient http;
  http.begin(client, serverName);

  String currDate = getCurrentTime();


  http.addHeader("Content-Type", "application/json");
  int httpResponseCode = http.POST("{\"rating\":\"" + String(rating) + "\",\"date\":\"" + currDate + "\"}");

  Serial.print("HTTP Response code: ");
  Serial.println(httpResponseCode);

  http.end();
}

String getCurrentTime() {
  timeClient.update();
  time_t epochTime = timeClient.getEpochTime();
  struct tm* ptm = gmtime((time_t*)&epochTime);

  int monthDay = ptm->tm_mday;
  int currentMonth = ptm->tm_mon + 1;
  int currentYear = ptm->tm_year + 1900;

  int hour = timeClient.getHours();
  int minutes = timeClient.getMinutes();
  int seconds = timeClient.getSeconds();

  String currentDate = String(monthDay) + "/" + String(currentMonth) + "/" + String(currentYear) + " " + String(hour) + ":" + String(minutes) + ":" + String(seconds);

  return currentDate;
}
