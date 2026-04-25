# Projeto: Implementação LGPD - Segundo Mini Projeto Fatec

Este repositório contém o código desenvolvido para o Segundo Mini Projeto da Fatec Rio Claro, focado na aplicação prática da Lei Geral de Proteção de Dados (LGPD). O objetivo central é implementar mecanismos de anonimização e manipulação de dados sensíveis para garantir a conformidade com as normas de privacidade e proteção de direitos fundamentais.
📋 Funcionalidades Implementadas

O projeto foi dividido em quatro atividades principais para lidar com o ciclo de vida e processamento de dados:

    Atividade 1: Anonimização de Dados

        Implementação de rotinas para mascarar informações sensíveis:

            Nome: Mantém a primeira letra e substitui as demais por asteriscos (*).

            CPF: Oculta os caracteres finais.

            E-mail: Aplicação de máscara nos caracteres centrais.

            Telefone: Exibição limitada ao final do número.

    Atividade 2: Exportação Filtrada

        Geração de arquivos (CSV ou XLS) contendo apenas os dados anonimizados de usuários filtrados por ano de nascimento.

    Atividade 3: Relatório Consolidado

        Criação de um arquivo único (CSV ou XLS) contendo Nome e CPF de todos os registros, mantendo os dados originais sem anonimização.

    Atividade 4: Monitoramento de Performance

        Utilização do decorador decorator_tempo.py para medir e registrar o tempo de execução das tarefas de processamento de dados.

🛠 Tecnologias Utilizadas

    Linguagem: Python.

    Banco de Dados: PostgreSQL (via SQLAlchemy).

    Manipulação de Dados: SQLAlchemy ORM e Core.


  Em breve novas atualizações.
