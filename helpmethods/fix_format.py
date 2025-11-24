import csv

def fix_csv_with_brackets(input_path: str, output_path: str):
    with open(input_path, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile, delimiter=';')
        fixed_rows = []
        for row in reader:
            # Оборачиваем каждое значение в [ ]
            fixed_row = [f'[{col}]' for col in row]
            fixed_rows.append(fixed_row)

    with open(output_path, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile, delimiter=';', quoting=csv.QUOTE_NONE, escapechar='\\')
        writer.writerows(fixed_rows)

if __name__ == '__main__':
    input_file = 'csv/pristine.csv'
    output_file = 'csv/l1.csv'
    fix_csv_with_brackets(input_file, output_file)
    print(f"Файл сохранён как {output_file}")