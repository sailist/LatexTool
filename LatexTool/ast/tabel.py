import xlrd,re
from pylatex import Tabular,MultiColumn,MultiRow,Table as TexTable,Center,NoEscape


re_endcom = re.compile("%$")
re_cline = re.compile(r"(\\cline{[^}]*})")

class Tabel:
    def __init__(self, xfile:[xlrd.sheet,str,xlrd.Book], sheet_flag:[int,str]=0,space_num = 4,**kwargs):
        self.space = " "*space_num

        if isinstance(xfile,str):
            excel = xlrd.open_workbook("test.xlsx")
            if isinstance(sheet_flag,int):
                self.sheet = excel.sheet_by_index(sheet_flag)  # Open the first tab
            elif isinstance(sheet_flag,str):
                self.sheet = excel.sheet_by_name(sheet_flag)
        elif isinstance(xfile,xlrd.sheet):
            self.sheet = xfile
        elif isinstance(xfile,xlrd.Book):
            excel = xfile
            self.sheet = excel.sheet_by_index(sheet_flag)
            if isinstance(sheet_flag,int):
                self.sheet = excel.sheet_by_index(sheet_flag)  # Open the first tab
            elif isinstance(sheet_flag,str):
                self.sheet = excel.sheet_by_name(sheet_flag)

        self.params = kwargs

        self.merge_cells = self.sheet.merged_cells
        self._summary()
        self._initial_var()


    def _initial_var(self):
        self.params.setdefault("center",True) # 中心
        self.params.setdefault("fill",True) # 全满
        self.params.setdefault("position","H") # Float 参数

    def _summary(self):
        self.shape = self.sheet.nrows,self.sheet.ncols

        col_max_lens = [0] * self.sheet.ncols
        for i in range(self.sheet.nrows):
            for j in range(self.sheet.ncols):
                col_max_lens[j] = max(col_max_lens[j],len(self.cell(i,j)))
        self.col_max_lens = col_max_lens

    def in_merge_cell(self,i,j):
        for index,mc in enumerate(self.merge_cells):
            if mc[0] == i and mc[2] == j:
                return 0,index # 起始点
            if mc[0]<i<mc[1] and mc[2] == j:
                return 1,index # 非起始点，但在同一列
            if mc[0] == i and mc[2]<j<mc[3]:
                return 2,index # 非起始点，但在同一行
            if mc[0]<i<mc[1] and mc[2]<j<mc[3]:
                return 3,index
        return -1,-1
    def cell(self,i,j):
        return NoEscape(self.sheet.cell_value(i,j))

    def ismultirow(self, index):
        res = self.sheet.merged_cells[index][1] - self.sheet.merged_cells[index][0]
        return  res> 1,res

    def ismulticol(self,index):
        res = self.sheet.merged_cells[index][3]-self.sheet.merged_cells[index][2]
        return  res > 1,res

    def cacu_col_ratio(self):
        col_max_lens = [min(i,10) for i in self.col_max_lens]
        ratio = [i/sum(col_max_lens) for i in col_max_lens]
        return ratio

    def _create_tabular(self):

        if self.params["fill"]:
            ratios = self.cacu_col_ratio()
            param = "|".join([rf"p{{{r:.2f}\tablewidth}}<{{\centering}}" for r in ratios])
            param = f"|{param}|"
        else:
            param = "|"+"|".join(["c"]*self.sheet.ncols)+"|"
        return Tabular(param)

    def _extract_range(self,all_range,extract):
        '''
        :param range: [[range_l,range_r]]
        :param extract: [r_l,r_r]
        :return:
        '''
        res = []
        for r in all_range:
            if extract[0]>r[0] and extract[1]<r[1]:
                res.append([r[0],extract[0]])
                res.append([extract[1],r[1]])
            elif extract[0] == r[0] and extract[1]<r[1]:
                res.append([extract[1],r[1]])
            else:
                res.append(r)
        return res

    def to_tex(self):

        tab = self._create_tabular()
        tab.add_hline()
        for i in range(self.sheet.nrows):
            line = []
            merge_set = set()
            for j in range(self.sheet.ncols):
                res,mindex = self.in_merge_cell(i,j)

                if res == -1:
                    line.append(self.cell(i,j))
                else:
                    merge_set.add(mindex)
                    cres, cnum = self.ismulticol(mindex)
                    rres, rnum = self.ismultirow(mindex)
                    if res == 0:
                        if cres:
                            if rres:
                                line.append(MultiColumn(cnum,
                                                        align='c|',
                                                        data=MultiRow(rnum,data=self.cell(i,j))))
                            else:
                                line.append(MultiColumn(cnum,
                                                        align='c|',
                                                        data=self.cell(i,j)))
                        else:
                            line.append(MultiRow(rnum,
                                                 data=self.cell(i,j)))
                    elif res == 1: # 不同行同列
                        if cres and rres:
                            line.append(MultiColumn(cnum,
                                                    align="c|",
                                                    data=""))
                        else:
                            line.append("")
                    elif res == 2: # 不同列同行
                        pass

            tab.add_row(line)

            all_range = [[0,self.sheet.ncols]]
            for mi in merge_set:
                merge_range = self.sheet.merged_cells[mi]
                if merge_range[1]-merge_range[0]>1 and merge_range[1]-i>1:
                    all_range = self._extract_range(all_range,merge_range[2:4])

            if all_range[0][0] == 0 and all_range[0][1] == self.sheet.ncols:
                tab.add_hline()
            else:
                for r in all_range:
                    tab.add_hline(r[0]+1,r[1])

        table = TexTable(position=self.params["position"])
        table.append(tab)

        res = table
        if self.params["center"]:
            c = Center()
            c.append(NoEscape(r"% \newlength\tablewidth % if haven't define the length 'tablewidth'"))
            c.append(
                NoEscape(
                    rf"\setlength\tablewidth{{\dimexpr (\textwidth -{2*self.sheet.ncols}\tabcolsep)}}"))
            c.append(table)
            res = c

        return self._format_tex(res.dumps())

    def _format_tex(self,tex):
        tex_line = tex.split("\n")

        tab_level = 0
        res = []
        for tex in tex_line:
            tex = re.sub(re_endcom,"",tex)
            if len(tex.strip()) == 0:
                continue
            if tex.startswith(r"\begin"):
                tex = self.space*tab_level+tex
                tab_level+=1
            elif tex.startswith(r"\end"):
                tab_level-=1
                tex = self.space * tab_level + tex
            else:
                tex = self.space * tab_level + tex

            res.append(tex)
        res = "\n".join(res)
        res = re.sub(re_cline,lambda x:x.group(1).replace(" ","").replace("\n",""),res)
        return res

