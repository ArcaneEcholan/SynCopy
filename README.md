# 配置文件位置及内容

运行之前要配置同步盘的路径(比如使用坚果云), 以下是配置文件路径:

- Windows 10+: `%APPDATA%/synclipboard/config.json`
  - 注：`%APPDATA%` 通常是：`/Users/你的用户名/AppData/Roaming/synclipboard`
- Linux: `~/.config/synclipboard/config.json`

手动创建 config.json, 内容示例：

```json
{
  "sync_dir": "/PATH/TO/SYNC/FODLER"
}
```

`sync_dir`: 剪切板同步文件夹的路径，剪切板的内容将在这里进行同步，如果路径不存在，会自动创建。

举例，假如你的坚果云同步路径是: `C:/Users/XiaoMing/nutfiles`

那么，`sync_dir` 可以指定为 `C:/Users/XiaoMing/nutfiles/synclipboard`

# 执行 main.py

确保安装python3

```shell
# 安装必要的依赖包
pip install pyperclip

# 运行
python3 ./main.py
```

# 原理

假设：

- 各个设备上的时间是同步的
- 同步盘（比如坚果云）是可靠的
- 网络是低时延的

关注单个设备：

- 当检测到同步盘有新的剪切板同步文件时, 将其内容覆盖到剪切板。
  - 由于假设各设备的时间是一致的，所以可以用文件的创建时间判断新旧。
- 当检测到剪切板内容更新时，向同步盘创建新的剪切板同步文件。
