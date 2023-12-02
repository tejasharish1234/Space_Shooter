from game import game_loop
import mysql.connector as m
from sorts import *
if __name__ != '__main__':
    def run_game(name):             #fn called in menu.py
            con = m.connect(host = 'localhost', username = 'root', passwd = 'fab4', db = 'project')

            score, time = game_loop()                           #run the game and store the returned values
            
            player = [100, name, score , time]
            if con.is_connected():
                mycursor = con.cursor()

                query1 = 'select * from space_fighters'
                mycursor.execute(query1)
                result = mycursor.fetchall()                    #returns result as tuples nested in a list
                lst = []

                if len(result) != 0:                            #if players data exists
                    for i in range(len(result)):
                        a = list(result[i])                     #convert result tuples into lists
                        lst.append(a)
                        
                    lst.append(player)                          #append player data
                    insertion_sort_scores(lst)                  #sort player ranking based on score
                    bubble_sort_time(lst)                       #based on time if their scores are equal

                    for i in range(len(lst)):                   #using index posn as iterable i, 
                        lst[i][0] = i+1                         #change rank to i+1 since indexing starts from 0
                        lst[i] = tuple(lst[i])                  #convert nested lists back to nested tuples
                    
                    if len(lst) > 5:
                        lst.pop()

                elif len(lst) == 0:                             #if no player data exists
                    lst.append(player)
                    lst[0][0] = 1                               #change rank to 1
                    lst[0] = tuple(lst[0])                      #convert nested list to nested tuple

                
                query2 = 'delete from space_fighters'              #delete existing data, since data may have changed after last play
                mycursor.execute(query2)
                con.commit()
                
                query3 = 'insert into space_fighters values (%s,%s,%s,%s)'         #insert new data into sql table
                mycursor.executemany(query3, lst)
                con.commit()

            con.close()

            if time == 65:       #return score to decide which window should be displayed - win or lose
                return 'win'
            else:
                return 'lose'


