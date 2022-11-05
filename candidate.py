from utility import *
import resume as r
import re

class Candidate:
    def __init__(self, _firstname, _lastname):
        self.firstname = _firstname.lower().replace(' ','_')
        self.lastname = _lastname.lower().replace(' ','_')
        self.titles = dict()
        self.locations = list()
        self.pay_range = list()
        self.years_experience = None
        self.education = None
        self.jobs = list()
        self.info_path = j_path('candidates', self.firstname + '_' + self.lastname)
        self.Resume = None

    def build_dir(self):
        file.makedir(self.info_path)
        file.makedir(j_path(self.info_path, 'resume'))
        file.makedir(j_path(self.info_path, 'cover letter'))
        with open(r_path(file.getcwd(), self.info_path, 'jobs.json'), 'w') as f: f.close()
        with open(r_path(file.getcwd(), self.info_path, 'resume.json'), 'w') as f: f.close()
        self.update_json()

    def request_titles(self):
        print("Enter all applicable job titles individually.")
        res, new_titles = None, list()
        while res != "":
            res = input('>> ')
            if res != "": 
                if res.lower() not in self.titles: self.titles[res.lower()] = list()
                new_titles.append(res.lower())
        for title in new_titles:
            print('Add keywords for the job title "' + title + '"')
            res = None
            while res != "":
                res = input('>> ')
                if res != "": [self.titles[title].append(x) for x in re.split(',\s*', res)]
            self.list_title(title)
        self.update_json()

    def list_titles(self):
        print("Candidate", self.get_name(), 'has the following titles:', [title for title in self.titles])

    def list_keywords(self, title):
        print("Candidate", self.get_name(), 'has the following keywords for title ', title + ':', [keyword for keyword in self.titles[title]])


    def delete_title(self, title):
        if title not in self.titles:
            comp = closest(title, self.titles)
            if comp != None:
                res = input("Unknown title. Did you mean '" + comp + "' (y/n)? >> ")
                if res != 'y': print(); return
                title = comp
            else: print("Title", title, "was not found for client", self.get_name(),"\n"); return
        del self.titles[title]
        print("Title deleted.\n")
        self.update_json()

    def request_locations(self):
        print("Enter all applicable job locations individually.")
        res = None
        while res != "":
            res = input('>> ')
            if res != "" and res.lower() not in self.titles: self.locations.append(res.lower())
        print('Locations listed for candidate', self.get_name() + ':', self.locations, '\n')
        self.update_json()

    def list_locations(self):
        print("Candidate", self.get_name(), 'has the following locations:', self.locations)

    def delete_location(self, location):
        if location not in self.locations:
            comp = closest(location, self.locations)
            if comp != None:
                res = input("Unknown location. Did you mean '" + comp + "' (y/n)? >> ")
                if res != 'y': print(); return
                location = comp
            else: print("Location", location, "was not found for client", self.get_name(),"\n"); return
        self.locations.remove(location)
        print("Location deleted.\n")
        self.update_json()

    def request_pay_range(self):
        print("Enter a pay range as a space delimeted minimum and maximum.")
        res = input(">> ")
        if res == '': return
        self.pay_range = [float(val.replace('$','').replace(',','')) for val in res.split(' ')]
        print("Pay Range for candidate", self.get_name() + ':', self.pay_range, '\n')
        self.update_json()

    def get_pay_range(self):
        print("Pay Range for candidate", self.get_name() + ':', self.pay_range, '\n')

    def request_years_experience(self):
        print("Enter the number of years experience in industry.")
        res = input(">> ")
        self.years_experience = res
        print("Years Experience in Industry for candidate", self.get_name() + ':', self.years_experience, '\n')
        self.update_json()

    def get_years_experience(self):
        print("Years Experience in Industry for candidate", self.get_name() + ':', self.years_experience, '\n')

    def request_education(self):
        print("Choose the highest level of education:\n  0) None\n  1) High School Diploma\n  2) Associate's Degree\n  3) Bachelor's Degree\n  4) Master's Degree\n  5) PhD Degree")
        res = input(">> ")
        ref = {0: "None", 1: "High School Diploma", 2: "Associate's Degree", 3: "Bachelor's Degree", 4: "Master's Degree", 5: "PhD Degree"}
        if res == '':
            return
        self.education = [ref[int(res)]]
        if int(res) > 1:
            res = input("What did the candidate receive their degree in? >> ")
            self.education.append(res)
            res = input("Is the candidate currently working on the degree (y/n)? >> ")
            if res == 'y': self.education.append(1)
            else: self.education.append(0)
        print("Education Completed for candidate", self.get_name() + ':', self.education, '\n')
        self.update_json()

    def get_education(self):
        print("Education Completed for candidate", self.get_name() + ':', self.education, '\n')

    def generate_resume(self):
        self.Resume = r.Resume(self.info_path)
        self.Resume.update_json()

    def resume(self):
        print()
        if self.Resume == None: self.Resume = load_obj(r_path(file.getcwd(), 'candidates', self.firstname + '_' + self.lastname, 'resume.json'), r.Resume(self.info_path))
        resume = self.Resume
        if resume.init == False:
            resume.new_resume(self.get_name())
        self.cmd_Resume()
        
    def cmd_Resume(self):
        resume = self.Resume
        print('What would you like to do with the Resume for candidate', self.get_name() + '?')
        cmd = ''
        commands =  {'list contact': ('resume.list_contact()', 'list contact information to be stated on the resume'),
                    'change contact': ('resume.request_contact()', 'change contact information to be stated on the resume'),
                    'list links': ('resume.list_links()', 'list links to be stated on the resume'),
                    'add links': ('resume.request_links()', 'add/change links to be stated on the resume'),
                    'delete link': ('resume.delete_link(input("Give the name of the link you would like to delete >> "))', 'delete a link from the resume'),
                    'list education': ('resume.list_education()', 'list the education experience to be stated on the resume'),
                    'add education': ('resume.request_education()', 'add education experience to be stated on the resume'),
                    'edit education': ('resume.edit_education()', 'change education experience to be stated on the resume'),
                    'delete education': ('resume.delete_education()', 'delete education experience from the resume'),
                    'list employment': ('resume.list_employment()', 'list the employment experience to be stated on the resume'),
                    'add employment': ('resume.request_employment()', 'add employment experience to be stated on the resume'),
                    'edit employment': ('resume.edit_employment()', 'change employment experience to be stated on the resume'),
                    'delete employment': ('resume.delete_employment()', 'delete employment experience from the resume'),
                    'list projects': ('resume.list_projects()', 'list the projects to be stated on the resume'),
                    'add projects': ('resume.request_projects()', 'add projects to be stated on the resume'),
                    'edit projects': ('resume.edit_projects()', 'change projects to be stated on the resume'),
                    'delete project': ('resume.delete_project()', 'delete a project from the resume'),
                    'list special': ('resume.list_special()', 'list the certifications/accomplishments to be stated on the resume'),
                    'add special': ('resume.request_special()', 'add certifications/accomplishments to be stated on the resume'),
                    'edit special': ('resume.edit_special()', 'change certifications/accomplishments to be stated on the resume'),
                    'delete special': ('resume.delete_special()', 'delete a certification/accomplishment from the resume'),
                    'build master': ('resume.build_resume()', 'generate master resume text file'),
                    'build custom': ('self.build_resume(self.title_keys())', 'generate a resume for a specific title'),
                    'analyze': ('self.analyze_resume()','analyze resume for spelling, grammar, and content suggestions'),
                    'done': ('', 'return to the Candidate command line')
                    }
        while cmd != 'done':
            print("Enter a Resume command or type 'help'")
            cmd = input('>> ')
            if cmd == 'done':
                break
            if cmd == 'help':
                print('Resume command line for candidate', self.get_name() + '. Use the commands below to get started:')
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
            _locals = locals()
            exec(commands[cmd][0], globals(), _locals)
        print('Returning to Candidate command line.\n')

    def build_resume(self, keywords):
        pass

    def analyze_resume(self):
        resume = self.Resume
        res = input('Would you like to perform a spelling and grammar check (y/n)? >> ')
        if res == 'y':
            print('Checking for spelling and grammar...\n')
            import language_tool_python as ltp
            lt = ltp.LanguageTool('en-US')
            for keyname in resume.__dict__:
                if keyname == "init" or keyname == "info_path" or keyname == "links" or keyname == "skills": continue
                if keyname == "education" or keyname == "employment" or keyname == "projects" or keyname == "special":
                    updated = False
                    base_list = list()
                    for d in resume.__dict__[keyname]:
                        for keykey in d:
                            if type(d[keykey]) is str and d[keykey] != None: 
                                res = self.check_language(d[keykey], lt)
                                if d[keykey] != res: d[keykey], updated = res, True
                        base_list.append(d)
                    if updated: setattr(resume, keyname, base_list)
                else:
                    if type(resume.__dict__[keyname]) is str and resume.__dict__[keyname] != None: 
                        res = self.check_language(resume.__dict__[keyname], lt)
                        if res != resume.__dict__[keyname]: setattr(resume, keyname, res)
            resume.build_resume(False)
            resume.update_skills()
            print('Resume updated with changes.\n')
        resume.check_skills()
        all_keywords = list()
        [all_keywords.extend([(k, title) for k in self.titles[title]]) for title in self.titles]
        self.check_keywords(resume.build_resume(False), all_keywords)
        print('Use the command line to implement the suggestions above.\n')

    def check_language(self, paragraph, lt):
        matches = lt.check(paragraph)
        replacements = list()
        for ind in range(len(matches)):
            print(matches[ind].message)
            print('Location:', matches[ind].offset, matches[ind].errorLength)
            print('{}\n{}'.format(matches[ind].context, ' ' * matches[ind].offsetInContext + '^' * matches[ind].errorLength))
            if len(matches[ind].replacements) == 1:
                res = input("Would you like to make the replacement '" + matches[ind].replacements[0] + "' (y/n) >> ")
                if res == 'y':
                    replacements.append((matches[ind].offset, matches[ind].errorLength, matches[ind].replacements[0]))
            else:
                print('Correct it by choosing one of the following or hit enter to skip:')
                [print(str(i + 1) + ') ' + matches[ind].replacements[i], end='  ') for i in range(len(matches[ind].replacements))]
                res = input('\n>> ')
                if res != '' and res.isdigit():
                    replacements.append((matches[ind].offset, matches[ind].errorLength, matches[ind].replacements[int(res) - 1]))
            print('_'*25)
        offset = 0
        for r in replacements:
            paragraph = str_rep(paragraph, r[2], r[0] + offset, r[0] + r[1] -1 + offset)
            offset += len(r[2]) - r[1]
        return paragraph

    def check_keywords(self, paragraph, keywords):
        paragraph = paragraph.lower()
        for k in keywords:
            if not(k[0], paragraph):
                print("Suggestion: Update the Resume to include candidate keyword '" + k[0] + "'.")

    def title_keys(self):
        print("Choose a title: " + (', ').join([title for title in self.titles]))
        res = input(">> ")
        if res != '' and res not in self.titles:
            comp = closest(res, self.titles)
            if comp != None:
                res = input("Unknown command. Did you mean '" + comp + "' (y/n)? >> ")
                if res != 'y': print(); return []
                res = comp
            else: print("Unknown title. Try again.\n"); return []
        return self.titles[res]

    def list_title(self, title):
        if title.lower() not in self.titles: print('[!!!] ERR:', title, 'not in job title list for candidate', self.get_name, '.'); return
        print('Job title', title.upper() + ':', self.titles[title.lower()], '\n')

    def update_json(self):
        update_json(r_path(self.info_path, 'candidate.json'), self, ['jobs','Resume'])

    def get_name(self):
        return ((' ').join([name[0].upper() + name[1:] for name in self.firstname.split('_') + self.lastname.split('_')]))