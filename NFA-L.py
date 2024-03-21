def transition(cur_state, letter):
    newstate = set({cur_state})
    temp = set({})

    if '.' in trans_table[cur_state]:
        temp.update(trans_table[cur_state]['.'])
        for x in trans_table[cur_state]['.']:
            temp.update(transition_discover(x))
    newstate = newstate | temp
    temp = set({})
    for state in newstate:
        if letter in trans_table[state]:
            temp.update(trans_table[state][letter])
    newstate = temp
    temp = set({})
    if len(newstate) != 0:
        for state in newstate:
            if '.' in trans_table[state]:
                temp.update(trans_table[state]['.'])
                for x in trans_table[state]['.']:
                    temp.update(transition_discover(x))
    newstate = newstate | temp
    return newstate


def transition_discover(cur_state):
    newstate = {}
    newstate = set(newstate)
    if '.' in trans_table[cur_state]:
        newstate.update(trans_table[cur_state]['.'])
        for x in trans_table[cur_state]['.']:
            if(cur_state!=x):
                newstate.update(transition_discover(x))
    return newstate
#this function finds all possible lambda/epsilon transitions from the current state


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
        # If the length is 1, then that means there are no left (lines[i] that enters break is the number of words
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


stage = 0
print(trans_table)
for word in lines[word_try+1:]:
    word = word.strip()
    cur = [init_state]
    for letter_index in range(len(word)):
        p = word[letter_index]
        p = p.strip()
        add_to_next = []
        if len(cur)!=0:
            for sta in cur:
                if sta in trans_table:
                    add_to_next += [transition(sta, p)]
        if add_to_next == [set()]:
            stage = 0
            break
        else:
            stage = 1
    if stage == 0:
        print("NU")
    else:
        print("DA")