# Line Chat Bot
## _for dinner and coding_
url:
https://orderchatbot-back.onrender.com
## Software Document
[SRD]-[SDD]-[STD]
## Features

## API
### Stores
- `GET /stores` - 獲取所有商店
- `POST /stores` - 創建新商店
- `GET /stores/<store_id>` - 根據 ID 獲取商店
- `DELETE /stores/<store_id>` - 根據 ID 刪除商店
- `PUT /stores/<store_id>` - 根據 ID 更新商店

### Menus
- `POST /menus` - 創建新菜單
- `GET /menus/<menu_id>` - 根據 ID 獲取菜單
- `PUT /menus/<menu_id>` - 根據 ID 更新菜單
- `DELETE /menus/<menu_id>` - 根據 ID 刪除菜單

### Menu Items
- `POST /menu_items` - 創建新菜單項目
- `GET /menu_items/<menu_item_id>` - 根據 ID 獲取菜單項目
- `PUT /menu_items/<menu_item_id>` - 根據 ID 更新菜單項目
- `DELETE /menu_items/<menu_item_id>` - 根據 ID 刪除菜單項目

### Cart
- `POST /cart` - 創建新購物車
- `GET /cart/<cart_id>` - 根據 ID 獲取購物車
- `PUT /cart/<cart_id>` - 根據 ID 更新購物車
- `DELETE /cart/<cart_id>` - 根據 ID 刪除購物車

### Cart Items
- `GET /cart_item/<cart_item_id>` - 根據 ID 獲取購物車項目詳情
- `POST /cart/<cart_id>/items` - 向購物車添加項目

## License

MIT

**Free Software, Hell Yeah!**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [SRD]: <https://docs.google.com/document/d/1jBRBsmAd5_j9aBS7fNSi0lGutVVIoUzgPKJUNFg4teY/edit?usp=sharing>
   [SDD]: <https://docs.google.com/document/d/1z1pH9ecRDiTR364HDEBv_qMK3sDL-g7iCd-U7wgamVU/edit?usp=sharing>
   [STD]: <https://docs.google.com/document/d/1ja0U4PFvpEipItSqtKO-dDrH9OwhK5AazDbihXM3CZc/edit?usp=sharing>
   
   [dill]: <https://github.com/joemccann/dillinger>
   [git-repo-url]: <https://github.com/joemccann/dillinger.git>
   [john gruber]: <http://daringfireball.net>
   [df1]: <http://daringfireball.net/projects/markdown/>
   [markdown-it]: <https://github.com/markdown-it/markdown-it>
   [Ace Editor]: <http://ace.ajax.org>
   [node.js]: <http://nodejs.org>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [jQuery]: <http://jquery.com>
   [@tjholowaychuk]: <http://twitter.com/tjholowaychuk>
   [express]: <http://expressjs.com>
   [AngularJS]: <http://angularjs.org>
   [Gulp]: <http://gulpjs.com>
