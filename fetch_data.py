import urllib.request
import json
from pynode.main import *

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
    def __init__(self, initial_state):
        self.id = initial_state['id']
        self.title = initial_state['title']
        self.short_title = initial_state['short_title']
        self.api_uri = initial_state['api_uri']
        self.first_name = initial_state['first_name']
        self.middle_name = initial_state['middle_name']
        self.last_name = initial_state['last_name']
        self.suffix = initial_state['suffix']
        self.date_of_birth = initial_state['date_of_birth']
        self.party = initial_state['party']
        self.leadership_role = initial_state['leadership_role']
        self.twitter_account = initial_state['twitter_account']
        self.facebook_account = initial_state['facebook_account']
        self.youtube_account = initial_state['youtube_account']
        self.govtrack_id = initial_state['govtrack_id']
        self.cspan_id = initial_state['cspan_id']
        self.votesmart_id = initial_state['votesmart_id']
        self.icpsr_id = initial_state['icpsr_id']
        self.crp_id = initial_state['crp_id']
        self.google_entity_id = initial_state['google_entity_id']
        self.fec_candidate_id = initial_state['fec_candidate_id']
        self.url = initial_state['url']
        self.rss_url = initial_state['rss_url']
        self.contact_form = initial_state['contact_form']
        self.in_office = initial_state['in_office']
        self.dw_nominate = initial_state['dw_nominate']
        self.ideal_point = initial_state['ideal_point']
        self.seniority = initial_state['seniority']
        self.next_election = initial_state['next_election']
        self.total_votes = initial_state['total_votes']
        self.missed_votes = initial_state['missed_votes']
        self.total_present = initial_state['total_present']
        self.ocd_id = initial_state['ocd_id']
        self.office = initial_state['office']
        self.phone = initial_state['phone']
        self.fax = initial_state['fax']
        self.state = initial_state['state']
        self.senate_class = initial_state['senate_class']
        self.state_rank = initial_state['state_rank']
        self.lis_id = initial_state['lis_id']
        self.missed_votes_pct = initial_state['missed_votes_pct']
        self.votes_with_party_pct = initial_state['votes_with_party_pct']
        pass


class Vote:
    def __init__(self, initial_state):

        # Populate class with data taken from JSON returned by ProPublica's Congress API request.
        # Result is one of the votes returned by a vote endpoint request.

        self.congress = initial_state['congress']
        self.session = initial_state['session']
        self.roll_call = initial_state['roll_call']
        self.chamber = initial_state['chamber']
        self.source = initial_state['source']
        self.url = initial_state['url']
        self.bill = Bill(initial_state['bill'])
        self.amendment = initial_state['amendment']
        self.question = initial_state['question']
        self.description = initial_state['description']
        self.vote_type = initial_state['vote_type']
        self.date = initial_state['date']
        self.time = initial_state['time']
        self.result = initial_state['result']
        self.democratic = Party(initial_state['democratic'])
        self.republican = Party(initial_state['republican'])
        self.independent = VoteTally(initial_state['independent'])
        self.total = VoteTally(initial_state['total'])
        self.positions = initial_state['positions']  # Replace this with positions[member_id] = {stuff}
        self.vacant_seats = initial_state['vacant_seats']


def get_api_key():
    global API_KEY
    api_file = open("propublica_api_key.txt")
    API_KEY = api_file.readline()
    api_file.close()


# Chamber: "house", "senate"
def get_members(chamber):
    request_str = "https://api.propublica.org/congress/v1/115/{chamber}/members.json".format(chamber=chamber)
    request = urllib.request.Request(request_str, headers={'X-API-Key': API_KEY})
    with urllib.request.urlopen(request) as res:
        chamber_members = json.loads(res.read().decode('utf-8'))

    return chamber_members['results']


# Chamber: "both", "house", "senate"
def get_recent_votes(chamber):

    request_str = "https://api.propublica.org/congress/v1/{chamber}/votes/recent.json".format(chamber=chamber)
    request = urllib.request.Request(request_str, headers={'X-API-Key': API_KEY})
    with urllib.request.urlopen(request) as res:
        recent_votes = json.loads(res.read().decode('utf-8'))

    if recent_votes['status'] != 'OK':  # Consider doing something if API status != OK
        pass

    return recent_votes['results']


def get_vote(vote_uri):
    request = urllib.request.Request(vote_uri, headers={'X-API-Key': API_KEY})
    with urllib.request.urlopen(request) as res:
        vote_data = json.loads(res.read().decode('utf-8'))

    return vote_data


def parse_recent_votes(recent_votes):
    vote_count = recent_votes['num_results']
    vote_arr = recent_votes['votes']
    vote_data = {}

    for i in range(vote_count):
        vote_id = vote_arr[i]['roll_call']
        vote_data[vote_id] = get_vote(vote_arr[i]['vote_uri'])

        print(vote_data[vote_id])

    return vote_data

get_api_key()
parse_recent_votes(get_recent_votes("house"))


#def pynode_run():
    #members = getMembers("house")[0]['members']
    #recent_votes = parseRecentVotes(getRecentVotes("house"))

    #vote_edges = {}

    #for i in recent_votes:
    #    vote_edges[i['name']] = i

    #for i in members:
    #    graph.add_node(id=(i['first_name'] + " " + i['last_name']))


#begin_pynode(pynode_run)