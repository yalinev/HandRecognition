import cv2
import math 
from cvzone.HandTrackingModule import HandDetector

# The button class 
class Button:
    def __init__(self, pos, width, height, value):

        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self, image):
        # filled color 
        cv2.rectangle(image, self.pos, (self.pos[0]+self.width, self.pos[1]+self.height),
                       (119, 80, 148), cv2.FILLED)
        
        # blackish grey 
        cv2.rectangle(image, self.pos, (self.pos[0]+self.width, self.pos[1]+self.height),
                       (50, 50, 50), 3)
        
        cv2.putText(image, self.value, (self.pos[0] + 30, self.pos[1] + 70), cv2.FONT_HERSHEY_PLAIN, 2, (50, 50, 50), 2)

    def checkClick(self, x, y):
        # x1 < x < x1 + width/height if y 
        if self.pos[0] < x < self.pos[0] + self.width and self.pos[1] < y < self.pos[1] + self.height:
            
            cv2.rectangle(image, self.pos, (self.pos[0]+self.width, self.pos[1]+self.height), (150, 111, 179), cv2.FILLED)
        
            cv2.rectangle(image, self.pos, (self.pos[0]+self.width, self.pos[1]+self.height), (50, 50, 50), 3)
        
            cv2.putText(image, self.value, (self.pos[0] + 40, self.pos[1] + 60), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 4)

            return True # if the button has been clicked
        
    
# For webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Camera not found or could not be opened.")
    exit()

# 3 = wdith, 4 = height 
cap.set(3, 640) # The width 
cap.set(4, 840) # The height 

# 0.8 = detection confidence 
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Creating the buttons
buttonValues = [
                ['sin', '7', '4', '1', '0'],
                ['cos', '8', '5', '2', '.'],
                ['tan', '9', '6', '3', '/'],
                ['log', '*', '-', '+', 'DEL'],
                ['sqrt', '^', '(', ')', '=']]

# To store the buttons 
buttonList = [] 

# 5 x 5 grid
for x in range(5):
    for y in range(5):
        xPos = x * 100 + 700
        yPos = y * 100 + 150
        buttonList.append(Button((xPos, yPos), 100, 100, buttonValues[x][y])) 


# Variables 
equation = ''
delayCounter = 0

# To evaluate the equation
def evaluate(eq):
    eq = eq.replace('sin', 'math.sin')
    eq = eq.replace('cos', 'math.cos')
    eq = eq.replace('tan', 'math.tan')
    eq = eq.replace('sqrt', 'math.sqrt')
    eq = eq.replace('^', '**')
    eq = eq.replace('log', 'math.log10')
    try: 
        return str(eval(eq))
    except:
        return "ERROR!" 

# LOOP 
while True:

    # Get image from the webcam
    success, image = cap.read()

    if not success:
        print("Error: Failed to capture image.")
        break

    image = cv2.flip(image, 1)

    # Detection of hand
    hands, image = detector.findHands(image, flipType=False)

    # Draws the rectangle (question box)
    # (pt1),(x + width, y + height)
    cv2.rectangle(image, (700, 40), (800 + 400, 70 + 100), (225, 225, 225), cv2.FILLED)
    cv2.rectangle(image, (700, 40), (800 + 400, 70 + 100), (50, 50, 50), 4)

    # Draw all buttons
    for button in buttonList:
        button.draw(image)

    # Check for hand 
    if hands:
        lmList = hands[0]['lmList'] # Contains all the finger points
        length, _, image = detector.findDistance(lmList[8][:2], lmList[12][:2], image) 
        
        x, y = lmList[8][:2]

        if length < 50:
            for i, button in enumerate(buttonList):
                if button.checkClick(x, y) and delayCounter == 0:
                    # column, row --> displays the numbers clicked 
                    value = buttonValues[int(i/5)][int(i%5)]
                    if value == "=":
                        equation = str(evaluate(equation)) # convert back to string 
                    else:
                        equation += value
                    delayCounter = 1
    else:
        cv2.putText(image, "Hand not detected!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (150, 111, 179), 2)

    # For duplicate values 
    if delayCounter != 0:   # 1 = had started
        delayCounter += 1
        if delayCounter > 10:
            delayCounter = 0


    # Display the result/equation
    cv2.putText(image, equation, (810, 120), cv2.FONT_HERSHEY_PLAIN, 3, (50, 50, 50), 3)

    # Display the image
    cv2.imshow("Image", image)

    # Checking for 'c' key press (clears)
    key = cv2.waitKey(1) & 0xFF

    # ord() --> converts char to int (Unicode)
    if key == ord('c'):
        equation = ''
    # q = quit 
    if key == ord('q'):
        break

# Close all 
cap.release()
cv2.destroyAllWindows()
