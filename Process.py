from itertools import combinations
import re
from unidecode import unidecode

from pandas import read_html
from tqdm.autonotebook import tqdm

from Custom_Data import custom_data

import concurrent.futures

class process:

    targets = []
    results = []
    regex = [
        '^%s\(.\): (.*) (\d{2}:\d{2})-(\d{2}:\d{2}) %s: (.*)$' % ('درس' , 'مکان'),
        '^%s\(.\): (.*) (\d{2}:\d{2})-(\d{2}:\d{2})$' % 'درس',
        #'^%s\(.\): (.*) (\d{2}:\d{2})-(\d{2}:\d{2}) %s: (.*)$' % ('حل تمرين' , 'مکان'),
        #'^%s\(.\): (.*) (\d{2}:\d{2})-(\d{2}:\d{2})$' % 'حل تمرين',
        '%s\(\d+_(\d{4}\.\d{2}\.\d{2})\) %s : (\d{2}:\d{2})-(\d{2}:\d{2})' % ('امتحان', 'ساعت'),
        '%s\((\d{4}\.\d{2}\.\d{2})\) %s : (\d{2}:\d{2})-(\d{2}:\d{2})' % ('امتحان عملي', 'ساعت'),
        #'^%s\(.\): (.*) (\d{2}:\d{2})-(\d{2}:\d{2}) %s$' % ('درس', 'هفته فرد'),
        #'^%s\(.\): (.*) (\d{2}:\d{2})-(\d{2}:\d{2}) %s$' % ('درس', 'هفته زوج'),
    ]
    def __init__(self, targets, golestan_html_path):
    
        bar = tqdm(total=100, desc='Process')

        self.__read_data(golestan_html_path)
        
        targets = list(map(unidecode,  targets))
                
        for target in targets:
            if len(target) == 7:
                self.__add_all_groups_of_course_to_targets(target)
            elif len(target) == 10:
                self.targets.append(target)
            else:
                raise Exception('input targets are invalid! They must be either 10 or 7 character long. %s' % target)
        
        bar.update(2)
        self.__reduce_data_to_targets()
        bar.update(2)
        self.__extract_course_timestamps()
        bar.update(30)
        self.__find_compatible_courses()
        bar.update(64)

    def get_results(self):
        return self.results
    
    def get_data(self):
        return self.data
    
    @staticmethod
    def validate_targets(targets):
        for target in targets:
            if not (re.match('^\d{7}$', target) or re.match('^\d{7}_\d{2}$', target)):
                raise ValueError('target <<%s>> is wrong. please fix it and run again.')


    def __read_data(self, golestan_html_path):
        try:
            lst = read_html(golestan_html_path, header=0, flavor = 'bs4', encoding = 'utf-8')
            if len(lst) != 1:
                raise Exception('golestan_html contains more than one table. make sure you click <<table view>> in 110 report!')
                
        except Exception as e:
            print('please double check golestan_html_path!')
            raise e

        self.data = lst[0]


    def __add_all_groups_of_course_to_targets(self, target):
        regex = '\A%s_..$\Z' % target
        temp = self.data['شماره و گروه درس']
        temp = temp.loc[temp.str.contains(regex)].to_list()
        self.targets.extend(temp)

    def __reduce_data_to_targets(self):
        tmp = self.data.loc[self.data['شماره و گروه درس'].isin(self.targets)]
        self.data = []
        self.data = tmp

    def __extract_course_timestamps(self):

        self.data['container'] = [[] for _ in range(len(self.data))]

        for i, record in enumerate(self.data['زمان و مكان ارائه/ امتحان']):

            if type(record) != str:
                print('\nthere isn\'t any datetime information')
                continue

            record = record.split('<BR>')

            for subrecord in record:

                subrecord = subrecord.strip().replace('  ', ' ')

                if subrecord == '':
                    continue

                func = lambda x: re.search(x, subrecord)

                subrecord = list(map(func, self.regex))

                indexes = [k for k, val in enumerate(subrecord) if val != None]

                if indexes == []:
                    #print('there is unsupported course in your schedule!')
                    continue
                else:
                    index = indexes[0]

                self.data.loc[self.data.index[i], 'container'].append(
                    custom_data(index, *subrecord[index].groups())
                )

                    

    def count_individual_courses(self, y):
        return len(
            set(x[:-3] if len(x) == 10 else x for x in y)
        )
    
    def process_targets(self, comb_i):

        def check_combination_time_overlap(comb):
            for i, j in combinations(comb, 2):
                a = self.data.loc[self.data['شماره و گروه درس']==i,'container'].to_list()
                b = self.data.loc[self.data['شماره و گروه درس']==j, 'container'].to_list() 
                lst = a[0]+ b[0]
                for k, h in combinations(lst, 2):
                    if custom_data.time_overlap(k, h):
                        return False
            return True
        
        if self.count_individual_courses(comb_i) != self.num_unique:
            return None        
        if check_combination_time_overlap(comb_i):
            return comb_i

    def __find_compatible_courses(self):
        self.num_unique =  self.count_individual_courses(self.targets)

        with concurrent.futures.ProcessPoolExecutor(8) as exe:
            for _ in exe.map(self.process_targets, combinations(self.targets, self.num_unique)):
                if _ != None:
                    self.results.append(_)
