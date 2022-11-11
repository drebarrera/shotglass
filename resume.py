from utility import *

class Resume:
    def __init__(self, info_path):
        self.init = False
        self.name = None
        self.title = None
        self.phone = None
        self.email = None
        self.location = None
        self.links = dict()
        self.education = list()
        self.employment = list()
        self.projects = list()
        self.special = list()
        self.skills = list()
        self.info_path = info_path

    def new_resume(self, name):
        self.name = name
        self.init = True
        self.request_contact()
        self.request_links()
        self.request_education()
        self.request_employment()
        self.request_projects()
        self.request_special()
        self.update_skills()

    def request_contact(self):
        print('Enter contact information to be displayed on the resume for candidate', self.name)
        res = input('Enter the phone number for candidate ' + self.name + ' >> ')
        if res != '': self.phone = res
        res = input('Enter the email for candidate ' + self.name + ' >> ')
        if res != '': self.email = res
        res = input('Enter the current location for candidate ' + self.name + ' >> ')
        if res != '': self.location = res
        print()
        self.update_json()

    def list_contact(self):
        print('Contact information for candidate', self.name)
        print('Phone:', self.phone)
        print('Email:', self.email)
        print('Location:', self.location)
        print()
    
    def request_links(self):
        print('Enter links to be displayed on the resume for candidate', self.name)
        link = None
        while link != '':
            link = input('Add a link for candidate ' + self.name + ' >> ')
            if link != '':
                name = input('Give a display name to the link ' + link + ' >> ')
                self.links[name] = link
        print()
        self.update_json()
    
    def list_links(self):
        print("Candidate", self.name, 'has the following links:', self.links,'\n')
    
    def delete_link(self, link):
        if link not in self.links:
            comp = closest(link, self.links)
            if comp != None:
                res = input("Unknown link. Did you mean '" + comp + "' (y/n)? >> ")
                if res != 'y': print(); return
                link = comp
            else: print("Link", link, "was not found for client", self.name,"\n"); return
        del self.links[link]
        self.update_json()
        print("Link deleted.\n")

    def request_education(self):
        print('Enter education experience to be displayed on the resume for candidate', self.name)
        while True:
            print('Enter a new diploma/degree:')
            res = input("Enter the title of the diploma/degree >> ")
            if res == '': break
            education = {'title': res}
            res = input("From what institution did/will the candidate receive their diploma/degree? >> ")
            education['institution'] = res
            res = input("When did/will the candidate receive their diploma/degree? >> ")
            education['date'] = res
            print("List relevant coursework:")
            education['coursework'] = list()
            while True:
                res = input(">> ")
                if res == '': break
                education['coursework'].append(res)
            self.education.append(education)
            print()
        print()
        self.update_json()

    def list_education(self):
        print("Candidate", self.name, 'has the following education listed:')
        [print(education) for education in self.education]
        print()

    def edit_education(self):
        print('Choose an education index to edit:')
        [print(str(ind + 1) + ')', self.education[ind]) for ind in range(len(self.education))]
        print(str(len(self.education) + 1) + ') New education experience')
        res = input('>> ')
        if res != '' and res.isdigit() and int(res) == len(self.education) + 1:
            self.request_education()
            print()
            return
        if res != '' and res.isdigit():
            ind = int(res) - 1
            print('Edit this diploma/degree:')
            res = input("Enter the title of the diploma/degree >> ")
            if res != '': self.education[ind]['title'] = res
            res = input("From what institution did/will the candidate receive their diploma/degree? >> ")
            if res != '': self.education[ind]['institution'] = res
            res = input("When did/will the candidate receive their diploma/degree? >> ")
            if res != '': self.education[ind]['date'] = res
            print("List relevant coursework:")
            self.education[ind]['coursework'] = list()
            while True:
                res = input(">> ")
                if res == '': break
                self.education[ind]['coursework'].append(res)
            self.update_json()
            print('Education updated.')
        print()

    def delete_education(self):
        print('Choose an education index to delete:')
        [print(str(ind + 1) + ')', self.education[ind]) for ind in range(len(self.education))]
        res = input('>> ')
        if res != '' and res.isdigit():
            del self.education[int(res) - 1]
            self.update_json()
            print('Education deleted.')
        print()

    def request_employment(self):
        print('Enter employment experience to be displayed on the resume for candidate', self.name)
        while True:
            print('Enter new employment history:')
            res = input("Enter the job title/position >> ")
            if res == '': break
            employment = {'position': res}
            res = input("What company is this job title associated with? >> ")
            employment['company'] = res
            res = input("Where was this position located? >> ")
            employment['location'] = res
            res = input("When did the candidate start this position? >> ")
            employment['start'] = res
            res = input("When did/will the candidate end this position (enter 'Current' if the position is currently held)? >> ")
            employment['end'] = res
            print("Enter a description of the position held:")
            employment['description'] = list()
            while True:
                res = input(">> ")
                if res == '': break
                employment['description'].append(res)
            print('Enter skills associated with this employment:')
            employment['skills'] = set()
            while True:
                res = input(">> ")
                if res == '': break
                employment['skills'].add(res)
            employment['skills'] = list(employment['skills'])
            self.employment.append(employment)
            print()
        print()
        self.update_json()
    
    def edit_employment(self):
        print('Choose an employment index to edit:')
        [print(str(ind + 1) + ')', self.employment[ind]) for ind in range(len(self.employment))]
        print(str(len(self.employment) + 1) + ') New employment experience')
        res = input('>> ')
        if res != '' and res.isdigit() and int(res) == len(self.employment) + 1:
            self.request_employment()
            print()
            return
        if res != '' and res.isdigit():
            ind = int(res) - 1
            print('Edit this employment:')
            res = input("Enter the job title/position >> ")
            if res != '': self.employment[ind]['position'] = res
            res = input("What company is this job title associated with? >> ")
            if res != '': self.employment[ind]['company'] = res
            res = input("Where was this position located? >> ")
            if res != '': self.employment[ind]['location'] = res
            res = input("When did the candidate start this position? >> ")
            if res != '': self.employment[ind]['start'] = res
            res = input("When did/will the candidate end this position (enter 'Current' if the position is currently held)? >> ")
            if res != '': self.employment[ind]['end'] = res
            print("Enter a description of the position held:")
            self.employment[ind]['description'] = list()
            while True:
                res = input(">> ")
                if res == '': break
                self.employment[ind]['description'].append(res)
            print('Add skills associated with this employment:')
            self.employment[ind]['skills'] = set(self.employment[ind]['skills'])
            while True:
                res = input(">> ")
                if res == '': break
                self.employment[ind]['skills'].add(res)
            self.employment[ind]['skills'] = list(self.employment[ind]['skills'])
            self.update_json()
            print('Employment updated.')
        print()

    def list_employment(self):
        print("Candidate", self.name, 'has the following employment listed:')
        [print(employment) for employment in self.employment]
        print()

    def delete_employment(self):
        print('Choose an employment index to delete:')
        [print(str(ind + 1) + ')', self.employment[ind]) for ind in range(len(self.employment))]
        res = input('>> ')
        if res != '' and res.isdigit():
            del self.employment[int(res) - 1]
            self.update_json()
            print('Employment deleted.')
        print()

    def request_projects(self):
        print('Enter project experience to be displayed on the resume for candidate', self.name)
        while True:
            print('Enter a new project:')
            res = input("Enter the project name >> ")
            if res == '': break
            project = {'name': res}
            res = input("What company/organization is this project associated with? >> ")
            project['association'] = res
            res = input("When did the project start? >> ")
            project['start'] = res
            res = input("When did/will the project end? >> ")
            project['end'] = res
            print("Enter a brief project description:")
            project['description'] = list()
            while True:
                res = input(">> ")
                if res == '': break
                project['description'].append(res)
            print('Enter skills associated with this project:')
            project['skills'] = set()
            while True:
                res = input(">> ")
                if res == '': break
                project['skills'].add(res)
            project['skills'] = list(project['skills'])
            self.projects.append(project)
            print()
        print()
        self.update_json()

    def edit_projects(self):
        print('Choose a project index to edit:')
        [print(str(ind + 1) + ')', self.projects[ind]) for ind in range(len(self.projects))]
        print(str(len(self.projects) + 1) + ') New project')
        res = input('>> ')
        if res != '' and res.isdigit() and int(res) == len(self.projects) + 1:
            self.request_projects()
            print()
            return
        if res != '' and res.isdigit():
            ind = int(res) - 1
            print('Edit this project:')
            res = input("Enter the project name >> ")
            if res != '': self.projects[ind]['name'] = res
            res = input("What company/organization is this project associated with? >> ")
            if res != '': self.projects[ind]['association'] = res
            res = input("When did the project start? >> ")
            if res != '': self.projects[ind]['start'] = res
            res = input("When did/will the project end? >> ")
            if res != '': self.projects[ind]['end'] = res
            print("Enter a brief project description:")
            self.projects[ind]['description'] = list()
            while True:
                res = input(">> ")
                if res == '': break
                self.projects[ind]['description'].append(res)
            print('Add skills associated with this project:')
            self.projects[ind]['skills'] = set(self.projects[ind]['skills'])
            while True:
                res = input(">> ")
                if res == '': break
                self.projects[ind]['skills'].add(res)
            self.projects[ind]['skills'] = list(self.projects[ind]['skills'])
            self.update_json()
            print('Project updated.')
        print()

    def list_projects(self):
        print("Candidate", self.name, 'has the following projects listed:')
        [print(project) for project in self.projects]
        print()

    def delete_project(self):
        print('Choose a project index to delete:')
        [print(str(ind + 1) + ')', self.projects[ind]) for ind in range(len(self.projects))]
        res = input('>> ')
        if res != '' and res.isdigit():
            del self.projects[int(res) - 1]
            self.update_json()
            print('Project deleted.')
        print()

    def request_special(self):
        print('Enter special certifications/accomplishments to be displayed on the resume for candidate', self.name)
        while True:
            print('Enter a new instance:')
            res = input("Enter the instance name >> ")
            if res == '': break
            special = {'name': res}
            res = input("When did the instance occur? >> ")
            special['date'] = res
            res = input("Would you like this instance to bypass job-specific filtering (y/n)? >> ")
            special['bypass_filter'] = True if res == 'y' else False
            print('Enter skills associated with this instance:')
            special['skills'] = set()
            while True:
                res = input(">> ")
                if res == '': break
                special['skills'].add(res)
            special['skills'] = list(special['skills'])
            self.special.append(special)
            print()
        print()
        self.update_json()

    def edit_special(self):
        print('Choose a certification/accomplishment index to edit:')
        [print(str(ind + 1) + ')', self.special[ind]) for ind in range(len(self.special))]
        print(str(len(self.special) + 1) + ') New certification/accomplishment')
        res = input('>> ')
        if res != '' and res.isdigit() and int(res) == len(self.special) + 1:
            self.request_special()
            print()
            return
        if res != '' and res.isdigit():
            ind = int(res) - 1
            print('Edit this instance:')
            res = input("Enter the instance name >> ")
            if res != '': self.special[ind]['name'] = res
            res = input("When did the instance occur? >> ")
            if res != '': self.special[ind]['date'] = res
            res = input("Would you like this instance to bypass job-specific filtering (y/n)? >> ")
            if res != '': self.special[ind]['bypass_filter'] = True if res == 'y' else False
            print('Enter skills associated with this instance:')
            self.special[ind]['skills'] = set(self.special[ind]['skills'])
            while True:
                res = input(">> ")
                if res == '': break
                self.special[ind]['skills'].add(res)
            self.special[ind]['skills'] = list(self.special[ind]['skills'])
            self.update_json()
            print('Certification/accomplishment updated.')
        print()

    def list_special(self):
        print("Candidate", self.name, 'has the following certifications/accomplishments listed:')
        [print(special) for special in self.special]
        print()

    def delete_special(self):
        print('Choose a certification/accomplishment index to delete:')
        [print(str(ind + 1) + ')', self.special[ind]) for ind in range(len(self.special))]
        res = input('>> ')
        if res != '' and res.isdigit():
            del self.special[int(res) - 1]
            self.update_json()
            print('Certification/accomplishment deleted.')
        print()

    def update_skills(self, relevance=dict(), update_json=True):
        skill_list = dict()
        for instance in self.employment + self.projects + self.special:
            for skill in instance['skills']:
                if skill not in skill_list and skill in relevance:  skill_list[skill] = relevance[skill]
                else: skill_list[skill] = 0
        self.skills = [k for k, v in sorted(skill_list.items(), key=lambda item: item[1], reverse=True)]
        if update_json: self.update_json()

    def check_skills(self, synonyms):
        for employment in self.employment:
            for skill in employment['skills']:
                if not key_in_str(skill, ( '').join(employment['description']), synonyms):
                    print("Suggestion: Update the Resume employment to include skill '" + skill + "' in the description for", employment['position'], 'at', employment['company'] + '.')
        for project in self.projects:
            for skill in project['skills']:
                if not key_in_str(skill, (' ').join(project['description']), synonyms):
                    print("Suggestion: Update the Resume projects to include skill '" + skill + "' in the description for", project['name'] + '.')

    def build_resume(self, load=True, update_json=True, update_skills=True):
        if update_skills: self.update_skills(update_json=update_json)
        resume = self.name.upper() + '\n'
        if self.title: resume += self.title + '\n'
        resume += ('Phone: {}\nEmail: {}\nLocation: {}\n\n').format(self.phone, self.email, self.location)
        for link in self.links: resume += link + ': ' + self.links[link] + '\n'
        resume += '\nEDUCATION'
        education_list = [self.education[date['ind']] for date in str_to_date([education['date'] if education['date'].lower() != 'current' else '3000' for education in self.education])]
        for education in education_list: 
            resume += ('\n{}\n{} | {}\n').format(education['title'], education['institution'], education['date'])
            if len(education['coursework']) > 0: resume += 'Relevant Coursework:\n'
            for coursework in education['coursework']: resume += ('- {}\n').format(coursework)
        resume += '\nWORK EXPERIENCE'
        employment_list = [self.employment[date['ind']] for date in str_to_date([employment['end'] if employment['end'].lower() != 'current' else '3000' for employment in self.employment], secondary_order=[len(employment['skills']) for employment in self.employment])]
        for employment in employment_list: 
            resume += ('\n{}\n{} | {}\n{} - {}\n').format(employment['position'], employment['company'], employment['location'], employment['start'], employment['end'])
            if len(employment['description']) > 1: 
                for description in employment['description']: resume += ('- {}\n').format(description)
            else: resume += employment['description'][0]
        resume += '\nRECENT PROJECTS'
        project_list = [self.projects[date['ind']] for date in str_to_date([project['end'] if project['end'].lower() != 'current' else '3000' for project in self.projects], secondary_order=[len(project['skills']) for project in self.projects])]
        for project in project_list: 
            resume += ('\n{} ({})\n{} - {}\n').format(project['name'], project['association'], project['start'], project['end'])
            if len(project['description']) > 1: 
                for description in project['description']: resume += ('- {}\n').format(description)
            else: resume += project['description'][0] + '\n'
        special_list = [self.special[date['ind']] for date in str_to_date([special['date'] if special['date'].lower() != 'current' else '3000' for special in self.special], secondary_order=[len(special['skills']) for special in self.special])]
        if len(special_list) > 0: resume += '\nCERTIFICATIONS/ACCOMPLISHMENTS\n'
        if len(special_list) > 0: resume += (' \u2022 ').join([('{} ({})').format(special['name'], special['date']) for special in special_list]) + '\n'
        resume += '\nRELEVANT SKILLS\n'
        resume += (', ').join(self.skills)
        f = open(r_path(file.getcwd(), self.info_path, 'resume', 'resume.txt'), 'w')
        f.write(resume)
        f.close()
        if load: 
            file.startfile(r_path(file.getcwd(), self.info_path, 'resume', 'resume.txt'))
            print('Resume generated.')
            print()
        return resume

    def update_json(self):
        return update_json(r_path(self.info_path, 'resume.json'), self)