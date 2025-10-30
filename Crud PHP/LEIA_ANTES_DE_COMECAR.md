O código foi criado em PHP no "VisualStudio Code" mas você pode desenvolver ele em qualquer editor de código.
O resto tem que ser idêntico.

É necessário a instalação e configuração dos seguintes aplicativos:
XAMPP (https://www.apachefriends.org/download.html).
Baixe conforme seu equipamento de estudo/trabalho (MacIOS, Linux, Windows, 32bits, 64bits, etc...).
Bootstrap (https://getbootstrap.com/docs/5.3/getting-started/download/).

Após isso, na pasta "Xampp" e na pasta "Bootstrap", haverá imagens e textos mostrando e detalhando as configurações.

Você irá executar o Xampp como administrador e startar o "Apache" e o "MySQL" igual ![nessa imagem](../Crud%20PHP/Imagens/apache_mysql.png)

No seu navegador voce vai abrir da seguinte forma (http://localhost/phpmyadmin)
Vai ![clicar em novo](../Crud%20PHP/Imagens/phpmyadmin_novo.png)
Vai ![nomear e clicar em criar](../Crud%20PHP/Imagens/nomear_criar.png) com o nome de cadastro
Vai ![nomear e selecionar o numero de dado](../Crud%20PHP/Imagens/qtd_dados.png) com o nome de "usuários" no nosso caso o numero de dados será 5 (nome, dt_nascimento, senha, id, email)
Muita atenção nessa ultima parte, voce vai colocar em cada campo, os seguintes dados: id, nome, email, senha e dt_nascimento, a ordem não importa, mas as respectivas configurações sim. Como mostro na imagem ![aqui](../Crud%20PHP/Imagens/dados_configurados.png) **OBSERVAÇÃO: NESTA PARTE ESQUECI DE COLOCAR O TAMANHO 255 NO EMAIL TAMBEM, COLOQUEM**
Por fim, vá até o fim da página ![e salve](../Crud%20PHP/Imagens/salvando.png)
Aqui terminam as configurações no banco de dados e é por aqui que voce terá acesso direto.

Para abrir a página do projeto em si, entrar pelo navegador da seguinte forma (http://localhost/projeto_crud/index.php)

Se tudo estiver correto, seu projeto final deve estar ![assim](../Crud%20PHP/Imagens/home.png) na página inicial e nas outras ![assim](../Crud%20PHP/Imagens/novo_usuario.png) e ![assim](../Crud%20PHP/Imagens/listar_usuario.png)

Conforme voce for testando e adicionando usuários, ele irá atualizar e aparecerá no listar usuários. Lembre-se que ele só abrirá no computador em que estiver configurado assim, este seu sistema não está público, logo, apenas você terá acesso.

Obrigado e bons estudos!