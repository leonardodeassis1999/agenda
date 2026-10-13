-- Meu Dia: estrutura do banco de dados
CREATE DATABASE IF NOT EXISTS agenda
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE agenda;

CREATE TABLE IF NOT EXISTS usuarios (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(100) NOT NULL,
  email VARCHAR(150) NOT NULL UNIQUE,
  senha_hash VARCHAR(255) NOT NULL,
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tarefas (
  id INT AUTO_INCREMENT PRIMARY KEY,
  usuario_id INT NOT NULL,
  titulo VARCHAR(150) NOT NULL,
  descricao TEXT NULL,
  categoria VARCHAR(50) NULL,
  prioridade VARCHAR(10) NOT NULL DEFAULT 'media',
  data_prevista DATE NOT NULL,
  tempo_estimado_min INT NOT NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'pendente',
  iniciada_em DATETIME NULL,
  concluida_em DATETIME NULL,
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX ix_tarefas_usuario_id (usuario_id),
  INDEX ix_tarefas_data_prevista (data_prevista),
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);
