# LatexTool
生成表格，绘制公式...等一系列工具（还未更新）


## 生成表格

```bash
pip install x2t
```
use directly in clt
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