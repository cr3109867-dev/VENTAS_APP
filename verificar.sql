-- Mostrar todas las tablas creadas
.tables

-- Verificar que exista el usuario admin
SELECT id, nombre, correo, rol FROM usuarios WHERE correo = 'admin@test.com';

-- Verificar que la contraseña está encriptada (no debe ser "1234" en texto plano)
SELECT contraseña FROM usuarios WHERE correo = 'admin@test.com';

-- Verificar que exista el producto de prueba
SELECT id, nombre, cantidad, precio, categoria, proveedor FROM productos WHERE id = 1;
