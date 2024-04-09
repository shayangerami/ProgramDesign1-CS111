
# MS4 - Full program          

""" 
File Header Comment

Identifies to whom a sequence of all 20 DNA sequences belongs. 
The program has no inputs, it loops through all 20 files and identify each one. 

For each of the STRs (from the first line of the STR counts file), 
program will compute the longest run of consecutive repeats of the STR in the DNA sequence to identify.

Lastly, program will print out the name of the matching individual for all DNA sequence files.

"""

import csv

def count_str_repeats(dna, strs):
    """
    Counts the longest consecutive repeats of STRs in a given DNA sequence.
    
    Parameters:
        dna (str): The DNA sequence.
        strs (list): A list of STRs to search for.
    
    Returns:
        dict: A dictionary with STRs as keys and the count of the longest
              consecutive repeats as values.
    """
    def find_longest_repeat(sequence, pattern):
        """
        Finds the longest repeat of a pattern in a sequence.
        
        Parameters:
            sequence (str): The sequence to search within.
            pattern (str): The pattern to search for.
        
        Returns:
            int: The longest consecutive repeat count of the pattern.
        """
        max_count = 0
        pattern_length = len(pattern)
        for i in range(len(sequence)):
            count = 0
            while sequence[i:i+pattern_length] == pattern:
                count += 1
                i += pattern_length
            max_count = max(max_count, count)
        return max_count
    
    # Dictionary to store STR and count
    longest_repeats = {}
    
    # Search through STR list
    for str_seq in strs:
        longest_repeats[str_seq] = find_longest_repeat(dna, str_seq)
    
    return longest_repeats
    
small_dict = {} # Stores names with their corresponding STR counts
with open(f'small.txt', 'r') as file:
    csv_reader = csv.reader(file)
    # Skip header row
    header_row = next(csv_reader)
    seq = header_row[1:] # List of DNA Sequences

    for row in csv_reader:
        name = row[0] # Getting name from each row
        seq_count = {seq[i]: int(row[i+1]) for i in range(len(seq))}
        small_dict[name] = seq_count

    for i in range(1,5): # Looping through small files
        with open(f'{i}.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()

            count_dict = {} # Dictionary to store STR and counts
            for j in seq:
                c = line.count(j)
                count_dict[j] = c

            n = ""
            for name, value in small_dict.items():
                if value == count_dict:
                    n += name

            if n == "":
                n += "No Match."

            print(f"Dna Sequence #{i} matches: {n}")
                             
large_dict = {} # Stores names with their corresponding STR counts
with open(f'large.txt', 'r') as file:
    csv_reader = csv.reader(file)
    # Skip header row
    header_row = next(csv_reader)
    seq = header_row[1:] # List of DNA Sequences

    for row in csv_reader:
        name = row[0] # Getting name from each row
        seq_count = {seq[i]: int(row[i+1]) for i in range(len(seq))}
        large_dict[name] = seq_count

    for i in range(5,21): # Looping through large files
        with open(f'{i}.txt', 'r') as file:
            # print('file', i)
            lines = file.readlines()
            for line in lines:
                line = line.strip() # Line is the same is DNA sequence

            patterns = [] # Stores all STRs
            for pattern in seq:
                patterns.append(pattern)

            longest_consecutive_repeats = count_str_repeats(line, patterns) # Calling count function

            match_name = ""
            for name, value in large_dict.items():
                if value == longest_consecutive_repeats:
                    match_name += name

            if match_name == '':
                match_name += "No Match."

            print(f"Dna Sequence #{i} matches: {match_name}")

        
# MS5 - Plots
            
"""

File Header Comment

Produces plots for each sequence showing an amount of each STR. 
The program has no inputs, it will loop through all 20 sequence files and plot each one. 

Note that the plot files will be saved in 'plots' folder.

Lastly the program will create one large plot with 20 smaller 
subplots to fit all DNA sequences saved as 'subplots.png'.

"""

import matplotlib.pyplot as plt
import csv

def count_str_repeats(dna, strs):
    """
    Counts the longest consecutive repeats of STRs in a given DNA sequence.
    
    Parameters:
        dna (str): The DNA sequence.
        strs (list): A list of STRs to search for.
    
    Returns:
        dict: A dictionary with STRs as keys and the count of the longest
              consecutive repeats as values.
    """
    def find_longest_repeat(sequence, pattern):
        """
        Finds the longest repeat of a pattern in a sequence.
        
        Parameters:
            sequence (str): The sequence to search within.
            pattern (str): The pattern to search for.
        
        Returns:
            int: The longest consecutive repeat count of the pattern.
        """
        max_count = 0
        pattern_length = len(pattern)
        for i in range(len(sequence)):
            count = 0
            while sequence[i:i+pattern_length] == pattern:
                count += 1
                i += pattern_length
            max_count = max(max_count, count)
        return max_count
    
    # Dictionary to store STR and count
    longest_repeats = {}
    
    # Search through STR list
    for str_seq in strs:
        longest_repeats[str_seq] = find_longest_repeat(dna, str_seq)
    
    return longest_repeats
    
small_dict = {} # Stores names with their corresponding STR counts
with open(f'small.txt', 'r') as file:
    csv_reader = csv.reader(file)
    # Skip header row
    header_row = next(csv_reader)
    seq = header_row[1:] # List of DNA Sequences

    for row in csv_reader:
        name = row[0] # Getting name from each row
        seq_count = {seq[i]: int(row[i+1]) for i in range(len(seq))}
        small_dict[name] = seq_count

    for i in range(1,5): # Looping through small files
        with open(f'{i}.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()

            count_dict = {} # Dictionary to store STR and counts
            for j in seq:
                c = line.count(j)
                count_dict[j] = c

            n = ""
            for name, value in small_dict.items():
                if value == count_dict:
                    n += name

            if n == "":
                n += "No Match."

            # Data for plotting
            strs = list(count_dict.keys())
            c = list(count_dict.values())

            # Creating the bar plot
            colors = ['red', 'green', 'blue']

            plt.figure()
            plt.bar(strs, c, color=colors)

            plt.title(f'{i}.txt : {n}')

            plt.savefig(f'plots/{i}.png')

large_dict = {} # Stores names with their corresponding STR counts
with open(f'large.txt', 'r') as file:
    csv_reader = csv.reader(file)
    # Skip header row
    header_row = next(csv_reader)
    seq = header_row[1:] # List of DNA Sequences

    for row in csv_reader:
        name = row[0] # Getting name from each row
        seq_count = {seq[i]: int(row[i+1]) for i in range(len(seq))}
        large_dict[name] = seq_count

    for i in range(5,21): # Looping through small files
        with open(f'{i}.txt', 'r') as file:
            # print('file', i)
            lines = file.readlines()
            for line in lines:
                line = line.strip() # Line is the same is DNA sequence

            patterns = [] # Stores all STRs
            for pattern in seq:
                patterns.append(pattern)

            longest_consecutive_repeats = count_str_repeats(line, patterns) # Calling count function

            match_name = ""
            for name, value in large_dict.items():
                if value == longest_consecutive_repeats:
                    match_name += name

            if match_name == '':
                match_name += "No Match."

            # Data for plotting
            strs = list(longest_consecutive_repeats.keys()) # STR Patterns
            c = list(longest_consecutive_repeats.values()) # Repeats

            # Creating the bar plot
            colors = ['red', 'green', 'blue', 'orange', 'purple', 'cyan', 'pink', 'yellow']

            plt.figure()
            plt.bar(strs, c, color=colors)

            plt.title(f'{i}.txt : {match_name}')

            plt.savefig(f'plots/{i}.png')

# Extra credit - Making subplots

import os

plots_dir = 'plots'

# Get a list of all sorted files 
plot_files = sorted(os.listdir(plots_dir), key=lambda x: int(os.path.splitext(x)[0]))

# Create a figure and subplot grid
fig, axes = plt.subplots(4, 5, figsize=(15, 10))

# Flatten the axes array if it's multidimensional
axes = axes.flatten()

# Iterate through each plot file
for i, plot_file in enumerate(plot_files):
    # Load and show the image
    img = plt.imread(os.path.join(plots_dir, plot_file))
    axes[i].imshow(img)
    
    # Remove axis ticks
    axes[i].axis('off')
    
    # Get the plot title 
    title = os.path.splitext(plot_file)[0]
    
    # Set the title
    axes[i].set_title(title)

# Adjust layout
plt.tight_layout()
# Save file
plt.savefig("subplots.png")


            


        
