# FindSimilar Laboratory

## Install

```commandline
git clone https://github.com/findsimilar/laboratory.git
cd laboratory
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Use with find-similar

### Use find-similar package from pypi

This is the easiest way. Just install find-similar from PyPi:
```commandline
pip install find-similar
```

### Use find-similar from disk

If you want to work with laboratory and find-similar package locally:
- clone find-similar source code
```commandline
git clone https://github.com/findsimilar/find-similar.git
```
- Uncomment this line `sys.path.append("../find-similar")` in the laboratory setting file (`settings.py`)
- Put correct path to your `find-similar` folder
- Install find-similar requirements (pip install -r ...) from `find-similar/requirements.txt`

## Easy start

- Confirm migrations
```
make migrate
```
- Run server
```
make server
```
- Run tests
```commandline
make test
```
- Check coverage
```commandline
make coverage
```
- Use linter
```commandline
make lint
```

## Management commands

### Get tokens from one text

Input:
```commandline
python manage.py tokenize_one "some text" "other text"
```

Output:
```commandline
Start
Get tokens for some text...
Done:
{'text', 'some'}
End
Start
Get tokens for other text...
Done:
{'text', 'other'}
End
```

### Get cos between two texts

Input:
```commandline
python manage.py compare_two "one" "two"
```

Output:
```commandline
Start
Get cos between "one" and "two"
Start
Get tokens for one...
Done:
{'one'}
End
Start
Get tokens for two...
Done:
{'two'}
End
Done:
0
End
```

### Example frequency analysis

Input:
```commandline
python manage.py example_frequency_analysis "mock"
```

Output:
```commandline
Start
Analyze "mock"...
Done:
(('mock', 2), ('example', 2), ('for', 2), ('tests', 2), ('this', 1), ('is', 1))
End
```

### Load training data

Input:
```commandline
python manage.py load_training_data 2x2 analysis/tests/data/2x2.xlsx 0
```

Output:
```commandline
Start
Loading data from "analysis/tests/data/2x2.xlsx"...
Done:
TrainingData object (None)
End
```

## FAQ

Empty yet