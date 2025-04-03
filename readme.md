<div align="center">
<sup>Дипломный проект "NLP веб-приложение"</sup>
  
<sup>Намнанов Арсалан Батоевич, 2024</sup>
<div><img src="gitpage_mats/logo.png" width="512" alt="Warp" /></div>
<div><b>Локальный чатбот "AI Chat"</b></div>

AI Chat — это чатбот, вдохновленный ChatGPT, с которым можно общаться на широкие темы,<br />способный помнить давно прошедшие разговоры.

[Презентация](#презентация) •
[Технологии](#технологии) •
[Принцип работы](#принцип-работы)
</div>

## Презентация
https://github.com/user-attachments/assets/3243483d-4016-4436-b134-9d0569b45859

## Технологии
Языковой функционал обеспечен LLM 
<a href="https://huggingface.co/tiiuae/falcon-7b"><u>Falcon 7B</u></a>,
тонко настроенной методом  
<a href="https://arxiv.org/abs/2106.09685"><u>LoRa</u></a>
на датасете
<a href="https://huggingface.co/datasets/tatsu-lab/alpaca"><u>Alpaca</u></a>.
Обучение модели было произведено с помощью фреймворка
<a href="https://github.com/Lightning-AI/litgpt"><u>LitGPT</u></a>,
а веб-приложение реализовано на
<a href="https://flask.palletsprojects.com/en/stable/"><u>Flask</u></a>
при помощи
<a href="https://flask-sqlalchemy.readthedocs.io/"><u>Flask-SQLAlchemy</u></a>.

## Принцип работы
фыва
