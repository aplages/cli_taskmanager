import json
#import argparse

# ideia: usar um arquivo local para salvar o nome do arquivo anteriormente usado pelo usuario

def getFileName():
    with open('task_cli_settings.txt', 'r') as settings:
        settings.readline()
        filename = settings.readline()
        #print(filename)
        file = open(filename, 'a')
        file.close()
    return filename

def setFileName(new_name=''):
    with open('task_cli_settings.txt', 'w') as settings:
        if new_name == '': # task_list_cli.json
            settings.write(f'# Modificar esse arquivo pode mudar o funcionamento do programa\ntask_list_cli.json')
            file = open(new_name, 'a')
            file.close()
        elif '.json' in new_name:
            settings.write(f'# Modificar esse arquivo pode mudar o funcionamento do programa\n{new_name}')
            file = open(new_name, 'a')
            file.close()
        else:
            settings.write(f'# Modificar esse arquivo pode mudar o funcionamento do programa\n{new_name}.json')
            file = open(f'{new_name}.json', 'a')
            file.close()

def getID(file_name=''):
    if file_name == '':
        file_name = getFileName()
    else:
        setFileName(file_name)


    with open(file_name, 'r') as file:
        linhas = file.readlines()
        if (linhas != None) and (linhas != ''):
            id_number = json.loads(linhas[::-1][0])['id']
            return id_number
        else:
            return 1


def add(description, id=getID()+1, status='to-do', createdAt='', updatedAt=''):
    task = {
        'id': id,
        'description': description,
        'status': status,
        'createdAt': createdAt,
        'updatedAt': updatedAt
    }
    write(task)


def write(task_dict, first=False, file_name=''):
    if file_name == '':
        file_name = getFileName()
    else:
        setFileName(file_name)

    with open(file_name, 'a') as file:
        task_json = json.dumps(task_dict)
        
        file.write(f'{task_json}\n')


def list(file_name=''):
    if file_name == '':
        file_name = getFileName()
    else:
        setFileName(file_name)

    with open(file_name, 'r') as file:
        for linha in file.readlines():
            json_line = json.loads(linha)
            print(f'ID: {json_line['id']}       Task: {json_line['description']}       Status: {json_line['status']}\n')


def update(id, state='', file_name=''):
    if file_name == '':
        file_name = getFileName()
    else:
        setFileName(file_name)

    with open(file_name, 'r') as file:
        tasklist = []
        for linha in file.readlines():
            tasklist.append(json.loads(linha))
        
        if len(tasklist) > 0:
            for task in tasklist:
                #print(task['id'])
                if task['id'] == id:
                    #print(task['description'])
                    #print(task['status'])
                    if state == '':
                        if (task['status'] == 'to-do'):
                            task['status'] = 'in-progress'
                        elif task['status'] == 'in-progress':
                            task['status'] = 'done'
                    elif state == 'to-do':
                        task['status'] = 'to-do'
                    elif state == 'done':
                        task['status'] = 'done'
                    elif state == 'in-progress':
                        task['status'] = 'in-progress'
                    break

    with open(file_name, 'w') as file:
        for task in tasklist:
            task_json = json.dumps(task)
            file.write(f'{task_json}\n')


def delete(id, file_name=''):
    if file_name == '':
        file_name = getFileName()
    else:
        setFileName(file_name)

    with open(file_name, 'r') as file:
        tasklist = []
        for linha in file.readlines():
            tasklist.append(json.loads(linha))
        

        if len(tasklist) > 0 :
            for n in range(len(tasklist)):
                if tasklist[n]['id'] == id:
                    #print(tasklist[n]['id'])
                    ind = n
                    #print(ind) --> o índice será (ID - 1)
                    tasklist.remove(tasklist[n])
                    break
            
            for task in tasklist:
                if task['id'] > ind:
                    task['id'] -= 1

    with open(file_name, 'w') as file:
        for task in tasklist:
            task_json = json.dumps(task)
            file.write(f'{task_json}\n')
