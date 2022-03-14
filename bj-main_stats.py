import numpy as np
import pandas as pd

CARD_VALUES_HIOPT2 = {
        '2': 1,
        '3': 1,
        '4': 2,
        '5': 2,
        '6': 1,
        '7': 1,
        '8': 0,
        '9': 0,
        '0': -2, # use '0' for 10 to keep everything a single character
        'J': -2,
        'Q': -2,
        'K': -2,
        'A': 0,
        '*': 0, # use '*' as an alias for 'A' to make using the number pad easier
        }
		
CARD_VALUES_HILO = {
        '2': 1,
        '3': 1,
        '4': 1,
        '5': 1,
        '6': 1,
        '7': 0,
        '8': 0,
        '9': 0,
        '0': -1, # use '0' for 10 to keep everything a single character
        'J': -1,
        'Q': -1,
        'K': -1,
        'A': -1,
        '*': -1, # use '*' as an alias for 'A' to make using the number pad easier
        }
		
CARD_VALUES_ZEN = {
        '2': 1,
        '3': 1,
        '4': 2,
        '5': 2,
        '6': 2,
        '7': 1,
        '8': 0,
        '9': 0,
        '0': -2, # use '0' for 10 to keep everything a single character
        'J': -2,
        'Q': -2,
        'K': -2,
        'A': -1,
        '*': -1, # use '*' as an alias for 'A' to make using the number pad easier
        }
        
DECKS = 8
arr = np.array([]) # deck count array
        
def deck_count(decks, count, aces, nobust_hand, bust_hand):
    rows = 2
    global arr
    if arr.size == 0:
        for row in range(rows):
            arr = np.array([[0.00,0.00,0.00,0.00], [0.00,0.00,0.00,0.00], [0.00,0.00,0.00,0.00], [0.00,0.00,0.00,0.00], [0.00,0.00,0.00,0.00]])

    if decks >= 1 and decks < 2 and arr[0][0] == 0:
        arr[0][0] = decks
        arr[1][0] = count
        arr[2][0] = aces
        arr[3][0] = nobust_hand
        arr[4][0] = bust_hand
    elif decks >= 2 and decks < 3 and arr[0][1] == 0:
        arr[0][1] = decks
        arr[1][1] = count
        arr[2][1] = aces
        arr[3][1] = nobust_hand
        arr[4][1] = bust_hand
    elif decks >= 3 and decks < 4 and arr[0][2] == 0:
        arr[0][2] = decks
        arr[1][2] = count
        arr[2][2] = aces
        arr[3][2] = nobust_hand
        arr[4][2] = bust_hand
    elif decks >= 4 and decks < 5 and arr[0][3] == 0:
        arr[0][3] = decks
        arr[1][3] = count
        arr[2][3] = aces
        arr[3][3] = nobust_hand
        arr[4][3] = bust_hand

    print(' ')
    print('Current Round:')
        
    a=pd.DataFrame(arr,index=['Decks','TCount','Aces','NoBust','Bust'],columns=['One', 'Two', 'Three', 'Four'])
    print(a)
    print(' ')
    
    #a.to_csv(r'stats.txt', header=True, index=True, sep='\t', mode='a')

def deck_main(true_count, decks_played, aces, nobust_hand, bust_hand):
    if decks_played >= 1 and decks_played < 2:
        deck_count(decks_played, true_count, aces, nobust_hand, bust_hand)
    elif decks_played >= 2 and decks_played < 3:
        deck_count(decks_played, true_count, aces, nobust_hand, bust_hand)
    elif decks_played >= 3 and decks_played < 4:
        deck_count(decks_played, true_count, aces, nobust_hand, bust_hand)
    elif decks_played >= 4 and decks_played < 5:
        deck_count(decks_played, true_count, aces, nobust_hand, bust_hand)

def main():
    count_hilo = 0
    count_hiopt2 = 0
    count_zen = 0
    cards = 0
    aces = 32
    nobust_hand = 0
    bust_hand = 0
    user_input = True
    decks_played = 0
    round_end = 0
    while user_input:
        user_input = input('>> ')
        cards += len(user_input)
        for card in user_input:
            if card.upper() != '-':
                if card.upper() != '+':
                    count_hilo += CARD_VALUES_HILO[card.upper()]
                    count_hiopt2 += CARD_VALUES_HIOPT2[card.upper()]
                    count_zen += CARD_VALUES_ZEN[card.upper()]
            if card.upper() == '*':
                aces -= 1
            if card.upper() == '-':
                nobust_hand += 1
            if card.upper() == '+':
                bust_hand += 1
        decks_played = round(cards / 52.0,2)
        true_count_hilo = round(count_hilo / (DECKS - decks_played),2)
        true_count_hiopt2 = round(count_hiopt2 / (DECKS - decks_played),2)
        true_count_zen = round(count_zen / (DECKS - decks_played),2)
        cards_left = (DECKS * 52)-cards
        deck_main(true_count_hilo, decks_played, aces, nobust_hand, bust_hand)
        print('Count: {}'.format(count_hilo))
        print('HILO TCount: {}'.format(true_count_hilo))
        print('HIOPT2 TCount: {}'.format(true_count_hiopt2))
        print('ZEN TCount: {}'.format(true_count_zen))
        print('Ace Count: {}'.format(aces))
        print('Decks played: {}'.format(decks_played))
        print('NoBust: {}, Bust: {}'.format(nobust_hand,bust_hand))
        #print('Cards: {}, Remaining Cards: {}'.format(cards,cards_left))
        
        if decks_played >= 4:
            if round_end == 0:
                a=pd.DataFrame(arr,index=['Decks','TCount','Aces','NoBust','Bust'],columns=['One', 'Two', 'Three', 'Four'])
                a.to_csv(r'stats.txt', header=True, index=True, sep='\t', mode='a')
                round_end = 1

if __name__ == '__main__':
    main()