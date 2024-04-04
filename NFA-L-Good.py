allstate = set({})

def lambda_discover(cur_state):
    global allstate
    if cur_state in trans_table:
        if '.' in trans_table[cur_state]:
            allstate.update(trans_table[cur_state]['.'])
            for x in trans_table[cur_state]['.']:
                if cur_state != x:
                    if '.' in trans_table[x]:
                        if all(item not in allstate for item in trans_table[x]['.']):
                            lambda_discover(x)
#this function finds all possible lambda/epsilon transitions from the current state

def transition_once(cur_state, letter):
    global allstate
    newstate = set({})
    if cur_state in trans_table:
        if '.' in trans_table[cur_state]:
            newstate.update(trans_table[cur_state]['.'])
            for x in trans_table[cur_state]['.']:
                lambda_discover(x)
        else:
            newstate = {cur_state}
        newstate = newstate | allstate
        allstate = set({})
        for x in newstate:
            if x in trans_table:
                if letter in trans_table[x]:
                    allstate.update(trans_table[x][letter])
        newstate = allstate
        allstate = set({})
        for x in newstate:
            if x in trans_table:
                if '.' in trans_table[x]:
                    allstate.update(trans_table[x]['.'])
                    for y in trans_table[x]['.']:
                        lambda_discover(y)
                else:
                    allstate.update(newstate)
        newstate = allstate
        allstate = set({})
    return newstate




with open("Input.txt", "r") as f:
    lines = f.readlines()

states = {x for x in lines[1].strip().split()}
# print(states)
# Saving the states of the LNFA inside a set

alphabet = {x for x in lines[3].strip().split()}
# print(alphabet)
# Saving the alphabet of the LNFA inside a set

init_state = str(lines[4].strip())
# print(init_state)
#Saving the initial state

final_states = {x for x in lines[6].strip().split()}
# print(final_states)
# Saving the final states of the LNFA inside a set

trans_table={}

word_try = 0

for i in range(8, len(lines)):
    if len(lines[i].split()) == 1:
        word_try = i
        # We try to enter all the transitions.
        # If the length is 1, then that means there are no transitions left
        # We save this number so that when trying words we do not have to go through dataset again
        break

    cur_line = lines[i].split()
    # Saving the transitions in a list form, for easier access.

    if cur_line[0] not in trans_table:
        trans_table[cur_line[0]] = {}
    # If we have not yet added a transition from this state, we will create an empty dict

    if cur_line[0] in trans_table and cur_line[1] not in trans_table[cur_line[0]]:
        trans_table[cur_line[0]][cur_line[1]] = [cur_line[2]]
    else:
        trans_table[cur_line[0]][cur_line[1]] += [(cur_line[2])]
    # We add the transitions


# lambda_discover('9909')
# print(allstate)
# print(transition_once('9909', 'd'))
print(trans_table)
with open('Output.txt', 'w') as f:
    for word in lines[word_try+1:]:
        word = word.strip()
        cur = {init_state}
        for letter in word:
            new_cur = set({})
            for state in cur:
                new_cur.update(transition_once(state, letter))
            cur = new_cur
        if any(state in cur for state in final_states):
            f.write('DA\n')
        else:
            f.write('NU\n')

#Made by Velcea Mihnea-Andrei, finished on 4/4/2024