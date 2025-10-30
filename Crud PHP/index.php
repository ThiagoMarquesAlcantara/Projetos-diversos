// Ao clicar "!" ele vai te dar uma base do código inicial do "HTML" mas pode fazer manualmente.

<!DOCTYPE html>

// Lembre-se de alterar para "pt-BR"
<html lang="pt-BR">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Cadastro</title>
    
    // Aqui você irá linkar o "css" do bootstrap colocando o arquivo dele (normalmente o caminho é o mesmo a seguir).
    <link href="css/bootstrap.min.css" rel="stylesheet">

  </head>  
  <body>

    // Essa navbar esta disponivel no site do bootstrap e tem varias opções lá, basta copiar, colar e configurar à sua vontade. Clicando aqui (https://getbootstrap.com/docs/5.3/components/navbar/#nav) você será redirecionado para a nav que peguei. Após isso, basta configurar.
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">Cadastro</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link active" aria-current="page" href="index.php">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="?page=novo">Novo Usuário</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="?page=listar">Listar Usuários</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
    
    // Essa div é um container que criamos para termos nosso switch. Em outras palavras, é um código que vai levar a fins diferentes conforme a situação. Criaremos um código "PHP" para cada uma dessas opções.
    <div class="container">
        <div class="row">
            <div class="col mt-5">
                <?php
                    include("config.php");
                    switch(@$_REQUEST["page"]){
                        // caso clique em novo
                        case "novo":
                            // redireciona a novo usuário
                            include("novo-usuario.php");
                        break;
                        // caso clique em listar
                        case "listar":
                            // redireciona a listar usuário
                            include("listar-usuario.php");
                        break;
                        // caso clique em salvar
                        case "salvar";
                            // redireciona a salvar usuário
                            include("salvar-usuario.php");
                        break;
                        // caso clique em editar
                        case "editar";
                            // redireciona a editar usuário
                            include("editar-usuario.php");
                        break;
                        //Aqui é um título simples
                        default:
                            print "<h1>Bem vindos ao meu sistema simples de cadastro!</h1>";
                    }
                ?>
            </div>
        </div>
    </div>

    // aqui linkamos o "js" do bootstrap igual fizemos anteriormente com o "css" no inicio do código.
    <script src="js/bootstrap.bundle.min.js"></script>

  </body>
</html>