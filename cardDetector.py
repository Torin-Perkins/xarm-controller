import cards
import videoStream
import cv2
import numpy as np
import time
import os

IM_WIDTH = 1280
IM_HEIGHT = 720
FRAME_RATE = 10

frame_rate_calc = 1
freq = cv2.getTickFrequency()


font = cv2.FONT_HERSHEY_SIMPLEX


videostream = videoStream.VideoStream((IM_WIDTH, IM_HEIGHT), FRAME_RATE, 2, 0).start()
time.sleep(1)  # Give the camera time to warm up

# Load the train rank and suit images
path = os.path.dirname(os.path.abspath(__file__))
train_ranks = cards.load_ranks(path + '/card_imgs/')
train_suits = cards.load_suits(path + '/card_imgs/')

### ---- MAIN LOOP ---- ###
# The main loop repeatedly grabs frames from the video stream
# and processes them to find and identify playing cards.

cam_quit = 0  # Loop control variable

# Begin capturing frames
while cam_quit == 0:

    # Grab frame from video stream
    image = videostream.read()
    cv2.imwrite("img.jpg", image)
    # Start timer (for calculating frame rate)
    t1 = cv2.getTickCount()

    # Pre-process camera image (gray, blur, and threshold it)
    pre_proc = cards.preprocess_image(image)

    # Find and sort the contours of all cards in the image (query cards)
    cnts_sort, cnt_is_card = cards.find_cards(pre_proc)
    # If there are no contours, do nothing
    if len(cnts_sort) != 0:

        # Initialize a new "cards" list to assign the card objects.
        # k indexes the newly made array of cards.
        cards_array = []
        k = 0

        # For each contour detected:
        for i in range(len(cnts_sort)):
            if (cnt_is_card[i] == 1):
                # Create a card object from the contour and append it to the list of cards.
                # preprocess_card function takes the card contour and contour and
                # determines the cards properties (corner points, etc). It generates a
                # flattened 200x300 image of the card, and isolates the card's
                # suit and rank from the image.
                cards_array.append(cards.preprocess_card(cnts_sort[i], image))
                print(len(cards_array))
                # Find the best rank and suit match for the card.
                cards_array[k].best_rank_match, cards_array[k].best_suit_match, cards_array[k].rank_diff, \
                    cards_array[k].suit_diff = cards.match_card(cards_array[k], train_ranks, train_suits)
                print(cards_array[k].best_rank_match)
                # Draw center point and match result on the image.
                image = cards.draw_results(image, cards_array[k])
                k = k + 1

        # Draw card contours on image (have to do contours all at once or
        # they do not show up properly for some reason)
        if (len(cards_array) != 0):
            temp_cnts = []
            for i in range(len(cards_array)):
                temp_cnts.append(cards_array[i].contour)
            cv2.drawContours(image, temp_cnts, -1, (255, 0, 0), 2)

    # Draw framerate in the corner of the image. Framerate is calculated at the end of the main loop,
    # so the first time this runs, framerate will be shown as 0.
    cv2.putText(image, "FPS: " + str(int(frame_rate_calc)), (10, 26), font, 0.7, (255, 0, 255), 2, cv2.LINE_AA)

    # Finally, display the image with the identified cards!
    cv2.imshow("Card Detector", image)

    # Calculate framerate
    t2 = cv2.getTickCount()
    time1 = (t2 - t1) / freq
    frame_rate_calc = 1 / time1

    # Poll the keyboard. If 'q' is pressed, exit the main loop.
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        cam_quit = 1

# Close all windows and close the PiCamera video stream.
cv2.destroyAllWindows()
videostream.stop()