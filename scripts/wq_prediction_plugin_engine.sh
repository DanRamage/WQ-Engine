#!/bin/bash

source /usr/local/virtualenv/pyenv-2.7.11/bin/activate;

cd /home/xeniaprod/scripts/WQ-Engine/scripts;

python wq-prediction-engine.py --PluginDirList=/home/xeniaprod/scripts/MyrtleBeach-Water-Quality/scripts,/home/xeniaprod/scripts/Florida-Water-Quality/scripts,/home/xeniaprod/scripts/Charleston-Water-Quality/scripts,/home/xeniaprod/scripts/KillDevilHillsWQ/scripts --LogConfigFile=/home/xeniaprod/scripts/WQ-Engine/config/prediction_plugin.conf >> /home/xeniaprod/tmp/log/wq_prediction_plugin_engine_sh.log 2>&1
