# Miscelanious: 
1. Project Describtion:

   First part of NLP web-app project.

   Project consists of two parts:

   a. Flask web-app

      https://github.com/AKAD0/diploma_project (this repo)

   b. Finetuned model

      https://huggingface.co/AKAD0/falcon-7b-alpaca/

2. Repository Branches:

   a. "master" - Base version of the Flask web-app.

                 Independent. (Doesn't involve model)

   b. "inferenced" - Modified version of 'master' branch:

                     1) "app.py" - modified "button()" endpoint to integrate model

                     Dependancies: library "litgpt[all]", model

   c. "memassist" - Modified version of 'inferenced' branch:

                    1) "venv\Lib\site-packages\litgpt\deploy\serve.py" - customized 'decode_request()' to include 'input' field from JSON payload

                    2) "app.py" - modified "button().response_json" variable to have 'input' field

3. 'master' Branch Installation:

   !!! path errors expected !!!

   Download the repo in root-folder.
