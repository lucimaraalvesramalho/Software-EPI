drop database if exists controle_epi;
CREATE DATABASE Controle_EPI;
use Controle_EPI;

CREATE TABLE funcionarios (
	matricula_funcionario VARCHAR(20) PRIMARY KEY NOT NULL UNIQUE,
    nome_funcionario VARCHAR(100) NOT NULL,
    cpf_funcionario VARCHAR(20) NOT NULL  UNIQUE,
    setor_funcionario VARCHAR(100) NOT NULL,
    funcao_funcionario VARCHAR(100) NOT NULL,
    data_admissao_funcionario DATE NOT NULL,
    telefone varchar(20) NOT NULL, 
    email varchar(100) NOT NULL,
    whatsapp varchar(30)
);

drop table if exists epi;
CREATE TABLE EPI (
    nome_epi VARCHAR(100) NOT NULL,
    tipo_epi VARCHAR(100) NOT NULL,
    certificado_aprovacao_epi VARCHAR(50) PRIMARY KEY NOT NULL  UNIQUE, 
    validade_certificado_aprovacao DATE NOT NULL
);

drop table if exists registros;
CREATE TABLE registros (
    matricula_funcionario VARCHAR(20) NOT NULL,
    ca_EPI varchar(50) NOT NULL,
    data_entrega date DEFAULT (current_date()) NOT NULL,
    data_devolucao date,
    data_troca date,
    motivo_devolucao VARCHAR(300),
    
    FOREIGN KEY(matricula_funcionario) references funcionarios(matricula_funcionario),
    FOREIGN KEY(ca_EPI) references epi(certificado_aprovacao_epi)
);

drop table if exists notificacoes_vencimento;
CREATE TABLE IF NOT EXISTS notificacoes_vencimento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ca_epi VARCHAR(50) NOT NULL,
    matricula_funcionario VARCHAR(50) NOT NULL,
    dias_para_vencimento INT NOT NULL,
    data_verificacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    enviado BOOLEAN DEFAULT FALSE,
    data_envio DATETIME NULL,
    FOREIGN KEY (ca_epi) REFERENCES epi(certificado_aprovacao_epi) ON DELETE CASCADE,
    FOREIGN KEY (matricula_funcionario) REFERENCES funcionarios(matricula_funcionario) ON DELETE CASCADE,
    INDEX idx_ca_epi (ca_epi),
    INDEX idx_matricula (matricula_funcionario),
    INDEX idx_enviado (enviado),
    INDEX idx_dias_vencimento (dias_para_vencimento)
);


INSERT INTO funcionarios (matricula_funcionario, nome_funcionario, cpf_funcionario, setor_funcionario, funcao_funcionario, data_admissao_funcionario, telefone, email, whatsapp) VALUES
('FUNC0001','Ana Souza','111.111.111-01','Administrativo','Assistente','2023-01-10','(34)90001-0001','ana.souza@empresa.com','(34)90001-0001'),
('FUNC0002','Bruno Lima','111.111.111-02','Manutenção','Técnico','2022-05-14','(34)90001-0002','bruno.lima@empresa.com','(34)90001-0002'),
('FUNC0003','Carla Mendes','111.111.111-03','RH','Analista','2021-09-20','(34)90001-0003','carla.mendes@empresa.com','(34)90001-0003'),
('FUNC0004','Diego Alves','111.111.111-04','Produção','Operador','2020-03-11','(34)90001-0004','diego.alves@empresa.com','(34)90001-0004'),
('FUNC0005','Elisa Rocha','111.111.111-05','Segurança','Vigilante','2019-07-01','(34)90001-0005','elisa.rocha@empresa.com','(34)90001-0005'),
('FUNC0006','Felipe Santos','111.111.111-06','Logística','Auxiliar','2023-02-17','(34)90001-0006','felipe.santos@empresa.com','(34)90001-0006'),
('FUNC0007','Gabriela Costa','111.111.111-07','Administrativo','Secretária','2022-11-25','(34)90001-0007','gabriela.costa@empresa.com','(34)90001-0007'),
('FUNC0008','Henrique Silva','111.111.111-08','TI','Suporte','2021-04-09','(34)90001-0008','henrique.silva@empresa.com','(34)90001-0008'),
('FUNC0009','Isabela Pereira','111.111.111-09','Produção','Operador','2020-08-19','(34)90001-0009','isabela.pereira@empresa.com','(34)90001-0009'),
('FUNC0010','João Ferreira','111.111.111-10','Manutenção','Eletricista','2018-12-30','(34)90001-0010','joao.ferreira@empresa.com','(34)90001-0010'),

('FUNC0011','Karen Oliveira','111.111.111-11','RH','Assistente','2022-06-15','(34)90001-0011','karen.oliveira@empresa.com','(34)90001-0011'),
('FUNC0012','Lucas Gomes','111.111.111-12','Produção','Operador','2021-03-03','(34)90001-0012','lucas.gomes@empresa.com','(34)90001-0012'),
('FUNC0013','Mariana Ribeiro','111.111.111-13','Segurança','Vigilante','2020-10-10','(34)90001-0013','mariana.ribeiro@empresa.com','(34)90001-0013'),
('FUNC0014','Nicolas Martins','111.111.111-14','Logística','Motorista','2019-05-22','(34)90001-0014','nicolas.martins@empresa.com','(34)90001-0014'),
('FUNC0015','Olivia Barros','111.111.111-15','Administrativo','Analista','2023-07-07','(34)90001-0015','olivia.barros@empresa.com','(34)90001-0015'),

('FUNC0016','Paulo Teixeira','111.111.111-16','TI','Desenvolvedor','2022-01-13','(34)90001-0016','paulo.teixeira@empresa.com','(34)90001-0016'),
('FUNC0017','Rafaela Nunes','111.111.111-17','Produção','Operador','2021-09-01','(34)90001-0017','rafaela.nunes@empresa.com','(34)90001-0017'),
('FUNC0018','Samuel Vieira','111.111.111-18','Manutenção','Mecânico','2020-02-28','(34)90001-0018','samuel.vieira@empresa.com','(34)90001-0018'),
('FUNC0019','Tatiane Souza','111.111.111-19','RH','Analista','2019-11-11','(34)90001-0019','tatiane.souza@empresa.com','(34)90001-0019'),
('FUNC0020','Ulisses Dias','111.111.111-20','Logística','Auxiliar','2023-03-30','(34)90001-0020','ulisses.dias@empresa.com','(34)90001-0020'),

('FUNC0021','Vanessa Lima','111.111.111-21','Produção','Operador','2022-08-08','(34)90001-0021','vanessa.lima@empresa.com','(34)90001-0021'),
('FUNC0022','William Castro','111.111.111-22','Segurança','Vigilante','2021-12-12','(34)90001-0022','william.castro@empresa.com','(34)90001-0022'),
('FUNC0023','Xavier Rocha','111.111.111-23','Manutenção','Técnico','2020-06-06','(34)90001-0023','xavier.rocha@empresa.com','(34)90001-0023'),
('FUNC0024','Yasmin Andrade','111.111.111-24','Administrativo','Recepcionista','2019-04-04','(34)90001-0024','yasmin.andrade@empresa.com','(34)90001-0024'),
('FUNC0025','Zeca Moreira','111.111.111-25','Produção','Operador','2023-09-09','(34)90001-0025','zeca.moreira@empresa.com','(34)90001-0025'),

('FUNC0026','Amanda Pires','111.111.111-26','RH','Assistente','2022-02-02','(34)90001-0026','amanda.pires@empresa.com','(34)90001-0026'),
('FUNC0027','Bruna Farias','111.111.111-27','Logística','Auxiliar','2021-01-01','(34)90001-0027','bruna.farias@empresa.com','(34)90001-0027'),
('FUNC0028','Caio Cardoso','111.111.111-28','TI','Suporte','2020-07-07','(34)90001-0028','caio.cardoso@empresa.com','(34)90001-0028'),
('FUNC0029','Daniela Reis','111.111.111-29','Produção','Operador','2019-08-18','(34)90001-0029','daniela.reis@empresa.com','(34)90001-0029'),
('FUNC0030','Eduardo Neves','111.111.111-30','Segurança','Vigilante','2018-10-10','(34)90001-0030','eduardo.neves@empresa.com','(34)90001-0030'),

('FUNC0031','Fernanda Azevedo','111.111.111-31','Administrativo','Analista','2023-04-14','(34)90001-0031','fernanda.azevedo@empresa.com','(34)90001-0031'),
('FUNC0032','Gustavo Melo','111.111.111-32','Manutenção','Eletricista','2022-09-19','(34)90001-0032','gustavo.melo@empresa.com','(34)90001-0032'),
('FUNC0033','Helena Pinto','111.111.111-33','RH','Analista','2021-06-06','(34)90001-0033','helena.pinto@empresa.com','(34)90001-0033'),
('FUNC0034','Igor Batista','111.111.111-34','Produção','Operador','2020-11-11','(34)90001-0034','igor.batista@empresa.com','(34)90001-0034'),
('FUNC0035','Juliana Freitas','111.111.111-35','Logística','Motorista','2019-03-03','(34)90001-0035','juliana.freitas@empresa.com','(34)90001-0035'),

('FUNC0036','Kaique Dias','111.111.111-36','TI','Desenvolvedor','2023-05-05','(34)90001-0036','kaique.dias@empresa.com','(34)90001-0036'),
('FUNC0037','Larissa Campos','111.111.111-37','Administrativo','Secretária','2022-10-10','(34)90001-0037','larissa.campos@empresa.com','(34)90001-0037'),
('FUNC0038','Mateus Ramos','111.111.111-38','Produção','Operador','2021-02-14','(34)90001-0038','mateus.ramos@empresa.com','(34)90001-0038'),
('FUNC0039','Natalia Souza','111.111.111-39','Segurança','Vigilante','2020-05-20','(34)90001-0039','natalia.souza@empresa.com','(34)90001-0039'),
('FUNC0040','Otavio Martins','111.111.111-40','Manutenção','Mecânico','2019-09-09','(34)90001-0040','otavio.martins@empresa.com','(34)90001-0040'),

('FUNC0041','Patricia Lopes','111.111.111-41','RH','Assistente','2023-06-06','(34)90001-0041','patricia.lopes@empresa.com','(34)90001-0041'),
('FUNC0042','Rennan Silva','111.111.111-42','Logística','Auxiliar','2022-03-03','(34)90001-0042','rennan.silva@empresa.com','(34)90001-0042'),
('FUNC0043','Sabrina Dias','111.111.111-43','Produção','Operador','2021-07-07','(34)90001-0043','sabrina.dias@empresa.com','(34)90001-0043'),
('FUNC0044','Thiago Rocha','111.111.111-44','TI','Suporte','2020-12-12','(34)90001-0044','thiago.rocha@empresa.com','(34)90001-0044'),
('FUNC0045','Ursula Lima','111.111.111-45','Administrativo','Analista','2019-01-15','(34)90001-0045','ursula.lima@empresa.com','(34)90001-0045'),

('FUNC0046','Victor Hugo','111.111.111-46','Produção','Operador','2023-08-08','(34)90001-0046','victor.hugo@empresa.com','(34)90001-0046'),
('FUNC0047','Wesley Souza','111.111.111-47','Manutenção','Técnico','2022-04-04','(34)90001-0047','wesley.souza@empresa.com','(34)90001-0047'),
('FUNC0048','Yago Ribeiro','111.111.111-48','Segurança','Vigilante','2021-10-10','(34)90001-0048','yago.ribeiro@empresa.com','(34)90001-0048'),
('FUNC0049','Zuleide Costa','111.111.111-49','RH','Analista','2020-01-01','(34)90001-0049','zuleide.costa@empresa.com','(34)90001-0049'),
('FUNC0050','Andre Martins','111.111.111-50','Logística','Motorista','2019-06-06','(34)90001-0050','andre.martins@empresa.com','(34)90001-0050');

truncate table epi;
INSERT INTO epi (nome_epi, tipo_epi, certificado_aprovacao_epi, validade_certificado_aprovacao) VALUES
('Capacete','Proteção Cabeça','CA 000001','2026-06-25'),
('Óculos de proteção','Proteção Olhos','CA 000002','2026-07-18'),
('Luvas de couro','Proteção Mãos','CA 000003','2026-08-05'),
('Botina de segurança','Proteção Pés','CA 000004','2026-09-12'),
('Protetor auricular','Proteção Auditiva','CA 000005','2026-06-21'),
('Máscara PFF2','Proteção Respiratória','CA 000006','2026-10-08'),
('Cinto de segurança','Trabalho em altura','CA 000007','2027-01-15'),
('Capacete com viseira','Proteção Completa','CA 000008','2026-11-03'),
('Luvas nitrílicas','Proteção Química','CA 000009','2026-07-02'),
('Avental de couro','Proteção Corpo','CA 000010','2027-03-18'),
('Máscara solda','Soldagem','CA 000011','2026-12-10'),
('Respirador semi facial','Respiratório','CA 000012','2026-06-28'),
('Luva térmica','Alta temperatura','CA 000013','2027-05-20'),
('Bota PVC','Proteção impermeável','CA 000014','2026-08-27'),
('Óculos ampla visão','Proteção Olhos','CA 000015','2026-07-09'),
('Protetor facial','Face shield','CA 000016','2027-02-14'),
('Macacão químico','Proteção Química','CA 000017','2026-11-22'),
('Capacete industrial','Proteção Cabeça','CA 000018','2028-01-11'),
('Luva látex','Proteção Geral','CA 000019','2026-06-23'),
('Protetor solar EPI','Proteção UV','CA 000020','2026-09-30'),
('Colete refletivo','Sinalização','CA 000021','2027-04-07'),
('Arnês de segurança','Altura','CA 000022','2026-10-14'),
('Trava-quedas','Altura','CA 000023','2026-12-28'),
('Máscara descartável','Respiratório','CA 000024','2026-07-01'),
('Capacete dielétrico','Elétrico','CA 000025','2027-06-19'),
('Luvas isolantes','Elétrico','CA 000026','2028-03-25'),
('Bota dielétrica','Elétrico','CA 000027','2026-08-18'),
('Protetor auricular tipo concha','Auditivo','CA 000028','2026-06-30'),
('Óculos anti impacto','Impacto','CA 000029','2027-01-09'),
('Avental PVC','Químico','CA 000030','2026-09-21'),
('Capacete ventilado','Cabeça','CA 000031','2027-08-12'),
('Luva anticorte','Corte','CA 000032','2026-07-25'),
('Bota antiderrapante','Pés','CA 000033','2026-10-03'),
('Máscara carvão ativado','Respiratório','CA 000034','2027-02-27'),
('Protetor facial solda','Solda','CA 000035','2026-06-26'),
('Capacete com jugular','Cabeça','CA 000036','2027-04-30'),
('Luvas vaqueta','Geral','CA 000037','2026-08-11'),
('Óculos escuro industrial','Proteção Luz','CA 000038','2026-11-16'),
('Avental térmico','Calor','CA 000039','2027-07-08'),
('Máscara full face','Respiratório','CA 000040','2026-09-08'),
('Capacete leve','Cabeça','CA 000041','2028-05-14'),
('Luvas borracha','Químico','CA 000042','2026-07-14'),
('Bota segurança aço','Impacto','CA 000043','2027-03-03'),
('Protetor auditivo plug','Auditivo','CA 000044','2026-06-20'),
('Macacão refletivo','Sinalização','CA 000045','2027-09-17'),
('Respirador industrial','Respiratório','CA 000046','2026-12-05'),
('Óculos ventilado','Olhos','CA 000047','2026-08-31'),
('Luva anti vibração','Vibração','CA 000048','2027-01-28'),
('Capacete alta resistência','Cabeça','CA 000049','2028-02-09'),
('Bota reforçada','Geral','CA 000050','2026-10-25');


truncate table registros;
INSERT INTO registros (matricula_funcionario, ca_EPI, data_entrega, data_devolucao, data_troca, motivo_devolucao) VALUES
('FUNC0001','CA 000001','2026-01-10','2026-04-10',NULL,NULL),
('FUNC0002','CA 000002','2026-01-10','2026-03-10','2026-02-10','Troca por desgaste'),
('FUNC0003','CA 000003','2026-01-11','2026-05-11',NULL,NULL),
('FUNC0004','CA 000004','2026-01-11','2026-03-11','2026-03-01',NULL),
('FUNC0005','CA 000005','2026-01-12','2026-02-12','2026-02-12','Perda do equipamento'),
('FUNC0006','CA 000006','2026-01-12','2026-06-12',NULL,NULL),
('FUNC0007','CA 000007','2026-01-13','2026-03-13','2026-02-13','Dano'),
('FUNC0008','CA 000008','2026-01-13','2026-04-13',NULL,NULL),
('FUNC0009','CA 000009','2026-01-14','2026-05-14',NULL,NULL),
('FUNC0010','CA 000010','2026-01-14','2026-02-14','2026-02-14','Troca preventiva'),

('FUNC0011','CA 000011','2026-01-15','2026-05-15',NULL,NULL),
('FUNC0012','CA 000012','2026-01-15','2026-04-15',NULL,NULL),
('FUNC0013','CA 000013','2026-01-16','2026-02-16','2026-02-16','Desgaste'),
('FUNC0014','CA 000014','2026-01-16','2026-06-16',NULL,NULL),
('FUNC0015','CA 000015','2026-01-17','2026-05-17',NULL,NULL),
('FUNC0016','CA 000016','2026-01-17','2026-03-17','2026-02-17','Quebra'),
('FUNC0017','CA 000017','2026-01-18','2026-06-18',NULL,NULL),
('FUNC0018','CA 000018','2026-01-18','2026-04-18',NULL,NULL),
('FUNC0019','CA 000019','2026-01-19','2026-03-19','2026-02-19','Troca padrão'),
('FUNC0020','CA 000020','2026-01-19','2026-07-19',NULL,NULL),

('FUNC0021','CA 000021','2026-01-20','2026-06-20',NULL,NULL),
('FUNC0022','CA 000022','2026-01-20','2026-02-20','2026-02-20','Perda'),
('FUNC0023','CA 000023','2026-01-21','2026-05-21',NULL,NULL),
('FUNC0024','CA 000024','2026-01-21','2026-04-21',NULL,NULL),
('FUNC0025','CA 000025','2026-01-22','2026-03-22','2026-03-01','Troca por atualização'),

('FUNC0026','CA 000026','2026-01-22','2026-06-22',NULL,NULL),
('FUNC0027','CA 000027','2026-01-23','2026-05-23',NULL,NULL),
('FUNC0028','CA 000028','2026-01-23','2026-02-23','2026-02-23','Dano'),
('FUNC0029','CA 000029','2026-01-24','2026-07-24',NULL,NULL),
('FUNC0030','CA 000030','2026-01-24','2026-06-24',NULL,NULL),

('FUNC0031','CA 000031','2026-01-25','2026-03-25','2026-02-25','Desgaste'),
('FUNC0032','CA 000032','2026-01-25','2026-07-25',NULL,NULL),
('FUNC0033','CA 000033','2026-01-26','2026-06-26',NULL,NULL),
('FUNC0034','CA 000034','2026-01-26','2026-02-26','2026-02-26','Quebra'),
('FUNC0035','CA 000035','2026-01-27','2026-05-27',NULL,NULL),

('FUNC0036','CA 000036','2026-01-27','2026-07-27',NULL,NULL),
('FUNC0037','CA 000037','2026-01-28','2026-03-28','2026-02-28','Troca'),
('FUNC0038','CA 000038','2026-01-28','2026-06-28',NULL,NULL),
('FUNC0039','CA 000039','2026-01-29','2026-07-29',NULL,NULL),
('FUNC0040','CA 000040','2026-01-29','2026-03-01','2026-03-01','Perda'),

('FUNC0041','CA 000041','2026-01-30','2026-06-30',NULL,NULL),
('FUNC0042','CA 000042','2026-01-30','2026-05-30',NULL,NULL),
('FUNC0043','CA 000043','2026-01-31','2026-03-01','2026-03-01','Dano'),
('FUNC0044','CA 000044','2026-01-31','2026-07-31',NULL,NULL),
('FUNC0045','CA 000045','2026-02-01','2026-06-01',NULL,NULL),

('FUNC0046','CA 000046','2026-02-01','2026-03-01','2026-03-01','Desgaste'),
('FUNC0047','CA 000047','2026-02-02','2026-07-02',NULL,NULL),
('FUNC0048','CA 000048','2026-02-02','2026-05-02',NULL,NULL),
('FUNC0049','CA 000049','2026-02-03','2026-03-03','2026-03-03','Troca preventiva'),
('FUNC0050','CA 000050','2026-02-03','2026-07-03',NULL,NULL);
