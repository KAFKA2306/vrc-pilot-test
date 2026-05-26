#!/bin/bash
# vrcpilot / inputtino Linux Setup Script
# このスクリプトは人間が sudo 権限で実行する必要があります。

set -e

echo "Setting up udev rules for inputtino..."
cat <<EOF | sudo tee /etc/udev/rules.d/99-inputtino.rules
# uinputの権限付与
KERNEL=="uinput", MODE="0660", GROUP="input", OPTIONS+="static_node=uinput"
# uhidの権限付与 (コントローラーエミュレーションに必要)
KERNEL=="uhid", MODE="0660", GROUP="input"
EOF

echo "Adding current user to 'input' group..."
sudo usermod -aG input $USER

echo "Reloading udev rules..."
sudo udevadm control --reload-rules
sudo udevadm trigger

echo "Setup complete. Please log out and log back in for group changes to take effect."
