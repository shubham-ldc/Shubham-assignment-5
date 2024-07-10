import json
import hashlib 
from uuid import uuid4 as v4
from collections import defaultdict

def hash_user_password(password):
    hash = hashlib.sha256(password.encode())
    hash = hash.hexdigest()
    return hash


def validate_hash_password(password, hash):
    hash_password = hash_user_password(password)
    
    if hash_password == hash:
        return True
    
    return False

def read_data_from_json_file(file_path):
    try:
        database = open(file_path)
        content = json.load(database)
        # print("read call")
        return content

    except json.JSONDecodeError:
        raise Exception(f"Unable to read user.json file")

def write_data_to_json_file(data, file_path):
    # file_path = 'users.json'
    try:
        #first read data.json file
        
        content = read_data_from_json_file(file_path)

        #open file as write mode
        database = open(file_path, 'w')

        #add new user_data to existing content
        content[data['_id']] = data
        
        #stringify the content from json
        content = json.dumps(content)

        #write new content to data.json file
        database.write(content)

        return content
        
    except Exception as error:
        print("write_file_exception", error)
        raise Exception(f"unable to write in {file_path}! {str(error)}")
  
def get_user_details(search_key,search_value):
    users = read_data_from_json_file('users.json')
    # print(users)
    for _, value in users.items():
        if value[search_key] == search_value:
            return value
    return None

def get_user_by_email(email):
    users = read_data_from_json_file('users.json')
    # print(users)
    for _, value in users.items():
        if value['email'] == email:
            return value
    return None

def update_json_file(id,data,file_path):
    try:
        
        content = read_data_from_json_file(file_path)

        user_to_update = content[id]
        for key , value in data.items():
            if isinstance(user_to_update[key],list):
                print("hello")
                user_to_update[key].append(value)
            else:
                user_to_update[key] = value
        write_data_to_json_file(user_to_update,file_path)
        return user_to_update
    
    except Exception as error:
        print("write_file_exception", error)
        raise Exception(f"Internal server error! {str(error)}")
    
def generate_uuid_id():
    return str(v4())


def create_post_data(scheme_data):
    _id = generate_uuid_id()
    scheme_name = scheme_data.get('scheme_name', "NA")
    scheme_type = scheme_data.get('scheme_type', "NA")
    creator_id = scheme_data.get('created_by', "NA")

    title = f"{scheme_name} - {scheme_type}"
    description = f"This post relates to the scheme named '{scheme_name}' of type '{scheme_type}'. Here we will provide updates, news, and important information about the scheme. Stay tuned for more details and how you can benefit from it."

    return {
        "title": title,
        "description": description,
        "created_by": creator_id,
        "_id": _id
    }



def get_user_scheme_data(user_id):

    all_users_data = read_data_from_json_file('users.json')
    all_schemes_data = read_data_from_json_file('schemes.json')

    current_user = all_users_data[user_id]
    user_scheme_id_list =current_user['created_scheme']

    user_scheme_data = []

    user_scheme_data = [all_schemes_data[scheme_id] for scheme_id in user_scheme_id_list ]

    # for scheme_id in user_scheme_id_list:
    #     if all_schemes_data.get(scheme_id):
    #         user_scheme_data.append(all_schemes_data.get(scheme_id))
    return user_scheme_data

def get_user_post_data(user_id):

    all_users_data = read_data_from_json_file('users.json')
    all_posts_data = read_data_from_json_file('posts.json')

    current_user = all_users_data[user_id]
    user_post_id_list =current_user['created_post']

    user_post_data = [all_posts_data[post_id] for post_id in user_post_id_list ]

    # for post_id in user_post_id_list:
    #     if all_posts_data.get(post_id):
    #         user_post_data.append(all_posts_data.get(post_id))
    return user_post_data



def create_user_scheme_portfolio(owner_id):
    data = read_data_from_json_file('schemes.json')
    # Filter schemes by owner_id
    user_schemes = [scheme for scheme in data.values() if scheme['created_by'] == owner_id]
    
    # Initialize a dictionary to hold counts and amounts for each scheme type
    portfolio_summary = defaultdict(lambda: {'count': 0, 'amount': 0})

    # Process the data to count schemes and sum their amounts
    for scheme in user_schemes:
        scheme_type = scheme['scheme_type'].lower().replace(" ", "-")
        portfolio_summary[scheme_type]['count'] += 1
        portfolio_summary[scheme_type]['amount'] += scheme['amount']
    
    # Convert defaultdict to a regular dict for the JSON response
    portfolio_summary = dict(portfolio_summary)
    print("portfolio" , portfolio_summary)
    return portfolio_summary
    

def get_top_n_investment_schemes(n):
    data = read_data_from_json_file('schemes.json')
    
    # Initialize a dictionary to hold counts and amounts for pdeach scheme type
    scheme_summary = defaultdict(lambda: {'count': 0, 'amount': 0})

    # Process the data to count schemes and sum their amounts
    for scheme in data.values():
        scheme_type = scheme['scheme_type'].lower().replace(" ", "-")
        scheme_summary[scheme_type]['count'] += 1
        scheme_summary[scheme_type]['amount'] += scheme['amount']
    
    # Convert defaultdict to a list of tuples for sorting
    scheme_list = [
        {'name': name, 'count': summary['count'], 'amount': summary['amount']}
        for name, summary in scheme_summary.items()
    ]

    # Sort the schemes first by count (descending) and then by amount (descending)
    sorted_schemes = sorted(scheme_list, key=lambda x: (x['count'], x['amount']), reverse=True)

    # Return the top n schemes
    return sorted_schemes[:n]








# def add_scheme_id_to_user_data(user_id, scheme_id,):
#     try:
#         content = read_data_from_json_file('users.json')

#         user_to_update = content[user_id]
#         user_to_update['created_scheme'].append(scheme_id)

#         write_data_to_json_file(user_to_update, 'users.json')

#         return user_to_update
    
#     except Exception as error:
#         print("write_file_exception", error)
#         raise Exception(f"unable to write in users.json! {str(error)}")
