import json

# Open the input and output files
with open('linkedin_profiles.jsonl', 'r') as infile, open('github_usernames.txt', 'w') as outfile:
    usernames = []
    
    # Read each line in the jsonl file
    for line in infile:
        # Parse the JSON object
        profile = json.loads(line)
        # Extract the github_username and add it to the list
        usernames.append(f'"{profile["github_username"]}"')
    
    # Join all usernames with commas and write to the output file
    outfile.write(", ".join(usernames))
