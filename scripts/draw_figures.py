from pathlib import Path
from html import escape
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'assets/images'
D.mkdir(parents=True,exist_ok=True)
FIGS=[
('测试与证明的覆盖范围','观察到的样本，与带条件的全称结论',[
('有限测试','输入 0、1、2、100','这些样本得到预期结果；其余输入仍需理由。'),
('形式化命题','∀ n : Nat, n + 0 = n','全称量词覆盖该模型中的每个自然数。'),
('现实边界','规格、实现、运行环境','证明覆盖形式模型；部署对应关系仍要核查。')]),
('命题如何成为证据','下面三行是逻辑结构，不是自动求解配方',[
('合取 P ∧ Q','提供 P 的证据 + Q 的证据','两项都齐备，才能构造合取的证据。'),
('蕴含 P → Q','接收 P 的证据，返回 Q 的证据','这是一个转换方法；不是说 P 已经成立。'),
('全称 ∀ x, R x','给任意 x，构造 R x 的证据','x 必须任意，不能只挑一个方便的样本。')]),
('证明状态的逐步变化','例：从 P ∧ Q 证明 Q ∧ P',[
('起点','h : P ∧ Q  ⊢  Q ∧ P','左侧是可用假设，右侧是当前目标。'),
('拆目标','目标一：Q       目标二：P','构造合取需要两份证据；两个子目标都要完成。'),
('使用假设','h 的右分量证明 Q；左分量证明 P','所有目标关闭后，完整证明项还须被内核接受。')]),
('从源文件到检查结果','编辑器反馈与内核接受承担不同角色',[
('编辑与解析','文件、依赖、语法与名称','报错可能来自版本、导入或语法，未必来自逻辑。'),
('展开与构造','补隐式参数，执行策略，生成证明项','策略可以很复杂；其任务是提出可检查的证据。'),
('内核检查','检查证明项是否具有声明的类型','接受结果须结合公理依赖、占位与工具链审计。')]),
('合取交换的证据路线','同一逻辑任务可以有不同的语言写法',[
('输入','一份 h : P ∧ Q','其中包含 P 的证据和 Q 的证据。'),
('投影','取出 h 的 Q 分量，再取 P 分量','不引入新假设，也不需要枚举 P 和 Q 的内容。'),
('输出','重新组合为 Q ∧ P','交换的是证据的排列；结论与输入有明确对应。')]),
('重写有方向，也有位置','已知 h : a = b；目标 f a = f b',[
('已有等式','a = b','h 是相等的证据；不是命令式变量赋值。'),
('替换目标中的 a','f a = f b   →   f b = f b','此处沿 h 从左到右替换；反向重写需明确指定。'),
('自反性关闭','f b 与 f b 相同','两边可定义相等时可用 rfl / reflexivity。')]),
('归纳证明的两份工作','递归定义提供了递减的结构',[
('基础情形','证明 P 0','没有前驱，不使用归纳假设。'),
('归纳步骤','任意 n，假设 ih : P n，证明 P (n+1)','ih 只覆盖更小对象；不能拿当前目标当假设。'),
('全体自然数','由基础与保持性得到 ∀ n, P n','若要依赖另一个变量，可能先把它保持为任意值。')]),
('追加列表为何长度相加','对左边列表 xs 做结构归纳',[
('空列表','[] ++ ys = ys','长度结论化为 length ys = 0 + length ys。'),
('非空列表','(x :: xs) ++ ys = x :: (xs ++ ys)','新列表在递归结果前保留一个头元素 x。'),
('归纳假设','length (xs ++ ys) = length xs + length ys','把递归结果的长度换成已知式，再处理外层的 +1。')]),
('规格连接输入与输出','例：自然数余额 balance 中扣除 amount',[
('前置条件','amount ≤ balance','金额足够时，才可用扣款后的守恒式。'),
('实现','result = balance - amount','自然数减法在零处截断；不能当作整数减法。'),
('后置条件','result + amount = balance','这只是纯函数规格；并发、数据库和网络需另外建模。')]),
('自动化提出证据，内核检查证据','库中的定理可以减少重复构造',[
('定位问题','先看目标形状、类型、可用假设','搜索等式、排序或成员关系；不要只猜定理名字。'),
('调用库或策略','匹配定理参数，生成证明项','化简集合与导入会影响自动化行为。'),
('检查与维护','内核检查；回看假设及依赖','策略成功不是对自然语言问题或现实系统的包保。')]),
('验证编译器的保证位于何处','示意语义保持，不是 CompCert 的全部架构',[
('源程序','源语言形式语义中的行为','源程序本身是否满足业务规格，需要另一份论证。'),
('编译保持定理','在定理条件下连接源与目标的行为','须查看支持的语言、目标、未定义行为等具体条件。'),
('目标程序与运行','目标语义中的行为 → 实际执行','汇编、链接、运行库、硬件等边界仍须分别说明。')]),
('可复查的证明工程','每次修改都需要重新建立证据链',[
('固定输入','命题、定义、工具链、依赖版本','说明要证明什么，以及允许采用哪些假设。'),
('构造并检查','编写证明，运行编译，审计公理','AI 可建议策略；检查状态不能由文字宣称代替。'),
('修改与重建','规格或依赖变更 → 重新检查','保留日志和可复现命令，让他人能独立复查。')])]
for i,(title,sub,rows) in enumerate(FIGS,1):
 s=['<svg xmlns="http://www.w3.org/2000/svg" width="960" height="640" viewBox="0 0 960 640">','<rect width="960" height="640" fill="#f4f6f9"/>','<g font-family="Noto Sans CJK SC, sans-serif">',f'<text x="42" y="55" font-size="17" fill="#126d79">证明有据 / 图 {i:02}</text>',f'<text x="42" y="105" font-size="31" font-weight="bold" fill="#152c46">{escape(title)}</text>',f'<text x="42" y="143" font-size="19" fill="#536579">{escape(sub)}</text>']
 for j,(tag,expr,caption) in enumerate(rows):
  y=176+j*145
  s += [f'<rect x="40" y="{y}" width="880" height="124" rx="14" fill="white" stroke="#d4dde8"/>',f'<rect x="40" y="{y}" width="8" height="124" rx="3" fill="#13818b"/>',f'<text x="66" y="{y+29}" font-size="17" fill="#13727c">{j+1:02} / {escape(tag)}</text>',f'<text x="66" y="{y+66}" font-size="24" fill="#162e47">{escape(expr)}</text>',f'<text x="66" y="{y+101}" font-size="18" fill="#56687a">{escape(caption)}</text>']
  if j<2:s += [f'<path d="M480 {y+127} v14 m-5 -5 l5 5 5 -5" fill="none" stroke="#13818b" stroke-width="2"/>']
 s+=['</g></svg>']
 (D/f'fig-{i:02}.svg').write_text('\n'.join(s))
print('Generated',len(FIGS),'figures')
def canvas(title,subtitle):
 return ['<svg xmlns="http://www.w3.org/2000/svg" width="960" height="640" viewBox="0 0 960 640"><rect width="960" height="640" fill="#f4f6f9"/><g font-family="Noto Sans CJK SC, sans-serif">',f'<text x="40" y="64" font-size="30" font-weight="bold" fill="#152c46">{title}</text>',f'<text x="40" y="105" font-size="20" fill="#536579">{subtitle}</text>']
def box(s,x,y,w,h,label,color='#13818b'):
 s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="white" stroke="{color}" stroke-width="3"/><text x="{x+w/2}" y="{y+h/2+8}" text-anchor="middle" font-size="25" fill="{color}">{escape(label)}</text>')
def line(s,x1,y1,x2,y2):
 s.append(f'<path d="M{x1} {y1} L{x2} {y2}" stroke="#8394a5" stroke-width="3" fill="none"/>')
def txt(s,x,y,t,size=21):
 s.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="#354d62">{escape(t)}</text>')
def save(s,n):
 (D/f'fig-{n:02}.svg').write_text('\n'.join(s+['</g></svg>']))
s=canvas('图 05 / 把合取证据拆开，再按相反顺序组合','线条展示证据的来源；上下两份证据始终保留各自类型。')
box(s,60,165,210,90,'h : P ∧ Q')
box(s,375,165,190,90,'p : P');box(s,375,340,190,90,'q : Q','#b25b35')
box(s,680,340,210,90,'Q ∧ P')
line(s,270,190,375,190);line(s,270,225,375,385)
line(s,565,210,680,405);line(s,565,385,680,365)
txt(s,310,155,'左分量',18);txt(s,300,330,'右分量',18)
txt(s,60,510,'Lean：And.intro h.right h.left',24)
txt(s,60,558,'Rocq：先 destruct h，再 split；依次给出 Q 和 P。',22)
save(s,5)
s=canvas('图 07 / 归纳依靠基础与保持性','不能跳过 P 0，也不能把尚未证明的 P (n+1) 当作归纳假设。')
for j,t in enumerate(['P 0','P 1','P 2','P 3']):
 x=65+j*215;y=360-j*65;box(s,x,y,150,75,t)
 if j:line(s,x-65,y+102,x,y+40)
txt(s,65,485,'基础：建立 P 0',25)
txt(s,65,530,'保持性：对任意 n，从 P n 的证据构造 P (n+1) 的证据。',23)
txt(s,65,575,'台阶仅帮助理解；归纳步骤必须对任意 n 成立。',21)
save(s,7)
s=canvas('图 08 / 追加保留左列表的头，递归处理尾部','例：[a, b] ++ [c] = [a, b, c]；长度性质要推广到任意列表。')
for y,labels in [(170,['a','b','+','c']),(290,['a','b','c'])]:
 for j,v in enumerate(labels):box(s,70+j*145,y,110,70,v,'#b25b35' if v=='c' else '#13818b')
txt(s,680,215,'2 + 1',28);txt(s,680,335,'= 3',28)
line(s,350,245,350,280)
box(s,65,415,830,80,'length (xs ++ ys) = length xs + length ys')
txt(s,65,545,'归纳对象：xs；基础是 []，步骤是 x :: xs。',23)
txt(s,65,590,'头元素贡献 1；尾部长度由归纳假设连接到等式。',23)
save(s,8)
