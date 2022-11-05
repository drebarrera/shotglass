from selenium import webdriver
from selenium.webdriver.common.by import By
import urllib.parse
import time
import job as j

class Shotglass:
    def __init__(self, browser='Firefox', headless=True, browser_path=None, executable_path=None):
        self.browser = browser
        self.headless = headless
        self.browser_path = browser_path
        self.executable_path = executable_path
        self.client = None
        self.Candidate = None
        self.jobs = list()

    def generate_browser(self):
        if self.browser == 'Firefox':
            firefoxOptions = webdriver.FirefoxOptions()
            if self.headless: firefoxOptions.headless = True
            if self.browser_path: firefoxOptions.binary_location = self.browser_path
            if self.executable_path: self.client = webdriver.Firefox(options=firefoxOptions, executable_path=self.executable_path)
            else: self.client = webdriver.Firefox(options=firefoxOptions)
        elif self.browser == 'Chrome':
            chromeOptions = webdriver.chrome.options.Options()
            if self.headless: chromeOptions.headless = True
            if self.browser_path: chromeOptions.binary_location = self.browser_path
            if self.executable_path: self.client = webdriver.Chrome(options=chromeOptions, executable_path=self.executable_path)
            else: self.client = webdriver.Chrome(options=chromeOptions)

    def shots(self, candidate):
        self.Candidate = candidate
        self.generate_browser()
        res = input("Choose a source or set of sources:\n  1) LinkedIn\n  2) ")

    def locate(self, method, identifier, max_search=500):
        st_locate, res = time.time_ns(), None
        while not res and time.time_ns() - st_locate < max_search * 1000000:
            try: res = self.client.find_element(method, identifier)
            except Exception as err: res = None
        if not res: print("[!!!] ERR: Identifier", identifier, "not found by", str(method), "method.")
        return res

    def locates(self, method, identifier, max_search=500):
        st_locate, res = time.time_ns(), None
        while not res and time.time_ns() - st_locate < max_search * 1000000:
            try: res = self.client.find_elements(method, identifier)
            except Exception as err: res = None
        if not res: print("[!!!] ERR: Identifier", identifier, "not found by", str(method), "method.")
        return res

    def crawl_linkedin(self, Candidate, title, location=None, experience_level=None, remote=False, passkey=None):
        client = self.client
        homepage = 'https://www.linkedin.com/'
        if passkey!=None:
            un = passkey[0]
            pw = passkey[1]
            client.get(homepage + 'login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
            for x in range(2):
                un_input = self.locate(By.CSS_SELECTOR, '[name="session_key"]')
                pw_input = self.locate(By.CSS_SELECTOR, '[name="session_password"]')
                submit = self.locate(By.CSS_SELECTOR, '[data-litms-control-urn="login-submit"]')
                if un_input and pw_input and submit:
                    un_input.send_keys(un)
                    pw_input.send_keys(pw)
                    submit.click()
                    break
        url = homepage + 'jobs/search/?keywords=' + urllib.parse.quote(title) + '&location=' + urllib.parse.quote(location) + '&f_JT=F'
        if experience_level: url += '&f_E=' + str(experience_level)
        if remote: url += '&f_WT=2'
        client.get(url)
        time.sleep(2)
        for x in range(2):
            results = self.locates(By.CLASS_NAME, 'jobs-search-results__list-item', 5000)
            if results:
                jobids = [result.get_attribute('data-occludable-job-id') for result in results]
                url = client.current_url.split('?currentJobId=')
                for jobid in jobids:
                    joburl = url[0] + '?currentJobId=' + jobid + '&' + url[1]
                    client.get(joburl)
                    time.sleep(2)
                    for x in range(2):
                        title = self.locate(By.CLASS_NAME, 'jobs-unified-top-card__job-title', 5000)
                        company = self.locate(By.CLASS_NAME, 'jobs-unified-top-card__company-name', 5000)
                        location = self.locate(By.CLASS_NAME, 'jobs-unified-top-card__bullet', 5000)
                        if title and company and location: 
                            job = j.Job()
                            job.title = title.text
                            job.site = 'LinkedIn'
                            job.id = jobid
                            job.company = company.text
                            job.location = location.text
                            self.jobs.append(job)
                            
                            break
                break

    def quit(self):
        self.client.quit()