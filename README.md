
KivyGO
====

<img align="right" width="30%" src="kivygo/images/icon-kivygo.png"/>

Interfaces de usuário inovadoras facilitadas.

KivyGO é um framework [Python] de plataforma cruzada de código aberto (https://www.python.org)
utilizado para o desenvolvimento de aplicações que fazem uso de tecnologias inovadoras,
interfaces de usuário com design complexo e inovador.

KivyGO é licenciado pelo MIT, para ser utilizado em um framework
chamado Kivy [Kivy Organization](https://kivy.org/#organization).


<!---Esses são exemplos. Veja https://shields.io para outras pessoas ou para personalizar este conjunto de escudos. Você pode querer incluir dependências, status do projeto e informações de licença aqui--->
#
![GitHub repo size](https://img.shields.io/github/repo-size/Heitor-Tasso/kivygo?style=for-the-badge)
![GitHub language count](https://img.shields.io/github/languages/count/Heitor-Tasso/kivygo?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/Heitor-Tasso/kivygo?style=for-the-badge)
![Bitbucket open issues](https://img.shields.io/bitbucket/issues/Heitor-Tasso/kivygo?style=for-the-badge)
![Bitbucket open pull requests](https://img.shields.io/bitbucket/pr-raw/Heitor-Tasso/kivygo?style=for-the-badge)
====
[✅ GoodPractices](#commit-pattern)<br>

### Ajustes e melhorias

O projeto ainda está em desenvolvimento e as próximas atualizações serão voltadas nas seguintes tarefas:

- [ ] Documentação Baseado na do Kivy
- [ ] Exemplo de cada Widget e funcionalidade, em Imagem/Vídeo e Código
- [ ] Definir um theme único para o framework
- [x] Adicionar todos os créditos devidos
- [ ] Refatorar todos widgets e deixá-los no padrão do framework
- [ ] Finalizar o desenvolvimento do uix/codeinput.py

## 💻 Pré-requisitos

Antes de começar, verifique se você atendeu aos seguintes requisitos:
<!---Estes são apenas requisitos de exemplo. Adicionar, duplicar ou remover conforme necessário--->
* Você instalou o `Python >= 3.9.7`.
* Você tem uma máquina `Windows / Linux / Mac / Android`.


## ☕ Utilizando o kivygo

Para usar o KivyGO, siga estas etapas:

 - Instale a lib pelo comando pip `pip install kivygo`.
 - Copie o código de exemplo da biblioteca e inicie.
 - Para fazer a instalação pelo github `pip install git+https://github.com/Heitor-Tasso/kivygo.git#egg=kivygo`.


## 📫 Contribuindo para o kivygo
<!---Se o seu README for longo ou se você tiver algum processo ou etapas específicas que deseja que os contribuidores sigam, considere a criação de um arquivo CONTRIBUTING.md separado--->
Para contribuir com o kivygo, siga estas etapas:

1. Bifurque este repositório.
2. Crie um branch: `git checkout -b dev`.
3. Faça suas alterações e confirme-as: `git commit -m '<mensagem_commit>'`
4. Envie para o branch: `git push origin dev`
5. Crie a solicitação de pull.

Como alternativa, consulte a documentação do GitHub em [como criar uma solicitação pull](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

# Commit Pattern

O commit semântico possui os elementos estruturais abaixo (tipos), que informam a intenção do seu commit ao utilizador(a) de seu código.

- `FEATURE`- Commits do tipo FEATURE indicam que seu trecho de código está incluindo um **novo recurso** (se relaciona com o MINOR do versionamento semântico).

- `FIXED` - Commits do tipo FIXED indicam que seu trecho de código commitado está **solucionando um problema** (bug FIXED), (se relaciona com o PATCH do versionamento semântico).

- `DOC` - Commits do tipo DOC indicam que houveram **mudanças na documentação**, como por exemplo no Readme do seu repositório. (Não inclui alterações em código).

- `TEST` - Commits do tipo TEST são utilizados quando são realizadas **alterações em testes**, seja criando, alterando ou excluindo testes unitários. (Não inclui alterações em código)

- `REQUIRE` - Commits do tipo REQUIRE são utilizados quando são realizadas modificações em **arquivos de REQUIRE e dependências**.

- `PERFORM` - Commits do tipo PERFORM servem para identificar quaisquer alterações de código que estejam relacionadas a **performance**.

- `STYLE` - Commits do tipo STYLE indicam que houveram alterações referentes a **formatações de código**, semicolons, trailing spaces, lint... (Não inclui alterações em código).

- `REFACTOR` - Commits do tipo REFACTOR referem-se a mudanças devido a **refatorações que não alterem sua funcionalidade**, como por exemplo, uma alteração no formato como é processada determinada parte da tela, mas que manteve a mesma funcionalidade, ou melhorias de performance devido a um code review.

## ☑️ Recomendações

- Adicione um título consistente com o título do conteúdo;
- Recomendamos que na primeira linha deve ter no máximo 4 palavras;
- Para descrever com detalhes, usar a descrição do commit;
- Usar um emoji no início da mensagem de commit representando sobre o commit;
- Um link precisa ser adicionado em sua forma mais autêntica, ou seja: sem encurtadores de link e links afiliados;

## 💻 Exemplos
<table>
  <thead>
    <tr>
      <th>Comando git</th>
      <th>Resultado no GitHub</th>
    </tr>
  </thead>
 <tbody>
    <tr>
      <td>
        <code>git commit -m ":tada: Commit inicial"</code>
      </td>
      <td>🎉 Commit inicial</td>
    </tr>
    <tr>
      <td>
        <code>git commit -m ":books: [ DOC ] - Atualizaçao do README"</code>
      </td>
      <td>📚 [ DOC ] - Atualizaçao do README</td>
    </tr>
    <tr>
      <td>
        <code>git commit -m ":bug: [ FIXED ] - Loop infinito na linha 50"</code>
      </td>
      <td>🐛 [ FIXED ] - Loop infinito na linha 50</td>
    </tr>
    <tr>
      <td>
        <code>git commit -m ":sparkles: [ FEATURE ] - Pagina de login"</code>
      </td>
      <td>✨ [ FEATURE ] - Pagina de login</td>
    </tr>
    <tr>
      <td>
        <code>git commit -m ":recycle: [ REFACTOR ] - Passando para arrow functions"</code>
      </td>
      <td>♻️ [ REFACTOR ] - Passando para arrow functions</td>
    </tr>
    <tr>
      <td>
        <code>git commit -m ":zap: [ PERFORM ] - Melhoria no tempo de resposta"</code>
      </td>
      <td>⚡ [ PERFORM ] - Melhoria no tempo de resposta</td>
    </tr>
    <tr>
      <td>
        <code>git commit -m ":boom: [ FIXED ] - Revertendo mudanças ineficientes"</code>
      </td>
      <td>💥 [ FIXED ] - Revertendo mudanças ineficientes</td>
    </tr>
    <tr>
      <td>
        <code>git commit -m ":lipstick: [ FEATURE ] - Estilizaçao CSS do formulario"</code>
      </td>
      <td>💄 [ FEATURE ] - Estilizaçao CSS do formulario</td>
    </tr>
    <tr>
      <td>
        <code>git commit -m ":test_tube: [ TEST ] - Criando novo teste"</code>
      </td>
      <td>🧪 [ TEST ] - Criando novo teste</td>
    </tr>
    <tr>
      <td>
        <code>git commit -m ":bulb: [ DOC ] - Comentários sobre a função LoremIpsum( )"</code>
      </td>
      <td>💡 [ DOC ] - Comentários sobre a função LoremIpsum( )</td>
    </tr>
  </tbody>
</table>

---
# Licenças de Bibliotecas utilizadas no Projeto

Abaixo estão as informações das licenças de cada biblioteca utilizada no projeto:

## Bibliotecas com Licenças Permitidas

- **MIT License:** Utilizada em:
    - [TapTargetView](https://github.com/shashi278/TapTargetView.git)
    - [KivyShaderTransitions](https://github.com/shashi278/KivyShaderTransitions.git)
    - [NeuKivy](https://github.com/Guhan-SenSam/NeuKivy.git)
    - [kivy-gradient](https://github.com/shashi278/kivy-gradient.git)
    - [kivy-circular-progress-bar](https://github.com/TheCodeSummoner/kivy-circular-progress-bar.git)
    - [svg-anim-kivy](https://github.com/shashi278/svg-anim-kivy.git)
    - [frostedglass](https://github.com/kivy-garden/frostedglass.git)
    - [drag_n_drop](https://github.com/kivy-garden/drag_n_drop.git)
    - [garden.pizza](https://github.com/kivy-garden/garden.pizza.git)
    - [garden.rotabox](https://github.com/kivy-garden/garden.rotabox.git)
    - [garden.simpletablelayout](https://github.com/kivy-garden/garden.simpletablelayout.git)
    - [garden.segment](https://github.com/kivy-garden/garden.segment.git)
    - [garden.circularlayout](https://github.com/kivy-garden/garden.circularlayout.git)
    - [garden.navigationdrawer](https://github.com/kivy-garden/garden.navigationdrawer.git)
    - [radialslider](https://github.com/kivy-garden/radialslider.git)
    - [garden.circulardatetimepicker](https://github.com/kivy-garden/garden.circulardatetimepicker.git)
    - [garden.progressspinner](https://github.com/kivy-garden/garden.progressspinner.git)
    - [garden.joystick](https://github.com/kivy-garden/garden.joystick.git)
    - [garden.androidtabs](https://github.com/kivy-garden/garden.androidtabs.git)
    - [kivy-particle](https://github.com/skitoo/kivy-particle.git)
    - [gl-transitions](https://github.com/gl-transitions/gl-transitions.git)

- **GNU GENERAL PUBLIC LICENSE:** Utilizada em:
    - [Resizable-Widget-in-Kivy](https://github.com/FilipeMarch/Resizable-Widget-in-Kivy.git)

- **Nenhuma Licença** Utilizada em:
    - [kivy-pipette](https://github.com/Neizvestnyj/kivy-pipette.git)
    - [CurvyKivy](https://github.com/quitegreensky/CurvyKivy.git)
    - [kivy_shader](https://github.com/adywizard/kivy_shader.git)

---


## 📝 Licença

Esse projeto está sob licença. Veja o arquivo [LICENCE](LICENSE) para mais detalhes.

---

## 🤝 Colaboradores

Agradecemos às seguintes pessoas que contribuíram para este projeto:

<table>
  <tr>
    <td align="center">
      <a href="#">
        <img src="https://avatars.githubusercontent.com/u/87236158?v=4" width="70px;" alt="Foto do Heitor-Tasso no GitHub"/><br>
        <sub>
          <b>Heitor Tasso</b>
        </sub>
      </a>
    </td>
  </tr>
</table>

---

Para ver quantidade de linhas do código no Visual Studio Code:
 - `(gci -include *.kv,*.py -recurse | select-string .).Count`

<br>[⬆ Voltar ao topo](#kivygo)<br>