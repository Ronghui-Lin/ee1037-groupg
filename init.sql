INSERT INTO acme_machine (
    name, 
    model, 
    serial_number, 
    status, 
    installation_date, 
    last_maintenance, 
    next_maintenance, 
    department, 
    location, 
    description
) VALUES 
-- CNC Drilling Machine
(
    'CNC Drilling Machine', 
    'MOD-001', 
    'SN-001', 
    'operational', 
    '2023-12-15',
    '2024-12-15',
    '2025-03-15',
    'Manufacturing', 
    'Building A', 
    'CNC Drilling Machine for precision drilling operations'
),
-- Lamination Press
(
    'Lamination Press', 
    'MOD-002', 
    'SN-002', 
    'operational', 
    '2023-11-02', 
    '2024-11-02', 
    '2025-02-02', 
    'Manufacturing', 
    'Building A', 
    'Lamination Press for PCB manufacturing'
),
-- Electroplating Machine
(
    'Electroplating Machine', 
    'MOD-003', 
    'SN-003', 
    'operational', 
    '2024-01-20', 
    '2025-01-20', 
    '2025-04-20', 
    'Manufacturing', 
    'Building B', 
    'Electroplating Machine for surface finishing'
),
-- Soldering Machine
(
    'Soldering Machine', 
    'MOD-004', 
    'SN-004', 
    'operational', 
    '2023-09-28', 
    '2024-09-28', 
    '2024-12-28', 
    'Assembly', 
    'Building B', 
    'Automated Soldering Machine for PCB assembly'
),
-- Electrical Testing Machine
(
    'Electrical Testing Machine', 
    'MOD-005', 
    'SN-005', 
    'operational', 
    '2023-10-14', 
    '2024-10-14', 
    '2025-01-14', 
    'Quality Control', 
    'Building C', 
    'Electrical Testing Machine for circuit validation'
),
-- Pick and Place Machine
(
    'Pick and Place Machine', 
    'MOD-006', 
    'SN-006', 
    'operational', 
    '2024-02-05', 
    '2025-02-05', 
    '2025-05-05', 
    'Assembly', 
    'Building C', 
    'Pick and Place Machine for component mounting'
),
-- Automated Optical Inspection
(
    'Automated Optical Inspection', 
    'MOD-007', 
    'SN-007', 
    'operational', 
    '2023-08-19', 
    '2024-08-19', 
    '2024-11-19', 
    'Quality Control', 
    'Building D', 
    'Automated Optical Inspection for quality assurance'
),
(
    'Automated Test Equipment', 
    'MOD-008', 
    'SN-008', 
    'operational', 
    '2023-05-11', 
    '2024-05-11', 
    '2024-11-19', 
    'Quality Control', 
    'Building D', 
    'Automated Test Equipment for Testing'
);


-- Insert admin user into Django's auth_user table (example)
INSERT INTO auth_user (
    password,
    last_login,
    is_superuser,
    username,
    first_name,
    last_name,
    email,
    is_staff,
    is_active,
    date_joined
) VALUES (
    'pbkdf2_sha256$600000$zTfQyJGVpyhU$5oGbAODJrMWvl2cV7jvO8C+TKQ2Mvb2aRVYKMt6f2XA=',  -- password = admin123
    NOW(),
    TRUE,
    'admin',
    'Admin',
    'User',
    'admin@example.com',
    TRUE,
    TRUE,
    NOW()
);