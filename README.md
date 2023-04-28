# kivygo

<!---Esses são exemplos. Veja https://shields.io para outras pessoas ou para personalizar este conjunto de escudos. Você pode querer incluir dependências, status do projeto e informações de licença aqui--->

![GitHub repo size](https://img.shields.io/github/repo-size/Heitor-Tasso/kivygo?style=for-the-badge)
![GitHub language count](https://img.shields.io/github/languages/count/Heitor-Tasso/kivygo?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/Heitor-Tasso/kivygo?style=for-the-badge)
![Bitbucket open issues](https://img.shields.io/bitbucket/issues/Heitor-Tasso/kivygo?style=for-the-badge)
![Bitbucket open pull requests](https://img.shields.io/bitbucket/pr-raw/Heitor-Tasso/kivygo?style=for-the-badge)


KivyGO
====

<img align="right" height="256" src="https://raw.githubusercontent.com/kivy/kivy/master/kivy/data/logo/kivy-icon-256.png"/>

Interfaces de usuário inovadoras facilitadas.

KivyGO é um framework [Python] de plataforma cruzada de código aberto (https://www.python.org)
utilizado para o desenvolvimento de aplicações que fazem uso de tecnologias inovadoras,
interfaces de usuário com design complexo e inovador.

KivyGO é licenciado pelo MIT, para ser utilizado em um framework
chamado Kivy [Kivy Organization](https://kivy.org/#organization).

### Ajustes e melhorias

O projeto ainda está em desenvolvimento e as próximas atualizações serão voltadas nas seguintes tarefas:

- [ ] Opção de poder utlizar o Wifi residencial
- [ ] Visualização pela plataforma
- [ ] Média de saúde de cada planta
- [x] Configurar WiFi pelo celular

## 💻 Pré-requisitos

Antes de começar, verifique se você atendeu aos seguintes requisitos:
<!---Estes são apenas requisitos de exemplo. Adicionar, duplicar ou remover conforme necessário--->
* Você instalou o `Python >= 3.9.7`.
* Você tem uma máquina `Windows / Linux / Mac / Android`.


## ☕ Utilizando o kivygo

Para usar o MorePlant, siga estas etapas:

 - Conecte-se à rede Wifi que o ESP8266 está conectado.
 - Inicialize o App e logue com sua conta.
 - Leia o QRCode do ESP8266 e tira e configure a Planta utilizada.
 - Agora é só apertar em iniciar e deixar que sua planta seja monitorada.


## 📫 Contribuindo para o kivygo
<!---Se o seu README for longo ou se você tiver algum processo ou etapas específicas que deseja que os contribuidores sigam, considere a criação de um arquivo CONTRIBUTING.md separado--->
Para contribuir com o kivygo, siga estas etapas:

1. Bifurque este repositório.
2. Crie um branch: `git checkout -b dev`.
3. Faça suas alterações e confirme-as: `git commit -m '<mensagem_commit>'`
4. Envie para o branch: `git push origin dev`
5. Crie a solicitação de pull.

Como alternativa, consulte a documentação do GitHub em [como criar uma solicitação pull](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

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


## 📝 Licença

Esse projeto está sob licença. Veja o arquivo [LICENÇA](LICENSE) para mais detalhes.
Para ver a licença dos repositórios utilizados, Veja o arquivo [LICENÇA](LIB_LICENSE.md) para mais detalhes.

[⬆ Voltar ao topo](#kivygo)<br>
# kivygo


Para ver quantidade de linhas do código no Visual Studio Code:
 - `(gci -include *.kv,*.py -recurse | select-string .).Count`
