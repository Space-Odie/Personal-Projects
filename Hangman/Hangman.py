import random

print('H A N G M A N')
#import wordlist
word_list = []
f = open('words.txt','r')
text = f.readlines()
for word in text:
    word_list.append(word)
word_select = (random.choice(word_list)).strip()

#print(word_select)
def main():
    count = 0
    answer = '-'*(len(word_select))

    #ask for user to input a letter
    while count < 8:
        guess = input(f"{answer}\nInput a letter:")

        #error handling
        if guess.isalpha()  == False:
            print('you entered an invalid character')

        if len(guess) == 1:
            #check guess and update answer
            answer, incrementer = checkguess(guess, word_select, answer)
            count = count + incrementer
        if answer == word_select:
            print('match')
            winner()
            break

        elif len(guess) > 1:
            if guess == word_select:
                winner()
                break
            else:
                count += 1

        if count == 8 and guess != word_select:
            print("You are hanged!")

        print('')
def winner():
    print('You guessed the word!')
    print('You survived!')

def checkguess(guess, word_select,string):
    guess_increase = 1
    no_improvement = 0
    no_letters = 0
    guess.lower()
    my_list = list(string)
    for number, letter in enumerate(word_select):
        if guess == letter:
            no_letters = 1
            if my_list[number] == guess:
                no_improvement = 1
            else:
                my_list[number] = guess
                guess_increase = 0

    if no_letters == 0:
        print('No such letter in the word')
    if no_improvement == 1:
        print('No improvements')
    return(''.join(my_list), guess_increase)

if __name__ == '__main__': main()

