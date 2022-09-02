from Process import process
from Visualize import visualize
targets = ['۱۷۱۲۳۱۵', '۱۷۱۲۳۰۱']
name = 'mamad'
golestan_html_path = './data/src.html'

if __name__ == '__main__':
    p = process(targets, golestan_html_path)
    process_results = p.get_results()
    print(process_results)
    process_data = p.get_data()

    visualize(name, process_data, process_results)


