def minion_game(string):
    vowels = {"A", "E", "I", "O", "U"}
    kevin = 0
    stuart = 0 
    n = len(string)
    for i, ch in enumerate(string):
        score = n - i
        if ch in vowels:
            kevin += score
        else:
            stuart += score
    if stuart > kevin:
        print(f"Stuart {stuart}")
    elif stuart == kevin:
        print("Draw")
    else:
        print(f"Kevin {kevin}")

minion_game("BANANATUNA")

tstamps = [
    "Sun 10 May 2015 13:54:36 -0700",
    "Sun 10 May 2015 13:54:36 -0000",
    "Sat 02 May 2015 19:54:36 +0530",
    "Fri 01 May 2015 13:54:36 -0000"]

from datetime import datetime
# Complete the time_delta function below.
def time_delta(t1, t2):
    format_str = "%a %d %b %Y %H:%M:%S %z"
    dt1 = datetime.strptime(t1, format_str)
    dt2 = datetime.strptime(t2, format_str)
    return str(int(abs((dt1 - dt2).total_seconds())))

print(time_delta(tstamps[0], tstamps[1]))