import sys
'''
Example use:
python3 merge_files.py input_file1.txt:"-1.20 0.80" input_file2.txt:"-3.15 -1.20" "first row in final merged file"
'''

def process_files(file_value_pairs, first_row_output):
    # Dictionary to store file contents
    file_contents = {}

    # Read files, remove first line, add second column with given value
    for file_value_pair in file_value_pairs:
        file_name, elements = file_value_pair.split(':')
        with open(file_name, 'r') as file:
            lines = file.readlines()[1:]  # Remove first line
            splitter = ''
            
            if ' '*3+'11'+' '*3 in lines[0]:
                splitter = ' '*3+'11'+' '*3
            elif ' '*3+'9'+' '*3 in lines[0]:
                splitter = ' '*3+'9'+' '*3
            else:
                print('NO GOOD SPLIT CHANGE THE SPLITTER HERE')
            
            new_lines = []
            
            for line in lines:
                for element in elements.split(','):
                    limits, value = element.split('?')
                    low_limit, up_limit = limits.split(' ')
                    eta = float(line.split()[1])
                    if eta > float(low_limit) and eta <= float(up_limit):
                        new_lines.append(line.split(splitter,1)[0] + ' ' + value + splitter + line.split(splitter,1)[1] + '\n')
            file_contents[file_name] = new_lines

    # Append file contents into output
    with open('output.txt', 'w') as output_file:
        # Add the given first row to the output file
        output_file.write(first_row_output.strip() + '\n')

        # Append contents of each file
        for file_name in file_contents:
            output_file.writelines(file_contents[file_name])

if __name__ == "__main__":
    # Get file-value pairs and first row from command line arguments
    file_value_pairs = sys.argv[1:-1]
    first_row_output = sys.argv[-1]

    # Process files and create output.txt
    process_files(file_value_pairs, first_row_output)

    #print("Output file 'output.txt' has been created successfully.")



