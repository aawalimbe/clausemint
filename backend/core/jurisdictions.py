# Jurisdictions Configuration for Clausemint

JURISDICTIONS = [
    {
        'name': 'India',
        'legal_system': 'Common Law',
        'default': True,
        'considerations': [
            'Indian Contract Act, 1872',
            'Information Technology Act, 2000',
            'Personal Data Protection Bill considerations',
            'Arbitration and Conciliation Act, 1996'
        ]
    },
    {
        'name': 'United States',
        'legal_system': 'Common Law',
        'default': False,
        'considerations': [
            'State-specific variations',
            'Trade secret protection',
            'Injunctive relief provisions',
            'Federal and state law compliance'
        ]
    },
    {
        'name': 'United Kingdom',
        'legal_system': 'Common Law',
        'default': False,
        'considerations': [
            'English law provisions',
            'UK-specific IP protection',
            'Brexit considerations',
            'UK court jurisdiction'
        ]
    },
    {
        'name': 'European Union',
        'legal_system': 'Civil Law',
        'default': False,
        'considerations': [
            'GDPR compliance',
            'Data protection requirements',
            'Cross-border considerations',
            'EU-specific remedies'
        ]
    },
    {
        'name': 'Canada',
        'legal_system': 'Common Law',
        'default': False,
        'considerations': [
            'Provincial variations',
            'Canadian privacy laws',
            'Federal and provincial jurisdiction',
            'Common law principles'
        ]
    },
    {
        'name': 'Australia',
        'legal_system': 'Common Law',
        'default': False,
        'considerations': [
            'State and territory variations',
            'Australian privacy principles',
            'Common law principles',
            'Federal court jurisdiction'
        ]
    },
    {
        'name': 'Singapore',
        'legal_system': 'Common Law',
        'default': False,
        'considerations': [
            'Singapore law provisions',
            'Personal Data Protection Act',
            'Arbitration-friendly jurisdiction',
            'Common law principles'
        ]
    },
    {
        'name': 'Hong Kong',
        'legal_system': 'Common Law',
        'default': False,
        'considerations': [
            'Hong Kong law provisions',
            'Personal Data (Privacy) Ordinance',
            'Common law principles',
            'International arbitration center'
        ]
    },
    {
        'name': 'Japan',
        'legal_system': 'Civil Law',
        'default': False,
        'considerations': [
            'Japanese Civil Code',
            'Act on the Protection of Personal Information',
            'Civil law principles',
            'Japanese court jurisdiction'
        ]
    },
    {
        'name': 'South Korea',
        'legal_system': 'Civil Law',
        'default': False,
        'considerations': [
            'Korean Civil Code',
            'Personal Information Protection Act',
            'Civil law principles',
            'Korean court jurisdiction'
        ]
    },
    {
        'name': 'Germany',
        'legal_system': 'Civil Law',
        'default': False,
        'considerations': [
            'German Civil Code (BGB)',
            'GDPR compliance',
            'German data protection laws',
            'Civil law principles'
        ]
    },
    {
        'name': 'France',
        'legal_system': 'Civil Law',
        'default': False,
        'considerations': [
            'French Civil Code',
            'GDPR compliance',
            'French data protection laws',
            'Civil law principles'
        ]
    },
    {
        'name': 'Netherlands',
        'legal_system': 'Civil Law',
        'default': False,
        'considerations': [
            'Dutch Civil Code',
            'GDPR compliance',
            'Dutch data protection laws',
            'Civil law principles'
        ]
    },
    {
        'name': 'Switzerland',
        'legal_system': 'Civil Law',
        'default': False,
        'considerations': [
            'Swiss Civil Code',
            'Federal Data Protection Act',
            'Civil law principles',
            'Swiss court jurisdiction'
        ]
    },
    {
        'name': 'Brazil',
        'legal_system': 'Civil Law',
        'default': False,
        'considerations': [
            'Brazilian Civil Code',
            'General Data Protection Law (LGPD)',
            'Civil law principles',
            'Brazilian court jurisdiction'
        ]
    },
    {
        'name': 'Mexico',
        'legal_system': 'Civil Law',
        'default': False,
        'considerations': [
            'Mexican Civil Code',
            'Federal Law on Protection of Personal Data',
            'Civil law principles',
            'Mexican court jurisdiction'
        ]
    },
    {
        'name': 'United Arab Emirates',
        'legal_system': 'Civil Law',
        'default': False,
        'considerations': [
            'UAE Civil Code',
            'UAE data protection laws',
            'Civil law principles',
            'UAE court jurisdiction'
        ]
    },
    {
        'name': 'Saudi Arabia',
        'legal_system': 'Islamic Law',
        'default': False,
        'considerations': [
            'Saudi Civil Code',
            'Saudi data protection laws',
            'Islamic law principles',
            'Saudi court jurisdiction'
        ]
    },
    {
        'name': 'South Africa',
        'legal_system': 'Mixed',
        'default': False,
        'considerations': [
            'South African law',
            'Protection of Personal Information Act',
            'Mixed legal system',
            'South African court jurisdiction'
        ]
    },
    {
        'name': 'International',
        'legal_system': 'Mixed',
        'default': False,
        'considerations': [
            'Choice of law provisions',
            'Dispute resolution mechanisms',
            'Cross-border enforcement',
            'International arbitration clauses'
        ]
    }
]

def get_jurisdictions_list():
    """Get list of jurisdiction names for dropdown"""
    return [jurisdiction['name'] for jurisdiction in JURISDICTIONS]

def get_default_jurisdiction():
    """Get the default jurisdiction"""
    for jurisdiction in JURISDICTIONS:
        if jurisdiction.get('default', False):
            return jurisdiction['name']
    return 'India'  # Fallback default

def get_jurisdiction_details(jurisdiction_name):
    """Get detailed information about a specific jurisdiction"""
    for jurisdiction in JURISDICTIONS:
        if jurisdiction['name'] == jurisdiction_name:
            return jurisdiction
    return None

def get_jurisdiction_considerations(jurisdiction_name):
    """Get legal considerations for a specific jurisdiction"""
    jurisdiction = get_jurisdiction_details(jurisdiction_name)
    if jurisdiction:
        return jurisdiction.get('considerations', [])
    return [] 