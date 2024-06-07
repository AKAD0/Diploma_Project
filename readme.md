# Project Describtion:
#### First part of NLP web-app project.
#### Project consists of two parts:
#### 1. Flask web-app
####    https://github.com/AKAD0/diploma_project (this repo)
#### 2. Finetuned model
####    https://huggingface.co/AKAD0/falcon-7b-alpaca/

# Repository Branches:
#### 1. "master" - Base version of the Flask web-app.
####               Independent. (Doesn't involve model)
#### 2. "inferenced" - Modified version that integrates the model within "app.py". 
####                   Dependancies: library "litgpt[all]", model

# 'inferenced' Branch Installation:
#### !!! path errors expected !!!
#### 1. Download the repo in root-folder.
#### 2. (venv) pip install "litgpt[all]" 
#### 3. Download the model and place it's files at '/venv/Lib/site-packages/litgpt/out/lora/final'