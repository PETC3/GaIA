---
projeto_pai: "PETCode"
nome_projeto: "Site PET C3"
tipo: "Desenvolvimento Web / Portfólio"
status: "Ativo"
tecnologias: ["HTML5", "CSS3", "Vanilla JavaScript", "SwiperJS", "Vercel", "GitHub"]
link_oficial: "https://petc3.vercel.app/"
---

# Contexto Geral
O sítio eletrônico oficial do PET C3 (https://petc3.vercel.app/) foi completamente reestruturado pela equipe do PETCode. O objetivo principal foi adotar um design moderno e responsivo, sem o uso de frameworks pesados (Vanilla Web). O diferencial do site é a injeção dinâmica de conteúdo via JavaScript (`js/projetos.js`), evitando a repetição de código HTML.

# Hospedagem e Deploy (Como atualizar o site online)
O site está hospedado gratuitamente na plataforma **Vercel**, que possui integração contínua (CI/CD) com o repositório do GitHub.
Para fazer qualquer modificação ir para o ar, não é necessário mexer em servidores manuais. O processo é simples:
1. Faça a alteração no código localmente.
2. Salve as alterações e envie para o GitHub utilizando os comandos `git commit` e `git push`.
3. A Vercel detectará o push automaticamente e atualizará o site oficial em questão de segundos.

# Guias de Manutenção Frequente

Como o PET tem alta rotatividade, as páginas de Membros e Apostilas são as que mais sofrem alterações. Abaixo estão os passos para atualizá-las:

**Como adicionar/atualizar um Membro:**
1. Salve a foto do novo membro (formato quadrado e preferencialmente em `.webp`) na pasta `/imagens/membros/`.
2. Abra o arquivo `paginas/membros.html`.
3. Copie um bloco inteiro de código de um membro existente (a `div` com a classe `image-container efeito`).
4. Cole o bloco na posição desejada dentro da `.grid-container`.
5. Altere o caminho da imagem `<img>`, o nome no `<h3>`, o texto de descrição `<p>` e os links das redes sociais na `div` de `.icon-links`.
6. Faça o commit e push para o GitHub.

**Como adicionar uma nova Apostila no site:**
1. Salve o arquivo `.pdf` da nova apostila na pasta `/Apostilas/`.
2. Abra o arquivo `paginas/apostilas.html`.
3. Copie um bloco de apostila existente (a `div` com a classe `pdf-card`).
4. Altere o ícone (buscando a classe apropriada no FontAwesome), o título `<h3>`, a breve descrição e, principalmente, atualize o link no `href` do botão para apontar para o novo PDF.
5. Faça o commit e push para o GitHub.