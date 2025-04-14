INSERT INTO users_useraccount (
    nomeDeUsuario, 
    email, 
    cnpj, 
    cpf, 
    password, 
    isActive, 
    dataRegistro, 
    dataDesativacao, 
    is_staff, 
    is_superuser
) VALUES 
(
    'joao_silva', 
    'joao.silva@exemplo.com', 
    '12345678000190', 
    '12345678901', 
    'pbkdf2_sha256$260000$abc123$def456ghi789jkl012mno345pqr678stu901vwx234yz', 
    TRUE, 
    '2023-01-15 10:30:00', 
    NULL, 
    FALSE, 
    FALSE
),
(
    'maria_souza', 
    'maria.souza@exemplo.com', 
    '98765432000181', 
    '98765432109', 
    'pbkdf2_sha256$260000$def456$ghi789jkl012mno345pqr678stu901vwx234yz567', 
    TRUE, 
    '2023-02-20 14:45:00', 
    NULL, 
    FALSE, 
    FALSE
),
(
    'carlos_lima', 
    'carlos.lima@exemplo.com', 
    '45678912000172', 
    '45678912304', 
    'pbkdf2_sha256$260000$ghi789$jkl012mno345pqr678stu901vwx234yz567abc', 
    FALSE, 
    '2023-03-10 09:15:00', 
    '2023-06-01 18:00:00', 
    FALSE, 
    FALSE
);

-- Inserindo um usuário administrador
INSERT INTO users_useraccount (
    nomeDeUsuario, 
    email, 
    cnpj, 
    cpf, 
    password, 
    isActive, 
    dataRegistro, 
    dataDesativacao, 
    is_staff, 
    is_superuser
) VALUES 
(
    'admin', 
    'admin@exemplo.com', 
    '11111111000101', 
    '11111111111', 
    'pbkdf2_sha256$260000$xyz789$abc123def456ghi789jkl012mno345pqr678stu901', 
    TRUE, 
    '2023-01-01 00:00:00', 
    NULL, 
    TRUE, 
    TRUE
);

-- Inserindo um usuário da equipe (staff)
INSERT INTO users_useraccount (
    nomeDeUsuario, 
    email, 
    cnpj, 
    cpf, 
    password, 
    isActive, 
    dataRegistro, 
    dataDesativacao, 
    is_staff, 
    is_superuser
) VALUES 
(
    'suporte', 
    'suporte@exemplo.com', 
    '22222222000102', 
    '22222222222', 
    'pbkdf2_sha256$260000$mno345$pqr678stu901vwx234yz567abc123def456ghi789', 
    TRUE, 
    '2023-01-05 08:00:00', 
    NULL, 
    TRUE, 
    FALSE
);

-- Questionario

INSERT INTO questionario_modulo (nome, perguntasQntd, descricao, tempo) VALUES
('Diagnóstico Organizacional', 0, 'O presente formulário é destinado a micro e pequenas empresas que pretendem realizar um diagnóstico de sua situação empresarial. Não há respostas certas ou erradas, as perguntas devem ser respondidas com sinceridade para maior precisão do resultado. O formulário está estruturado em 7 dimensões e o tempo previsto de preenchimento é de 5 minutos.', 0);

INSERT INTO questionario_dimensao (titulo, descricao, tipo, modulo_id) VALUES
('Estratégia Empresarial', 'Avalie as questões referentes à ESTRATÉGIA EMPRESARIAL da sua empresa, indicando em uma escala de concordância de 1 a 5 onde 1 significa discordo totalmente e 5 significa concordo totalmente.', 'OBRIGATORIO', 1),
('Estrutura Organizacional', 'Avalie as questões referentes à ESTRUTURA ORGANIZACIONAL da sua empresa, indicando em uma escala de concordância de 1 a 5 onde 1 significa discordo totalmente e 5 significa concordo totalmente.', 'OBRIGATORIO', 1),
('Gestão de Marketing', 'Avalie as questões referentes à GESTÃO DE MARKETING da sua empresa, indicando em uma escala de concordância de 1 a 5 onde 1 significa discordo totalmente e 5 significa concordo totalmente.', 'OBRIGATORIO', 1),
('Gestão Financeira', 'Avalie as questões referentes à GESTÃO FINANCEIRA da sua empresa, indicando em uma escala de concordância de 1 a 5 onde 1 significa discordo totalmente e 5 significa concordo totalmente.', 'OBRIGATORIO', 1),
('Gestão de Pessoas', 'Avalie as questões referentes à GESTÃO DE PESSOAS da sua empresa, indicando em uma escala de concordância de 1 a 5 onde 1 significa discordo totalmente e 5 significa concordo totalmente.', 'OBRIGATORIO', 1),
('ESG', 'Avalie as questões referentes às políticas ESG (Ambiental, Social e Governança) da sua empresa, indicando em uma escala de concordância de 1 a 5 onde 1 significa discordo totalmente e 5 significa concordo totalmente.', 'OBRIGATORIO', 1),
('Gestão Comercial', 'Avalie as questões referentes à GESTÃO COMERCIAL da sua empresa, indicando em uma escala de concordância de 1 a 5 onde 1 significa discordo totalmente e 5 significa concordo totalmente.', 'COMERCIO', 1),
('Gestão Industrial', 'Avalie as questões referentes à GESTÃO INDUSTRIAL da sua empresa, indicando em uma escala de concordância de 1 a 5 onde 1 significa discordo totalmente e 5 significa concordo totalmente.', 'INDUSTRIA', 1),
('Prestação de Serviços', 'Avalie as questões referentes à Prestação de Serviços da sua empresa, indicando em uma escala de concordância de 1 a 5 onde 1 significa discordo totalmente e 5 significa concordo totalmente.', 'SERVICO', 1);

INSERT INTO questionario_pergunta (pergunta, explicacao, dimensao_id) VALUES
('As tarefas na empresa são claras e de conhecimento de toda a equipe.', 'explicacao', 1);

INSERT INTO questionario_pergunta (pergunta, explicacao, dimensao_id) VALUES
('As tarefas na empresa são claras e de conhecimento de toda a equipe.', 'explicacao', 2),
('Os processos dentro da empresa estão bem definidos.', 'explicacao', 2),
('As funções das pessoas e equipes dentro da sua empresa estão bem-organizadas.', 'explicacao', 2),
('Sua empresa possui uma clara organização e estruturação interna.', 'explicacao', 2),
('As atividades na empresa possuem um bom fluxo de trabalho.', 'explicacao', 2);