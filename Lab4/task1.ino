#include <Arduino.h>
 
#include <SPI.h>
#include <Wire.h>
#include <Arduino_LSM6DS3.h>//for IMU library to read sensor data
#include <ArduinoJson.h>
#include <PubSubClient.h>//for MQTT clients library 
#include <WiFiNINA.h>//for wifi library 

#define CONVERT_G_TO_MS2 9.80665f //value of gravity 
#define FREQUENCY_HZ 104
#define INTERVAL_MS (1000 / (FREQUENCY_HZ + 1))

//define 3 axis 
struct Acc_senseData{

  float acc_x = 0.0F;
  float acc_y = 0.0F;
  float acc_z = 0.0F;

};

struct Gyr_senseData
{
  float gyr_x = 0.0F;
  float gyr_y = 0.0F;
  float gyr_z = 0.0F;
};

void setup_wifi();
void reconnect();

static char payload[256]; //payload msg send - 256 chrctr lmt
static Acc_senseData acc_data;
static Gyr_senseData gyr_data;
StaticJsonDocument<256> doc; //create JSON to hold data msgs
//i hate tokens
#define TOKEN ""
#define DEVICEID ""

//don't steal my wifi 
const char* ssid = "Zerivon_Home";
const char* password = "housenood0h!23";
const char mqtt_server[] = "mqtt.eclipseprojects.io"; //local server
const char publishTopic[] = "ece180da/hana/lab4/imu";

//create a client object 
WiFiClient wifiClient;
PubSubClient mqtt(wifiClient);

// Function will keep trying to connect if no connection is successful. 
// Once connected the network details will be printed to the serial monitor.
void setup_wifi(){

  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  while( WiFi.status() != WL_CONNECTED){

    delay(500);
    Serial.print("."); 
  }

  randomSeed(micros());
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
 
}

// reconnect and try to connect again
void reconnect(){

  while(!mqtt.connected()){
  
    //Serial.print("Attempting MQTT connection ....");
    //String clientID = "nano33_accelerometer-";
    //clientID += String(random(0xffff), HEX);
  
    if (mqtt.connect(DEVICEID, TOKEN, NULL)) {
    
      Serial.println("Connected to MQTT broker");
      digitalWrite(LED_BUILTIN, HIGH);
    }

    else
    {
      Serial.print("failed to connect to MQTT broker, rc=");
      Serial.print(mqtt.state());
      Serial.println("try again in 5 seconds");
      digitalWrite(LED_BUILTIN, LOW);
      delay(5000);

    }
     
  }
 
}

void setup() {

  pinMode(LED_BUILTIN, OUTPUT);//LED feedback
  Serial.begin(9600);
  while (!Serial);
 
 //initialize communication with the IMU  
  if (!IMU.begin())
  {
    Serial.println("Failed to initialize IMU!");
    while(1);
  }
  
  //connect to wifi then mqtt server
  setup_wifi();
  mqtt.setServer(mqtt_server, 1883);

}

void loop() {

  //if not connected, reconnect
  if (!mqtt.connected())
  {
    reconnect();
  }

  //MQTT client loop
  mqtt.loop();


  static unsigned long last_interval_ms = 0;

  float a_x, a_y, a_z;
  float g_x, g_y, g_z;

  if (millis() > last_interval_ms + INTERVAL_MS)
  {

    last_interval_ms = millis();

    //read accelerometer data
    IMU.readAcceleration(a_x, a_y, a_z); 
    // save data to structures
    acc_data.acc_x = a_x;
    acc_data.acc_y = a_y;
    acc_data.acc_z = a_z;
    //save data to document 
    doc["ACC_X"] = acc_data.acc_x * CONVERT_G_TO_MS2;
    doc["ACC_Y"] = acc_data.acc_y * CONVERT_G_TO_MS2;
    doc["ACC_Z"] = acc_data.acc_z * CONVERT_G_TO_MS2;

    IMU.readGyroscope(g_x, g_y, g_z);
    gyr_data.gyr_x = g_x;
    gyr_data.gyr_y = g_y;
    gyr_data.gyr_z = g_z;
    doc["GYR_X"] = gyr_data.gyr_x;
    doc["GYR_Y"] = gyr_data.gyr_y;
    doc["GYR_Z"] = gyr_data.gyr_z;

    //publish data through MQTT
    serializeJsonPretty(doc, payload);
    mqtt.publish(publishTopic, payload);
    Serial.println(payload);
 
  }

}

// Citations
// https://community.element14.com/challenges-projects/design-challenges/design-for-a-cause-2021/b/blog/posts/connecting-the-arduino-nano-33-iot-with-local-mqtt-broker-2