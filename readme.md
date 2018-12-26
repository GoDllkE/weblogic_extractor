# Weblogic extractor
---
Versão: 1.0.0

Este script foi desenvolvido com o propósito de extrair todas as informações/configurações de um weblogic a fim de ser utilizado posteriormente nas automações de gerenciamento do weblogic utilizando o modulo puppet [lalala](lalalala).


#### Requisitos

- Python 2.7
- Pyyaml


#### Extraindo os dados

##### 1. O script é modular!

O script utiliza templates para extrair as informações e possui o funcionamento modular, isto é, você pode gerenciar seus templates conforme suas necessidades na pasta [resources](resources/), onde você pode encontrar um exemplo de arquivo template.

##### 2. Os templates!

O template é basicamente um arquivo YAML, contendo as chaves respectivas aos nomes das chaves que deseja buscar a informação e o valor é onde esse valor é encontrado. Ao criar uma nova chave, o script de inicialização vai buscar a funcão responsável por essa chave na pasta [funcions](funcions/), que **deve possuir o mesmo nome da chave raiz**, por exemplo:

A chave: *profile_weblogic::single_domain::adminserver::workmanagers* vai buscar uma função chamada *workmanagers*.

##### 3. As funções!

As funções são scripts python executandos dentro do WLST (API não supre as necessidades), portanto, por mais que se pareçam com python, na verdade são scripts **JYTHON**, então, para funcionalidades de bibliotecas mais avançadas, tenha certeza que sua biblioteca é carregável via WLST para que o script JYTHON possa importar.

Os scripts encontrados em [functions](functions/) foram escritos de forma a contornar qualquer uso de bibliotecas terceiras do JYTHON, ou seja, apenas funcionalidades build-in.

#### 4. Executando o script

Agora que voce possui o template que atende suas necessidades e as suas respectivas funções, basta executar o script de inicialização [weblogic_query](weblogic_query.py) com o seguinte argumento:

    $ python2 weblogic_query.py [OPICIONAL]

Onde, o opicional pode ser tanto "-d" de DEBUG ou "-v" de VERBOSE.
Ao final da execução, será gerado um arquivo YAML respectivo a tecnologia com os dados do template respectivos ao do Weblogic informado.

#### Contribuidores

> Gustavo Toledo - gustavot53@gmail.com
> Tiago Albuquerque - tiago.Albuquerque@gmail.com
