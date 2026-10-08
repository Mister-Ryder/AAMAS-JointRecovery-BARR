# Joint Recovery：问题模型、解析筛选与伪代码

对每条候选窗口 `v=(s_v,a_v,b_v,e_v)` 选择或放弃完整窗口，权重
$w_v=e_v-b_v>0$。同一卫星或同一天线上的两个窗口，按开始时刻排序后，
若后一窗口开始减前一窗口结束小于对应资源的间隔要求，则形成冲突边。
间隔恰好等于该资源要求时，该资源不产生冲突。

$$\max_{x\in\{0,1\}^{|V|}}\sum_v w_vx_v,
\qquad x_u+x_v\le1\quad(\{u,v\}\in E).$$

固定可行 incumbent $S$，对外部集合 $A$ 中的独立子集 $T$，定义
$B_v=N(v)\cap S$、$B(T)=\bigcup_{v\in T}B_v$。恢复后的解为
$S'=(S\setminus B(T))\cup T$，增益为

$$g_S(T)=W(T)-W(B(T)).$$

令 $d_v=W(B_v)-w_v$。对不冲突的两个外部点：

$$g_S(\{a,b\})=W(B_a\cap B_b)-d_a-d_b,
\qquad U_{ab}=\min(W(B_a),W(B_b))-d_a-d_b\ge g_S(\{a,b\}).$$

若全部 $d_v\ge0$，无共享阻塞点的 pair 增益必不为正。这是二跳共享阻塞枚举的覆盖条件。
完整扫描、全部单点增益非正且没有正见证时，返回本状态的至多二点插入零证书。
partial 或 seed 截断的零见证仅记录已扫描结果。

对扩展外部点的冲突 clique 分区 $\mathcal C$，令
$h_b=|\{C\in\mathcal C:N(b)\cap C\ne\varnothing\}|$，并令
$r_v=w_v-\sum_{b\in B_v}\lfloor w_b/h_b\rfloor$。安全上界为

$$U(A)=\sum_{C\in\mathcal C}\max(0,\max_{v\in C}r_v).$$

一般 backbone 的消元表示为：给定可行外部点选择 $T$，每个受影响二分分量 $C$
返回 $\operatorname{MWIS}(G[C\setminus N(T)])$，将其响应作为外部变量上的因子。
在候选 B 的 singleton backbone 中，每个已选阻塞点 $b$ 的响应为
$w_b\mathbf1[N(b)\cap T=\varnothing]$。原始外部冲突边仍作为硬约束。

```text
Algorithm 1  Pair-fusion population search
Initialize population P, historical incumbent S*, global deadline
while deadline remains:
    advance local search for each member; offer each state to archive
    if warmup/stagnation/cooldown/credit conditions do not hold: continue
    choose elite or rotating target
    if eligible fourth gate: fuse elite with farthest member; descend fused state
    if the exact state has a cached complete zero certificate:
        apply eligible fused-state population feedback; continue
    (T, gain, completion) <- Algorithm 2
    cache state only when completion supplies a zero certificate
    if gain > 0:
        verify S'=(S\B(T)) union T; offer S' to archive immediately
        S' <- Algorithm 3(S,T,S',event_deadline)
        verify S'; offer to archive; update local state and population
    charge the whole event to the umbrella budget
return historical feasible incumbent S*
```

```text
Algorithm 2  Shared-blocker scout
Compute all outsider deficits and retain positive singleton witnesses
Build sorted, flat selected-blocker lists; verify maintained weights
Rotate the all-outsider seed order for this event
for each seed a and outsider b sharing a selected blocker, counted once:
    if U_ab <= 0 or a and b conflict: continue
    gain <- weight of exact blocker-list intersection - d_a - d_b
    retain the highest positive singleton/pair witness, with fixed tie breaks
on deadline: retain the feasible lower-bound witness; mark partial
on complete coverage and all deficits nonnegative: mark complete <=2
if additionally no positive witness: mark complete zero certificate
return witness, gain and completion flags
```

```text
Algorithm 3  Positive-seed structured refinement
Mark blockers already paid by the verified seed
Expand through these blockers; rank by unpaid marginal reward; retain negatives
Compute clique allocation upper bound U and feasible sketch lower bound
Keep the better verified witness
if U exceeds the retained gain and time remains:
    induce all affected backbone components and outsiders as a full-boundary Kernel
    compile response factors; perform bounded-width elimination
    if unresolved and time remains: bounded branch or feasible recovery
    lift and retain only a feasible candidate exceeding the current witness
on timeout/size limit: keep the already verified positive witness
return retained candidate
```

证书邻域的一个整数例子：三个互不相邻的已选点权重均为 3；三个互不相邻的外部点权重
均为 4，阻塞集合分别为 `{u,v}`、`v,w`、`w,u`。每个单点增益为 −2，每个 pair
增益为 −1，三个外部点联合增益为 3。这里至多二点零证书的定义与三点交换相区分。

完整参数、计时规则和代码位置见 [ALGORITHM.md](ALGORITHM.md)。
