import PySimpleGUI as sg
import sys
import os
import subprocess
import json

# ================== Config ===================
config = {'repository': None}
config_path = 'config.json'
try:
    with open(config_path, 'r') as file:
        config = json.loads(file.read())
except:
    with open(config_path, 'w') as file:
        file.write(json.dumps(config))
# =============================================


# ==================== GUI ====================
sg.theme('DarkGrey13')

sync = sg.Frame('Sync', [[sg.Text('Commit message:')],
                        [sg.Input('', key='-COMMITMSG-'), sg.Button('Commit'), sg.Button('Push'), sg.Button('Pull')]])
branch = sg.Frame('Branch',[[sg.Text('Current branch:')],
                           [sg.Input('', key='-BRANCH-'), sg.Button('Checkout'), sg.Button('List'), sg.Button('New'), sg.Button('Delete')]])
merge_main = sg.Column([[sg.Text('Merges current branch into the one typed here:')], [sg.Input('master', key='-MERGE-'), sg.Button('Merge')]])
merge_strategy = sg.Column([[sg.Text('In case of conflicts prefer changes from:')], [sg.Radio('Current Branch', 1, default=False), sg.Radio('Other Branch', 1, default=True, key='-MERGESTRATEGY-')]])
merge = sg.Frame('Merge', [[merge_main, merge_strategy]])
repository = sg.Frame('Repository', [[sg.Input(None, key='-REPOSITORY-'), sg.FolderBrowse('Browse', target='-REPOSITORY-'), sg.Button('Open')]])
other = sg.Frame('Other', [[sg.Button('Clear'), sg.Button('Log')]])

layout = [[sg.Multiline(key='-OUTPUT-', autoscroll=True, expand_y=True, reroute_stdout=True, reroute_cprint=True, auto_refresh=True, enable_events=True, enter_submits=True, size=(40, 15)),
           sg.Button('Enter', visible=False, bind_return_key=True),
           sg.Column([[sync], [branch], [merge], [repository], [other]], vertical_alignment='top')]]

window = sg.Window('EasyGit', layout, finalize=True)
# =============================================


# =============== Functions ===================
def cmd(command, disp_cmd=True, disp_output=True, hb=False):
    global config
    if disp_cmd:
        print(command)
    result = subprocess.run(command, cwd=config['repository'], capture_output=True)
    if disp_output:
        for line in result.stdout.decode('utf8').split('\n'):
            if hb:
                print('----------------------------------------------')
            print(line)
    return result.stdout.decode('utf8')

def exec():
    command = window.Element('-OUTPUT-').get().split('\n')[-3]
    cmd(command, disp_cmd=False)

def commit():
    global window
    message = window.Element('-COMMITMSG-').get()
    cmd('git add --all')
    cmd(f'git commit -m "{message}"')

def pull():
    cmd('git pull')

def push():
    cmd('git push')

def new_branch():
    cmd('git branch -b ' + window.Element('-BRANCH-').get())
    cmd('git push --set-upstream origin')

def delete_branch():
    cmd('git branch -d' + window.Element('-BRANCH-').get())
    cmd('git push -d origin ' + window.Element('-BRANCH-').get())

def merge_branch():
    strategy = 'ours' if window.Element('-MERGESTRATEGY-').get() else 'theirs'
    cmd('git checkout ' + window.Element('-MERGE-').get())
    cmd('git merge ' + window.Element('-BRANCH-').get() + '-s recursive -X' + strategy)

def checkout_branch():
    cmd('git checkout ' + window.Element('-BRANCH-').get())

def current_branch():
    return [x for x in cmd('git branch', False, False).split('\n') if x.startswith('*')][0].replace('*', '').strip()

def branches():
    return cmd('git branch -a').replace('* ', '')

def open_repo():
    global config_path
    global config
    global window
    path = window.Element('-REPOSITORY-').get()
    config['repository'] = path
    with open(config_path, 'w') as file:
        file.write(json.dumps(config))
    print('cd ' + path)
    window.Element('-BRANCH-').update(value=current_branch())

def log():
    cmd('git log --oneline --all', hb=True)

def clear_console():
    window.Element('-OUTPUT-').update(value='')

# =============================================


# =============================================
if config['repository'] is not None:
    window.Element('-REPOSITORY-').update(value=config['repository'])
    open_repo()
# =============================================


event_handlers = {'Commit': commit,
                  'Push': push,
                  'Open': open_repo,
                  'Log' : log,
                  'Checkout': checkout_branch,
                  'List': branches,
                  'New': new_branch,
                  'Delete': delete_branch,
                  'Merge': merge_branch,
                  'Clear': clear_console,
                  'Enter': exec,}

while True:
    event, values = window.read()
    if event in event_handlers:
        event_handlers[event]()
    elif event == sg.WIN_CLOSED:
        break;
