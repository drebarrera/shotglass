import system as s
from utility import *

system = s.System()

config = open('config.txt', 'r')
CONFIGS = {line.replace(' ','').split('=')[0]: line.replace(' ','').split('=')[1] for line in config.read().split('\n')}
config.close()
BROWSER = 'Chrome' if CONFIGS['BROWSER'] == '' else CONFIGS['BROWSER']
BROWSER_PATH = None if CONFIGS['BROWSER_PATH'] == '' else CONFIGS['BROWSER_PATH']
BROWSER_HEADLESS = True if CONFIGS['BROWSER_HEADLESS'].lower() == 'true' else False
BROWSER_EXECUTABLE = None if CONFIGS['BROWSER_EXECUTABLE'] == '' else CONFIGS['BROWSER_EXECUTABLE']

system.generate_shotglass(browser=BROWSER, headless=BROWSER_HEADLESS, browser_path=BROWSER_PATH, executable_path=BROWSER_EXECUTABLE)

def config_shotglass():
    global BROWSER, BROWSER_PATH, BROWSER_HEADLESS, BROWSER_EXECUTABLE, CONFIGS
    print("Enter 'skip' to skip a config.")
    browser = input('Choose your browser >> ')
    if browser != 'skip': BROWSER = 'Chrome' if closest(browser, ['Chrome', 'Firefox']) == None else closest(browser, ['Chrome', 'Firefox'])
    else: browser = CONFIGS['BROWSER']
    browser_headless = input('Would you like to use headless mode (y/n) >> ')
    if browser_headless != 'skip': BROWSER_HEADLESS = True if browser_headless == 'y' else False
    else: browser_headless = CONFIGS['BROWSER_HEADLESS']
    browser_path = input('Declare a browser path or hit enter if browser is at a default location >> ')
    if browser_path != 'skip': BROWSER_PATH = None if browser_path == '' else browser_path
    else: browser_path = CONFIGS['BROWSER_PATH']
    browser_executable = input('Declare a driver executable path or hit enter if driver is on the system PATH >> ')
    if browser_executable != 'skip': BROWSER_EXECUTABLE = None if browser_executable == '' else browser_executable
    else: browser_executable = CONFIGS['BROWSER_EXECUTABLE']
    config = open('config.txt', 'w')
    CONFIGS = {'BROWSER': browser, 'BROWSER_PATH': browser_path, 'BROWSER_HEADLESS': 'True' if browser_headless == 'y' else 'False', 'BROWSER_EXECUTABLE': browser_executable}
    config.write(('\n').join([c+'='+CONFIGS[c] for c in CONFIGS]))
    config.close()
    system.generate_shotglass(browser=BROWSER, headless=BROWSER_HEADLESS, browser_path=BROWSER_PATH, executable_path=BROWSER_EXECUTABLE)
    print('Shotglass configured.\n')

if __name__ == "__main__":
    print('-' * 22 + 'SHOTGLASS' + '-' * 22)
    cmd = ''
    commands =  {'scrub': ('system.clean()', 'delete all stored data and clear system.'), 
                'load': ('system.load()', 'load all stored candidates'),
                'clear': ('system.clear()', 'clear all loaded candidates and system info'),
                'new candidate': ('system.new_Candidate(input("enter a first name >> "), input("enter a last name >> "))', 'generate a new candidate'),
                'load candidate': ('system.load_Candidate(input("enter a first name >> "), input("enter a last name >> "))', 'load a candidate'),
                'list candidates': ('system.list_candidates()', 'list all loaded candidates'),
                'config shotglass': ('config_shotglass()', 'configure the shotglass'),
                'exit': ('', 'exit the system')
                }

    while cmd != 'exit':
        print("Enter a command or type 'help'")
        cmd = input('>> ')
        if cmd == 'exit':
            break
        if cmd == 'help':
            print('Shotglass is a smart job search application. Use the commands below to get started:')
            [print('* %-16s - %s' % (command, commands[command][1])) for command in commands]
            print()
            continue
        if cmd not in commands:
            comp = closest(cmd, commands)
            if comp != None:
                res = input("Unknown command. Did you mean '" + comp + "' (y/n)? >> ")
                if res != 'y': print(); continue
                cmd = comp
            else: print("Unknown command. Type 'help' for a list of commands.\n"); continue
        exec(commands[cmd][0])

    print('System exit.\n')
    #
    #system.clean()
    #me = system.new_Candidate('Andres Enrique', 'Barrera')
    #
    #system.Shotglass.generate_browser()
    #system.Shotglass.crawl_linkedin('software developer', 'austin, texas', experience_level=2, passkey=('drebarrera@yahoo.com','Bac0npig'))
    #system.Shotglass.quit()