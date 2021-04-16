# websocket_demo
flask-sockets


```
gunicorn -k flask_sockets.worker -b 0.0.0.0:5005 server:app
```

浏览器访问:
`localhost:5005/jack`