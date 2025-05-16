# SynCopy

## SyncCopy 是什么

SyncCopy 基于文件同步实现跨设备实时同步剪贴板内容。为多设备间互传简单文本提供极大便利。

SyncCopy 监听系统剪贴板的变化，并将内容保存到本地。同时，它还监听本地文件的变化，并将其同步到系统剪贴板。

## 安装

```
git clone https://github.com/ArcaneEcholan/synclipboard
```

## 使用

**配置**

配置同步文件夹（比如坚果云）, 配置文件路径：

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

那么 `sync_dir` 指定为 `C:/Users/XiaoMing/nutfiles/synclipboard`

**运行**

确保安装 python3

```shell
# 安装必要的依赖包
pip install pyperclip

# 运行
python3 ./main.py
```
