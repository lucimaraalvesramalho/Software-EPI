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

CREATE TABLE EPI (
    nome_epi VARCHAR(100) NOT NULL,
    tipo_epi VARCHAR(100) NOT NULL,
    certificado_aprovacao_epi VARCHAR(50) PRIMARY KEY NOT NULL  UNIQUE, 
    validade_certificado_aprovacao DATE NOT NULL
);

CREATE TABLE registros (
    matricula_funcionario VARCHAR(20)  PRIMARY KEY NOT NULL,
    ca_EPI varchar(50) NOT NULL,
    data_entrega date DEFAULT (current_date()) NOT NULL,
    data_devolucao date,
    data_troca date,
    motivo_devolucao VARCHAR(300),
    
    FOREIGN KEY(matricula_funcionario) references funcionarios(matricula_funcionario),
    FOREIGN KEY(ca_EPI) references epi(certificado_aprovacao_epi)
);

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
