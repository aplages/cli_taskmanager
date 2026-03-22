import json
import argparse
from datetime import datetime

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
        #print(linhas)
        if (linhas != None) and (linhas != '') and (linhas != []):
            id_number = json.loads(linhas[::-1][0])['id']
            return id_number
        else:
            return 0


def add(description_list: list): # status='to-do', id=None):

    description = ''
    space = False
    for w in description_list:
        if not space:
            description += str(w)
            space = True
        else:
            description += f' {w}'

    #if id == None:     --> caso eu queira dar opcao de escolher o ID...
    id = int(getID()+1)
    createdAt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    updatedAt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f'Adding <\033[36m{description}\033[m - ID: \033[36m{id}\033[m> to tasklist')
    task = {
        'id': id,
        'description': description,
        'status': 'to-do',
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


def list(file_name='', task_status=''):

    if file_name == '':
        file_name = getFileName()
    else:
        setFileName(file_name)

    with open(file_name, 'r') as file:
        if task_status == '':
            print(f'Listing tasks:\n')
            for linha in file.readlines():
                json_line = json.loads(linha)

                
                if json_line['status'] == 'to-do':
                    print(f'ID: {json_line['id']}       Task: {json_line['description']}       Status: \033[31m{json_line['status']}\033[m\n')
                elif json_line['status'] == 'in-progress':
                    print(f'ID: {json_line['id']}       Task: {json_line['description']}       Status: \033[33m{json_line['status']}\033[m\n')
                elif json_line['status'] == 'done':
                    print(f'ID: {json_line['id']}       Task: {json_line['description']}       Status: \033[32m{json_line['status']}\033[m\n')
            
        elif task_status=='to-do':
            print(f'Listing \033[31mto-do\033[m tasks:\n')
            for linha in file.readlines():
                json_line = json.loads(linha)

                if json_line['status'] == 'to-do':
                    print(f'ID: {json_line['id']}       Task: {json_line['description']}       Status: \033[31m{json_line['status']}\033[m\n')

        elif task_status=='in-progress':
            print(f'Listing \033[33min-progress\033[m tasks:\n')
            for linha in file.readlines():
                json_line = json.loads(linha)

                if json_line['status'] == 'in-progress':
                    print(f'ID: {json_line['id']}       Task: {json_line['description']}       Status: \033[33m{json_line['status']}\033[m\n')

        elif task_status=='done':
            print(f'Listing \033[32mdone\033[m tasks:\n')
            for linha in file.readlines():
                json_line = json.loads(linha)

                if json_line['status'] == 'done':
                    print(f'ID: {json_line['id']}       Task: {json_line['description']}       Status: \033[32m{json_line['status']}\033[m\n')


            #print(f'ID: {json_line['id']}       Task: {json_line['description']}       Status: {json_line['status']}\n')


def update(id, state='', file_name=''):
    if file_name == '':
        file_name = getFileName()
    else:
        setFileName(file_name)

    updata = False
    with open(file_name, 'r') as file:
        tasklist = []
        for linha in file.readlines():
            tasklist.append(json.loads(linha))
        
        if (len(tasklist) > 0) and (len(tasklist) >= id > 0):
            for task in tasklist:
                #print(task['id'])
                if task['id'] == id:
                    #print(task['description'])
                    #print(task['status'])
                    if state == '':
                        if (task['status'] == 'to-do'):
                            task['status'] = 'in-progress'
                            print(f'Updating <ID: \033[36m{id}\033[m : \033[36m{task['description']}\033[m> --> \033[33min-progress\033[m')
                            task['updatedAt'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                        elif task['status'] == 'in-progress':
                            task['status'] = 'done'
                            print(f'Updating <ID: \033[36m{id}\033[m : \033[36m{task['description']}\033[m> --> \033[32mdone\033[m')
                            task['updatedAt'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        elif task['status'] == 'done':
                            print('Task already \033[32mdone\033[m')

                    elif state == 'to-do':
                        task['status'] = 'to-do'
                        print(f'Updating <ID: \033[36m{id}\033[m : \033[36m{task['description']}\033[m> --> \033[31mto-do\033[m')
                        task['updatedAt'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    elif state == 'done':
                        task['status'] = 'done'
                        print(f'Updating <ID: \033[36m{id}\033[m : \033[36m{task['description']}\033[m> --> \033[32mdone\033[m')
                        task['updatedAt'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    elif state == 'in-progress':
                        task['status'] = 'in-progress'
                        print(f'Updating <ID: \033[36m{id}\033[m : \033[36m{task['description']}\033[m> --> \033[33min-progress\033[m')
                        task['updatedAt'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    updata = True
                    
                    break

        elif not (len(tasklist) >= id > 0):
            print('ID não existe.')
        elif not (len(tasklist) > 0):
            print('Tasklist vazia.')
    if updata:
        with open(file_name, 'w') as file:
            for task in tasklist:
                task_json = json.dumps(task)
                file.write(f'{task_json}\n')


def delete(id, file_name=''):
    if file_name == '':
        file_name = getFileName()
    else:
        setFileName(file_name)

    deleta = False

    with open(file_name, 'r') as file:
        tasklist = []
        for linha in file.readlines():
            tasklist.append(json.loads(linha))
        

        if (len(tasklist) > 0) and (len(tasklist) >= id > 0):
            for n in range(len(tasklist)):
                if tasklist[n]['id'] == id:
                    #print(tasklist[n]['id'])
                    ind = n
                    #print(ind) --> o índice será (ID - 1)
                    print(f'Deleting <ID: \033[36m{id}\033[m : \033[36m{tasklist[n]['description']}\033[m> from tasklist')
                    tasklist.remove(tasklist[n])
                    deleta = True
                    break
        elif not (len(tasklist) >= id > 0):
            print('ID não existe.')
        elif not (len(tasklist) > 0):
            print('Tasklist vazia.')
            
            for task in tasklist:
                if task['id'] > ind:
                    task['id'] -= 1
    if deleta:
        
        for task in tasklist:
            if task['id'] >= id:
                task['id'] -= 1

        with open(file_name, 'w') as file:
            for task in tasklist:
                task_json = json.dumps(task)
                file.write(f'{task_json}\n')
        


## Program:

parser = argparse.ArgumentParser(description='A taskmanager program via CLI')

subparsers = parser.add_subparsers(dest='command', required=True, help='Available arguments')

##

parser_add = subparsers.add_parser('add', help='adds to the list')
parser_add.add_argument('task_description', help='The task needs a name/description', nargs='*')

##

parser_delete = subparsers.add_parser('delete', help='deletes given ID from the tasklist')
parser_delete.add_argument('id', help='The ID from the task you wish to delete', type=int)


##

parser_update = subparsers.add_parser('update', help="updates the the given ID task's progress")
parser_update.add_argument('id', help='The ID from the task you wish to update', type=int)

update_group = parser_update.add_mutually_exclusive_group()
update_group.add_argument('-todo', '-td', action='store_true')
update_group.add_argument('-inprogress', '-inp', action='store_true')
update_group.add_argument('-done', action='store_true')

##

parser_list = subparsers.add_parser('list', help='shows the tasklist')
list_group = parser_list.add_mutually_exclusive_group()

list_group.add_argument('-todo', '-td', action='store_true', help='Shows the tasks that are in a \033[31m<to-do>\033[m status')
list_group.add_argument('-inprogress', '-inp', action='store_true', help='Shows the tasks that are in a \033[33m<in-progress>\033[m status')
list_group.add_argument('-done', action='store_true', help='Shows the tasks that are in a \033[32m<done>\033[m status')

##


args = parser.parse_args()

print()
#print(args)

#print(args.command)
#print()


if args.command == 'add':
    add(args.task_description)

elif args.command == 'delete':
    delete(args.id)


elif args.command == 'update':
    if args.todo:
        update(args.id, state='to-do')

    elif args.inprogress:
        update(args.id, state='in-progress')

    elif args.done:
        update(args.id, state='done')

    else:
        update(args.id)

elif args.command == 'list':
    if args.todo:
        list(task_status='to-do')

    elif args.inprogress:
        list(task_status='in-progress')

    elif args.done:
        list(task_status='done')

    else:
        list()

print()