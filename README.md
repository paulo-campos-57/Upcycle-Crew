# Upcycle-Crew 
<img src="https://skillicons.dev/icons?i=python,react" /><br>
<h3>Descrição</h3>
Esse projeto foi desenvolvido durante o Hackaton BB, no Rec'n Play 2024. O projeto consiste num MVP de um totem de um ponto de descarte de resíduo eletrônico, que utiliza visão computacional para analisar o resíduo a ser descartado pelo usuário. Caso seja um resíduo eletrônico, a lixeira é aberta, recebe o descarte do usuário, e o retorna um agradecimento por e-mail. Caso contrário, a porta não é aberta, informa ao usuário que aquele não é um resíduo válido, e não abre a porta. 

<h3>Requisitos</h3>
Para rodar esse projeto, é necesário cumprir os seguintes requisitos:<br>
<table>
  <tr>- Python3</tr><br>
  <tr>- NodeJs</tr><br>
  <tr>- Npm</tr><br>
  <tr>- Chave da API da Google Vision</tr>
</table>

<h3>Execução do projeto</h3>
<table>
  <tr>- Inicialmente, você deve clonar o repositório em seu computador através do comando: 
    <dt>

      git clone https://github.com/paulo-campos-57/Upcycle-Crew.git
  </dt>
  </tr>
  <tr>- Quando o projeto estiver clonado, navegue para o diretório upcycleproject (onde está localizado o manage.py)</tr><br>
  <tr>- Nessa pasta, execute o comando
    <dt>

      pip install -r requirements.txt
  </dt>
  </tr>
  <tr>- Na mesma pasta, crie um arquvo .env, e nele insira sua chave de API da Google Vision</tr><br>
  <tr>- Na terminal da pasta, execute os seguintes comandos:
    <dt>

      python manage.py makemigrations
  </dt>
  <dt>

      python manage.py migrate
  </dt>
  <dt>

      python manage.py runserver
  </dt>
  </tr>
  <tr>- Com isso, o servidor de BackEnd estará pronto.</tr><br>
  <tr>- Abra um novo terminal, e navegue até a pasta upcyclefront</tr><br>
  <tr>- Neste terminal, execute os seguintes comandos: 
    <dt>

      npm install
  </dt>
  <dt>

      npm start
  </dt>
  </tr>
  <tr>Com isso, servidor frontend estará pronto, rodando na url localhost:3000/</tr>
</table>

<h3>Desenvolvedores</h3>
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
