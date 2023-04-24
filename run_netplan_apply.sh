#!/bin/bash
sudo systemctl daemon-reload
sudo systemctl start netplan-apply.service
