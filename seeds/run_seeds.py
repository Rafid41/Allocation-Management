import os
import sys
import django
import importlib.util

# Universal Seeding Orchestrator for Allocation Management
# --------------------------------------------------------
# This script orchestrates the serial execution of all numbered provisioning
# scripts (e.g., 1.items.py, 2.pbs_units.py, 3.balances.py) to initialize
# the global system database in the correct relational order.

# 1. Setup Django Environment Context
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Allocation_Management.settings')
django.setup()

def load_seed_module(filename):
    """Dynamically loads and initializes a Python module from the seeds directory."""
    module_name = filename.replace('.py', '')
    module_path = os.path.join(os.path.dirname(__file__), filename)
    
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def orchestrate_seeding():
    """
    Executes the prioritized chain of database provisioning transactions.
    """
    print("\n" + "="*50)
    print("STARTING GLOBAL SYSTEM SEEDING TRANSACTION")
    print("="*50)

    try:
        # Step 1: Master Inventory Items
        print("\n[STEP 1] Executing 1.items.py (Inventory Master Data)...")
        items_seed = load_seed_module("1.items.py")
        items_seed.run_seed()

        # Step 2: Regional Infrastructure (PBS & Zonals)
        print("\n[STEP 2] Executing 2.pbs_pbsAcc_HQ_ZO_SZO.py (PBS & Regional Accounts)...")
        pbs_seed = load_seed_module("2.pbs_pbsAcc_HQ_ZO_SZO.py")
        pbs_seed.run_seed()

        # Step 3: Transactional Master Balances
        print("\n[STEP 3] Executing 3.item_entry_in_zonal_pbs.py (Inventory distributed snapshots)...")
        balance_seed = load_seed_module("3.item_entry_in_zonal_pbs.py")
        balance_seed.run_seed()

        print("\n" + "="*50)
        print("SUCCESS: FULL SYSTEM DATABASE INITIALIZATION COMPLETED.")
        print("="*50 + "\n")

    except Exception as e:
        print("\n" + "!"*50)
        print(f"CRITICAL SEEDING FAILURE: {str(e)}")
        print("!"*50 + "\n")
        sys.exit(1)

if __name__ == "__main__":
    orchestrate_seeding()
