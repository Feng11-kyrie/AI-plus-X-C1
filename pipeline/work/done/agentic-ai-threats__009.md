### 提取智能体工具 schema

#### 目标

攻击者试图提取每个智能体的工具 schema。虽然用户只能直接访问编排智能体，但他们可以明确要求编排智能体把查询转发给特定的智能体。图 5 表明，攻击者可以利用智能体之间的通信信道，把同一份利用载荷投递给每一个智能体。

*图 5. 提取智能体工具 schema。*

#### 攻击载荷说明

与提取智能体指令的攻击类似，表 4 中给出的每段提示词都面向一个特定的目标智能体。在 CrewAI 中，编排者把任务“[分派](https://docs.crewai.com/how-to/hierarchical-process)”给协作智能体；而在 AutoGen 中，编排者把任务“[移交](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/swarm.html)”给协作智能体。

#### 整合起来
