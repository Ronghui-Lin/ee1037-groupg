# machine_manager/management/commands/seed_machines.py

from django.core.management.base import BaseCommand
from django.db import IntegrityError
from acme.models import Machine # <-- Make sure this import path is correct for your model

class Command(BaseCommand):
    help = 'Seeds the database with initial Acme Machine data.'

    def handle(self, *args, **options):
        self.stdout.write('Checking if initial machine data needs seeding...')

        # Define the data using Python dictionaries
        machines_data = [
            {
                'name': 'CNC Drilling Machine', 'model': 'MOD-001', 'serial_number': 'SN-001',
                'status': 'operational', 'installation_date': '2023-12-15', 'last_maintenance': '2024-12-15',
                'next_maintenance': '2025-03-15', 'department': 'Manufacturing', 'location': 'Building A',
                'description': 'CNC Drilling Machine for precision drilling operations'
            },
            {
                'name': 'Lamination Press', 'model': 'MOD-002', 'serial_number': 'SN-002',
                'status': 'operational', 'installation_date': '2023-11-02', 'last_maintenance': '2024-11-02',
                'next_maintenance': '2025-02-02', 'department': 'Manufacturing', 'location': 'Building A',
                'description': 'Lamination Press for PCB manufacturing'
            },
            {
                'name': 'Electroplating Machine', 'model': 'MOD-003', 'serial_number': 'SN-003',
                'status': 'operational', 'installation_date': '2024-01-20', 'last_maintenance': '2025-01-20',
                'next_maintenance': '2025-04-20', 'department': 'Manufacturing', 'location': 'Building B',
                'description': 'Electroplating Machine for surface finishing'
            },
            {
                'name': 'Soldering Machine', 'model': 'MOD-004', 'serial_number': 'SN-004',
                'status': 'operational', 'installation_date': '2023-09-28', 'last_maintenance': '2024-09-28',
                'next_maintenance': '2024-12-28', 'department': 'Assembly', 'location': 'Building B',
                'description': 'Automated Soldering Machine for PCB assembly'
            },
            {
                'name': 'Electrical Testing Machine', 'model': 'MOD-005', 'serial_number': 'SN-005',
                'status': 'operational', 'installation_date': '2023-10-14', 'last_maintenance': '2024-10-14',
                'next_maintenance': '2025-01-14', 'department': 'Quality Control', 'location': 'Building C',
                'description': 'Electrical Testing Machine for circuit validation'
            },
            {
                'name': 'Pick and Place Machine', 'model': 'MOD-006', 'serial_number': 'SN-006',
                'status': 'operational', 'installation_date': '2024-02-05', 'last_maintenance': '2025-02-05',
                'next_maintenance': '2025-05-05', 'department': 'Assembly', 'location': 'Building C',
                'description': 'Pick and Place Machine for component mounting'
            },
            {
                'name': 'Automated Optical Inspection', 'model': 'MOD-007', 'serial_number': 'SN-007',
                'status': 'operational', 'installation_date': '2023-08-19', 'last_maintenance': '2024-08-19',
                'next_maintenance': '2024-11-19', 'department': 'Quality Control', 'location': 'Building D',
                'description': 'Automated Optical Inspection for quality assurance'
            },
            {
                'name': 'Automated Test Equipment', 'model': 'MOD-008', 'serial_number': 'SN-008',
                'status': 'operational', 'installation_date': '2023-05-11', 'last_maintenance': '2024-05-11',
                'next_maintenance': '2024-11-19', 'department': 'Quality Control', 'location': 'Building D',
                'description': 'Automated Test Equipment for Testing'
            }
        ]

        # Check if data already exists (optional, but good practice)
        # Let's assume we only seed if the table is empty
        if Machine.objects.exists():
             self.stdout.write(self.style.WARNING('Machine data already exists, skipping seeding.'))
             return

        self.stdout.write('Seeding initial machine data...')
        created_count = 0
        for data in machines_data:
            try:
                Machine.objects.create(**data)
                created_count += 1
            except IntegrityError as e:
                 # This might happen if using update_or_create logic instead and there's a unique constraint issue
                 self.stdout.write(self.style.WARNING(f"Could not add machine {data.get('serial_number', 'N/A')}: {e}"))
            except Exception as e:
                 self.stdout.write(self.style.ERROR(f"Error adding machine {data.get('serial_number', 'N/A')}: {e}"))


        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {created_count} machines.'))


