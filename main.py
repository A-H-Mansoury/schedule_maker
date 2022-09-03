from Process import process
from Visualize import visualize

targets = """
    ۱۷۱۲۳۱۵
    ۱۷۱۴۳۰۳
    ۱۷۱۴۳۹۶
    ۱۷۱۶۳۱۰
    ۱۷۱۸۳۰۳
    ۱۷۳۲۲۰۴
    ۱۷۳۲۳۰۳
"""

name = 'temp'

golestan_html_path = './data/src.html'
is_drive  = False

if __name__ == '__main__':

    targets = targets.strip().split()
    process.validate_targets(targets)
    p = process(targets, golestan_html_path)
    process_results = p.get_results()
    process_data = p.get_data()
    visualize(name, process_data, process_results, is_drive)