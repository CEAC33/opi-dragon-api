# opi-dragon-api

![image](https://user-images.githubusercontent.com/51218415/123738429-65252c00-d86a-11eb-8735-3472ae37c046.png)

# Run locally

```
make restart
```

# Endpoints

## Healtcheck

- http://localhost:8000/health/status

Response:
```
{
    "status": "OK"
}
```

## Auth

- http://localhost:8000/auth

Payload:
```
{
    "username": "XXXX",
    "password": "XXXX"
}
```

Response:
```
{
    "access_token": "XXXX.XXXX.XXXX"
}
```

## Predictive Model

- http://localhost:8000/v1/predictive_model

Payload:
```
{
    "n1": 4.0,
    "n2": 5.0
}
```

Response:
```
{
    "result": 41.0
}
```
