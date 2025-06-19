import argparse
import csv
from tabulate import tabulate
from typing import List, Dict, Union

def read_csv(file_path: str) -> List[Dict[str, str]]:
    """Чтение csv-файла."""
    with open(file_path, mode='r', encoding='utf-8') as file:
        return list(csv.DictReader(file))

def apply_filter(data: List[Dict[str, str]], condition: str) -> List[Dict[str, str]]:
    if not condition:
        return data
    
    operators = {'>', '<', '='}
    op = next((o for o in operators if o in condition), None)
    if not op:
        raise ValueError(f"Invalid condition format: {condition}")
    
    column, value = condition.split(op, 1)
    column = column.strip()
    value = value.strip()
    
    try:
        # Пробуем числовое сравнение
        value_float = float(value)
        return [
            row for row in data 
            if _compare(float(row[column]), value_float, op)
        ]
    except ValueError:
        #Вернёмся к сравнению строк
        return [
            row for row in data 
            if _compare(row[column], value, op)
        ]

def _compare(a, b, op: str) -> bool:
    if op == '=':
        return a == b
    elif op == '>':
        return a > b
    elif op == '<':
        return a < b
    raise ValueError(f"Unknown operator: {op}")

def apply_aggregation(data: List[Dict[str, str]], agg_spec: str) -> Dict[str, float]:
    if not agg_spec:
        return {}
    
    column, operation = agg_spec.split('=', 1)
    column = column.strip()
    operation = operation.strip()
    
    try:
        values = [float(row[column]) for row in data]
    except ValueError:
        raise ValueError(f"Cannot aggregate non-numeric column: {column}")
    
    if operation == 'avg':
        result = sum(values) / len(values)
    elif operation == 'min':
        result = min(values)
    elif operation == 'max':
        result = max(values)
    else:
        raise ValueError(f"Unknown operation: {operation}")
    
    return {operation: result}

def main():
    parser = argparse.ArgumentParser(description='Process CSV files.')
    parser.add_argument('--file', required=True, help='Path to CSV file')
    parser.add_argument('--where', help='Filter condition (e.g. "rating>4.5")')
    parser.add_argument('--aggregate', help='Aggregation spec (e.g. "rating=avg")')
    
    args = parser.parse_args()
    
    data = read_csv(args.file)
    
    if args.where:
        data = apply_filter(data, args.where)
        
    if args.aggregate:
        result = apply_aggregation(data, args.aggregate)
        print(tabulate([result], headers='keys', tablefmt='grid'))
    else:
        print(tabulate(data, headers='keys', tablefmt='grid'))

if __name__ == '__main__':
    main()
