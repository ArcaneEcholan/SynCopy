# SynCopy

## 背景

在 Ubuntu 主机中安装 VirtualBox 以支持企业微信，但双向剪贴板经常出错。日常写代码时，跟同事沟通时，体验割裂。即使传递一小段文本，也需多次中转。后来发现，剪贴板实时同步不仅能解决主机与虚拟机间的问题，也能在 VPN 连接到公司桌面时用得上。

## SyncCopy 是什么

SyncCopy 基于 **文件同步** 实现跨设备 **实时同步** 剪贴板内容。为多设备间互传简单文本提供极大便利。

SyncCopy 监听系统剪贴板的变化，并将内容保存到本地。同时，它还监听本地文件的变化，并将其同步到系统剪贴板。

## 安装

```
git clone https://github.com/ArcaneEcholan/SynCopy
```

## 使用

**配置**

配置同步文件夹（比如坚果云）, 配置文件路径：

- Windows 10+: `%APPDATA%/SynCopy/config.json`
  - 注：`%APPDATA%` 通常是：`/Users/你的用户名/AppData/Roaming/SynCopy`
- Linux: `~/.config/SynCopy/config.json`

手动创建 config.json, 内容示例：

```json
{
  "sync_dir": "/PATH/TO/SYNC/FODLER"
}
```

`sync_dir`: 剪切板同步文件夹的路径，剪切板的内容将在这里进行同步，如果路径不存在，会自动创建。

举例，假如你的坚果云同步路径是: `C:/Users/XiaoMing/nutfiles`

那么 `sync_dir` 指定为 `C:/Users/XiaoMing/nutfiles/SynCopy`

**运行**

确保安装 python3.8 以上

```shell
# 安装必要的依赖包
pip install pyperclip

# 运行
python3 ./main.py
```

![](/images/使用截图.png)
