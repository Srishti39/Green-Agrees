#include <Wire.h>
#include <Adafruit_VL53L0X.h>
#include <MPU6050.h>

Adafruit_VL53L0X lox = Adafruit_VL53L0X();
MPU6050 mpu;
int pos=0;

int distanceArray[256];

void setup() {
  Serial.begin(9600);
  Serial.println("\nStarting setup...");

  Wire.begin();
  Serial.println("I2C Initialized");

  // Initialize the VL53L0X sensor
  if (!lox.begin()) {
    Serial.println(F("Failed to boot VL53L0X"));
    while (1); 
  } else {
    Serial.println("VL53L0X connected successfully!");
  }
  lox.setMeasurementTimingBudgetMicroSeconds(200000);

  // Initialize MPU6050
  mpu.initialize();
  if (!mpu.testConnection()) {
    Serial.println("MPU6050 connection failed.");
    while (1);
  } else {
    Serial.println("MPU6050 connected successfully!");
  }
}

int measure_dist() {
  VL53L0X_RangingMeasurementData_t measure;
  lox.rangingTest(&measure, false);  // Take a distance measurement
  
  if (measure.RangeStatus != 4) {  // If measurement is valid
    int smoothedDistance = measure.RangeMilliMeter;
    delay(500);
    Serial.print(F("   Distance:  "));
    Serial.print(smoothedDistance);
    Serial.print(F(" mm   "));
    return smoothedDistance;
  } else {
    Serial.println(F("Distance: Out of range"));
    return -1;
  }
}

void measure_mpu() {
  int16_t ax, ay, az;
  int16_t gx, gy, gz;

  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
  
  Serial.print("   Accel X: "); Serial.print(ax);
  Serial.print("   Accel Y: "); Serial.print(ay);
  Serial.print("   Accel Z: "); Serial.print(az);

  Serial.print("   Gyro X: "); Serial.print(gx);
  Serial.print("   Gyro Y: "); Serial.print(gy);
  Serial.print("   Gyro Z: "); Serial.println(gz);
}

void loop() {
      int dist = measure_dist();
      distanceArray[pos] = dist;
      measure_mpu();
      delay(100);  // Increased delay to allow sensor to read and process data
      pos=pos+1;
     
}

