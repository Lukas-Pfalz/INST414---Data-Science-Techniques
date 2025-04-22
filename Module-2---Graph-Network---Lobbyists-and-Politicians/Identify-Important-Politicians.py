import requests
import json
from collections import defaultdict

API_KEY = 'YOUR_OPENSECRETS_API_KEY'
BASE_URL = 'https://www.opensecrets.org/api/'

# Util: Fetch data from OpenSecrets API
def fetch_opensecrets_data(method, params):
    params['apikey'] = API_KEY
    params['output'] = 'json'
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code, response.text)
        return None

# Get top politicians (example with House)
def get_politicians():
    params = {
        'method': 'getLegislators',
        'id': 'NY'  # New York as example state
    }
    data = fetch_opensecrets_data('getLegislators', params)
    return data['response']['legislator'] if data else []

# Get contributions to a politician
def get_contributions(crp_id):
    params = {
        'method': 'candContrib',
        'cid': crp_id,
        'cycle': '2024'
    }
    data = fetch_opensecrets_data('candContrib', params)
    if data and 'contributor' in data['response']['contributors']:
        return data['response']['contributors']['contributor']
    return []

# Get lobbying data for a lobbyist
def get_lobbyist_data():
    params = {
        'method': 'getOrgs',
        'org': 'Exxon Mobil'
    }
    data = fetch_opensecrets_data('getOrgs', params)
    return data['response']['organization'] if data else []

# Process politician entity
def build_politician_entity(leg):
    info = leg['@attributes']
    crp_id = info['cid']
    contributions = get_contributions(crp_id)
    lobbyist_money = {}
    for contrib in contributions:
        attribs = contrib['@attributes']
        lobbyist_money[attribs['org_name']] = attribs['total']
    return {
        "type": "Politician",
        "name": info['firstlast'],
        "position": info['office'],
        "party": info['party'],
        "lobbyist_donations": lobbyist_money
    }

# Example of lobbyist entity (manually using Exxon Mobil)
def build_lobbyist_entity():
    org_info = get_lobbyist_data()
    if not org_info:
        return {}
    org = org_info['@attributes']
    # Simulate contribution targets
    example_recipients = {
        "Chuck Schumer": "20000",
        "Kirsten Gillibrand": "15000"
    }
    return {
        "type": "Lobbyist",
        "name": org['orgname'],
        "interest": org['industry'],
        "donations": example_recipients
    }

# Main dataset builder
def build_dataset():
    entities = []

    print("Fetching politicians...")
    politicians = get_politicians()[:5]  # limit to 5 for example
    for leg in politicians:
        p = build_politician_entity(leg)
        entities.append(p)

    print("Fetching lobbyist data...")
    l = build_lobbyist_entity()
    entities.append(l)

    return entities

# Run
if __name__ == "__main__":
    dataset = build_dataset()
    print(json.dumps(dataset, indent=4))


        for actor_id, actor_name in movie['actors']:
            g.add_node(actor_id, name=actor_name)
        for left_actor_id, left_actor_name in movie['actors']:
            for right_actor_id, right_actor_name in movie['actors'][i + 1:]:
                g.add_edge(left_actor_id, right_actor_id)

    degree_centrality = nx.degree_centrality(g)
    eigenvector_centrality = nx.eigenvector_centrality(g)
    # closeness_centrality = nx.closeness_centrality(g)

    nx.draw(g)
