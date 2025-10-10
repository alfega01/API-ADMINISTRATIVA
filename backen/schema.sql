-- schema.sql
DROP DATABASE IF EXISTS negocio_db;
CREATE DATABASE negocio_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE negocio_db;

-- Usuarios / Auth (opcional)
CREATE TABLE usuario (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(80) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  nombre VARCHAR(120),
  rol VARCHAR(50),
  creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Clientes
CREATE TABLE cliente (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(255) NOT NULL,
  identificacion VARCHAR(100),
  telefono VARCHAR(50),
  correo VARCHAR(255),
  direccion VARCHAR(255),
  creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Proveedores
CREATE TABLE proveedor (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(255) NOT NULL,
  nit VARCHAR(100),
  telefono VARCHAR(50),
  correo VARCHAR(255),
  direccion VARCHAR(255),
  creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Productos / Stock
CREATE TABLE producto (
  id INT AUTO_INCREMENT PRIMARY KEY,
  codigo VARCHAR(100) UNIQUE,
  nombre VARCHAR(255) NOT NULL,
  categoria VARCHAR(120),
  cantidad INT DEFAULT 0,
  precio DECIMAL(12,2) DEFAULT 0.00,
  creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Facturas (tabla general; tipo = 'compra' o 'venta')
CREATE TABLE factura (
  id INT AUTO_INCREMENT PRIMARY KEY,
  tipo ENUM('compra','venta') NOT NULL,
  numero VARCHAR(100) DEFAULT NULL,
  fecha DATE NOT NULL,
  cliente_id INT NULL,
  proveedor_id INT NULL,
  total DECIMAL(12,2) DEFAULT 0.00,
  notas TEXT,
  creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (cliente_id) REFERENCES cliente(id) ON DELETE SET NULL,
  FOREIGN KEY (proveedor_id) REFERENCES proveedor(id) ON DELETE SET NULL
);

-- Detalle de factura (líneas)
CREATE TABLE factura_linea (
  id INT AUTO_INCREMENT PRIMARY KEY,
  factura_id INT NOT NULL,
  producto_id INT NULL,
  descripcion VARCHAR(500),
  cantidad INT DEFAULT 1,
  precio_unitario DECIMAL(12,2) DEFAULT 0.00,
  subtotal DECIMAL(12,2) GENERATED ALWAYS AS (cantidad * precio_unitario) VIRTUAL,
  FOREIGN KEY (factura_id) REFERENCES factura(id) ON DELETE CASCADE,
  FOREIGN KEY (producto_id) REFERENCES producto(id) ON DELETE SET NULL
);

-- Movimientos generales (para auditoría / últimos movimientos)
CREATE TABLE movimiento (
  id INT AUTO_INCREMENT PRIMARY KEY,
  tipo VARCHAR(50), -- e.g., 'venta', 'compra', 'ajuste'
  referencia_id INT, -- id de la factura u otra entidad
  descripcion VARCHAR(500),
  monto DECIMAL(12,2) DEFAULT 0.00,
  creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Config / Soporte (guardar links a redes)
CREATE TABLE configuracion (
  id INT AUTO_INCREMENT PRIMARY KEY,
  clave VARCHAR(100) NOT NULL UNIQUE,
  valor TEXT,
  actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Datos iniciales (opcional)
INSERT INTO configuracion (clave, valor) VALUES
('soporte_instagram', 'https://instagram.com/tu_perfil'),
('soporte_whatsapp', 'https://wa.me/123456789'),
('soporte_gmail', 'mailto:soporte@tusistema.com');
