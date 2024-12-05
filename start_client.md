要在 Ubuntu 上创建一个脚本，以便在开机时自启动运行 `python3 client.py`，可以按照以下步骤进行操作：

### 1. 创建 Python 脚本

确保你的 `client.py` 脚本可以正常运行，并且它的路径是已知的。

### 2. 创建启动脚本

你可以创建一个简单的 shell 脚本来运行你的 Python 程序。打开终端并执行以下命令：

```bash
nano ~/start_client.sh
```

在打开的编辑器中，输入以下内容：

```bash
#!/bin/bash
# 运行 Python 脚本
python3 /path/to/your/client.py
```

请将 `/path/to/your/client.py` 替换为你的实际 Python 脚本的路径。

保存并退出编辑器（在 nano 中，按 `CTRL + X`，然后按 `Y` 确认保存，最后按 `Enter`）。

### 3. 使脚本可执行

接下来，给这个脚本添加执行权限：

```bash
chmod +x ~/start_client.sh
```

### 4. 创建 systemd 服务

为了在开机时自启动该脚本，你可以使用 `systemd` 创建一个服务。执行以下命令创建一个新的服务文件：

```bash
sudo nano /etc/systemd/system/client.service
```

在打开的编辑器中，输入以下内容：

```ini
[Unit]
Description=Start Python Client

[Service]
ExecStart=/bin/bash /home/rasp3b/facial-recognition-master/start_client.sh
WorkingDirectory=/home/rasp3b/facial-recognition-master/
StandardOutput=journal
StandardError=journal
Restart=always
User=rasp3b

[Install]
WantedBy=multi-user.target
```

请将 `your_username` 替换为你的实际用户名。

### 5. 启用服务

保存并退出编辑器后，执行以下命令以启用服务：

```bash
sudo systemctl enable client.service
```

### 6. 启动服务

你可以立即启动服务来测试它：

```bash
sudo systemctl start client.service
```

### 7. 查看服务状态

你可以查看服务的状态以确保它正在运行：

```bash
sudo systemctl status client.service
```

### 8. 日志查看

如果你想查看 Python 脚本的输出，可以使用 `journalctl` 命令：

```bash
journalctl -u client.service -f
```

这将实时显示该服务的日志。

### 总结

现在，你的 Python 脚本将在每次开机时自动运行。如果需要停止或禁用该服务，可以使用以下命令：

- 停止服务：

```bash
sudo systemctl stop client.service
```

- 禁用服务：

```bash
sudo systemctl disable client.service
```

按照这些步骤，你应该能够成功地在 Ubuntu 上设置 Python 脚本的开机自启动。



[Unit]
Description=Start Python Client

[Service]
ExecStart=/bin/bash /home/rasp3b/facial-recognition-master/start_client.sh
WorkingDirectory=/home/rasp3b/facial-recognition-master
StandardOutput=journal
StandardError=journal
Restart=always

[Install]
WantedBy=default.target


nano ~/.config/systemd/user/client.service
systemctl --user daemon-reload
systemctl --user start client.service
systemctl --user stop client.service
systemctl --user enable client.service