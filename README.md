# Implementação da LGPD - Segundo Mini Projeto Fatec Rio Claro

## Introdução à LGPD

Este projeto foi desenvolvido como parte das atividades acadêmicas da Fatec Rio Claro e visa a aplicação prática da Lei Geral de Proteção de Dados Pessoais (LGPD). A Lei nº 13.709/2018 entrou em vigor em setembro de 2020 e estabelece o marco regulatório sobre a coleta, utilização, armazenamento e compartilhamento de dados pessoais por organizações públicas e privadas.

## Objetivos principais da LGPD:

* Proteger a privacidade e os direitos fundamentais de indivíduos.
* Garantir maior transparência sobre como os dados são utilizados.
* Padronizar as regras de proteção de dados no Brasil.

## Detalhamento das Atividades

*A implementação foca no tratamento técnico de dados sensíveis, estruturada em quatro pilares fundamentais:*

### Atividade 1 - Anonimização

*Processamento de dados para impedir a identificação direta do titular. A função LGPD aplica transformações específicas baseadas nos requisitos de privacidade:*

* Campo	Regra de Anonimização	Exemplo Original	Exemplo Anonimizado
* Nome	Mantém a inicial; substitui as demais letras por asteriscos.	Olivia Araújo	O***** Araújo
* CPF	Oculta os dois blocos centrais e o dígito verificador.	237.615.809-59	237.***.***-**
* E-mail	Mantém a inicial e mascara o restante da parte local antes do @.	nuneserick@example.com	n*********@example.com
* Telefone	Exibe exclusivamente os últimos quatro dígitos.	+55 (011) 9483-6810	6810

### Atividade 2 - Segmentação Anual

*O software filtra a base de dados por ano de nascimento e gera arquivos individuais em formato CSV ou XLS (ex: 1990.xls, 1991.csv). Todos os registros exportados nestes arquivos de segmentação são obrigatoriamente anonimizados conforme as regras da Atividade 1.*

### Atividade 3 - Relatório Geral

*Geração do arquivo consolidado todos.csv (ou todos.xls). Este relatório contém exclusivamente as colunas Nome e CPF em formato original (não anonimizado), simulando uma exportação para uso administrativo interno restrito.*

### Atividade 4 - Monitoramento e Logs

Para assegurar a rastreabilidade e análise de performance, o script utiliza o decorador medir_tempo. Tecnicamente, este decorador utiliza functools.wraps e time.perf_counter() para mensurar com precisão a execução das funções csv_anual_oculto() e csv_geral(). Os logs de execução são registrados simultaneamente no console e no arquivo excucao.log (conforme definido no logging.FileHandler do código).

## Configuração do Ambiente e Banco de Dados

### Configuração do Banco de Dados (.env)

O projeto utiliza variáveis de ambiente para gerenciar a conexão com o banco de dados PostgreSQL. Para execução em ambiente de desenvolvimento, utilize a estrutura abaixo no arquivo .env:

    DB_USER=alunos
    DB_PASSWORD=AlunoFatec
    DB_HOST=200.19.224.150
    DB_PORT=5432
    DB_NAME=atividade2


*Conformidade Técnica:* A utilização de arquivos .env gerenciados pela biblioteca python-dotenv (load_dotenv()) é uma prática essencial de engenharia de software. Ela mitiga o risco de Sensitive Data Exposure (referenciado no OWASP Top 10) e adere à metodologia 12-Factor App, que preconiza a separação estrita entre configurações de ambiente e o código-fonte.

# Requisitos e Execução

## Tecnologias e Dependências

As dependências do projeto estão fixadas ("pinned") no arquivo requirements.txt para garantir a reprodutibilidade do build:

    * SQLAlchemy==2.0.43
    * psycopg2-binary==2.9.12
    * python-dotenv==1.2.2
    * Faker==37.11.0
    * greenlet==3.2.4
    * typing_extensions==4.15.0
    * tzdata==2025.2

## Instruções de Execução

1. Instalação: Instale as bibliotecas necessárias via terminal:
2. Configuração: Crie o arquivo .env na raiz do projeto com as credenciais de desenvolvimento.
3. Conectividade: Certifique-se de possuir acesso à rede para o host 200.19.224.150.
4. Processamento: Execute o script principal:

# Arquivos Ocultos e Segurança (.gitignore)

*O arquivo .gitignore é configurado para evitar que metadados e informações sensíveis sejam rastreados pelo Git:*

    * __pycache__/
    * .env
    * *.csv
    
* pycache__/: Impede o envio de bytecodes compilados.
* .env: Protege as credenciais de acesso ao banco de dados contra exposição pública.
* *.csv: Evita o vazamento de dados gerados que, embora anonimizados em parte, pertencem ao escopo de processamento restrito.

## **Essa configuração é um requisito crítico para manter a integridade do repositório e evitar o vazamento de segredos tecnológicos.**
