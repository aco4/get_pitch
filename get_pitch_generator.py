import os, math



# get_pitch_floor.mcfunction

# execute if entity @s[x_rotation=-90..0] run function namespace:-90t0
# execute if entity @s[x_rotation=0..90] run function namespace:0t90
# execute if entity @s[x_rotation=90] run scoreboard players set @s pitch 90

    # -90t0.mcfunction
    # execute if entity @s[x_rotation=-90..-45] run function namespace:-90t-45
    # execute if entity @s[x_rotation=-45..0] run function namespace:-45t0

        # -90t-45.mcfunction
        # execute if entity @s[x_rotation=-90..-67] run function namespace:-90t-67
        # execute if entity @s[x_rotation=-67..-45] run function namespace:-67t-45

            # -90t-67.mcfunction
            # execute if entity @s[x_rotation=-90..-78] run function namespace:-90t-78
            # execute if entity @s[x_rotation=-78..-67] run function namespace:-78t-67

                # -90t-78.mcfunction
                # execute if entity @s[x_rotation=-90..-84] run function namespace:-90t-84
                # execute if entity @s[x_rotation=-84..-78] run function namespace:-84t-78

                    # -90t-84.mcfunction
                    # execute if entity @s[x_rotation=-90..-87] run function namespace:-90t-87
                    # execute if entity @s[x_rotation=-87..-84] run function namespace:-87t-84

                        # -90t-87.mcfunction
                        # execute if entity @s[x_rotation=-90..-88] run function namespace:-90t-88
                        # execute if entity @s[x_rotation=-88..-87] run scoreboard players set @s pitch -88

                            # -90t-88.mcfunction
                            # execute if entity @s[x_rotation=-90..-89] run scoreboard players set @s pitch -90
                            # execute if entity @s[x_rotation=-89..-88] run scoreboard players set @s pitch -89

                # -78t-67.mcfunction
                # execute if entity @s[x_rotation=-78..-72] run function namespace:-78t-72
                # execute if entity @s[x_rotation=-72..-67] run function namespace:-72t-67

                    # -78t-72.mcfunction
                    # execute if entity @s[x_rotation=-78..-75] run function namespace:-78t-75
                    # execute if entity @s[x_rotation=-75..-72] run function namespace:-75t-72

                        # -78t-75.mcfunction
                        # execute if entity @s[x_rotation=-78..-76] run function namespace:-78t-76
                        # execute if entity @s[x_rotation=-76..-75] run function namespace:-76t-75

                            # -78t-76.mcfunction
                            # execute if entity @s[x_rotation=-78..-77] run scoreboard players set @s pitch -78
                            # execute if entity @s[x_rotation=-77..-76] run scoreboard players set @s pitch -77

            # -67t-45.mcfunction
            # execute if entity @s[x_rotation=-67..-56] run function namespace:-67t-56
            # execute if entity @s[x_rotation=-56..-45] run function namespace:-56t-45

        # -45t0.mcfunction
        # execute if entity @s[x_rotation=-45..-22] run function namespace:-45t-22
        # execute if entity @s[x_rotation=-22..0] run function namespace:-22t0

            # -45t-22.mcfunction
            # execute if entity @s[x_rotation=-45..-33] run function namespace:-45t-33
            # execute if entity @s[x_rotation=-33..-22] run function namespace:-33t-22

            # -22t0.mcfunction
            # execute if entity @s[x_rotation=-22..-11] run function namespace:-22t-11
            # execute if entity @s[x_rotation=-11..0] run function namespace:-11t0

    # 0t90.mcfunction
    # execute if entity @s[x_rotation=0..45] run function namespace:0t45
    # execute if entity @s[x_rotation=45..90] run function namespace:45t90

        # 0t45.mcfunction
        # execute if entity @s[x_rotation=0..23] run function namespace:0t23
        # execute if entity @s[x_rotation=23..45] run function namespace:23t45

        # 45t90.mcfunction
        # execute if entity @s[x_rotation=45..68] run function namespace:45t68
        # execute if entity @s[x_rotation=68..90] run function namespace:68t90


def branch(oldpair):

    # Make new function (e.g. -78t-76.mcfunction)
    with open(f'{working_directory}/{oldpair[0]}t{oldpair[1]}.mcfunction', 'x') as f:

        angles = split_angle(oldpair[0], oldpair[1])

        for pair in angles:
            # Difference of 1 (e.g. -78 and -77) (means end of a branch)
            if pair[0] - pair[1] == -1:
                f.write(f'execute if entity @s[x_rotation={pair[0]}..{pair[1]}] run scoreboard players set {player} {objective} {pair[0]}\n')

            else:
                f.write(f'execute if entity @s[x_rotation={pair[0]}..{pair[1]}] run function {namespace}:{pack_path}/{pair[0]}t{pair[1]}\n')

                branch(pair)



def split_angle(lower, upper):

    middle = lower + math.ceil((upper - lower) / 2)

    return ((lower, middle), (middle, upper))


# Debug split_angle
#while True:
    #print(split_angle(int(input('lower: ')), int(input('upper: '))))


# The name of the folder to generate all the files inside
FOLDER_NAME = 'get_pitch'

script_directory = os.path.dirname(__file__)
print('The parent directory of the script: ' + script_directory)

working_directory = os.path.join(script_directory, FOLDER_NAME)

if os.path.exists(working_directory):
    print('FAILED: First delete pre-existing function tree')
    exit()

os.mkdir(working_directory)



print(f'''
This script will generate a function tree (at {script_directory}/{FOLDER_NAME}) that stores the player's pitch (x rotation) to a score.
Normally, this can be done via an NBT check, but using a function tree with x_rotation selectors is more efficient.

Before generating the tree, it is important to understand that the player's rotation is stored as a Float value, whereas scoreboard values are stored as Integers.
Depending on how intermediate values (like 45.5) are rounded, the resultant scoreboard value may vary.

Choose the behavior that best suits your needs:

  1. Floor: Round down to nearest integer
  2. Ceiling: Round up to nearest integer
''')

behavior = ''
while behavior != 1 and behavior != 2:
    behavior = int(input('Select option (1 or 2): '))

namespace = ''
while namespace == '' or not namespace.isalnum():
    namespace = input('Namespace: ').lower()
    if not namespace.isalnum():
        print('\nNamespace must be alphanumeric!\n')

player = ''
while player == '':
    player = input('Player to store Rotation in (selector such as @s or a fake player name): ')

objective = ''
while objective == '':
    objective = input('Objective to store Rotation in: ')



pack_path = ''
while pack_path == '':
    pack_path = input(f'How do you want to execute the function tree? Complete the following: /function {namespace}:')



# Make main function exe.mcfunction
with open(f'{working_directory}/exe.mcfunction', 'x') as f:
    angles = split_angle(-90, 90)

    for pair in angles:
        f.write(f'execute if entity @s[x_rotation={pair[0]}..{pair[1]}] run function {namespace}:{pack_path}/{pair[0]}t{pair[1]}\n')

        branch(pair)

    f.write(f'execute if entity @s[x_rotation=90] run scoreboard players set {player} {objective} 90')



print(f'''Done! To use your function tree, have your player run /function {namespace}:exe''')

