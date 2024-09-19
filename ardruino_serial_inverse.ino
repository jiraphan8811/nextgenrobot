// Define pins for the X and Y axis stepper motors
const int dirXPin = 5;    // X-axis direction pin
const int stepXPin = 2;   // X-axis step pin
const int dirYPin = 6;    // Y-axis direction pin
const int stepYPin = 3;   // Y-axis step pin

const int stepsPerRevolution = 200;  // Change this value based on your motor (for a 1.8° step motor, 200 steps = 360°)
int currentXPosition = 0;  // Track current position of the X axis
int currentYPosition = 0;  // Track current position of the Y axis
int speedDelay = 2000;  // Speed delay in microseconds (increase this to make the movement slower)

void setup() {
  // Set pins as output
  pinMode(dirXPin, OUTPUT);
  pinMode(stepXPin, OUTPUT);
  pinMode(dirYPin, OUTPUT);
  pinMode(stepYPin, OUTPUT);

  // Initialize serial communication
  Serial.begin(9600);
  Serial.println("Ready to receive data...");
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');  // Read the incoming data as a string
    int commaIndex = data.indexOf(',');          // Find the comma separator

    if (commaIndex > 0) {
      // Parse the two angles
      String angleXStr = data.substring(0, commaIndex);
      String angleYStr = data.substring(commaIndex + 1);

      int targetX = angleXStr.toInt();  // Convert X angle to integer
      int targetY = angleYStr.toInt();  // Convert Y angle to integer

      // Calculate the required movement in degrees for X and Y
      int deltaX = targetX - currentXPosition;
      int deltaY = targetY - currentYPosition;

      // Convert degrees to steps (for 1.8° step motor, 200 steps = 360°)
      int stepsX = map(abs(deltaX), 0, 360, 0, stepsPerRevolution);
      int stepsY = map(abs(deltaY), 0, 360, 0, stepsPerRevolution);

      // Set directions based on the sign of the delta values
      setDirection(dirXPin, deltaX);
      setDirection(dirYPin, deltaY);

      // Move the stepper motors
      moveStepper(stepsX, stepXPin, speedDelay);
      moveStepper(stepsY, stepYPin, speedDelay);

      // Update current positions
      currentXPosition = targetX;
      currentYPosition = targetY;

      // Debugging: print the received angles and positions
      Serial.print("X angle: ");
      Serial.print(targetX);
      Serial.print(" (steps: ");
      Serial.print(stepsX);
      Serial.print("), Y angle: ");
      Serial.print(targetY);
      Serial.print(" (steps: ");
      Serial.print(stepsY);
      Serial.println(")");
    }
  }
}

// Function to set direction based on the sign of delta (CW or CCW)
void setDirection(int dirPin, int delta) {
  if (delta > 0) {
    digitalWrite(dirPin, HIGH);  // Move in CW direction (positive degrees)
  } else if (delta < 0) {
    digitalWrite(dirPin, LOW);   // Move in CCW direction (negative degrees)
  }
  // If delta is 0, no movement will occur
}

// Function to move stepper motor
void moveStepper(int steps, int stepPin, int delayTime) {
  for (int i = 0; i < steps; i++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(delayTime);  
    digitalWrite(stepPin, LOW);
    delayMicroseconds(delayTime);  
  }
}
