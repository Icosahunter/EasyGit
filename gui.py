import PySimpleGUI as sg

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
