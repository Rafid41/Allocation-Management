import os
import django
import sys
import string
import random

# Setup Django Environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Allocation_Management.settings')
django.setup()

from django.contrib.auth.models import User
from PBSWise_Balance.models import PBS_List, PBS_Zonals
from App_Login.models import User_Group

def generate_pbs_password():
    length = 10
    specials = "!@#$%^&"
    chars_upper = string.ascii_uppercase
    chars_lower = string.ascii_lowercase
    chars_digits = string.digits
    password = [
        random.choice(chars_upper),
        random.choice(chars_lower),
        random.choice(chars_digits),
        random.choice(specials)
    ]
    all_chars = chars_upper + chars_lower + chars_digits + specials
    password += [random.choice(all_chars) for _ in range(length - 4)]
    random.shuffle(password)
    return "".join(password)

def get_pbs_username(pbs_name):
    clean_name = "".join(pbs_name.split())
    return f"breb-pbs-{clean_name}"

def run_seed():
    print("Deleting existing PBS entries and associated regional accounts...")
    
    # Securely delete all Specific_PBS_Account users and groups
    User.objects.filter(user_group__user_group_type="Specific_PBS_Account").delete()
    
    # Delete parent models (cascades to Zonals if configured)
    PBS_List.objects.all().delete()
    PBS_Zonals.objects.all().delete()
    
    pbs_data = {
    "Bagerhat PBS": [
        "HQ",
        "Fakirhat-ZO",
        "Mollahat-ZO",
        "Citolmari-ZO",
        "Rampal-ZO",
        "Khacua-SZO",
        "Rupsha-SZO",
        "Mongla-SZO"
    ],
    "Barishal PBS-1": [
        "HQ",
        "Bakergonj-ZO",
        "Muladhi-ZO",
        "Hizla-SZO",
        "Mehendigonj-ZO"
    ],
    "Barishal PBS-2": [
        "HQ",
        "Agailjhara-ZO",
        "Gournadi-ZO",
        "Banaripara-SZO",
        "Wzirpur-ZO"
    ],
    "Bhola PBS": [
        "HQ",
        "Lalmohon-ZO",
        "Charfassion-ZO",
        "Porangonj-ZO",
        "Dakhin Aicha-SZO",
        "Tajumuddin-SZO",
        "Borhanuddain-SZO"
    ],
    "Bogura PBS-1": [
        "HQ",
        "Kahalu-ZO",
        "Mokamtala-ZO",
        "Dupchacia-ZO",
        "Nondigram-ZO",
        "Pirob-SZO"
    ],
    "Bogura PBS-2": [
        "HQ",
        "Gabtali-ZO",
        "Sherpur-ZO",
        "Sariakandi-ZO",
        "Sonatola-ZO",
        "Dhunot-ZO"
    ],
    "Brahmanbaria PBS": [
        "HQ",
        "Akhaura-ZO",
        "Nabinagar-ZO",
        "Kasba-ZO",
        "Nasirnagar-ZO",
        "Bijoynagar-SZO",
        "Kasba Sadar-ZO",
        "Shibpur-SZO",
        "Sultanpur-SZO",
        "Shamagram-SZO",
        "Auruail-SZO"
    ],
    "Chandpur PBS-1": [
        "HQ",
        "Sharasti-ZO",
        "Kachua-ZO",
        "Sachar-SZO"
    ],
    "Chandpur PBS-2": [
        "HQ",
        "Foridgonj-ZO",
        "Matlab North-ZO",
        "Matlab South-ZO",
        "Kamta-SZO",
        "Haimchor-SZO"
    ],
    "Chittagong PBS-1": [
        "HQ",
        "Lohagara-ZO",
        "Boailkhali-ZO",
        "Banshkhali-ZO",
        "Chandanish-ZO",
        "Anowar-ZO",
        "Satkania-ZO",
        "Karnofuly-ZO",
        "Gunagari-SZO"
    ],
    "Chittagong PBS-2": [
        "HQ",
        "Fatikchari-ZO",
        "Rangunia-ZO",
        "Noapara-ZO",
        "Azadibazar-ZO",
        "Dhamairhat-SZO",
        "Datmara-SZO",
        "Nazirhat-SZO"
    ],
    "Chittagong PBS-3": [
        "HQ",
        "Mirsarai-ZO",
        "Hathazari-ZO",
        "Boroiarhat-ZO",
        "Bangabandhu Sheikh Mujib Shilpanagar-SZO"
    ],
    "Comilla PBS-1": [
        "HQ",
        "Companygonj-ZO",
        "Debidwar-ZO",
        "Borura-ZO",
        "Banggura-ZO",
        "Nawabpur-SZO",
        "Poyalgacha-SZO",
        "Murad Nagor-SZO",
        "Rammohan-SZO",
        "Kutombopur-SZO"
    ],
    "Comilla PBS-2": [
        "HQ",
        "Bagmara-ZO",
        "Chauddagram-ZO",
        "Brahmanpara-ZO",
        "Miya bazar-SZO",
        "Gunbati-ZO",
        "Burichong-ZO",
        "Moynamoti-ZO",
        "Bhushci Bazar-SZO"
    ],
    "Comilla PBS-3": [
        "HQ",
        "Daudkandi-ZO",
        "Homna-ZO",
        "Gojaria-ZO",
        "Bancharampur-ZO",
        "Megna-SZO",
        "Titas-SZO"
    ],
    "Comilla PBS-4": [
        "HQ",
        "Nangolkoat-ZO",
        "Monohorgonj-ZO",
        "Jodda-SZO",
        "Natherpetua-SZO"
    ],
    "Cox'sBazar PBS": [
        "HQ",
        "Teknaf-ZO",
        "Chakaria-ZO",
        "Moheskhali-ZO",
        "Ukhia-ZO",
        "Eidgoan-ZO",
        "Pekuwa-SZO"
    ],
    "Dhaka PBS-1": [
        "HQ",
        "Ashulia-ZO",
        "Sreepur-ZO",
        "Mouchak-ZO",
        "Chandra-ZO",
        "Kaliakair-ZO",
        "Jamgora-ZO",
        "Yearpur-SZO",
        "Bishmile-SZO",
        "Zirani-SZO"
    ],
    "Dhaka PBS-2": [
        "HQ",
        "Dohar-ZO",
        "Bandura-SZO",
        "Narisha-SZO"
    ],
    "Dhaka PBS-3": [
        "HQ",
        "Kushura-ZO",
        "Dhamrai-ZO",
        "Aminbazar-ZO",
        "Shimultala-ZO",
        "Teinari-ZO",
        "Kalampur-ZO",
        "Nawarhat-SZO",
        "Razashon-SZO",
        "Fulbaria-SZO"
    ],
    "Dhaka PBS-4": [
        "HQ",
        "Hasnabad-ZO",
        "Suvadda-ZO",
        "Kalatia-ZO",
        "Abdullahpur-SZO",
        "Ati Bazar-SZO",
        "Ruhitpur-SZO"
    ],
    "Dinajpur PBS-1": [
        "HQ",
        "Ranirbaondar-ZO",
        "Birol-ZO",
        "Birgonj-ZO",
        "Chirirbandor-ZO",
        "Kaharol-SZO",
        "Buchagonj-SZO",
        "Godagari-SZO",
        "Khanshama-SZO"
    ],
    "Dinajpur PBS-2": [
        "HQ",
        "Parbotipur-ZO",
        "Raniganj-ZO",
        "Nawabgonj-ZO",
        "Hilli-SZO",
        "Ambari-SZO",
        "Raniganj-SZO"
    ],
    "Faridpur PBS": [
        "HQ",
        "Boalmari-ZO",
        "Nagarkanda-ZO",
        "Madukhali-ZO",
        "Sadarpur-SZO",
        "Alfadanga-SZO",
        "Puliya-SZO",
        "Saltha-SZO",
        "Corvhodrason-SZO"
    ],
    "Feni PBS": [
        "HQ",
        "Fulgazi-ZO",
        "Chhagolnaiyhan-ZO",
        "Sonagazi-ZO",
        "Dagonbhuyan-ZO",
        "Parshuram-ZO",
        "Rajapur-SZO",
        "Koska-SZO",
        "Kazirhat-SZO"
    ],
    "Gaibandha PBS": [
        "HQ",
        "Bonarpar-ZO",
        "Gobindagonj-ZO",
        "Mohimagonj-SZO",
        "Kalirbazar-SZO",
        "Dariapur-SZO",
        "Palashbari-SZO"
    ],
    "Gazipur PBS-1": [
        "HQ",
        "Chayabithi-ZO",
        "BoardBazar-ZO",
        "Kaligonj-ZO",
        "Konabari-ZO",
        "Pubail-ZO",
        "Kashimpur-ZO",
        "Salna-SZO"
    ],
    "Gazipur PBS-2": [
        "HQ",
        "Kapasiya-ZO",
        "Amraid-SZO"
    ],
    "Gopalgonj PBS": [
        "HQ",
        "Muksudpur-ZO",
        "Kashinai-ZO",
        "Kotalipara-ZO",
        "Tungipara-ZO",
        "Takerhat-SZO",
        "Ramdia-SZO"
    ],
    "Habigonj PBS": [
        "HQ",
        "Nobigonj-ZO",
        "Chunarughat-ZO",
        "Noyapara-ZO",
        "Baniachong-ZO",
        "Bahubol-SZO",
        "Lakhi-ZO",
        "Azmerigonj-SZO",
        "Madobpur-SZO",
        "Enayetgonj-SZO"
    ],
    "Joypurhat PBS": [
        "HQ",
        "Panchbibi-ZO",
        "Akkelpur-ZO",
        "Kalai-ZO",
        "Etakhola-SZO"
    ],
    "Jhalakathi PBS": [
        "HQ",
        "Rajapur-ZO",
        "Nalcity-SZO"
    ],
    "Jamalpur PBS": [
        "HQ",
        "Sorishabari-ZO",
        "Islampur-ZO",
        "Bakshigonj-ZO",
        "Malandha-ZO",
        "Rumari-ZO",
        "Madargonj-ZO",
        "Nandina-ZO",
        "Dawangonj-ZO",
        "Namajer chor/Jaforgonj-SZO",
        "Sanandahbary-SZO",
        "Fulkocha-SZO",
        "Koyra-SZO"
    ],
    "Jessore PBS-1": [
        "HQ",
        "Sarsa-ZO",
        "Bagharpara-ZO",
        "Jhikorgacha-ZO",
        "Chowgacha-ZO",
        "Baganchra-SZO",
        "Bankra-SZO",
        "Rupdia-SZO",
        "Khazura-SZO",
        "Benapole-SZO",
        "Purapa-SZO"
    ],
    "Jessore PBS-2": [
        "HQ",
        "Keshobpur-ZO",
        "Nowapar-ZO",
        "Narail-ZO",
        "Rajgonj-SZO",
        "Laxipasha-ZO",
        "Kalai-ZO",
        "Sagordari-SZO",
        "singari-SZO"
    ],
    "Jhenaidah PBS": [
        "HQ",
        "Mohespur-ZO",
        "Shailpupa-ZO",
        "Kaligonj-ZO",
        "Horinakundu-ZO",
        "Kotchandpur-SZO",
        "Hatfazilpur-SZO",
        "Barobazar-SZO"
    ],
    "Khulna PBS": [
        "HQ",
        "Sanarbazar-ZO",
        "Dumurai-ZO",
        "Paikghacha-ZO",
        "Koyra-ZO",
        "Dacope-SZO",
        "Terokhada-SZO",
        "Shahpur-SZO"
    ],
    "Kishoreganj PBS": [
        "HQ",
        "Nandail-ZO",
        "Kotiyadi-ZO",
        "Hossainpur-ZO",
        "Karimgonj-ZO",
        "Pakundia-ZO",
        "Nikli-SZO",
        "MITHAMOIN-ZO",
        "TARAIL-ZO",
        "Kanurampur-SZO"
    ],
    "Kuri-Lal PBS": [
        "HQ",
        "Nageswari-ZO",
        "Ulipru-ZO",
        "Lalmonirhar-ZO",
        "Adithmari-ZO",
        "Bhurungamari-ZO",
        "Chilmari-ZO",
        "Fulbari-ZO",
        "Kachakata-SZO"
    ],
    "Kustia PBS": [
        "HQ",
        "Dalutpur-ZO",
        "Mirpur-ZO",
        "Kumarkhali-ZO",
        "Bharamara-ZO",
        "Khuksha-SZO",
        "Sastipur-ZO",
        "Poradaha-SZO",
        "Pragpur-SZO"
    ],
    "Laximpur PBS": [
        "HQ",
        "Ramgonj-ZO",
        "Raypur-ZO",
        "Ramgot-ZO",
        "Chandraqngonj-ZO",
        "Vobanigonj-ZO",
        "Komolnogor-ZO"
    ],
    "Madaripur PBS": [
        "HQ",
        "Shibchor-ZO",
        "Kalkini-ZO",
        "Takerhat-ZO",
        "Khoazpur-SZO",
        "Dasar-SZO"
    ],
    "Magura PBS": [
        "HQ",
        "Arpara-ZO",
        "Mohammadpur-ZO",
        "Sreepur-ZO"
    ],
    "Manikgonj PBS": [
        "HQ",
        "Manikgonj-ZO",
        "Singair-ZO",
        "Geyur-ZO",
        "Saturia-ZO",
        "Jhitkha-ZO",
        "Utoli-SZO",
        "Doulotpur-SZO"
    ],
    "Meherpur PBS": [
        "HQ",
        "Chuadanga-ZO",
        "Alomdanga-ZO",
        "Ghangni-ZO",
        "Mojibnagar-SZO",
        "Bamundi-SZO",
        "Jibonnagar-ZO",
        "Dorsona-SZO",
        "Karpasdanga-SZO",
        "Hatboalia-SZO"
    ],
    "Munshigonj PBS": [
        "HQ",
        "Munshigonj-ZO",
        "Tongibari-ZO",
        "Sreenagar-ZO",
        "Sirajdikhan-ZO",
        "Louhajang-ZO",
        "Nowapara-SZO",
        "Nimtola-SZO",
        "Chardumuria-SZO",
        "Vhaggakul-SZO",
        "Dikrirchar-SZO"
    ],
    "Moulavibazar PBS": [
        "HQ",
        "Moulavibazar-ZO",
        "Komolgonj-ZO",
        "Borlekha-ZO",
        "Rajnagar-ZO",
        "Kulaura-SZO",
        "Sindurkhan-SZO"
    ],
    "Mymensingh PBS-1": [
        "HQ",
        "Modhupur-ZO",
        "Fulbaria-ZO",
        "Gopalpur-ZO",
        "Ghatail-ZO",
        "Dahanbari-ZO",
        "Kalibari-SZO",
        "Acim-SZO",
        "Bhuapur\u00a0-SZO"
    ],
    "Mymensingh PBS-2": [
        "HQ",
        "Gophorgaon-ZO",
        "Sreepur-ZO",
        "Mowna-ZO",
        "Trisal-ZO",
        "Batajor-SZO",
        "Jamirdia Masterbari-ZO",
        "Kawraid-SZO"
    ],
    "Mymensingh PBS-3": [
        "HQ",
        "Pulpur-ZO",
        "Ishorgonj-ZO",
        "Dubawura-ZO",
        "Tarakanda-SZO",
        "HALUAGHAT-ZO"
    ],
    "Naogaon PBS-1": [
        "HQ",
        "Niamotpur-ZO",
        "Manda-ZO",
        "Raninagar-ZO",
        "Atria-ZO",
        "Badalgachi-ZO",
        "Satihat-SZO"
    ],
    "Naogaon PBS-2": [
        "HQ",
        "Mohadebpur-ZO",
        "Pursha-ZO",
        "Sapahar-ZO",
        "Dhamerhat-ZO"
    ],
    "Narayangonj PBS-1": [
        "HQ",
        "Modonpur-ZO",
        "Bandar-ZO",
        "Tarabo-ZO",
        "Sonargaon-ZO",
        "Nabigonj-SZO",
        "Barodi-SZO",
        "Maghnaghat-SZO",
        "Borpa-SZO"
    ],
    "Narayangonj PBS-2": [
        "HQ",
        "Purbachal-ZO",
        "Araihajar-ZO",
        "Gopaldi-ZO",
        "Murapara-SZO"
    ],
    "Narsingdi PBS-1": [
        "HQ",
        "Madhabdi-ZO",
        "Ghorashal-ZO",
        "Taltali-SZO"
    ],
    "Narsingdi PBS-2": [
        "HQ",
        "Sadar-ZO",
        "Morjal-ZO",
        "Monohardi-ZO",
        "Shibpur-ZO",
        "Kuliarchar-ZO",
        "Raypura-ZO",
        "Karimpur-SZO",
        "Sarsubuddhi-SZO",
        "Sararchar-SZO",
        "Belab-SZO"
    ],
    "Natore PBS-1": [
        "HQ",
        "Singra-ZO",
        "Puthia-ZO",
        "Bagmara-ZO",
        "Bagatipara-SZO",
        "Naldanga-SZO",
        "Hatgangopara-SZO"
    ],
    "Natore PBS-2": [
        "HQ",
        "Charghat-ZO",
        "Gurudaspur-ZO",
        "Lalpur-ZO",
        "Bagha-ZO",
        "Lakshmikol-SZO",
        "Dayarampur-SZO"
    ],
    "Chapai Nababgonj PBS": [
        "HQ",
        "Shibgonj-ZO",
        "Moharajrur-SZO",
        "Volahat-ZO",
        "Nachol-ZO",
        "Sahapara-SZO"
    ],
    "Netrokona PBS": [
        "HQ",
        "Madan-ZO",
        "Mohongonj-ZO",
        "Durghapur-ZO",
        "Kendua-ZO",
        "Purbodhola-ZO",
        "Kolmakanda-ZO",
        "Atpara-SZO",
        "Dharmapasha-SZO",
        "Barhatta-ZO",
        "Shamgonj-SZO",
        "Khaliajuri-SZO"
    ],
    "Noakhali PBS": [
        "HQ",
        "Senbag-ZO",
        "Companygonj-ZO",
        "Chatkil-ZO",
        "Sonapur-ZO",
        "Sonaimordi-ZO",
        "Kabirhat-ZO",
        "Amin Bazar Z/O",
        "Subornochor-ZO",
        "Noyonpur-SZO"
    ],
    "Nilphamari PBS": [
        "HQ",
        "Domar-ZO",
        "Jaldhaka-ZO",
        "Kishorgonj-ZO",
        "Dimla-SZO"
    ],
    "Pabna PBS-1": [
        "HQ",
        "Dashuria-ZO",
        "Faridpur-SZO",
        "Atghoria-ZO",
        "Bhangura-ZO"
    ],
    "Pabna PBS-2": [
        "HQ",
        "Ataikula-ZO",
        "Bera-ZO",
        "Suzanagar-ZO",
        "Santhia-SZO",
        "Badharhat-SZO",
        "Sheripur-SZO"
    ],
    "Pirojpur PBS": [
        "HQ",
        "Swarupkato-ZO",
        "Morelgonj-ZO",
        "Mothbaria-ZO",
        "Najirpur-ZO",
        "Vandari-SZO",
        "Pathorghata-ZO",
        "ShoronKhula-SZO",
        "BAMNA-SZO"
    ],
    "Patuakhali PBS": [
        "HQ",
        "Bauphal-ZO",
        "Barguna-ZO",
        "Kalapara-ZO",
        "Dashmina-SZO",
        "Amtoli-ZO",
        "Golachipa-ZO",
        "Mirzaganj-SZO",
        "Kuakata-SZO",
        "Rangabali-SZO",
        "Batagi-SZO",
        "Dumki-SZO"
    ],
    "Rajbari PBS": [
        "HQ",
        "Pangsha-ZO",
        "Baliakandi-SZO",
        "Gowalondho-SZO",
        "Kalukhali-SZO"
    ],
    "Rajshahi PBS": [
        "HQ",
        "Durgapur-ZO",
        "Mohonpur-ZO",
        "Tanore-ZO",
        "Kakonhat-ZO"
    ],
    "Rangpur PBS-1": [
        "HQ",
        "Pirgasa-ZO",
        "Pigonj-ZO",
        "Sundargonj-ZO",
        "Sadullahpur-ZO",
        "Vendabari-SZO",
        "Boiratihat-SZO"
    ],
    "Rangpur PBS-2": [
        "HQ",
        "Gangachara-ZO",
        "Kaunia-ZO",
        "Badargonj-ZO",
        "Taragonj-ZO",
        "Haragach-ZO",
        "ModernMoor-SZO",
        "Saidpur-SZO"
    ],
    "Sariatpur PBS": [
        "HQ",
        "Damudya-ZO",
        "Jajira-ZO",
        "Naria-ZO",
        "Sokhipur-ZO",
        "Gosairhat-ZO",
        "Bhedoregonj-SZO",
        "Naodoba-SZO"
    ],
    "Satkhira PBS": [
        "HQ",
        "Jhaudanga-ZO",
        "Kaligonj-ZO",
        "Asashuni-ZO",
        "Shamnagar-ZO",
        "Kalarowa-ZO",
        "Tala-SZO",
        "Debhata-SZO",
        "Budhhata-SZO",
        "Krishnanagar-SZO",
        "Nurnagar-SZO",
        "JugiKhali-SZO"
    ],
    "Sherpur PBS": [
        "HQ",
        "Nalitabari-ZO",
        "Sribordi-ZO",
        "Nukla-SZO",
        "Jhinaigati-SZO"
    ],
    "Sirajgonj PBS-1": [
        "HQ",
        "Shazadpur-ZO",
        "Bhuyaghati-ZO",
        "Tarash-ZO",
        "Khukni-SZO",
        "Salonga-SZO"
    ],
    "Sirajgonj PBS-2": [
        "HQ",
        "Belkhuchi-ZO",
        "Kazipur-ZO",
        "PipulBaria-SZO",
        "Kamarkhand-SZO",
        "Tamai-SZO"
    ],
    "Sunamgonj PBS": [
        "HQ",
        "Chatak-ZO",
        "Biswamvorpur-SZO",
        "Jogonathpur-SZO",
        "Derai-SZO",
        "South Sunamgonj-SZO",
        "Tahirpur-SZO",
        "Doarabazar-SZO",
        "Jamalganj-SZO"
    ],
    "Sylhet PBS-1": [
        "HQ",
        "Goalpgonj-ZO",
        "Osmaninagar-ZO",
        "Zakigonj-ZO",
        "Beanibazar-ZO",
        "Bishwanath-ZO",
        "Fenchuganj-ZO",
        "Balagonj-SZO"
    ],
    "Sylhet PBS-2": [
        "HQ",
        "Companigonj-ZO",
        "Kanaighat-ZO",
        "Shiber Bazar-SZO",
        "Goainghat-SZO",
        "Gachbari-SZO"
    ],
    "Tangail PBS": [
        "HQ",
        "Mirzapur-ZO",
        "Delduar-ZO",
        "Bashail-ZO",
        "Gorai-ZO",
        "Nagorpur-ZO",
        "Elangha-ZO"
    ],
    "Thakurgaon PBS": [
        "HQ",
        "Panchagara-ZO",
        "Pirgaonj-ZO",
        "Boda-SZO",
        "Baliyadangi-ZO",
        "Ranisonkil-ZO",
        "Atwari-SZO",
        "Debiganj-ZO",
        "Ruhia-ZO",
        "Haripur-SZO",
        "ZO+SZO",
        "HQ+ZO+SZO"
    ]
}
    
    total_pbs = len(pbs_data)
    print(f"Provisioning {total_pbs} PBS units and their corresponding zonal network...")
    
    for i, (pbs_name, zonals) in enumerate(pbs_data.items(), 1):
        # 1. Create PBS
        pbs_obj = PBS_List.objects.create(pbs_name=pbs_name)
        
        # 2. Create User Account
        username = get_pbs_username(pbs_name)
        password = generate_pbs_password()
        
        if not User.objects.filter(username=username).exists():
            new_user = User.objects.create_user(username=username, password=password)
            User_Group.objects.create(
                user=new_user, 
                user_group_type="Specific_PBS_Account",
                cleartext_password=password
            )
            
        # 3. Create Zonals
        for zn in zonals:
            trimmed = zn.strip()
            ztype = 'Zonal' # Default
            
            if trimmed == "HQ":
                ztype = 'HQ'
            elif trimmed.endswith('SZO'):
                ztype = 'Sub-Zonal'
            elif trimmed.endswith('ZO'):
                ztype = 'Zonal'
            else:
                # Fallback for complex names like "HQ+ZO+SZO"
                if "HQ" in trimmed: ztype = 'HQ'
                elif "SZO" in trimmed: ztype = 'Sub-Zonal'
                else: ztype = 'Zonal'
            
            PBS_Zonals.objects.create(
                pbs=pbs_obj,
                zonal_name=trimmed,
                zonal_type=ztype
            )
        
        if i % 5 == 0 or i == total_pbs:
            print(f" -> Progress: {i}/{total_pbs} PBS units provisioned...")
            
    print("SUCCESS: Full regional infrastructure provisioning completed.")

if __name__ == "__main__":
    run_seed()
