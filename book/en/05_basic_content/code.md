(code)=
# Code Blocks

Code blocks are fundamental in science: they show computational formulas, analysis scripts, and step-by-step procedures.

## Syntax highlighting

Add the language after the backticks:

````md
```python
import numpy as np

data = np.array([3.2, 4.1, 3.8, 4.5, 3.9])
mean = np.mean(data)
print(f"Mean: {mean:.2f}")
```
````

Result:

```python
import numpy as np

data = np.array([3.2, 4.1, 3.8, 4.5, 3.9])
mean = np.mean(data)
print(f"Mean: {mean:.2f}")
```

## Line numbers

Use the `{code-block}` directive with `:linenos:` to show line numbers. This option does not work inside a normal block written as ```` ```python ````; in that case it is interpreted as one more line of code.

````md
```{code-block} python
:linenos:

def calculate_std(data):
    n = len(data)
    mean = sum(data) / n
    variance = sum((x - mean) ** 2 for x in data) / n
    return variance ** 0.5
```
````

Result:

```{code-block} python
:linenos:

def calculate_std(data):
    n = len(data)
    mean = sum(data) / n
    variance = sum((x - mean) ** 2 for x in data) / n
    return variance ** 0.5
```

## Highlight specific lines

Use `:emphasize-lines:` inside `{code-block}` to highlight specific lines:

````md
```{code-block} python
:emphasize-lines: 3

def read_data(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()  # This line will be highlighted
    return [float(l.strip()) for l in lines]
```
````

Result:

```{code-block} python
:emphasize-lines: 3

def read_data(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    return [float(l.strip()) for l in lines]
```

## Other languages

Highlighting works with many languages:

```bash
# Bash example
curl -O https://example.com/data.csv
head -5 data.csv
```

```sql
-- SQL example
SELECT name, grade
FROM students
WHERE grade >= 5.0
ORDER BY grade DESC;
```

## Common languages in science


The following table summarizes the main elements of this section.

**Table. Common languages in science.**

| Language | When to use it |
|----------|---------------|
| `python` | Data analysis, numerical computing |
| `r` | Statistics, biostatistics |
| `matlab` | Engineering, signal processing |
| `sql` | Database queries |
| `bash` | Task automation |
| `json` / `yaml` | Configuration files |

```{tip}
This template includes `sphinx-copybutton`: a **Copy** button appears in the corner of each code block. Readers can copy code with one click.
```
