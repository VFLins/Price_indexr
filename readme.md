<details>
    <summary> <h3> English </h3> </summary>
    
# Description

### What it does?

Price_indexr is intended to get a set of product prices for a given search on google shopping and store it in a database or a .csv file. It will return up to 20 results, if no product is found at the moment it will register a message in a text file in the same folder as the script. It is recomended to automate this task to be performed periodically with [cron](https://cron-job.org/en/) to schedule new data over time.

### How can this help me?

This can be used to satisfy business and personal necessities, for stablishing market prices, help on calculating price indexes for specific types of products or monitoring the price of a product you want to buy.

    # Requirements

- Python version 3.8 or superior and packages:
    - [bs4](https://pypi.org/project/beautifulsoup4/)
    - [sqlalchemy](https://pypi.org/project/SQLAlchemy/)
    - [requests](https://pypi.org/project/requests/)
- Any popular internet browser installed, and [know it's User Agent](https://developers.whatismybrowser.com/useragents/parse/?analyse-my-user-agent=yes#parse-useragent) (If you want to troubleshoot)

<details>
    <summary> <b>Recommended for scheduling</b> </summary>
    
For macOS/Unix operating systems:
- [Bash](http://tiswww.case.edu/php/chet/bash/bashtop.html)
- [cron/anacron](https://cron-job.org/en/) or [cronitor](https://cronitor.io) installed

For Windows operating systems:
- [PowerShell](https://docs.microsoft.com/pt-br/powershell/scripting/overview?view=powershell-7.2)
- [Windows Task Scheduler](https://docs.microsoft.com/en-us/windows/win32/taskschd/task-scheduler-start-page)
    
</details>

# How to use?

***Currently this project is under construction, and may not be working properly (~~maybe not working at all~~)***

The intended usage is on a terminal:

```
python price_indexr.py "<Database connection string or '.csv'>" "my product search" "<location code [optional]>"
```

This will use python to run the ```price_indexr.py``` script with 3 different arguments in order:
1. A connection string to a database supported by SQLAlchemy on it's [Included Dialects](https://docs.sqlalchemy.org/en/14/dialects/#included-dialects), or simply ".csv" to save in a text file;
2. A search that you would type on google's search field. Must be inside quotes or double qutoes if it contains more than one word;
3. [Optional] A location code for the country (e.g. "us" for the United States, or "pt-br" for Brazil). If not included, google search engine will guess the country by the IP address that you are using.

### How the search works?

The search results could come with a lot of similar products that doesn't meet your expectations. For that reason, every word you type in the search argument is a filter, Price_indexr works with two kinds of filters:

1. **Positive:** this filter contains every word that you demand to be in the title of the product. This also will be used to fill the google shopping's search bar.
2. **Negative:** this filter contains every word that you demand ***NOT*** to be in the title of the product. This will never be used to fill the google shopping's search bar, as it would bring more unwanted results.

So your search would look like: ```"gtx 1660 -pc -notebook"```*

In the example above, "gtx" and "1660" are positive filters and "pc" and "notebook" are negative. In this case you want to search the "gtx 1660" graphics card's price, but as the results might bring unwanted computers and notebooks that comes with this graphics card equiped, you should use negative filters such as those to avoid adding them to your database. The positive filters would naturally prevent you from getting similar graphics cards such as "gtx 1650" and ensuring you get data only from the desired model.

 *Note that positive filters should **always** come first.

### Scheduling on Unix/macOS with Bash

<details>
    <summary> Example of automation with crontab </summary>

    ```
    PYTHON_PATH="<path to desired python interpreter>"
    SCRIPT_PATH="<path to price_indexr.py>"
    DB_CON="<your database connection string>" 
    # or ".csv" to save in a text file in the same folder of your script instead of a database

    crontab -e
    @monthly "$PYTHON_PATH" "$SCRIPT_PATH" "$DB_CON" "my product search"
    # To check the schedules made:
    crontab -l
    ```
</details> 

### Scheduling on Windows with PowerShell

<details>
    <summary> Example of automation with Windows Task Scheduler </summary>

    ```
    $PYTHON_PATH = "<path to desired python interpreter>"
    $SCRIPT_PATH = "<path to price_indexr.py>"
    $DB_CON = "<your database connection string>" 

    $price_indexr_action = New-ScheduledTaskAction 
        -Execute "python3 $SCRIPT_PATH $DB_CON 'my product search'"
    $monthly = New-ScheduledTaskTrigger -Monthly -At 0:00am
    $task_<unique name> = Register-ScheduledTask 
        -Action $price_indexr_action
        -Trigger $monthly 
        -TaskName "<unique name>" 
        -Description "<Your Description>"
    $task_<unique name> | Set-ScheduledTask
    ```
</details>

If a database was selected to store the data, a table called "price_indexr-my_product_search" will be created in the database on the first execution. Next executions will append new data to the same table. If you preferred a text file, the name of the file will follow the same naming pattern.
    
# Troubleshooting

1. Depending on the user-agent, the results may or not appear for Price_indexr, usually, changing the user-agent on the line 125 of the script will solve the problem.

</details>
    
<details>
    <summary> <h3> Portugu??s </h3> </summary>

# Descri????o

## O que faz?

Price_indexr tem a inten????o de obter o pre??o de um conjunto de bens para uma dada pesquisa no google shopping, e armazenar os dados obtidos em um arquivo de texto .csv ou numa base de dados. Ele pode retornar at?? ~80 resultados dependendo da pesquisa, a quantidade exata de resultados registrados fica registrada num arquivo de texto de f??cil interpreta????o no mesmo diret??rio em que fica salvo o script. ?? recomend??vel automatizar esta tarefa, usando [cron](https://cron-job.org/en/) para programar a entrada de novos dados ao longo do tempo.

## Como pode me ajudar?
    
Pode ser usado para solucionar problemas de neg??cios e pessoais, como para encontrar o pre??o de mercado de um dado tipo de bem, ajudar na estipula????o de um ??ndice de pre??os, ou ajudar um comprador a encontrar o melhor momento para adquirir um produto.

# Requisitos
    
- Python 3.8 ou superior;
    - [bs4](https://pypi.org/project/beautifulsoup4/)
    - [sqlalchemy](https://pypi.org/project/SQLAlchemy/)
    - [requests](https://pypi.org/project/requests/)
- Qualquer navegador popular e [conhecer seu User Agent](https://developers.whatismybrowser.com/useragents/parse/?analyse-my-user-agent=yes#parse-useragent) (se quiser solucionar problemas)

<details>
    <summary> <b> Recomendado para automa????o </b> </summary>
    
Para macOS/Unix:
- [Bash](http://tiswww.case.edu/php/chet/bash/bashtop.html)
- [cron/anacron](https://cron-job.org/en/) ou [cronitor](https://cronitor.io) instalado

Para Windows:
- [Agendador de Tarefas do Windows](https://docs.microsoft.com/en-us/windows/win32/taskschd/task-scheduler-start-page)
    
</details>
    
# Como usar?
    
***Atualmente este projeto est?? em constru????o e pode ou n??o estar funcionando apropriadamente (~~talvez nem isso~~)***

A maneira planejada para se usar, ?? atrav??s de um comando no terminal:

```
python price_indexr.py "<Database connection string or '.csv'>" "my product search" "<location code [optional]>"
```
    
Isto vai usar o python para executar o script ```price_indexr.py``` com 3 argumentos diferentes na ordem:
1. Um string de conex??o usado pelo SQLAlchemy nos seus [Dialetos Inclu??dos](https://docs.sqlalchemy.org/en/14/dialects/#included-dialects), ou simplesmente ".csv" para salvar num arquivo de texto;
2. Uma pesquisa que voc?? digitaria na pesquisa do google. Deve estar dentro de aspas simples ou duplas se possuir mais de uma palavra (mais detalhes no pr??ximo t??pico);
3. [Opcional] O c??digo de localiza????o para um pa??s (por exemplo: "us" para os estados unidos, ou "pt-br" para o Brasil). Se n??o for fornecido, a engine de pesquisa de google vai adivinhar o pa??s pelo endere??o IP que voc?? estiver usando.

## Como a pesquisa funciona?

O resultado das pesquisas pode trazer diversos produtos similares que podem n??o ser do seu interesse, por este motivo, cada palavra que voc?? digitar vai servir como filtro, **Price_indexr** funciona com dois tipos de filtros:

1. *Positivo:* S??o as palavras que voc?? exige que estejam no t??tulo do produto. Isto tamb??m vai ser usado para preencher a barra de pesquisa;
2. *Negativo:* S??o as palavras que voc?? exige que ***N??O*** estejam no t??tulo do produto. N??o ser?? usada no termo de pesquisa, pois se fosse, iria trazer mais produtos indesejados nos resultados.
    
Ent??o sua pesquisa iria parecer com isto: ```"gtx 1660 -pc -notebook"```*
    
No exemplo acima, "gtx" e "1660" s??o filtros positivos, enquanto "pc" e "notebook" s??o negativos. Neste caso voc?? estaria querendo pesquisar o pre??o de placas de v??deo do modelo "gtx 1660", mas como os resultados podem trazer PCs e Notebooks indesejados que v??m com este modelo de placa de v??deo equipado, voc?? deveria usar estes filtros negativos para evitar adicionar estes resultados na sua base de dados. Os filtros positivos v??o naturalmente garantir que voc?? obtenha apenas o modelo desejado, em vez de outros modelos similares que tamb??m podem aparecer nos resultados, como a "gtx 1650".
    
*Perceba que os filtros positivos devem **sempre** aparecer primeiro.

### Scheduling on Unix/macOS with Bash

<details>
    <summary> Exemplo de automa????o com crontab </summary>

    ```
    PYTHON_PATH="<path to desired python interpreter>"
    SCRIPT_PATH="<path to price_indexr.py>"
    DB_CON="<your database connection string>" 
    # or ".csv" to save in a text file in the same folder of your script instead of a database

    crontab -e
    @monthly "$PYTHON_PATH" "$SCRIPT_PATH" "$DB_CON" "my product search"
    # To check the schedules made:
    crontab -l
    ```
</details> 

### Automa????o no Windows

<details>
    <summary> Example of automation with Windows Task Scheduler </summary>

    ```
    $PYTHON_PATH = "<path to desired python interpreter>"
    $SCRIPT_PATH = "<path to price_indexr.py>"
    $DB_CON = "<your database connection string>" 

    $price_indexr_action = New-ScheduledTaskAction 
        -Execute "python3 $SCRIPT_PATH $DB_CON 'my product search'"
    $monthly = New-ScheduledTaskTrigger -Monthly -At 0:00am
    $task_<unique name> = Register-ScheduledTask 
        -Action $price_indexr_action
        -Trigger $monthly 
        -TaskName "<unique name>" 
        -Description "<Your Description>"
    $task_<unique name> | Set-ScheduledTask
    ```
</details>

Se voc?? escolheu salvar os dados numa base de dados, uma tabela com o nome "price_indexr-produto_pesquisado" ser?? criada no banco de dados escolhido. Futuras execu????es adicionar??o novas linhas de dados abaixo dos dados existentes. Se voc?? escolheu um arquivo de texto, o nome do arquivo vai seguir o mesmo padr??o de nomea????o.

# Resolvendo problemas

1. Dependendo do user-agent, os resultados podem n??o aparecer para Price_indexr, normalmente, mudar o c??digo do user-agent na linha 125 do script resolveria o problema.

</details>
