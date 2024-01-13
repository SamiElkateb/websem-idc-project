import pandas as pd
import argparse
import subprocess

def run_command(command):
    try:
        subprocess.run([command], shell=True, check=True,text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert csv to rdf')
    parser.add_argument('--blockSize', type=int, help='Size of blocks to be processed')
    parser.add_argument('-b', type=int, help='shorthand for --blockSize')
    parser.add_argument('--path', type=str, help='Path for root')
    parser.add_argument('-p', type=str, help='shorthand for --path')
    args = parser.parse_args()
    blockSize = args.blockSize
    if blockSize is None:
        blockSize = args.b
    if blockSize is None:
        blockSize = 10
    path = args.path
    if path is None:
        path = args.p
    if path is None:
        path = ''
    RECIPES_PATH = path + 'data/recipes.csv'
    csv_save = pd.read_csv(RECIPES_PATH)
    print('Number of lines:', len(csv_save))
    print('blockSize =', blockSize)
    nb_lines = len(csv_save.index)
    current_index = 0
    content_output = ''
    first = True
    while current_index < nb_lines:
        if current_index + blockSize >= nb_lines:
            csv_save[current_index:].to_csv(RECIPES_PATH, index=False)
        else:
            csv_save[current_index:current_index + blockSize].to_csv(RECIPES_PATH, index=False)
        current_index += blockSize
        run_command('make recipesHandling')
        with open('output/recipes.ttl', 'r') as f:
            if first:
                first = False
                content_output = f.read()
            else:
                line = f.readline()
                while line:
                    if not line.startswith("@prefix"):
                        content_output += line
                    line = f.readline()
        print('Processed', current_index, 'lines (', (current_index / nb_lines) * 100, '%)')
    with open(path + 'output/recipes.ttl', 'w') as f:
        f.write(content_output)
    print('Recipes Done')
    csv_save.to_csv('data/recipes.csv', index=False)
#     run_command('make foodWeightsHandling')
#     run_command('docker compose up -d')
#     run_command('make formatting')
#     run_command('docker compose down')
    print('All Done')