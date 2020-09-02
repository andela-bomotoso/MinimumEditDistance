#Author: Bukola Grace  Omotoso
# CSCI 6350-001
# Lab ID: Proj 1
# Due Date: 01/30/2020

'''ANALYSIS
A. COMPARE AND CONTRAST
     The confusion cost matrix gave a min edit distance that is lower than or equal
    to the min edit distance from the Levenshtein min edit distance. The confusion
    cost matrix seems to put other factors into consideration when determining a
    substitution cost between a source character and target character. Therefore,
    not giving all characters a equal chance of being siubstituted for another.

    The levenshstein cost matrix might be easier to work with since the substition
    cost values are fixed, one may not need to reference the cost table every time
    during computation, therefore increasing its tendency to be faster. One always
    has to look up the confusion matrix during computation, therefore making it
    slower to use.
    A far as accuracy is concerned, I would say using the confusion cost matrix may
    give a more accurate result than the Levenshtein cost matrix since it does a 
    more indept comparison puting other factors into consideration.

B. HOW IT FITS INTO A  LARGER NLP CONTEXT

 1. The soulution proposed in this project can be used to do a spell check. Given
    a word on a text editor that is not properly spelt, we can go through a bank of
    words that look similar to the incorrectly spelt word. The word with a minimum
    edit distance will stand a great chance of being the correct word.
    e.g If I type the word "hygene", the spell check of my text editor has a better
    chance of suggesting to me to type "hygeine" than the chance of suggesting the
    word "high" because the min edit distance between hygene and hygeine is less than
    that between "high" and "hygeine".

 2. Secondly, the solution proposed can be used to evaluate machine translation and
    speech recognition
     e.g
        Grace likes   to turn in her project early ---- stmt 1
        Grace prefers to turn in her project early ---- stmt 2
        Grace hates   to turn in her project early ---- stmt 3

    stmt 1 and stmt 2 look more related compared to stmt l and stmt 3. A machine can easily
    translate the word "likes" as "prefers" than it does translate the word "likes" as
    "hates".

C. HOW TO DEVISE A NEW SET OF COSTS
    a. A new set of cost can be devised by  looking at similarities between words
       not just characters.
    b. One can go through the process by training some datasets of synonyms
    c. Real life data can collected from people. Give a sentence to people, remove a word
        from the sentence and ask them to fill the blank. Compare what people tend to choose
        most among other options
    d. One can run an analysis to see words that are often used interchangeably

        e.g The scenario given above from stmt 1 - stmt 3. Finding the min distance
        between the words "likes and prefers" returns a higher value than "likes" and "hates".
        This should not be, given that people would mostly interchange "likes" and "prefers"
        that they would interchange "likes" and "hates".

        p***refers
        ||||||||||
        *lik*e***s
        diiidkdddk (8)

        p*refer*s
        |||||||||
        *l**ik*es
        diddssdik (6)
        --------------------------------------------------
        *hat**es
        ||||||||
        l***ikes
        idddiikk (6)

        hate*s
        ||||||
        l*ikes
        sdssik (2)


        Devising a solution that would rather consider the source and target word as a
        whole instead of going through each character will help to tackle this problem.

'''

import string
import csv
import random
#import the levenshtein cost matrix
def importLevCosts():
    with open('costs.csv', newline='') as infile:
        return list(csv.reader(infile))

#import the confusion cost matrix
def importConCosts():
    with open('costs2.csv', newline='') as infile:
        return list(csv.reader(infile))

#import the words file
def importWords():
    words_list = [];
    with open('words.txt', 'r') as infile:
        words_list = [line.split() for line in infile]
    return words_list

#   A Helper function to get the substitution cost between a src character
#    and a target  character

def getCost(cost_list, src_ch, trgt_ch):
    src_idx = ord(src_ch) - 96;
    trgt_idx = ord(trgt_ch) - 96;
    return cost_list[src_idx][trgt_idx];

#    A Helper function that fetches the cost value from the substitution matrix
#    based on a given row and col. The function helps to populate the min cost matrix
#    and the direction matrix'''

def findCellCost(matrix,  cost_mat, row, col, src, trg ):
    costs = [];
    direction = ""
    if (row == 0):
        return  (col, "1")
    elif (col == 0):
        return (row, "2")
    else:

        # check for insertion
        ins = matrix[row][col-1] + 1
        costs.append(ins)
        delt = matrix[row-1][col] + 1
        costs.append(delt)
        sub = matrix[row-1][col-1] + int(getCost(cost_mat, src[row-1], trg[col-1]));
        costs.append(sub)
        min_cost =  min(costs)
        # use 1 to denote insert
        if (ins == min_cost):
            direction+="1"
        # use 2 to denote delete
        if (delt == min_cost):
            direction+="2"
        # use 3 to denote substitution
        if (sub == min_cost):
            direction+="3";
    return (min_cost, direction)

# A function to create the min cost matrix  and direction matrix
# given a substitution cost matrix, a source and a target
def createCostMatrix(cost_mat, source, target):
    src_len = len(source)+1
    trgt_len = len(target) + 1
    min_cost = 0
    direction = ""
    # initialize the min cost matrix and the direction matrix 
    cost_matrix = [[0 for row in range(trgt_len)] for col in range(src_len)];
    dir_matrix = [["" for row in range(trgt_len)] for col in range(src_len)];
     # Populate the min cost matrix and the direction matrix with values
    for row in range(src_len):
        for col in range(trgt_len):
            min_cost, direction = findCellCost(cost_matrix, cost_mat, row, col, source, target );
            cost_matrix[row][col] = min_cost
            dir_matrix[row][col] += direction
    return(cost_matrix, dir_matrix)

#A function to find a path across the min cost table
# given a direction matrix, source and the target
def findPath(dir_matrix, source, target):
    dir_list = []
    row = len(source)
    col = len(target)
    num = 0
    last_cell =  False
    while(row >= 0 and col >=0):
        if ((row == 0 and col == 1)or (col == 0 and row == 1)):
            last_cell = True
        min_dir = dir_matrix[row][col]

        if(len(min_dir) == 3):
            #Pick any of the three direction
           num = int(min_dir[random.randint(0,2)])
        elif (len(min_dir) == 2):
            #Pick any of the three direction
            num = int(min_dir[random.randint(0,1)])
        else:
            num = int(min_dir)
            
        if(num == 1):
            #Move to the left, since 1 denotes insertion
            #according to the way we populated the direction matrix
            col = col - 1           
        elif(num == 2):
            #Move up since 2 denotes deletion
            #according to the way we populated the direction matrix
            row = row - 1
        else:
            #Move to the diagonal since 3 denotes substitution
            #according to the way we populated the direction matrix
            col = col - 1
            row = row -1
        dir_list.append(num)
        if ((last_cell == True) or (row==0 and col==0)):
            break;
    return dir_list

#Print log given a substition cost matrix, a min path, a source and a target
#1 denotes insertion, 2 denotes deletion, #3 denotes substition.
# e.g a path of 1233211323 could mean idssdiisds. 
def printLog(cost_list, path, source, target):
    path.reverse()
    src_out = ""
    tgt_out =""
    cost_out = ""
    src_cnt = 0
    tgt_cnt = 0
    min_cost = 0
    delim="";
    
    list_len = len(path);
    for i in range(list_len):
        if (path[i] == 1): # This is an insert
            src_out+= "*"
            tgt_out+=target[tgt_cnt];
            tgt_cnt+=1;
            cost_out+="i"
            min_cost+=1;
        elif (path[i] == 2): # This is a delete
            tgt_out+= "*"
            src_out+=source[src_cnt];
            src_cnt+=1
            cost_out+="d"
            min_cost+=1
        else: # This is substitution
            #Check if the cost between the target char and source char is null
            costval = getCost(cost_list, source[src_cnt], target[tgt_cnt]);
            if (int(costval) == 0 and source[src_cnt] ==  target[tgt_cnt]): # keep the char
                cost_out+="k"
            else:           # Make a substitution
                cost_out+="s"
                min_cost+=int(costval)
            # In both cases, the source and target characters remain
            src_out+=source[src_cnt]
            src_cnt+=1
            tgt_out+=target[tgt_cnt]
            tgt_cnt+=1
        delim+="|";
    cost_out+=" ("+str(min_cost)+")"

    print(src_out)
    print(delim)
    print(tgt_out)
    print(cost_out)
                    

    
def main():

    # import all the needed files
    lev_cost = importLevCosts()
    con_cost = importConCosts()
    words = importWords();
    
    # Loop through the words 
    for line in words:
        num_words = len(line)
        target = line[0]
        for i in range(1,num_words):
            source = line[i]
            #Use the leveinstein cost matrix
            #Generate the min cost matrix
            cost_matrix, dir_matrix = createCostMatrix(lev_cost, source, target);
            #Find the min path across the min cost matrix
            path = findPath(dir_matrix, source, target)
            #Print the log of the min path trace
            printLog(lev_cost, path, source, target)

            print() # new line

            #Use the constitution cost matrix
            #Generate the min cost matrix
            cost_matrix, dir_matrix = createCostMatrix(con_cost, source, target);
            #Find the min path across the min cost matrix
            path = findPath(dir_matrix, source, target)
            #Print the log of the min path trace
            printLog(con_cost, path, source, target)

            # Separate each pair of words using 50 hyphens
            str=""
            for i in range(50):
                str+="-"
            print(str)

    
    
# Call the main function
main();
