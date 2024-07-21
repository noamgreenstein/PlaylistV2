def gen_options(n, items):
    result = options_text
    for i in range(n):
        result += f'{i + 1}: {items[i]}'
    return result + enter_text


add_artist = 'add to favorite artists'
options_text = 'Options: \n'
enter_text = '\n\nEnter Option: '
input_text = gen_options(3, [add_artist, 'add to albums', 'rate a track'])
result_text = '{}: {}\n'
basic_keys = ['name', 'id']
basic_search = '1: search by artist\n2: search by album'
album_input_text = options_text + basic_search + enter_text
track_input_text = options_text + basic_search + '\n3: search by track name' + enter_text


def choose_from_list(item_list, desc, has_other):
    n = len(item_list)
    for i, item in enumerate(item_list):
        print(f'{i + 1}: {item}')
    if has_other:
        print(f'{n + 1}: Other')
    choice = int(input(f'Select {desc}: '))
    while not 0 < choice < n + 2:
        choice = int(input('Please choose valid option: '))
    return choice - 1
