# Thebe + Binder: Live Code

**Thebe** allows readers to run Python code from the web version of the book. In this project it connects to a **remote Binder kernel**.

```{warning}
Thebe is an **HTML-only** feature. It is not available in PDF export.
```

```{warning}
This feature is **optional** and requires additional configuration of a Jupyter server or Binder. You do not need it for the basic TeachBook setup.
```

## How does it work?

1. Click the **"Live Code"** button below.
2. Binder starts a remote environment (this may take a few seconds the first time).
3. Code cells become editable and executable — try it!

---

## Try it: executable code

Click the button to activate interactive mode. Then you can edit and run the cells.

```{thebe-button}
```

````{div} full-width
```{code-block} python
:class: thebe

import numpy as np

# Create an array from 0 to 2*pi
x = np.linspace(0, 2 * np.pi, 100)

# Calculate sine and cosine
y_sin = np.sin(x)
y_cos = np.cos(x)

print(f"Mean of sine: {np.mean(y_sin):.4f}")
print(f"Mean of cosine: {np.mean(y_cos):.4f}")
print(f"Max value of sine: {np.max(y_sin):.4f}")
print("It works! Try changing np.sin to another function.")
```
````

````{div} full-width
```{code-block} python
:class: thebe

import matplotlib.pyplot as plt
import numpy as np

# Modifiable parameters
frequency = 2    # Hz
amplitude = 1.0  # Scale
phase = 0        # Radians

t = np.linspace(0, 2*np.pi, 200)
signal = amplitude * np.sin(frequency * t + phase)

plt.figure(figsize=(8, 3))
plt.plot(t, signal, 'b-', linewidth=2, label=f'{amplitude}*sin({frequency}t + {phase})')
plt.title('Interactive Sine Wave')
plt.xlabel('Time (rad)')
plt.ylabel('Amplitude')
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()
```
````

---

## How to add this to your pages

### 1. Activation button

Add this directive where you want the "Live Code" button to appear:

````md
```{thebe-button}
```
````

### 2. Executable cell

Use `code-block` with the `thebe` class:

````md
```{code-block} python
:class: thebe

import numpy as np
print("Hello from the browser!")
```
````

You may also find examples written with the `{code-cell}` directive:

````md
```{code-cell} python
import numpy as np
print(np.sqrt(16))
```
````

That syntax turns the block into an executable cell when Thebe is configured.

### 3. `_config.yml` configuration

Your `_config.yml` must include the `sphinx-thebe` extension:

```yaml
sphinx:
  extra_extensions:
    - sphinx_thebe
  config:
    thebe_config:
      always_load: false
      repository_url: https://github.com/binder-examples/jupyter-stacks-datascience
      repository_branch: master
```

This configuration uses **Thebe + Binder**, meaning the code runs in a remote Binder environment.

```{admonition} Simpler alternative
:class: tip
If you don't want to set up Thebe, you can use **Google Colab**. Upload your notebook to Colab and share the link in your TeachBook. Students can run the code in the cloud with no installation.
```

```{admonition} Summary
Thebe is powerful but optional. Start with static content and notebooks, and consider Thebe when your students need to experiment with code in real time.
```
