# frontend

## Перед сборкой проекта:

**Изменить строку**

*src/store/index.js*
```
state:{
    ...
    с: url: 'http://192.168.1.19:8000/api/'
    на: url: 'http://<backendIP:port>/api/
    ...
}
```


## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).
