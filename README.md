# Data Logger
>Not too sure what this exists for. Didn't design this with any use case in mind

Logs data to a finite FIFO queue and returns this queue when queried. Logger for
administrative monitoring of application.


Could be used for HTTP to Mosquitto data-logging 
### Run
#### Requirements
```shell
pip3 install -r requirements.txt
```

#### Run
```shell
python3 main.py
```

## Usage

### ping
```shell
curl -X GET http://localhost:3030/ping
```

### GET records
```shell
curl -X GET http://localhost:3030/
```


### POST json data
```shell
curl -d '{"key1":"value1", "key2":"value2"}' -H "Content-Type: application/json" -X POST http://localhost:3030/log-data
```

### 