# bocounty

## 環境建構101

### 本地端設定

基於python 3.11.X

```shell
pip install -r ./requirements.txt
```

### 使用docker

```shell
docker compose up
```

## 啟動伺服器

### 本地端

```shell
(在bocounty資料夾中執行)
flask run -h 0.0.0.0 -p 8000
```

```shell
flask run -h \<ip\> -p \<port\>
```

### 使用docker

若使用docker建置環境，則不需要啟動，預設port為8000

## API文檔

[API doc](./api_doc)

