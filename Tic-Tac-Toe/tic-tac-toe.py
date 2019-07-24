def print_board():
    for i in range(0,3):
        for j in range(0,3):
            print map[2-i][j],
            if j != 2:
                print "|",
        print ""


def check_done():
    for i in range(0,3):
        if map[i][0] == map[i][1] == map[i][2] != " " \
        or map[0][i] == map[1][i] == map[2][i] != " ":
            if turn == user:
                print "You won!!!"
            else:
                print "Computer won!!!"
            return True

    if map[0][0] == map[1][1] == map[2][2] != " " \
    or map[0][2] == map[1][1] == map[2][0] != " ":
        if turn == user:
            print "You won!!!"
        else:
            print "Computer won!!!"
        return True

    if " " not in map[0] and " " not in map[1] and " " not in map[2]:
        print "Draw"
        return True


    return False

#Search for immediate win/loss positions
def search_immediate_win_loss_position(key):

    #Check row wise
    for i in range(0,3):
        if map[i][0] == map[i][1] == key and map[i][2] == " ":
            return i,2
        if map[i][0] == map[i][2] == key and map[i][1] == " ":
            return i,1
        if map[i][1] == map[i][2] == key and map[i][0] == " ":
            return i,0

    #Check column wise
    for i in range(0,3):
        if map[0][i] == map[1][i] == key and map[2][i] == " ":
            return 2,i
        if map[0][i] == map[2][i] == key and map[1][i] == " ":
            return 1,i
        if map[1][i] == map[2][i] == key and map[0][i] == " ":
            return 0,i

     #Check diagonal wise
    if map[0][0] == map[1][1] == key  and map[2][2] == " ":
        return 2,2
    if map[0][0] == map[2][2] == key and map[1][1] == " ":
        return 1,1
    if map[1][1] == map[2][2] == key and map[0][0] == " ":
        return 0,0
    if map[0][2] == map[1][1] == key and map[2][0] == " ":
        return 2,0
    if map[0][2] == map[2][0] == key and map[1][1] == " ":
        return 1,1
    if map[2][0] == map[1][1] == key and map[0][2] == " ":
        return 0,2

    #Indicating computer can move its game as per wish
    return -1,-1


#Its important to get the center as it creates more possibilties for not to lose
def get_center():
    if map[1][1] == " ":
        return 1,1
    else:
        return -1,-1

def get_corner_rowwise(row,key):
    if map[1][1] == key:
        if map[0][0] == " ":
            return 0,0
        if map[0][2] == " ":
            return 0,2
        if map[2][0] == " ":
            return 2,0
        if map[2][2] == " ":
            return 2,2
    if map[row][0] != " " and map[row][2] == " ":
        return row,2
    if map[row][2] != " " and map[row][0] == " ":
        return row,0
    return -1,-1

def get_diagonally_opposite(row,col):
    if row == 0 and col == 0 and map[0][0] != " " and map[2][2] == " ":
        return 2,2
    elif row == 2 and col == 2 and map[2][2] != " " and map[0][0] == " ":
        return 0,0
    elif row == 0 and col == 2 and map[0][2] != " " and map[2][0] == " ":
        return 2,0
    elif row == 2 and col == 0 and map[2][0] != " " and map[0][2] == " ":
        return 0,2
    return -1,-1

def get_middle_positions():
    if map[0][1] == " ":
        return 0,1
    if map[1][0] == " ":
        return 1,0
    if map[1][2] == " ":
        return 1,2
    if map[2][1] == " ":
        return 2,1
    return -1,-1


#Decide next move if there's no chance of immediate loss or win
def decide_next_move(user, computer):

        (X,Y) = get_center()
        if (X,Y) != (-1,-1):
            return X,Y
        #Search for immediate winning position
        (X,Y) = search_immediate_win_loss_position(key=computer)
        if (X,Y) != (-1,-1):
            return X,Y
        #Search and protect from immediate losing position
        (X,Y) = search_immediate_win_loss_position(key=user)
        if (X,Y) != (-1,-1):
            return X,Y

        #At this stage no immediate win/loss position within next one move
        #Assign an absolute priority between cells rgarding which one to go for
        #next move. Target center one first. Then one of the corners and then
        #middle ones according to board stage

        #  |   | X
        #  | O |
        #X |   |
        if map[0][0] == map[2][2] == user and map[1][1] == computer \
        or map[0][2] == map[2][0] == user and map[1][1] == computer:
           (X,Y) = get_middle_positions()
           if (X,Y) != (-1,-1):
               return X,Y

         #X |   |
         #  | O | X
         #  |   |
        if map[0][0] == map[1][2] == user and map[0][2] == " ":
            (X,Y) = (0,2)
            return X,Y
        elif map[0][0] == map[2][1] == user and map[2][0] == " ":
            (X,Y) = (2,0)
            return X,Y
        elif map[0][2] == map[1][0] == user and map[0][0] == " ":
            (X,Y) = (0,0)
            return X,Y
        elif map[0][2] == map[2][1] == user and map[2][2] == " ":
            (X,Y) = (2,2)
            return X,Y
        elif map[2][0] == map[0][1] == user and map[0][0] == " ":
            (X,Y) = (0,0)
            return X,Y
        elif map[2][0] == map[1][2] == user and map[2][2] == " ":
            (X,Y) = (2,2)
            return X,Y
        elif map[2][2] == map[1][0] == user and map[2][0] == " ":
            (X,Y) = (2,0)
            return X,Y
        elif map[2][2] == map[0][1] == user and map[0][2] == " ":
            (X,Y) = (0,2)
            return X,Y

        #This is the generic absolute priority of the positions. Most off the times
        #execution will not come here especially as the game progresses
        (X,Y) = get_corner_rowwise(row=0,key=user)
        if (X,Y) != (-1,-1):
            return X,Y
        (X,Y) = get_corner_rowwise(row=2,key=user)
        if (X,Y) != (-1,-1):
            return X,Y
        (X,Y) = get_diagonally_opposite(row=0,col=0)
        if (X,Y) != (-1,-1):
            return X,Y
        (X,Y) = get_diagonally_opposite(row=0,col=2)
        if (X,Y) != (-1,-1):
            return X,Y
        (X,Y) = get_diagonally_opposite(row=2,col=0)
        if (X,Y) != (-1,-1):
            return X,Y
        (X,Y) = get_diagonally_opposite(row=2,col=2)
        if (X,Y) != (-1,-1):
            return X,Y
        (X,Y) = get_middle_positions()
        return X,Y



turn = "X"
map = [[" "," "," "],
       [" "," "," "],
       [" "," "," "]]
done = False
user = "X"
computer = "O"

print "Select which player to take..."
player = input("Select(1st player or 2nd player): ")
if player == 1:
    user = "X"
    computer = "O"
    turn = user
    print "You're first player and Mr. Computer is the second"
elif player == 2:
    user = "O"
    computer = "X"
    turn = computer
    print "You're the second player and should wait till computer's first turn"
else:
    player = 1
    print "Wrong Choice. We're moving ahead with you as first player"


while done != True:

    moved = False
    while moved != True:


        #User's turn
        if turn == user:
            print "Please select position by typing in a number between 1 and 9, see below for which number that is which position..."
            print "7|8|9"
            print "4|5|6"
            print "1|2|3"
            print

            try:
                pos = input("Select: ")
                if pos <=9 and pos >=1:
                    Y = pos/3
                    X = pos%3
                    if X != 0:
                        X -=1
                    else:
                         X = 2
                         Y -=1

                    if map[Y][X] == " ":
                        map[Y][X] = turn
                        moved = True
                        print "After Users turn"
                        print_board()
                        done = check_done()

                        if done == False:
                            turn = computer
                        else:
                            break


            except:
                print "You need to add a numeric value"

        #Computer's turn
        if turn == computer:
            (X,Y) = decide_next_move(user,computer)
            if (X,Y) != (-1,-1):
                map[X][Y] = turn
                moved = True
                print "After Computer's turn"
                print_board()
                done = check_done()

                if done == False:
                    turn = user
                else:
                    break
            else:
                print "Computer doesn't know what to do!!!"
