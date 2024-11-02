import requests
import base64
from time import sleep


PATH_TO_IMAGE = "/home/usr/Downloads/41f28357a0b2464287415c383c7d1b7a.pdf"


PROJECT_ID = "U_RATE_2"
TOKEN = "<ваш токен>"
MACHINE_UID = "<ваш идентификатор машины>"


# вид документа
TYPE = "PASSPORT_REG"


# кодируем изображение в base64
with open(PATH_TO_IMAGE, "rb") as image_file:
   image = base64.b64encode(image_file.read()).decode()
   image_file.close()


# отправляем изображение документа в beorg
document = requests.post(
   "https://api.beorg.ru/api/bescan/add_document",
   headers={"Content-Type": "application/json", "Accept-Language": "ru"},
   json={
       "project_id": PROJECT_ID,
       "token": TOKEN,
       "machine_uid": MACHINE_UID,
       "images": [image],
       "process_info": [
           {
               "type": TYPE
           }
       ],
   },
)


# достаем из ответа номер для отслеживания
document_id = document.json().get("document_id")


print(f"Номер для отслеживания: {document_id}")




if document_id is not None:
   # опрашиваем API пока не получим результат
   result_req = requests.get(f"https://api.beorg.ru/api/document/result/{document_id}?token={TOKEN}")


   while result_req.status_code != 200:
       print("Документ обрабатывается")
       sleep(1)
       result_req = requests.get(f"https://api.beorg.ru/api/document/result/{document_id}?token={TOKEN}")


   # достаем данные из ответа API
   result = result_req.json()


   print("/////////////////////")
   print("Результат:")
   print(result)
