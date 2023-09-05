# Schedule Maker

## Introduction

**Schedule Maker** is a Python script that helps you organize and visualize your course schedule using data from Golestan, the student information system at IUT (Isfahan University of Technology). This tool allows you to customize your course selection and generate a visual representation of your schedule.

## How to Use

Follow these simple steps to get started:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/A-H-Mansoury/schedule_maker.git
    ```

2. **Navigate to the cloned folder:**

    ```bash
    cd schedule_maker
    ```

3. **Install the required Python packages from `requirements.txt`:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Customize your course selection by editing the `targets` list in `main.py`. Add or remove course IDs according to your preferences.**

5. **Run the main script:**

    ```bash
    python main.py
    ```

## Customizing Data

To update the default data for your schedule, follow these steps:

1. **Visit the Golestan 110 report page.**

2. **Click the "نمایش جدولی" (View Table) button.**

3. **Save the page as an HTML file.**

4. **Set the `golestan_html_path` variable in `main.py` to the path of the saved HTML file.**

## Example

Here's an example of how to configure the `main.py` script:

```python
from Process import process
from Visualize import visualize

targets = [
    '۱۷۱۴۳۰۳_۰۲',
    '۱۷۱۶۴۲۴_۰۱',
    '۱۷۱۶۴۳۵_۰۱',
    '۱۷۱۶۳۱۵_۰۱',
    '۱۷۳۲۳۰۸_۰۱',
    '۱۷۱۴۳۰۴_۰۲', 
]

name = 'main'
golestan_html_path = './data/src.html'

if __name__ == '__main__':
    p = process(targets, golestan_html_path)
    process_results = p.get_results()
    process_data = p.get_data()
    visualize(name, process_data, process_results)
```


## Credits
This project is maintained by [@A-H-Mansoury](https://github.com/A-H-Mansoury).

## License
This project is licensed under the [MIT License](LICENSE).
