
from flask import Flask, render_template
import mediapipe as mp
import cv2
from main import main_func
from autocorrect_complete import auto_corr

app = Flask(__name__)


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hand = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5)


text = str()
stop = False

@app.route("/")
def index():
    return render_template("index.html")


@app.route('/data')
def data():
    global text
    """send current content"""
    return text



@app.route('/run')
def run():
    global text
    global stop
    text = ''
    stop = False

    vid = cv2.VideoCapture(1)
    if vid.read()[0] == False:
        vid = cv2.VideoCapture(0)

    counter = 0
    while True:
        # Capture the video frame
        # by frame

        res,image = vid.read()


        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hand.process(image)

        # Draw the hand annotations on the image.
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

        # Flip the image horizontally for a selfie-view display.qr
        cv2.imshow('Output Frame', cv2.flip(image, 1))



        counter +=1
        try:
            if counter % 45 == 0:
            # pred_char, probability = main(image)
                pred_char, probability = main_func(image)
                
                if probability > 80:
                    if pred_char == ' ':
                        text = auto_corr(text)
                    else:
                        text += pred_char
    
        except Exception as e:
            print(e)
    
        
        if stop or (cv2.waitKey(1) & 0xFF == ord('q')):
            break

    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()

    return ('', 204)


@app.route('/stop')
def stop_app():
    global stop
    stop = True

    return ('', 204)


if __name__ == '__main__':
    app.run(debug=True)