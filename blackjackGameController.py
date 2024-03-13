import blackJackBrain
import cards
import videoStream
import cv2
import time
import os
import learm

camera_pos = [1500, 500, 500, 1189, 2500]
card_values = {
    "Ace": "A",
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
    "Six": 6,
    "Seven": 7,
    "Eight": 8,
    "Nine": 9,
    "Ten": 10,
    "Jack": 10,
    "Queen": 10,
    "King": 10
}


def get_blackjack_val(card):
    return card_values.get(card)


def play_game(dummy=True):
    arm = learm.LeArm()
    arm.moveToPosition(camera_pos, True)
    brain = blackJackBrain.dum_e_brain(False)
    # Camera settings
    IM_WIDTH = 1280
    IM_HEIGHT = 720
    FRAME_RATE = 10

    # Initialize calculated frame rate because it's calculated AFTER the first time it's displayed
    frame_rate_calc = 1
    freq = cv2.getTickFrequency()

    # Define font to use
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Initialize camera object and video feed from the camera. The video stream is set up
    # as a seperate thread that constantly grabs frames from the camera feed.
    # See VideoStream.py for VideoStream class definition
    # IF USING USB CAMERA INSTEAD OF PICAMERA,
    # CHANGE THE THIRD ARGUMENT FROM 1 TO 2 IN THE FOLLOWING LINE:
    videostream = videoStream.VideoStream((IM_WIDTH, IM_HEIGHT), FRAME_RATE, 2, 0).start()
    time.sleep(1)  # Give the camera time to warm up

    # Load the train rank and suit images
    path = os.path.dirname(os.path.abspath(__file__))
    train_ranks = cards.load_ranks(path + '/card_imgs/')
    train_suits = cards.load_suits(path + '/card_imgs/')

    game_loop = 1
    player_cards = []
    dealer_card = 0
    while game_loop:
        player_cards = []
        dealer_card = 0
        num_cards = input("How many cards do I have? ")

        for j in range(int(num_cards)):
            print("Please show me card #" + str(j + 1))
            time.sleep(10)

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

            cv2.putText(image, "FPS: " + str(int(frame_rate_calc)), (10, 26), font, 0.7, (255, 0, 255), 2, cv2.LINE_AA)

            # Finally, display the image with the identified cards!
            cv2.imshow("Card Detector", image)

            # Calculate framerate
            t2 = cv2.getTickCount()
            time1 = (t2 - t1) / freq
            frame_rate_calc = 1 / time1

            player_cards.append(cards_array[0].best_rank_match)
        print("My cards are ", player_cards)
        correct_player_cards = input("Is this correct? ")
        if correct_player_cards == 'n':
            continue
        """
        print("Please show me the dealers card")
        time.sleep(10)

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
        else:
            print("No card detected")
            continue
        dealer_card = cards_array[0].best_rank_match
        print("Dealer Card is ", dealer_card)
        correct_dealer_cards = input("Is this correct? ")
        if correct_dealer_cards == 'n':
            continue
        """
        valued_p_cards = []
        for i in player_cards:
            valued_p_cards.append(get_blackjack_val(i))

        move = brain.make_move(valued_p_cards, get_blackjack_val(dealer_card))
        print(move)


if __name__ == "__main__":
    play_game(True)
