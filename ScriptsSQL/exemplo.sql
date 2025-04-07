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

INSERT INTO questionario_secao (titulo, descricao, tipo) VALUES
('Estratégia Empresarial', 'Avalie as questões referentes à ESTRATÉGIA EMPRESARIAL da sua empresa, indicando em uma escala de concordância de 1 a 5 onde 1 significa discordo totalmente e 5 significa concordo totalmente.', 'OBRIGATORIO'),
('Estrutura Organizacional', 'Avalie as questões referentes à ESTRUTURA ORGANIZACIONAL da sua empresa, indicando em uma escala de concordância de 1 a 5 onde 1 significa discordo totalmente e 5 significa concordo totalmente.', 'OBRIGATORIO'),
('Gestão Industrial', 'Avalie as questões referentes à GESTÃO INDUSTRIAL da sua empresa, indicando em uma escala de concordância de 1 a 5 onde 1 significa discordo totalmente e 5 significa concordo totalmente.', 'INDUSTRIA');

INSERT INTO questionario_pergunta (secao_id, pergunta, explicacao) VALUES
('Estratégia Empresarial', 'A empresa possui objetivos de longo prazo (mais de 1 ano).', 'Explicacao'),
('Estrutura Organizacional', 'As tarefas na empresa são claras e de conhecimento de toda a equipe.', 'Explicacao'),
('Gestão Industrial', 'A empresa tem um bom controle de estoque.', 'Explicacao');