# Requisitos Funcionais

| Código | Descrição |
|--------|-----------|
| RF01 | O sistema deve permitir que o usuário se cadastre utilizando um e-mail válido e senha forte |
| RF02 | Recuperação de senha |
| RF03 | Login com autenticação do e-mail e senha |
| RF04 | O sistema deve permitir a criação de projetos, com título e descrição |
| RF05 | Criador e/ou administradores podem alterar permissões de outros usuários dentro da plataforma |
| RF06 | Exibir lista de projetos que o usuário tem acesso |
| RF07 | O usuário criador e/ou administrador do projeto pode editar ou excluir um projeto |
| RF08 | Existência de diferentes níveis de permissões entre usuários em cada projeto (administradores ou colaboradores) |
| RF09 | Criador do projeto pode convidar usuários para participar de projeto, enviando notificação interna e e-mail para aceitar ou recusar |
| RF10 | Usuário pode mencionar outro usuário com @nome e este receberá uma notificação |
| RF11 | O usuário poderá criar tarefas com título, descrição, data e prioridade, podendo visualizar a página específica da tarefa |
| RF12 | As tarefas poderão ser excluídas ou editadas, alterando título, descrição, prazo e status |
| RF13 | Usuário deve poder alterar o status da tarefa (a fazer, em andamento, concluído) |
| RF14 | Tarefas podem ser atribuídas para diferentes usuários associados ao projeto; atribuição feita por administradores |
| RF15 | As tarefas devem ser exibidas em uma lista com os status (a fazer, em andamento ou concluída) |
| RF16 | Usuários poderão ver uma lista com as tarefas, organizadas por prioridades e/ou ordem escolhida por criadores/administradores |
| RF17 | Filtros por prioridades, usuários e data |
| RF18 | Usuários poderão comentar nas tarefas, registrando autor e data |
| RF19 | Opção de editar e excluir o próprio comentário |
| RF20 | Usuário pode mencionar outro usuário com @nome e este receberá uma notificação |
| RF21 | Deve ser mantido um histórico de todas as alterações feitas até o momento na tarefa |
| RF22 | Login pode ser permitido por autenticação via Google e Facebook |
| RF23 | Deve ser enviado um e-mail de verificação após o cadastro |
| RF24 | A senha pode ser recuperada por meio de um processo de recuperação por e-mail |
| RF25 | O usuário poderá escolher o responsável pela tarefa ao gerenciar os usuários (campo de usuários cadastrados) |

# Requisitos não Funcionais

| Código | Descrição |
|--------|-----------|
| RNF01 | A senha deve ter pelo menos 6 caracteres, incluindo números, letras maiúsculas e caracteres especiais |
| RNF06 | Filtro de tarefas por status |
| RNF07 | Organização das tarefas baseadas no status, prazo ou responsável |
| RNF08 | Os comentários serão dispostos em ordem cronológica |
| RNF09 | Os comentários poderão ser excluídos tanto pelo autor quanto pelo responsável do projeto |
| RNF10 | O histórico deve ser acessível a partir da tela de detalhes da tarefa |
| RNF11 | O histórico deve registrar data, hora e o responsável pela alteração |
| RNF12 | O sistema deve suportar um número significativo de usuários simultâneos sem degradação de performance |
| RNF13 | O tempo de resposta para criação ou alteração de uma tarefa não deve ser extenuante |
| RNF14 | Deve-se garantir uma forma eficiente de consulta de dados |
| RNF15 | As informações pessoais devem ser criptografadas |
| RNF16 | Deve ser implementada a autenticação multifatorial |
| RNF17 | A interface deve ser simples e intuitiva |
| RNF18 | O sistema deve ser responsivo, funcionando adequadamente em dispositivos móveis e desktop |
| RNF19 | Deve ser fornecido um feedback claro ao usuário (ex.: confirmações ao cadastrar, editar ou excluir tarefas) |
| RNF20 | O código deve ser bem documentado, permitindo fácil manutenção e expansão |
| RNF21 | O sistema deve ser capaz de recuperar dados após falhas ou quedas de servidor por meio de backup |
