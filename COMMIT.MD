## 🦄 Commit-Pattern

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

<br>[🔝 Voltar ao topo](#Commit-Pattern) <br>
