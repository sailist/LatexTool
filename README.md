# LatexTool
生成表格，绘制公式...等一系列工具（还未更新）

```bash
pip install textool
```

## Generate Table Perfectly

use directly in command line
```bash
x2t file.xlsx -f -c
```

use in python language
```python
from LatexTool.ast.tabel import *
tab = Tabel("filename",fill = True,center=True)
print(tab.to_tex())
```

where fill is strech table to \textwidth, and center is use \centering

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