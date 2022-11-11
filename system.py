from utility import *
import candidate as c
import shotglass as sg

class System:
    def __init__(self):
        self.candidates = list()
        self.Shotglass = None

    def clean(self):
        res = input('Are you sure you would like to delete all stored data? (y/n) >> ')
        if res != 'y':
            print('System spared. Scrub not executed.\n')
            return
        candidates = file.listdir("candidates")
        [file.delete_dir(j_path("candidates", candidate)) if file.isdir(j_path("candidates", candidate)) else file.delete_file(j_path("candidates", candidate))  for candidate in candidates]
        self.clear()
        print('System scrubbed.\n')
        return

    def clear(self):
        self.candidates = list()
        if self.Shotglass != None: 
            del self.Shotglass
            self.Shotglass = None
        print('System cleared.\n')

    def load(self):
        candidates = file.listdir("candidates")
        for candidate in candidates:
            candidate = self.Candidate('', '', candidate)
        print()

    def cmd_Candidate(self, candidate: c.Candidate):
        print('What would you like to do with candidate', candidate.get_name() + '?')
        cmd = ''
        commands =  {'delete': ('', 'permanently delete candidate'),
                    'list titles': ('candidate.list_titles()', 'list titles associated with the candidate'),
                    'list keywords': ('candidate.list_keywords(input("Which title would you like to investigate? >> "))', 'list keywords associated with a candidate title'),
                    'add titles': ('candidate.request_titles()', 'add titles and title keywords to the candidate'),
                    'delete title': ('candidate.delete_title(input("Which title would you like to delete? >> "))', 'delete a title from the candidate'),
                    'list locations': ('candidate.list_locations()', 'list locations associated with candidate'),
                    'add locations': ('candidate.request_locations()', 'add locations to the candidate'),
                    'delete location': ('candidate.delete_location(input("Which location would you like to delete? >> "))', 'delete a location from the candidate'),
                    'get pay': ('candidate.get_pay_range()', 'get the pay range associated with the candidate'),
                    'change pay': ('candidate.request_pay_range()', 'change the pay range associated with the candidate'),
                    'get experience': ('candidate.get_years_experience()', 'get the years of experience associated with the candidate'),
                    'change experience': ('candidate.request_years_experience()', 'change the years of experience associated with the candidate'),
                    'get education': ('candidate.get_education()', 'get the education associated with the candidate'),
                    'change education': ('candidate.request_education()', 'change the education associated with the candidate'),
                    'resume': ('candidate.resume()', 'enters the Resume command line for resume changes'),
                    'shots': ('sg.shots(candidate)', 'starts shotglass data collection for the candidate'),
                    'done': ('', 'return to main command line')
                    }
        while cmd != 'done':
            print("Enter a Candidate command or type 'help'")
            cmd = input('>> ')
            if cmd == 'done':
                break
            if cmd == 'help':
                print('Candidate command line for candidate', candidate.get_name() + '. Use the commands below to get started:')
                [print('* %-16s - %s' % (command, commands[command][1])) for command in commands]
                print()
                continue
            if cmd == 'delete':
                if self.delete_Candidate(candidate): break
                else: continue
            if cmd not in commands:
                comp = closest(cmd, commands)
                if comp != None:
                    res = input("Unknown command. Did you mean '" + comp + "' (y/n)? >> ")
                    if res != 'y': print(); continue
                    cmd = comp
                else: print("Unknown command. Type 'help' for a list of commands.\n"); continue
            _locals = locals()
            exec(commands[cmd][0], globals(), _locals)
        print('Returning to main command line.\n')

    def Candidate(self, _firstname, _lastname, _fullname=None):
        candidate = c.Candidate(_firstname, _lastname)
        cname = _firstname.lower().replace(' ','_') + '_' + _lastname.lower().replace(' ','_') if _fullname == None else _fullname
        if file.pathexists(r_path(file.getcwd(), 'candidates', cname)):
            if not file.pathexists(r_path(file.getcwd(), 'candidates', cname, 'candidate.json')): return None
            candidate = load_obj(r_path(file.getcwd(), 'candidates', cname, 'candidate.json'), candidate)
            print('Candidate', candidate.get_name(), 'retrieved.\n')
        else:
            if _fullname != None: print('[!!!] ERR: Name assignment error.'); return None
            candidate.build_dir()
            print('Candidate', candidate.get_name(), 'created.\n')
        c_exists = False
        for ci in self.candidates:
            if ci.firstname == candidate.firstname and ci.lastname == candidate.lastname:
                c_exists = True
        if not c_exists: self.candidates.append(candidate)
        return candidate

    def new_Candidate(self, _firstname, _lastname):
        if self.candidate_exists(_firstname, _lastname):
            print('Candidate', _firstname, _lastname, 'already exists.')
            res = input('Would you like to override? (y/n) >> ')
            if res == 'y':
                cname = _firstname.lower().replace(' ','_') + '_' + _lastname.lower().replace(' ','_')
                file.delete_dir(j_path("candidates", cname)) if file.isdir(j_path("candidates", cname)) else file.delete_file(j_path("candidates", cname))
            else:
                print("Candidate preserved. Use command 'load candidate' to retrieve existing candidate.\n")
                return
        candidate = self.Candidate(_firstname, _lastname)
        candidate.request_titles()
        candidate.request_locations()
        candidate.request_pay_range()
        candidate.request_years_experience()
        candidate.request_education()
        candidate.generate_resume()
        print('New Candidate', candidate.get_name(), 'generated.')
        return candidate

    def find_Candidate(self, _firstname, _lastname):
        candidate = None
        for ci in self.candidates:
            if ci.firstname == _firstname and ci.lastname == _lastname:
                candidate = ci
        if candidate == None and not self.candidate_exists(_firstname, _lastname):
            comp = closest(_firstname + ' ' + _lastname, [c.firstname + ' ' + c.lastname for c in self.candidates])
            if comp != None:
                res = input('Candidate ' + _firstname + ' ' + _lastname + " does not exist. Did you mean '" + comp + "' (y/n)? >> ")
                if res == 'y': candidate = self.Candidate(comp.split(' ')[0], comp.split(' ')[1])
            if candidate == None:
                print()
                res = input('Unkown candidate. Would you like to create a new candidate? (y/n) >> ')
                if res == 'y': candidate = self.new_Candidate(_firstname, _lastname)
                else:
                    print("No candidate created. Use command 'new candidate' to create a new candidate.\n")
                    return None
        if candidate == None: candidate = self.Candidate(_firstname, _lastname)
        return candidate

    def load_Candidate(self, _firstname, _lastname):
        firstname = _firstname.lower().replace(' ','_')
        lastname = _lastname.lower().replace(' ','_')
        if firstname == "" and lastname == "" and len(self.candidates) == 1: candidate = self.candidates[0]
        else: candidate = self.find_Candidate(firstname, lastname)
        if candidate == None: return
        self.cmd_Candidate(candidate)

    def delete_Candidate(self, candidate: c.Candidate):
        res = input('Are you sure you would like to permanently delete candidate ' + candidate.get_name()  + '? (y/n) >> ')
        if res != 'y':
            print("Candidate", candidate.get_name(), 'spared.\n')
            return False
        cname = candidate.firstname + '_' + candidate.lastname
        file.delete_dir(j_path("candidates", cname)) if file.isdir(j_path("candidates", cname)) else file.delete_file(j_path("candidates", cname)) 
        self.candidates.remove(candidate)
        del candidate
        print('Candidate deleted.\n')
        return True

    def candidate_exists(self, _firstname, _lastname):
        cname = _firstname.lower().replace(' ','_') + '_' + _lastname.lower().replace(' ','_')
        if file.pathexists(r_path(file.getcwd(), 'candidates', cname)):
            return True
        else:
            return False

    def list_candidates(self):
        if len(self.candidates) == 0:
            print("No candidates loaded. Use command 'load' to load all candidates.\n")
            return
        print('Currently loaded candidates:')
        [print(candidate.get_name()) for candidate in self.candidates]
        print()
        
    def generate_shotglass(self, browser='Firefox', headless=True, browser_path=None, executable_path=None):
        self.Shotglass = sg.Shotglass(browser=browser, headless=headless, browser_path=browser_path, executable_path=executable_path)