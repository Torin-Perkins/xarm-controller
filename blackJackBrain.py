import numpy as np


class dum_e_brain:
    agro = False

    def __init__(self, agressive):
        agro = agressive

    def remove_items(test_list, item):

        # using list comprehension to perform the task
        res = [i for i in test_list if i != item]
        return res
    def make_move(self, cards, dealer_card):
        print("My total is:", cards)
        if sum(cards) < 17:
            return "Hit"
        elif 17 < sum(cards) <= 21:
            return "Sit"
        elif sum(cards) > 21:
            return "Bust"
        """
        print("My total is:", np.sum(cards))
        if "A" not in cards and np.sum(cards) > 21:
            return "Bust"
        elif "A" in cards:
            temp = self.remove_items(cards, "A")
            if np.sum(temp) > 21:
                return "Bust"
        if "A" in cards and len(set(cards)) == 1:
            return "H"
        if "A" not in cards:
            if np.sum(cards) < 12:
                return "H"
            elif np.sum(cards) >= 17:
                return "S"
            elif not dealer_card == 'A':
                if dealer_card < 4 and np.sum(cards) == 12:
                    return "H"
                elif dealer_card < 7 and np.sum(cards) <= 21:
                    return "S"
                elif dealer_card > 7 and np.sum(cards) < 17:
                    return "H"
            elif dealer_card == 'A':
                if np.sum(cards) < 17:
                    return "H"
                else:
                    return "S"
        else:
            if 'A' in cards:
                cards = self.remove_items(cards, "A")
                if np.sum(cards) < 7:
                    return "H"
                elif np.sum(cards) == 7:
                    if dealer_card > 8:
                        return "H"
                    else:
                        return "S"
                elif np.sum(cards) >= 8:
                    return 'S'
            else:
                return "H"
        """
