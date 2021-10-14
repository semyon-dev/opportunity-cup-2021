# Решение для for case-cup-2021

# BACKEND for case-cup-2021

Решение для IT кейса

*ПРОЕКТ ЕЩЕ НУЖНО ДОДЕЛАТЬ ДО 10 УТРА!*

## запросы

* Посчитать потери переноса: `GET /offset` (пример: /offset?id=4&offset=4)
* Получить все задачи: `GET /data`


<img src="img_1.png" alt="drawing" width="500"/>
<img src="img_2.png" alt="drawing" width="500"/>


## heroku api demo url

https://opportunity-cup-2021.herokuapp.com/

## Стэк

* Python 3.10
* MongoDB
* Flask

## Run

`python main.py`

## .env example

```dotenv
# mongodb url
CONNECTION_STRING="mongodb+srv://username:password@cluster0.ik40a.mongodb.net/Cluster0?retryWrites=true&w=majority&tls=true"
PORT=8080
```

# FRONTEND

Frontend for opportunity cup 2021. Written in Vue.js with Vuetify and Vuex set up it is ready to be used.
Starting point is main.ts, the logic behind '/' path can be found at views/Gantt-simple.vue. After different experiments Home.vue and Gantt.vue are still there just as heritage

## Project setup

```
yarn install
```

### Compiles and hot-reloads for development

```
yarn serve
```

### Compiles and minifies for production

```
yarn build
```
