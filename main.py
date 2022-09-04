from Process import process
from Visualize import visualize

import argparse
import sys

def parse_args():
    p = argparse.ArgumentParser(description='Schedule Maker')
    p.add_argument('-t', '--targets', metavar='targets', type=str, help="a multiline string of course_ids")
    p.add_argument('-n', '--name', metavar='name', type=str, help="a random name")
    
    p.add_argument('-i', '--is_drive', metavar='is_drive', action=argparse.BooleanOptionalAction , help="whether save results in google drive or not")
    
    if len(sys.argv) <= 1:
        sys.argv.append('--help')
    args = p.parse_args()
    print(args)
    globals().update(vars(args))
    
golestan_html_path = './data/src.html'


if __name__ == '__main__':
    parse_args()
    targets = targets.strip().split()
    process.validate_targets(targets)
    p = process(targets, golestan_html_path)
    process_results = p.get_results()
    process_data = p.get_data()
    visualize(name, process_data, process_results, is_drive)