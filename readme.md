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
#### 2. "inferenced" - Modified version of 'master' branch:
####                   1) "app.py" - modified "button()" endpoint to integrate model
####                   Dependancies: library "litgpt[all]", model
#### 3. "memassist" - Modified version of 'inferenced' branch:
####                  1) "venv\Lib\site-packages\litgpt\deploy\serve.py" - customized 'decode_request()' to include 'input' field from JSON payload
####                  2) "app.py" - modified "button().response_json" variable to have 'input' field

# 'master' Branch Installation:
#### !!! path errors expected !!!
#### 1. Download the repo in root-folder.