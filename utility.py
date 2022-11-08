import json
import filemanager as file
import difflib
import datetime
import re
import os

def j_path(*args):
    return os.path.join(*args)

def r_path(*args):
    return file.realpath(os.path.join(*args))

def update_json(filedir, dump_obj, exclude=[]):
    dict_obj = replicate_dict(dump_obj.__dict__)
    dict_obj = {dict_key:dict_obj[dict_key] for dict_key in dict_obj if dict_key not in exclude}
    for dict_key in dict_obj:
        try:
            json.dumps(dict_obj[dict_key])
        except:
            if type(dict_obj[dict_key]) == dict:
                dict_obj[dict_key] = {keyname: None for keyname in dict_obj[dict_key]}
            else:
                dict_obj[dict_key] = None
    serial_obj = json.dumps(dict_obj, indent=4)
    file.write_to_file(filedir, serial_obj)
    return serial_obj

def replicate_dict(dict_obj):
    dict_copy = dict()
    for keyname in dict_obj:
        dict_copy[keyname] = dict_obj[keyname]
    return dict_copy

def retrieve_vars_from_file(filedir, var_name):
    cmd = file.read_file(filedir)
    _locals = locals()
    exec(cmd, globals(), _locals)
    return _locals[var_name]
    
def load_obj(filedir, obj):
    json_data = file.read_json(filedir)
    for key_name in json_data:
        exec("obj." + key_name + " = json_data['" + key_name + "']")
    return obj

def closest(sample, population):
    if type(population) is dict:
        population = [pop for pop in population]
    similarity = sorted({p: difflib.SequenceMatcher(None, sample, p).ratio() for p in population}.items(), key=lambda item: item[1], reverse=True)
    if similarity[0][1] > 0.4: return similarity[0][0]
    return None

def str_rep(string, replacement, start, end):
    return string[:start] + replacement + string[end + 1:]

def str_to_date(dates, DATE_FORMAT='MM-DD-YY', secondary_order=None):
    date_dicts = dict()
    if secondary_order == None: secondary_order = [None] * len(dates)
    for ind in range(len(dates)):
        date = dates[ind]
        datedict = {'year':0, 'month':0, 'day':0, 'ind': ind, 's': secondary_order[ind]}
        months = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}
        if '/' in date: 
            date = date.split('/')
            if (len(date) == 2 and not (date[0].isdigit() and date[1].isdigit())) or (len(date) == 3 and not (date[0].isdigit() and date[1].isdigit() and date[2].isdigit())): dates[ind] = datedict
            if DATE_FORMAT == 'MM-DD-YY' and (len(date[0]) == 4 or int(date[0]) > 31):
                return str_to_date(dates, DATE_FORMAT='YY-MM-DD', secondary_order=secondary_order)
            elif DATE_FORMAT == 'MM-DD-YY' and int(date[0]) > 12:
                return str_to_date(dates, DATE_FORMAT='DD-MM-YY', secondary_order=secondary_order)
            elif DATE_FORMAT == 'MM-DD-YY' and len(date) == 2:
                datedict['year'], datedict['month'], datedict['day'] =  int(date[1]), int(date[0]), 0
            elif DATE_FORMAT == 'MM-DD-YY':
                datedict['year'], datedict['month'], datedict['day'] =  int(date[2]), int(date[0]), int(date[1])
            elif DATE_FORMAT == 'DD-MM-YY':
                datedict['year'], datedict['month'], datedict['day'] =  int(date[2]), int(date[1]), int(date[0])
            elif DATE_FORMAT == 'YY-MM-DD':
                datedict['year'], datedict['month'], datedict['day'] =  int(date[0]), int(date[1]), int(date[2])
            date_dicts[ind] = datedict
        elif '-' in date: 
            date = date.split('-')
            if not (date[0].isdigit() and date[1].isdigit() and date[2].isdigit()): dates[ind] = datedict
            if DATE_FORMAT == 'MM-DD-YY' and (len(date[0]) == 4 or int(date[0]) > 31):
                return str_to_date(dates, DATE_FORMAT='YY-MM-DD', secondary_order=secondary_order)
            elif DATE_FORMAT == 'MM-DD-YY' and int(date[0]) > 12:
                return str_to_date(dates, DATE_FORMAT='DD-MM-YY', secondary_order=secondary_order)
            elif DATE_FORMAT == 'MM-DD-YY' and len(date) == 2:
                datedict['year'], datedict['month'], datedict['day'] =  int(date[1]), int(date[0]), 0
            elif DATE_FORMAT == 'MM-DD-YY':
                datedict['year'], datedict['month'], datedict['day'] =  int(date[2]), int(date[0]), int(date[1])
            elif DATE_FORMAT == 'DD-MM-YY':
                datedict['year'], datedict['month'], datedict['day'] =  int(date[2]), int(date[1]), int(date[0])
            elif DATE_FORMAT == 'YY-MM-DD':
                datedict['year'], datedict['month'], datedict['day'] =  int(date[0]), int(date[1]), int(date[2])
            date_dicts[ind] = datedict
        else:
            date = date.replace('.','')
            date = re.split(', |,|\s', date)
            if (len(date) == 2 and not date[1].isdigit()) or (len(date) == 3 and not (date[1].isdigit() and date[2].isdigit())): dates[ind] = datedict
            if len(date) == 3: datedict['year'], datedict['month'], datedict['day'] = int(date[2]), months[closest(date[0], months)], int(date[1])
            elif len(date) == 2: datedict['year'], datedict['month'], datedict['day'] = int(date[1]), months[closest(date[0], months)], 0
            elif len(date) == 1 and date[0].isdigit(): datedict['year'], datedict['month'], datedict['day'] = int(date[0]), 0, 0
            date_dicts[ind] = datedict
    curr_year = datetime.date.today().year
    curr_year_abbrv = curr_year % 1000
    date_list = list()
    for date_dict_key in date_dicts:
        d = date_dicts[date_dict_key]
        if d['year'] < 100 and curr_year_abbrv > d['year']: d['year'] =  (curr_year // 100) * 100 + d['year']
        elif d['year'] < 100: d['year'] =  (curr_year // 100 - 1) * 100 + d['year']
        date_list.append(d)
    for i in range(len(date_list)):
        sorting_complete = True
        for j in range(len(date_list) - i - 1):
            d1 = date_list[j]
            d2 = date_list[j + 1]
            if d2['year'] > d1['year'] or (d2['year'] == d1['year'] and d2['month'] > d1['month']) or (d2['year'] == d1['year'] and d2['month'] == d1['month'] and d2['day'] > d1['day']) or (d2['year'] == d1['year'] and d2['month'] == d1['month'] and d2['day'] == d1['day'] and d1['s'] != None and d2['s'] > d1['s']):
                date_list[j], date_list[j+1] = d2, d1
                sorting_complete = False
        if sorting_complete: break
    return date_list
        
def key_in_str(sample, population, synonyms=dict()):
    sample = sample.lower()
    population = population.lower()
    if sample in synonyms:
        for s in synonyms[sample]:
            r_str = '\s+|/' if '-' in s else '\s+|/|-'
            if len(s) <= 3: p = re.split(r_str, multi_replace(population, '.;,[]()', ''))
            else: p = population
            if s.lower() in p:
                return True
        return False
    r_str = '\s+|/' if '-' in sample else '\s+|/|-'
    if len(sample) <= 3: p = re.split('\s+|/|-', multi_replace(population, '.;,[]()', ''))
    else: p = population
    if sample in p:
        return True
    return False

def multi_replace(s, replace, replacement):
    for r in replace:
        s = s.replace(r, replacement)
    return s

def str_date_compare(date1, date2):
    pass