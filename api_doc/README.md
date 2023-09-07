# API 要求

> 所有輸入輸出都是使用 json 格式

## 錯誤回應碼

`NotLogin: Code = Code(http_code=401, api_code=200)`

表示使用者尚未登入

`NotGrant: Code = Code(http_code=401, api_code=201)`

表示使用者並未使用管理員帳號或是尚未登入

`Wrong_Format: Code = Code(http_code=400, api_code=202)`

使用者未給予規定的參數

`CoinNotEnough: Code = Code(http_code=200, api_code=204)`

使用者未擁有足夠滿足此操作的硬幣數量

`WrongLoginInfo: Code = Code(http_code=200, api_code=205)`

未知的使用者帳號密碼組合

`InstanceNotExist: Code = Code(http_code=200, api_code=206)`

未知的操作目標

`AlreadyExec: Code = Code(http_code=200, api_code=207)`

呼叫不能重複操作的 API

`InvalidAccess: Code = Code(http_code=200, api_code=208)`

並未擁有權限

## 驗證 API

- [x] Login

方法：POST

描述：獲得使用者 token

    - 輸入
        - student_id: str

          使用者註冊之學號

        - password: str

          使用者設定之密碼

    - 回應
        - status: int

          表示API要求的狀態。

- [x] /Register

方法：POST

描述：註冊帳號，並在註冊成功後取得使用者 token

    - 輸入
        - student_id: str

          使用者註冊之學號

        - name: str

          使用者註冊之名稱

        - password: str

          使用者註冊之密碼

    - 回應
        - status: int

          表示API要求的狀態。

- [x] /Logoff

方法：POST

描述：使使用者 token 失效

    - 輸入

      無需輸入

    - 回應
        - status: int

          表示API要求的狀態。

## 會員資訊操作 API

- [x] getUserInfo

方法：GET

描述：取得使用者資訊

    - 輸入

      不需要輸入

    - 回應
        - status: int

          表示API要求的狀態。

        - id: str

          使用者編號

        - name

          該使用者的名字

        - intro

          該使用者的簡介

- [x] getUserInfo/<id>

方法：GET

描述：依照 ID 取得使用者資訊

    - 輸入

      不需要輸入

    - 回應
        - status: int

          表示API要求的狀態。

        - id: str

          使用者編號

        - name

          該使用者的名字

        - intro

          該使用者的簡介

- [x] checkUserVerify

方法：GET

描述：確認使用者郵件認證狀態

    - 輸入

      無需輸入

    - 回應
        - status: int

          表示API要求的狀態。

        - verify: int

          表示認證狀態

          | 代碼 | 認證狀態 |
          | ---  | ---    |
          | 0 | 尚未認證   |
          | 1 | 已完成認證  |

- [x] getUserOutlook

方法：GET

描述：取得使用者外觀設定

    - 輸入

      不需要輸入

    - 回應
        - status: int

          表示API要求的狀態。

        - list: list[obj]

          使用者裝備列表

            - type: int

              此配備的種類

            - photo: str

              此配備的圖片

            - id: str

              此配備的編號

            - name: str

              此配備的名字

- [x] getUserOutlook/<id>

方法：GET

描述：依照 ID 取得使用者外觀設定

    - 輸入

      不需要輸入

    - 回應
        - status: int

          表示API要求的狀態。

        - list: list[obj]

          使用者裝備列表

            - type: int

              此配備的種類

            - photo: str

              此配備的圖片

            - id: str

              此配備的編號

            - name: str

              此配備的名字

- [x] getUserItem

方法：GET

描述：取得使用者已擁有的物品

    - 輸入

      不需要輸入

    - 回應
        - status: int

          表示API要求的狀態。

        - list: list[obj]

          包含持有裝備的資訊

            - item_id: str

              配件編號

            - type: int

              配件種類

            - photo: str

              配件圖片路徑

            - name: str

              配件名稱

- [x] getUserCoin

方法：GET

描述：取得使用者擁有之硬幣數量

    - 輸入

      不需要輸入

    - 回應
        - status: int

          表示API要求的狀態。

        - num: int

          持有多少硬幣

- [x] changeUserInfo

方法：POST

描述：上傳變更後的使用者名稱或簡介

    - 輸入
        - name: str

          選填，更改後的名字

        - intro: str

          選填，更改後的自我介紹

    - 回應
        - status: int

          表示API要求的狀態。

- [x] changeUserOutlook

方法：POST

描述：更改使用者更改後的服裝搭配。

    - 輸入
        - list: list[obj]

          更動裝備列表

            - id: str

              更動裝備編號

            - action: int

              更動操作

              | 編號 | 操作 |
                              | --- | --- |
              | 0 | 卸除 |
              | 1 | 裝備 |
    - 回應
        - status: int

          表示API要求的狀態。

## 物品操作 API

- [x] getPoolItemList/<id>

方法：GET

描述：給定編號取得該抽獎池中的物品

    - 輸入

      不需要輸入

    - 回應
        - status: int

          表示API要求的狀態。

        - items: list[int]

          存放所有抽獎池內的物品編號

- [x] drawCards

方法：POST

描述：給定模式與抽獎池編號，給出抽獎結果

    - 輸入
        - type

          表示抽獎類型

          | 編號 | 操作 |
                      | --- | --- |
          | 0 | 單抽 |
          | 1 | 十連抽 |
        - pool

          抽卡池編號

    - 回應
        - status: int

          表示API要求的狀態。

        - list: list[str]

          此次收抽獎所獲得的物品圖片路徑

- [x] listPool

方法：GET

描述：取出卡池列表

    - 輸入

      不需要輸入

    - 回應
        - status: int

          表示API要求的狀態。

        - pool_list: list[obj]

          卡池資料集合

            - id: str

              卡池編號

            - num: int

              卡池內容物數量

            - name: str

              卡池名稱

            - photo: str

              卡池圖片路徑

## 委託操作 API

- [x] getUserOrder

方法：GET

描述：取得使用者發出的委託

    - 輸入

      不需要輸入

    - 回應
        - status: int

          表示API要求的狀態。

        - list: list[obj]
            - id: str

              委託編號

            - status: int

              委託狀態

            - title: str

              委託標題

            - start_time: str

              委託創建時間

- [x] getOpenOrder

方法：GET

描述：取得招募中之委託

    - 輸入

      不需要輸入

    - 回應
        - status: int

          表示API要求的狀態。

        - list: list[obj]
            - id: str

              委託編號

            - status: int

              委託狀態

            - title: str

              委託標題

            - start_time: str

              委託創建時間

- [x] getJoinOrder

方法：GET

    - 輸入

      不需要輸入

    - 回應
        - status: int

          表示API要求的狀態。

        - list: list[obj]
            - id: str

              委託編號

            - status: int

              委託狀態

            - title: str

              委託標題

            - start_time: str

              委託創建時間

            - chatroom_id: str

              聊天室編號

- [ ] getOrderList

描述：依條件取得委託列表

    - 輸入
        - type: int

          取出委託列表的種類

          | 代號 | 取出資料 |
                      | --- | --- |
          | 0 | 使用者發出之委託 |
          | 1 | 使用者參加之委託 |
          | 2 | 招募委託列表 |
    - 回應
        - status: int

          表示API要求的狀態。

        - order_list: list[obj]

          根據要求給出的委託列表

            - order_state: int

              表示此委託的狀態

              | 編號 | 代表 |
                              | --- | --- |
              | 0 | 招募中 |
              | 1 | 進行中 |
              | 2 | 已完成 |
            - title: str

              此委託的標題

- [x] getOrderInfo/<id>

方法：GET

描述：給定編號取得該委託之資料

    - 輸入

      不需要輸入

    - 回應
        - status: int

          表示API要求的狀態。

        - order_state: int

          表示此委託的狀態

          | 編號 | 代表 |
                      | --- | --- |
          | 0 | 招募中 |
          | 1 | 進行中 |
          | 2 | 已完成 |
        - title: str

          委託的標題

        - intro: str

          委託的介紹內容

        - price: int

          委託的酬勞

        - time: str

          委託的執行時間

        - owner: str

          委託人的編號

- [ ] pushOrderState

描述：給定編號使該委託進入下一階段

    - 輸入
        - id: str

          委託之編號

    - 回應
        - status: int

          表示API要求的狀態。

        - order_state: int

          委託現在的狀態

          | 編號 | 代表 |
                      | --- | --- |
          | 0 | 招募中 |
          | 1 | 進行中 |
          | 2 | 已完成 |

- [x] createOrder

方法：POST

描述：創建新的委託

    - 輸入
        - title: str

          此委託的標題

        - close_time: str

          此委託的招募期限

        - exec_time: str

          此委託的執行時間

        - price: int

          此委託的酬勞

        - intro: str

          此委託的介紹內容

    - 回應
        - status: int

          表示API要求的狀態。

        - id: str

          新委託的編號

- [x] deleteOrder/<id>

方法：GET

描述：依照 ID 刪除委託

    - 輸入

      不需要輸入

    - 回應
        - status:int

          表示API要求的狀態。

- [x] joinOrder/<id>

方法：GET

描述：使用者參加選定的委託

    - 輸入

      不需要輸入

    - 回應
        - status: int

          表示API要求的狀態。

        - chat_id: str

          給予參與者的聊天室編號

## 訊息操作 API

- [x] sendMessage

方法：POST

描述：使用者傳送訊息至指定聊天室

    - 輸入
        - chatroom_id: str

          聊天室的編號

        - content: str

          傳送內容

    - 回應
        - status: str

          表示API要求的狀態。

- [x] getChatInfo/<id>

方法：GET

描述：給定編號取得該聊天室資訊

    - 輸入

      不需要輸入

    - 回應
        - status: int

          表示API要求的狀態。

        - chaters: list[str]

          此聊天室參加人的編號列表

        - owner_id: str

          聊天室擁有者編號

- [x] getChatHistory/<id>

方法：GET

描述：給定編號取得該聊天室之歷史內容

    - 輸入

      不需要編號

    - 回應
        - status: int

          表示API要求的狀態。

        - message:list[obj]

          訊息紀錄

            - content: str

              訊息內容

            - sender_id: str

              訊息傳送方編號

            - time: str

              訊息傳送時間

- [x] assignOrder/<id>

方法：POST

描述：指派委託給聊天室的另一方

    - 輸入

      不需要輸入

    - 回應
        - status: int

          表示API要求的狀態。

- [x] confirmOrder/<id>

方法：POST

描述：依照給定聊天室 ID，確認承接人完成委託並且發放獎勵

    - 輸入

      不需要輸入

    - 回應
        - status: int

          表示API要求的狀態。

## 管理員 API

- [x] createPool

方法：POST

描述：創建新的抽卡池

    - 輸入
        - name: str

          卡池名稱

        - photo: str

          圖片資料，使用base64轉換成字串
          ex: data:image/jpeg;base64, <base64 資料>

          上述範例為jpeg檔案

    - 回應
        - status: int

          表示API要求的狀態

        - pool_id:

          新建卡池編號

- [x] deletePool/<id>

方法：POST

描述：刪除抽卡池

    - 輸入

      不需要輸入

    - 回應
        - status: int

          表示API要求的狀態。

- [x] modifyPoolItem

方法：POST

描述：變更抽卡池內容

    - 輸入
        - id: str

          卡池編號

        - modify_list: list[obj]

          更改後的物品編號列表

            - id: str

              更改的物品id

            - action: int

              代表操作的模式

              | 編號 | 操作 |
                              | --- | --- |
              | 0 | 新增 |
              | 1 | 刪除 |
    - 回應
        - status: int

          表示API要求的狀態。

- [x] listItem

方法：GET

描述：列出系統內發行的道具

    - 輸入

      無需輸入

    - 回應
        - status: int

          表示API要求的狀態。

        - item_list: list[obj]

          配件列表

            - id: str

              此配件的編號

            - name: str

              此配件的名稱

            - photo: str

              此配件圖片路徑

            - type: int

              配件的種類

- [x] createItem

方法：POST

描述：新增物品

    - 輸入
        - name: str

          此配件的名稱

        - type: int

          此配件的種類

        - photo: str

          此配件圖片，使用base64將圖片資料轉換成字串

    - 回應
        - status: int

          表示API要求的狀態。

        - id: str

          新增加道具的編號。

- [x] deleteItem/<id>

方法：POST

描述：刪除物品

    - 輸入
        - id: str

          此配件的編號

    - 回應
        - status: int

          表示API要求的狀態。

- [x] modifyItemInfo

方法：POST

描述：更改配件資訊

    - 輸入
        - id: str

          更改配件的編號

        - name: str

          選填，更改後的名稱

        - photo: str

          選填，更改後的照片資料，以base64編碼

        - type: int

          選填，更改後的配件類型

    - 回應
        - status: int

          表示API要求的狀態。
