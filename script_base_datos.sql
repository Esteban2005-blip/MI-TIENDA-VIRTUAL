-- =====================================================
-- SCRIPT DE BASE DE DATOS - TIENDA VIRTUAL
-- Autor: Proyecto Tienda Virtual
-- Motor: MySQL 8+
-- =====================================================

CREATE DATABASE IF NOT EXISTS tienda_virtual
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE tienda_virtual;

-- =========================
-- TABLA: usuarios
-- =========================
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario  INT AUTO_INCREMENT PRIMARY KEY,
    nombre      VARCHAR(100)  NOT NULL,
    email       VARCHAR(150)  NOT NULL UNIQUE,
    password    VARCHAR(255)  NOT NULL
) ENGINE=InnoDB;

-- =========================
-- TABLA: productos
-- =========================
CREATE TABLE IF NOT EXISTS productos (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    nombre          VARCHAR(150)    NOT NULL,
    descripcion     TEXT,
    precio          DECIMAL(10, 2)  NOT NULL DEFAULT 0.00,
    cantidad        INT             NOT NULL DEFAULT 0,
    categoria       VARCHAR(100),
    imagen          VARCHAR(255),
    fecha_creacion  DATETIME        DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- =========================
-- TABLA: clientes
-- =========================
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente      INT AUTO_INCREMENT PRIMARY KEY,
    nombre          VARCHAR(100)  NOT NULL,
    email           VARCHAR(150)  NOT NULL UNIQUE,
    telefono        VARCHAR(30),
    ciudad          VARCHAR(100),
    direccion       VARCHAR(255),
    total_compras   INT           NOT NULL DEFAULT 0,
    fecha_registro  DATETIME      DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- =========================
-- TABLA: facturas
-- =========================
CREATE TABLE IF NOT EXISTS facturas (
    id_factura      INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente      INT NOT NULL,
    fecha_emision   DATETIME      DEFAULT CURRENT_TIMESTAMP,
    total           DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    metodo_pago     VARCHAR(50),
    estado          VARCHAR(30)   NOT NULL DEFAULT 'Pagada',
    direccion_envio VARCHAR(255),
    nota            VARCHAR(255),
    items_resumen   TEXT,
    CONSTRAINT fk_facturas_clientes
        FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE=InnoDB;

-- =====================================================
-- FIN DEL SCRIPT
-- =====================================================
