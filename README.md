# 定时POST请求工作流

这个 GitHub Actions 工作流用于每5分钟向指定API发送一次POST请求，适用于需要定期触发的接口调用场景。

## 功能说明

- 定时任务：每5分钟自动执行一次
- 操作内容：向指定API发送包含认证信息的POST请求
- 安全机制：使用GitHub Secrets存储敏感信息（session3rd）

## 前置条件

- 拥有一个GitHub账号和仓库
- 已获取有效的`session3rd`值（用于API认证）

## 配置步骤

### 1. 部署工作流文件

1. 在你的GitHub仓库中创建以下路径和文件：
   ```
   .github/workflows/single-post.yml
   ```

2. 将工作流配置内容复制到该文件中并提交推送

### 2. 设置敏感信息（session3rd）

1. 进入你的GitHub仓库页面，点击顶部导航栏的 **Settings**
2. 在左侧菜单中找到 **Secrets and variables** → **Actions**
3. 点击 **New repository secret** 按钮
4. 在弹出的表单中：
   - **Name** 填写：`SESSION_3RD`
   - **Secret** 填写：你的实际session3rd值
   - 苹果在 GitHub Secrets 中创建 SESSION_3RDS（注意名称）
   - 安卓从GitHub Secrets中获取session3rd值，命名为AZID
以逗号分隔的形式添加所有会话值，例如：abc123,def456,ghi789
5. 点击 **Add secret** 保存

## 工作原理

1. 工作流通过cron表达式 `*/5 * * * *` 设置每5分钟触发一次
2. 运行时从GitHub Secrets中读取`SESSION_3RD`的值
3. 使用axios库向目标API发送POST请求，包含预设的请求头和参数
4. 请求结果（成功/失败信息）会记录在Actions运行日志中

## 查看运行结果

1. 进入仓库的 **Actions** 标签页
2. 在左侧工作流列表中找到 **Single Session & URL POST Request**
3. 点击进入后可以看到所有运行记录
4. 点击具体某次运行记录可以查看详细日志，包括：
   - 请求状态码
   - 响应内容
   - 错误信息（如果请求失败）

## 自定义修改

### 调整执行频率

修改工作流文件中的cron表达式：on:
  schedule:
    - cron: '*/5 * * * *'  # 每5分钟执行一次，可修改为其他频率
cron表达式格式说明：`分 时 日 月 周`
- `*/10 * * * *` 表示每10分钟
- `0 * * * *` 表示每小时整点
- `0 8 * * *` 表示每天早上8点

### 修改请求参数

如果需要修改请求的URL、请求头或表单数据，可以直接编辑工作流文件中的对应部分：
- `url` 变量：修改目标API地址
- `headers` 对象：调整请求头信息
- `data` 变量：修改POST表单数据

## 注意事项

- GitHub Actions的定时任务可能存在±1分钟的延迟，这是正常现象
- 请确保你的`session3rd`值有效，过期后需要及时更新Secrets
- 免费版GitHub Actions有运行时间限制，过度频繁的执行可能会消耗配额
- 如遇请求失败，请先检查日志中的错误信息，确认网络连接和参数正确性
