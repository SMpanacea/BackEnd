# BackEnd

Panacea 앱의 백엔드 코드


## Installation
```sh
pip install -r requirements.txt
```


## Starting
```sh
flask run
or
python app.py
```


## filesystem
```bash
📦BackEnd
┣ 📂controllers
┃ ┣ 📜barcodecontroller.py
┃ ┣ 📜chatcontroller.py
┃ ┣ 📜medicinecontroller.py
┃ ┗ 📜usercontroller.py
┣ 📂models
┃ ┣ 📜models.py
┃ ┗ 📜schemas.py
┣ 📂service
┃ ┣ 📜barcode_service.py
┃ ┣ 📜barcode_service_imp.py
┃ ┣ 📜chat_service.py
┃ ┣ 📜chat_service_imp.py
┃ ┣ 📜email.service_imp.py
┃ ┣ 📜email_service.py
┃ ┣ 📜json_service.py
┃ ┣ 📜json_service_imp.py
┃ ┣ 📜medicine_service.py
┃ ┣ 📜medicine_service_imp.py
┃ ┣ 📜user_service.py
┃ ┗ 📜user_service_imp.py
┣ 📂templates
┃ ┗ 📜email.html
┣ 📜.gitignore
┣ 📜app.py
┣ 📜README.md
┗ 📜requirements.txt
 ```