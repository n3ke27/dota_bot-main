import sqlite3


connection = sqlite3.connect('customers.db', check_same_thread=False)
cursor = connection.cursor()
def construct():
 cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    userid INT PRIMARY KEY,
    fname TEXT,
    lname TEXT,
    school INT,
    money DOUBLE,
    nickname TEXT,
    status TEXT);""")

 cursor.execute("""CREATE TABLE IF NOT EXISTS players(
    userid INT PRIMARY KEY,
    teamid INT,
    steamid INT,
    name TEXT,
    surname TEXT,
    school TEXT);""")

 cursor.execute("""CREATE TABLE IF NOT EXISTS teams(
    teamid INT PRIMARY KEY,
    adminid INT);""")
 
 connection.commit()


def change_status(userid, status):
    cursor.execute("select * from users where userid='" + str(userid) +"'" )
    result = cursor.fetchone()
    result1 = (result[0], result[1], result[2], result[3], result[4], result[5], status)
    cursor.execute("delete from users where userid="+str(result[0]))
    cursor.execute("insert into users values(?, ?, ?, ?, ?, ?, ?)", result1)
    connection.commit()
    
def change_player_atribute(userid, atribute, value):
    cursor.execute("select * from players where userid='"+str(userid)+"'")
    player = cursor.fetchone()
    cursor.execute("delete from players where userid="+str(player[0]))
    match atribute:
        case 'name':
            player1 = (player[0], player[1], player[2], value, player[4], player[5])
            cursor.execute("insert into players values(?, ?, ?, ?, ?, ?)", player1)
        case 'surname':
            player1 = (player[0], player[1], player[2], player[3], value, player[5])
            cursor.execute("insert into players values(?, ?, ?, ?, ?, ?)", player1)
        case 'team':
            player1 = (player[0], value, player[2], player[3], player[4], player[5])
            cursor.execute("insert into players values(?, ?, ?, ?, ?, ?)", player1)
        case 'school': 
            player1 = (player[0], player[1], player[2], player[3], player[4], value)
            cursor.execute("insert into players values(?, ?, ?, ?, ?, ?)", player1)
        case 'steam':
            player1 = (player[0], player[1], value, player[3], player[4], player[5])
            cursor.execute("insert into players values(?, ?, ?, ?, ?, ?)", player1)
    connection.commit()
            
def player_info(nickname):
    cursor.execute("select * from users where nickname='"+str(nickname)+"'")
    user = cursor.fetchone()
    cursor.execute("select * from players where userid = " + str(user[0]))
    player = cursor.fetchone()
    string = "Вот какую информацию удалось получить: \n" + "name: " + str( player[3] ) +" \n"+ "surname: " + str( player[4] ) + " \n" + "school: " + str( player[5] ) + " \n" + "steam: " + str(player[2])
    return string
