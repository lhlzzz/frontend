# AGENTS.md - web

## Mission

`web` 是 Hermes 的前端控制智能体。它负责：

- 启动、停止和定位独立系统的浏览器入口
- Social Media OS 的统一观察界面
- Financial OS 与 Social Media OS 的受控前端运行边界

`web` 不负责交易、平台数据库、知识库或外部账号动作。

## Current Gateway Boundary

受 `web` 控制的系统保持独立：

| System | Public port | Responsibility |
|---|---:|---|
| Financial OS | `3000` | Financial agents and investment workflows |
| Social Media OS | `4000` | Six social-media agent observation entries |

Social Media OS contains:

- `douyin`：抖音
- `xiaohongshu`：小红书
- `kuaishou`：快手
- `x`：X
- `shipinghao`：视频号
- `xianyu`：闲鱼

浏览器不得直连平台数据库或内部 adapter。Social Media OS 的浏览器入口为
`http://localhost:4000`; Financial OS 需要查看或进入它时使用该独立入口，
不得把社交媒体页面、数据模型或数据库并入自身。

未来社交媒体智能体只有明确纳入后才增加对应的本地适配器和观察入口。

## Data Boundary

数据库不是 Web 端口。各智能体继续维护自己的数据库和内部数据库端口，
由 Social Media OS 的服务端 API 在服务器侧访问。浏览器只能访问
`localhost:4000/api/*`，不得直连 PostgreSQL 或其他内部服务端口。

## Architecture Rules

1. Financial OS 与 Social Media OS 是独立系统，不共享应用代码或数据库。
2. Social Media OS 在 `4000` 提供六个平台的唯一共享前端。
3. 新增平台时只修改 Social Media OS 的注册表和内部只读适配器。
4. Financial OS 只能通过独立 URL 或受控控制入口访问 Social Media OS。
5. 各智能体继续独立维护业务逻辑、任务调度、数据库和知识库。

## Start / Stop

```bash
bash start.sh social
bash start.sh financial
bash stop.sh social
bash stop.sh financial
```
