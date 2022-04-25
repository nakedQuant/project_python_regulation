source /Users/hengxinliu/.zshrc
conda activate fdj
python -m flake8 --output-file flake8.txt
python -m junit_conversor flake8.txt flake8_junit.xml
python -m pytest tests/