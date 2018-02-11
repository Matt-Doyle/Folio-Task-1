import urllib.request
import json
import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
H = nx.Graph()

from typing import Dict

API_KEY = ""


class Bill:
    def __init__(self, initial_state):
        pass


class VoteTally:
    def __init__(self, initial_state):
        self.yes = initial_state['yes']
        self.no = initial_state['no']
        self.present = initial_state['present']
        self.not_voting = initial_state['not_voting']


class Party(VoteTally):
    def __init__(self, initial_state):
        VoteTally.__init__(self, initial_state)

        self.majority_position = initial_state['majority_position']


# A data structure pertaining to a member of congress
class Member:
    def __init__(self, initial_state: Dict):
        self.id = initial_state.get('id')
        self.title = initial_state.get('title')
        self.short_title = initial_state.get('short_title')
        self.api_uri = initial_state.get('api_uri')
        self.first_name = initial_state.get('first_name')
        self.middle_name = initial_state.get('middle_name')
        self.last_name = initial_state.get('last_name')
        self.suffix = initial_state.get('suffix')
        self.date_of_birth = initial_state.get('date_of_birth')
        self.party = initial_state.get('party')
        self.leadership_role = initial_state.get('leadership_role')
        self.twitter_account = initial_state.get('twitter_account')
        self.facebook_account = initial_state.get('facebook_account')
        self.youtube_account = initial_state.get('youtube_account')
        self.govtrack_id = initial_state.get('govtrack_id')
        self.cspan_id = initial_state.get('cspan_id')
        self.votesmart_id = initial_state.get('votesmart_id')
        self.icpsr_id = initial_state.get('icpsr_id')
        self.crp_id = initial_state.get('crp_id')
        self.google_entity_id = initial_state.get('google_entity_id')
        self.fec_candidate_id = initial_state.get('fec_candidate_id')
        self.url = initial_state.get('url')
        self.rss_url = initial_state.get('rss_url')
        self.contact_form = initial_state.get('contact_form')
        self.in_office = initial_state.get('in_office')
        self.dw_nominate = initial_state.get('dw_nominate')
        self.ideal_point = initial_state.get('ideal_point')
        self.seniority = initial_state.get('seniority')
        self.next_election = initial_state.get('next_election')
        self.total_votes = initial_state.get('total_votes')
        self.missed_votes = initial_state.get('missed_votes')
        self.total_present = initial_state.get('total_present')
        self.ocd_id = initial_state.get('ocd_id')
        self.office = initial_state.get('office')
        self.phone = initial_state.get('phone')
        self.fax = initial_state.get('fax')
        self.state = initial_state.get('state')
        self.senate_class = initial_state.get('senate_class')
        self.state_rank = initial_state.get('state_rank')
        self.lis_id = initial_state.get('lis_id')
        self.missed_votes_pct = initial_state.get('missed_votes_pct')
        self.votes_with_party_pct = initial_state.get('votes_with_party_pct')

    @property
    def full_name(self) -> str:
        return self.first_name + " " + self.last_name


class Vote:
    def __init__(self, initial_state):

        # Populate class with data taken from JSON returned by ProPublica's Congress API request.
        # Result is one of the votes returned by a vote endpoint request.

        self.congress = initial_state['vote']['congress']
        self.session = initial_state['vote']['session']
        self.roll_call = initial_state['vote']['roll_call']
        self.chamber = initial_state['vote']['chamber']
        self.source = initial_state['vote']['source']
        self.url = initial_state['vote']['url']
        self.bill = Bill(initial_state['vote']['bill'])
        self.amendment = initial_state['vote']['amendment']
        self.question = initial_state['vote']['question']
        self.description = initial_state['vote']['description']
        self.vote_type = initial_state['vote']['vote_type']
        self.date = initial_state['vote']['date']
        self.time = initial_state['vote']['time']
        self.result = initial_state['vote']['result']
        self.democratic = Party(initial_state['vote']['democratic'])
        self.republican = Party(initial_state['vote']['republican'])
        self.independent = VoteTally(initial_state['vote']['independent'])
        self.total = VoteTally(initial_state['vote']['total'])
        self.positions = {}

        positions = initial_state['vote']['positions']
        for member in positions:
            self.positions[member['member_id']] = member['vote_position']

        self.vacant_seats = initial_state['vacant_seats']

    def __str__(self):
        vote_tostr = ""
        vote_tostr += "congress: " + str(self.congress)
        vote_tostr += "\nsession: " + str(self.session)
        vote_tostr += "\nroll_call: " + str(self.roll_call)
        vote_tostr += "\nchamber: " + str(self.chamber)
        vote_tostr += "\nsource: " + str(self.source)
        vote_tostr += "\nurl: " + str(self.url)
        vote_tostr += "\nbill: " + str(self.bill)
        vote_tostr += "\namendment: " + str(self.amendment)
        vote_tostr += "\nquestion: " + str(self.question)
        vote_tostr += "\ndescription: " + str(self.description)
        vote_tostr += "\nvote_type: " + str(self.vote_type)
        vote_tostr += "\ndate: " + str(self.date)
        vote_tostr += "\ntime: " + str(self.time)
        vote_tostr += "\nresult: " + str(self.result)
        vote_tostr += "\ndemocratic: " + str(self.democratic)
        vote_tostr += "\nrepublican: " + str(self.republican)
        vote_tostr += "\nindependent: " + str(self.independent)
        vote_tostr += "\ntotal: " + str(self.total)
        vote_tostr += "\npositions: " + str(self.positions)
        vote_tostr += "\nvacant_seats: " + str(self.vacant_seats)

        return vote_tostr


def get_api_key():
    global API_KEY
    api_file = open("propublica_api_key.txt")
    API_KEY = api_file.readline()
    api_file.close()


# Chamber: "house", "senate"
def get_members(chamber: str) -> Dict[str, Member]:
    request_str = "https://api.propublica.org/congress/v1/115/{chamber}/members.json".format(chamber=chamber)
    request = urllib.request.Request(request_str, headers={'X-API-Key': API_KEY})
    with urllib.request.urlopen(request) as res:
        chamber_members = json.loads(res.read().decode('utf-8'))

    member_arr = {}

    for i in chamber_members['results'][0]['members']:
        member_arr[i['id']] = Member(i)

    return member_arr


# Chamber: "both", "house", "senate"
def get_recent_votes(chamber: str):

    request_str = "https://api.propublica.org/congress/v1/{chamber}/votes/recent.json".format(chamber=chamber)
    request = urllib.request.Request(request_str, headers={'X-API-Key': API_KEY})
    with urllib.request.urlopen(request) as res:
        recent_votes = json.loads(res.read().decode('utf-8'))

    if recent_votes['status'] != 'OK':  # Consider doing something if API status != OK
        pass

    return parse_recent_votes(recent_votes['results'])


def get_vote(vote_uri: str):
    request = urllib.request.Request(vote_uri, headers={'X-API-Key': API_KEY})
    with urllib.request.urlopen(request) as res:
        vote_data = Vote(json.loads(res.read().decode('utf-8'))['results']['votes'])

    return vote_data


def parse_recent_votes(recent_votes) -> Dict[int, Vote]:
    vote_count = recent_votes['num_results']
    vote_arr = recent_votes['votes']
    vote_data = {}

    for i in range(vote_count):
        vote_id = vote_arr[i]['roll_call']
        vote_data[vote_id] = get_vote(vote_arr[i]['vote_uri'])

    return vote_data

get_api_key()

vote_nodes = []
democrat_nodes = []
republican_nodes = []
independent_nodes = []
labels = {}
votes_together = {}


def create_graph():
    members = get_members("senate")
    recent_votes = get_recent_votes("senate")

    for i in members:
        G.add_node(members[i].id)
        H.add_node(members[i].id)

        if members[i].party == "D":
            democrat_nodes.append(members[i].id)
        elif members[i].party == "R":
            republican_nodes.append(members[i].id)
        else:
            independent_nodes.append(members[i].id)

        labels[members[i].id] = members[i].full_name

    for i in recent_votes:
        positions: Dict[str, str] = recent_votes[i].positions

        yes_list = []
        no_list = []

        vote_nodes.append(recent_votes[i].roll_call)
        G.add_node(recent_votes[i].roll_call)

        for j in positions:
            if positions[j].lower() == 'yes':
                yes_list.append(j)
            elif positions[j].lower() == 'no':
                no_list.append(j)

        for x in yes_list:
            for y in yes_list:
                if H.get_edge_data(x, y) is not None:
                    H[x][y]['weight'] += 1
                else:
                    H.add_edge(x, y, weight=1)

        for x in no_list:
            for y in no_list:
                if H.get_edge_data(x, y) is not None:
                    H[x][y]['weight'] += 1
                else:
                    H.add_edge(x, y, weight=1)


create_graph()
edge_dict = {}

to_remove = []
weights = []

for u, v, data in H.edges(data=True):
    if data['weight'] < 30:
        to_remove.append([u, v])

for k in to_remove:
    H.remove_edge(k[0], k[1])

for u, v in H.edges():
    weights.append(H[u][v]['weight'] / 40)

pos = nx.kamada_kawai_layout(H)
nx.draw_networkx_nodes(H, pos, nodelist=republican_nodes, node_color='r')
nx.draw_networkx_nodes(H, pos, nodelist=democrat_nodes, node_color='b')
nx.draw_networkx_nodes(H, pos, nodelist=independent_nodes, node_color='y')
nx.draw_networkx_edges(H, pos, alpha=0.8, width=weights)
nx.draw_networkx_labels(H, pos, labels, font_size=4)
plt.show()
