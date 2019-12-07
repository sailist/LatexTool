# LatexTool
A series of tools to make it easier to generate table, create formula, insert figure...  

```bash
pip install textool
```

## Generate Table Perfectly

used directly in command line
```bash
x2t file.xlsx -f -c
```

used in python
```python
from LatexTool.ast.tabel import *
tab = Tabel("filename",fill = True,center=True)
print(tab.to_tex())
```

"fill" option is to choose whether strech table to \textwidth, and "center" is to use \centering environment.


## Quick Paste Figure

```bash
pst filename
```

Then the file will be saved as ./filename.png, and the filename will be copied in clipboard.


```bash
pst filename -f
```
Then the content of clipboard will be:
```bash
\begin{figure}[H]
   \centering
   \includegraphics[width=0.8\textwidth]{filename.png}
   \caption{filename}
   \label{fig:filename}
\end{figure}
```

## LaTeX formula Editor
Developed by using MathJax. 

![](./img/lfe.png)

[click this](https://sailist.github.io/LatexTool/latexEditor.html) 

## More
To be Continued...

