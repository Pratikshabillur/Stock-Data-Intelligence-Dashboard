import re, pathlib

for f in ['main.py', 'data_collector.py', 'predictor.py', 'requirements.txt', 'index.html']:
    try:
        text = pathlib.Path(f).read_text(encoding='utf-8')
        cleaned = re.sub(r'<<<<<<< HEAD\n', '', text)
        cleaned = re.sub(r'\n=======\n.*?>>>>>>> [^\n]+', '', cleaned, flags=re.DOTALL)
        pathlib.Path(f).write_text(cleaned, encoding='utf-8')
        print('Fixed:', f)
    except FileNotFoundError:
        print('Not found:', f)