// Motor direction pins (L298N)
const int IN1 = 8;  // Left motor
const int IN2 = 7;
const int IN3 = 5;  // Right motor
const int IN4 = 4;

// Ultrasonic sensor pins
const int trigPin = 10;
const int echoPin = 11;

// Movement timing constants
const int FORWARD_DELAY = 800;  // Increased for more reliable movement
const int TURN_DELAY = 500;     // Increased for more reliable turns

void setup() {
  Serial.begin(9600);

  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  stopMotors();
}

void loop() {
  if (Serial.available()) {
    char command = Serial.read();
    if (command == 'F') {
      moveForward();
    } else if (command == 'L') {
      turnLeft();
    } else if (command == 'R') {
      turnRight();
    } else if (command == 'S') {
      stopMotors();
    } else if (command == 'D') {
      int dist = measureDistance();
      Serial.println(dist);
    }
  }
}

void moveForward() {
  // Reverse the motor directions to fix forward movement
  digitalWrite(IN1, LOW);   // Changed from HIGH to LOW
  digitalWrite(IN2, HIGH);  // Changed from LOW to HIGH
  digitalWrite(IN3, HIGH);  // Changed from LOW to HIGH
  digitalWrite(IN4, LOW);
  delay(FORWARD_DELAY);
  stopMotors();
}

void turnLeft() {
  digitalWrite(IN1, HIGH);  // Left motor backward
  digitalWrite(IN2, LOW);

  digitalWrite(IN3, HIGH);  // Right motor forward
  digitalWrite(IN4, LOW);

  delay(TURN_DELAY);
  stopMotors();
}


void turnRight() {
  digitalWrite(IN1, LOW);   // Left motor forward
  digitalWrite(IN2, HIGH);

  digitalWrite(IN3, LOW);   // Right motor backward
  digitalWrite(IN4, HIGH);

  delay(TURN_DELAY);
  stopMotors();
}


void stopMotors() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}

int measureDistance() {
  // Clear the trigger pin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  // Send trigger pulse
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Read the echo pulse
  long duration = pulseIn(echoPin, HIGH);

  // Calculate distance in centimeters
  // Speed of sound is 340 m/s or 0.034 cm/microsecond
  // Distance = (duration * speed of sound) / 2 (round trip)
  int distance = duration * 0.034 / 2;

  // Add a small delay to ensure stable readings
  delay(50);

  return distance;
}