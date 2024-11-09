# Upcycle-Crew 

![Tech Stack](https://skillicons.dev/icons?i=python,react)

### Descrição
Esse projeto foi desenvolvido durante o Hackaton BB, no Rec'n Play 2024. O projeto consiste num MVP de um totem de um ponto de descarte de resíduo eletrônico, que utiliza visão computacional para analisar o resíduo a ser descartado pelo usuário. Caso seja um resíduo eletrônico, a lixeira é aberta, recebe o descarte do usuário, e o retorna um agradecimento por e-mail. Caso contrário, a porta não é aberta, informa ao usuário que aquele não é um resíduo válido, e não abre a porta.

Obs: todas as configurações presentes e códigos foram invalidados. para testar a app, é necessário criar novas credenciais no google vision e no SMTP

[Veja o vídeo explicativo do projeto](https://www.youtube.com/embed/xHFCFc4cy6Q?si=075jgECFjIfwg5P1)

### Requisitos
Para rodar esse projeto, é necessário cumprir os seguintes requisitos:

- Python3
- NodeJs
- Npm
- Chave da API da Google Vision

### Execução do projeto
1. Inicialmente, você deve clonar o repositório em seu computador através do comando:

    ```bash
    git clone https://github.com/paulo-campos-57/Upcycle-Crew.git
    ```

2. Quando o projeto estiver clonado, navegue para o diretório `upcycleproject` (onde está localizado o `manage.py`).

3. Nessa pasta, execute o comando:

    ```bash
    pip install -r requirements.txt
    ```

4. Na mesma pasta, crie um arquivo `.env`, e nele insira sua chave de API da Google Vision, sua chave de envio do Django e-mail, seu usuário do e-mail, etc. Para mais informações, recomendamos o vídeo seguinte: [Acesse esse vídeo](https://www.youtube.com/watch?v=iGPPhzhXBFg)

5. No terminal da pasta, execute os seguintes comandos:

    ```bash
    python manage.py makemigrations
    ```

    Agora, o migrate está feito. Você deverá ver uma mensagem de inicialização com alguns clientes criados após essa inicialização. Retenha seus nomes, pois são os primeiros 3 do banco que serão usados para os testes. Lembre-se dos seus CPFs na hora de enviar mensagens pelo front-end.

    ```bash
    python manage.py migrate
    ```

    ```bash
    python manage.py runserver
    ```

6. Com isso, o servidor de BackEnd estará pronto.

7. Abra um novo terminal, e navegue até a pasta `upcyclefront`.

8. Neste terminal, execute os seguintes comandos:

    ```bash
    npm install
    ```

    ```bash
    npm start
    ```

Com isso, o servidor frontend estará pronto, rodando na url `localhost:3000/`.

### Desenvolvedores
<table>
  <tr>
    <td align="center">
      <a href="https://github.com/CarlosAugustoP">
        <img src="https://avatars.githubusercontent.com/u/117591564?v=4" width="100px;" alt="Foto Albert"/><br>
        <sub>
          <b>Carlos Augusto</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/grossiter04">
        <img src="https://avatars.githubusercontent.com/u/116268469?v=4" width="100px;" alt="Foto Caio"/><br>
        <sub>
          <b>Gabriel Rossiter</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/EstelaLacerda">
        <img src="https://avatars.githubusercontent.com/u/117921412?v=4" width="100px;" alt="Foto Stora"/><br>
        <sub>
          <b>Estela Lacerda</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/paulo-campos-57">
        <img src="https://avatars.githubusercontent.com/u/77108503?v=4" width="100px;" alt="Foto Megas"/><br>
        <sub>
          <b>Paulo Campos</b>
        </sub>
      </a>
    </td>
  </tr>
</table>
