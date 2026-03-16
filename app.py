# app.py
from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('wordnet')

app = Flask(__name__)

# ── Load model and vectorizer
with open('crisis_model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('tfidf_vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

# ── Load data files
districts = pd.read_excel('states_districts.xlsx')
cities    = pd.read_excel('union_territories_cities.xlsx')
helplines = pd.read_excel('dataset_3helplines.xlsx')

# ── Build location lookup
dist_state = dict(zip(
    districts['Location_Name'].str.lower().str.strip(),
    districts['State'].str.lower().str.strip()
))
city_ut = dict(zip(
    cities['Location_Name'].str.lower().str.strip(),
    cities['Union_Territory'].str.lower().str.strip()
))

# ── Build helpline lookup
gov_helplines = helplines[helplines['Organization_Type'] == 'Government']
state_helpline = {}
state_org      = {}
for _, row in gov_helplines.iterrows():
    k = row['State_UT'].lower().strip()
    if k not in state_helpline:
        state_helpline[k] = str(row['Helpline_Number'])
        state_org[k]      = str(row['Authority_Name'])

# ── Text preprocessing
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^a-zA-Z ]', '', text)
    words = text.split()
    words = [lemmatizer.lemmatize(w) for w in words if w not in stop_words]
    return ' '.join(words)


# ── Location extractor
def extract_location(text):
    t = text.lower()

    # 1. Common city aliases
    city_aliases = {
        'mumbai':             ('Mumbai',             'Maharashtra'),
        'delhi':              ('Delhi',              'Delhi'),
        'bangalore':          ('Bangalore',          'Karnataka'),
        'bengaluru':          ('Bengaluru',          'Karnataka'),
        'hyderabad':          ('Hyderabad',          'Telangana'),
        'chennai':            ('Chennai',            'Tamil Nadu'),
        'kolkata':            ('Kolkata',            'West Bengal'),
        'pune':               ('Pune',               'Maharashtra'),
        'ahmedabad':          ('Ahmedabad',          'Gujarat'),
        'surat':              ('Surat',              'Gujarat'),
        'jaipur':             ('Jaipur',             'Rajasthan'),
        'lucknow':            ('Lucknow',            'Uttar Pradesh'),
        'kanpur':             ('Kanpur',             'Uttar Pradesh'),
        'nagpur':             ('Nagpur',             'Maharashtra'),
        'patna':              ('Patna',              'Bihar'),
        'indore':             ('Indore',             'Madhya Pradesh'),
        'bhopal':             ('Bhopal',             'Madhya Pradesh'),
        'visakhapatnam':      ('Visakhapatnam',      'Andhra Pradesh'),
        'bhubaneswar':        ('Bhubaneswar',        'Odisha'),
        'coimbatore':         ('Coimbatore',         'Tamil Nadu'),
        'madurai':            ('Madurai',            'Tamil Nadu'),
        'ranchi':             ('Ranchi',             'Jharkhand'),
        'raipur':             ('Raipur',             'Chhattisgarh'),
        'dehradun':           ('Dehradun',           'Uttarakhand'),
        'shimla':             ('Shimla',             'Himachal Pradesh'),
        'guwahati':           ('Guwahati',           'Assam'),
        'varanasi':           ('Varanasi',           'Uttar Pradesh'),
        'agra':               ('Agra',               'Uttar Pradesh'),
        'amritsar':           ('Amritsar',           'Punjab'),
        'ludhiana':           ('Ludhiana',           'Punjab'),
        'kochi':              ('Kochi',              'Kerala'),
        'thiruvananthapuram': ('Thiruvananthapuram', 'Kerala'),
        'vijayawada':         ('Vijayawada',         'Andhra Pradesh'),
        'gurgaon':            ('Gurgaon',            'Haryana'),
        'noida':              ('Noida',              'Uttar Pradesh'),
        'thane':              ('Thane',              'Maharashtra'),
        'imphal':             ('Imphal',             'Manipur'),
        'chandigarh':         ('Chandigarh',         'Chandigarh'),
        'meerut':             ('Meerut',             'Uttar Pradesh'),
    }

    for city, (display, state) in city_aliases.items():
        if city in t:
            return display, state

    # 2. Check districts Excel data
    for loc, state in dist_state.items():
        if loc in t:
            return loc.title(), state.title()

    # 3. Check union territories cities Excel data
    for loc, ut in city_ut.items():
        if loc in t:
            return loc.title(), ut.title()

    # 4. Check state names directly
    state_names = {
        'andhra pradesh':    'Andhra Pradesh',
        'arunachal pradesh': 'Arunachal Pradesh',
        'assam':             'Assam',
        'bihar':             'Bihar',
        'chhattisgarh':      'Chhattisgarh',
        'goa':               'Goa',
        'gujarat':           'Gujarat',
        'haryana':           'Haryana',
        'himachal pradesh':  'Himachal Pradesh',
        'jharkhand':         'Jharkhand',
        'karnataka':         'Karnataka',
        'kerala':            'Kerala',
        'madhya pradesh':    'Madhya Pradesh',
        'maharashtra':       'Maharashtra',
        'manipur':           'Manipur',
        'meghalaya':         'Meghalaya',
        'mizoram':           'Mizoram',
        'nagaland':          'Nagaland',
        'odisha':            'Odisha',
        'punjab':            'Punjab',
        'rajasthan':         'Rajasthan',
        'sikkim':            'Sikkim',
        'tamil nadu':        'Tamil Nadu',
        'telangana':         'Telangana',
        'tripura':           'Tripura',
        'uttar pradesh':     'Uttar Pradesh',
        'uttarakhand':       'Uttarakhand',
        'west bengal':       'West Bengal',
        'delhi':             'Delhi',
        'jammu':             'Jammu & Kashmir',
        'kashmir':           'Jammu & Kashmir',
        'ladakh':            'Ladakh',
    }

    for s_lower, s_display in state_names.items():
        if s_lower in t:
            return s_display, s_display

    return 'Unknown', None


# ── Disaster type detector
def detect_disaster_type(text):
    t = text.lower()
    if re.search(r'flood|water.rising|river.overflow|inundation', t):
        return 'Flood'
    if re.search(r'cyclone|storm|hurricane|typhoon', t):
        return 'Storm'
    if re.search(r'earthquake|tremor|seismic|quake', t):
        return 'Earthquake'
    if re.search(r'landslide|mudslide|rockfall', t):
        return 'Landslide'
    if re.search(r'fire|blaze|burning|flame', t):
        return 'Fire'
    if re.search(r'drought|crop.dying|water.scarcity', t):
        return 'Drought'
    if re.search(r'heatwave|extreme.heat', t):
        return 'Heatwave'
    if re.search(r'accident|crash|vehicle|highway|collision', t):
        return 'Transport'
    if re.search(r'factory|industrial|chemical|gas.leak', t):
        return 'Industrial'
    return 'General'


# ── Help type detector
def detect_help_type(disaster_type):
    mapping = {
        'Flood':      'Rescue',
        'Storm':      'Shelter',
        'Earthquake': 'Medical',
        'Landslide':  'Rescue',
        'Fire':       'Fire Brigade',
        'Drought':    'Relief',
        'Heatwave':   'Medical',
        'Transport':  'Ambulance',
        'Industrial': 'Hazmat',
        'General':    'General Emergency',
    }
    return mapping.get(disaster_type, 'General Emergency')


# ── Confidence score
def get_confidence(level, text):
    t = text.lower()
    high_kws = [
        'trapped', 'critical', 'fatal', 'urgent', 'immediately',
        'need help', 'stuck', 'collapsed', 'many injured',
        'rising', 'overflow', 'rescue'
    ]
    score = sum(2 for k in high_kws if k in t)
    if level == 'High':
        return min(97, 72 + score * 2)
    return max(45, 55 + score * 3)


# ── Routes
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    data    = request.get_json()
    message = data.get('message', '').strip()

    if not message:
        return jsonify({'error': 'Empty message'}), 400

    # 1. Preprocess + predict
    clean = clean_text(message)
    X     = vectorizer.transform([clean])
    level = model.predict(X)[0]

    # 2. Extract location
    location, state = extract_location(message)

    # 3. Disaster type + help
    disaster_type = detect_disaster_type(message)
    help_type     = detect_help_type(disaster_type)

    # 4. Helpline lookup
    if state:
        state_key = state.lower().strip().replace('&', 'and')
        helpline  = state_helpline.get(state_key, '1070')
        org       = state_org.get(state_key, 'State Disaster Management Authority')
    else:
        helpline  = '011-26701700'
        org       = 'NDMA Control Room'

    # 5. Confidence
    confidence = get_confidence(level, message)

    # 6. Return response
    return jsonify({
        'emergency_level': level,
        'confidence':      confidence,
        'location':        location,
        'state':           state or '',
        'disaster_type':   disaster_type,
        'help_type':       help_type,
        'helpline':        helpline,
        'org':             org,
    })


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
