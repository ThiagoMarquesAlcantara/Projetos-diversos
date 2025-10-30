// Aqui é mais um "caso" para salvar o cadastro dos usuários ou sua respectiva alteração ou exclusão
<?php
    switch ($_REQUEST["acao"]) {
        case 'cadastrar':
            $nome = $_POST["nome"];
            $email = $_POST["email"];
            $senha = md5($_POST["senha"]);
            $dt_nascimento = $_POST["dt_nascimento"];

            $sql = "INSERT INTO usuarios (nome, email, senha, dt_nascimento) VALUES ('{$nome}', '{$email}', '{$senha}', '{$dt_nascimento}')";

            $res = $conn->query($sql);
            break;

            if($res==true){
                print "<script>alert('Cadastrado com sucesso');</script>";
                print "<script>location.href='?page=listar');</script>";
            }else{
                print "<script>alert('Não foi possível cadastrar');</script>";
                print "<script>location.href='?page=listar');</script>";
            }
            break;

        case 'editar':
            $nome = $_POST["nome"];
            $email = $_POST["email"];
            $senha = md5($_POST["senha"]);
            $dt_nascimento = $_POST["dt_nascimento"];
            
            $sql = "UPDATE usuarios SET nome='{$nome}', email='{$email}', senha='{$senha}', dt_nascimento='{$dt_nascimento}'
                WHERE
                    id=".$_REQUEST["id"];
            
            $res = $conn->query($sql);
            break;

            if($res==true){
                print "<script>alert('Editado com sucesso!');</script>";
                print "<script>location.href='?page=listar');</script>";
            }else{
                print "<script>alert('Não foi possível editar!');</script>";
                print "<script>location.href='?page=listar');</script>";
            }

            break;
        case 'excluir':
            $sql = "DELETE FROM usuarios WHERE id=".$_REQUEST["id"];

            $res = $conn->query($sql);
            break;

            if($res==true){
                print "<script>alert('Excluído com sucesso!');</script>";
                print "<script>location.href='?page=listar');</script>";
            }else{
                print "<script>alert('Não foi possível excluir!');</script>";
                print "<script>location.href='?page=listar');</script>";
            }

            break;
    }
?>