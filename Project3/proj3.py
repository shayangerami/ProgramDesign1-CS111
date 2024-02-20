#Proj 3
    
# MS 5
    
'''
This milestone addds to the program that prompts the user for a state name and then draws a panel showing 
the votes distribution between Democrats and Republicans in all of that state districts.  
Most of this has already been written in driver.py.

Open up the pannel that will appear, to have a better look at the drawings.

'''

import driver # you need to this call draw_panel -- do not remove

# Open district.txt
with open(r"districts.txt") as file:  # Using 'with' statement to automatically close the file
    lines = file.readlines()
    
state_list = [] # collecting state names
state_info = {} # collecting state info
state_votes = {} #collecting state eligible voters

#nested dicts to collect votes for each district in each state
dem_dict = {} #democrate
rep_dict = {} #republican

for line in lines:
    line = line.strip().split(',')

    # Check if the last element is an empty string (lines 26 & 48 in district.txt)
    if line[-1] == '':
        line = line[:-1]

    #extract states
    state = line[0].lower()
    state_list.append(state)

    #extract info
    info = line[1:]
    state_info[state] = info
    
    #extract votes
    votes = 0
    for i in range(0, len(info), 3):
        district_num = str(info[i])
        dem_vote = int(info[i+1])
        rep_vote = int(info[i+2])

        votes += rep_vote + dem_vote

        if state not in dem_dict:
            dem_dict[state] = {}
        if state not in rep_dict:
            rep_dict[state] = {}
            
        dem_dict[state][district_num] = dem_vote # for democrate votes
        rep_dict[state][district_num] = rep_vote # for republican votes

    state_votes[state] = votes

# Open eligible_votes.txt
with open(r"eligible_voters.txt") as file:  # Using 'with' statement to automatically close the file
    lines = file.readlines()

state_voters = {}

for line in lines:
    line = line.strip().split(',')

    #extract states
    state = line[0].lower()
    state_list.append(state)

    #extract voters
    voters = line[1]
    state_voters[state] = voters

    
#Intro 
   
print('This program allows you to search through\n' +
'data about congressional voting districts\n' +
'and determine whether a particular state is\n' +
'gerrymandered.')


input_state = input('\nWhich state do you want to look up? \n')
input_state_lower = input_state.lower()

if input_state_lower not in state_list:
   print(f'{input_state} not found.')

else:
    
    prop_list = [] # List of tuples containing percentages
    dem_waste = 0
    rep_waste = 0
    for district in dem_dict[input_state_lower]: # Iterating through all districts in the dictionary

        dem_votes = dem_dict[input_state_lower][district]
        rep_votes = rep_dict[input_state_lower][district]
        total_votes = dem_votes + rep_votes

        # Avoid division by zero in Florida's case

        if total_votes != 0:
            dem_prop = round((dem_votes / total_votes) * 100)
            rep_prop = round((rep_votes / total_votes) * 100)

        else:
            dem_prop = 0
            rep_prop = 0

        # Append the tuple to the list
        prop_list.append((dem_prop, rep_prop))

        print(f'District {district}:', 'D' * dem_prop + 'R' * rep_prop)

        if dem_votes > rep_votes:
            loser_waste = rep_votes # All votes in the party that has lost are considered wasted
            over_half = round((total_votes / 2) + 1)
            over_waste = dem_votes -over_half

            dem_waste += over_waste
            rep_waste += loser_waste
            
        elif dem_votes < rep_votes:
            loser_waste = dem_votes
            over_half = round((total_votes / 2) + 1)
            over_waste = rep_votes -over_half
            
            rep_waste += over_waste
            dem_waste += loser_waste

    if len(dem_dict[input_state_lower]) >= 3:
        diff = abs(rep_waste - dem_waste) # Getting the absolute value to avoid negative numbers in case rep_wast is less
        eff_gap = round(((diff / state_votes[input_state_lower]) * 100), 2) # Round up to 2 decimals

        if eff_gap >= 7:
            GerryMandering = True
        else:
            GerryMandering = False
    else:
        GerryMandering = False

    print("\nGerrymandered?", "Yes" if GerryMandering else "No" )

    if len(dem_dict[input_state_lower]) >= 3 and GerryMandering:
        #These two statements will only be printed if the state is Gerrymandered
        print("Gerrymandered against:", "Democrats" if dem_waste > rep_waste else "Republicans") 
        print(f"Efficiency Factor: {eff_gap}%") 

    print(f'\nWasted Democratic votes: {dem_waste}')
    print(f'Wasted Republican votes: {rep_waste}')
    print('Eligible voters:', state_voters[input_state_lower])
    
    # Calling driver function 
    # len(dem_dict[input_state_lower]) is equal to the number of districts in the input state
    driver.draw_panel(state_voters[input_state_lower], prop_list, len(dem_dict[input_state_lower]))
