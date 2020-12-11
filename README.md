# dataStorage

## запуск демона
1) активируем виртуальное окружение 
   <br/>
    <code>
        source ./venv/bin/activate 
    </code>
    <br/>   
    <br/>   

2) запустим демона
   <br/>
    <code>
        python ./dataStorage.py start 
   </code>
   <br/>
   <br/>
   по умолчанию сервер работает на http://127.0.0.1:8082
   
## команды демона
1) убить демона
    
    <code>
        python ./dataStorage.py stop 
   </code>


2) перезапустить демона

    <code>
        python ./dataStorage.py restart 
   </code>


## запустить End to End (E2E) тест сервера
<code>
    python -m unittest tests.TestServerE2E.test_E2E in ./datastorage
</code>

в тесте происходит 

- проверка загрузки файлов
- проверка скачивания файлов
- проверка удаления файлов


    