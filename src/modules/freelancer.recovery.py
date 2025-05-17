from _types import Module
from _util import Session, Print
import datetime

requests = Session()
debug    = True

@Module(
    module_type         = 'info_exposure',
    proxies_required    = False,
    module_data         = {'should_validate_username': True}
)
def run(module_data, email: str) -> dict:
    try:
        if module_data.get('should_validate_username') == True:
            if '@' not in email:
                Print.log(f"Invalid email format: {email}", level='ERROR')
                return {'is_valid': False, 'error': 'invalid_format'}

        if debug:
            Print.log('Creating recovery request')

        # Attempt account recovery
        resp = requests.post(
            'https://www.freelancer.com/auth/forgot',
            data={'email': email}
        )
        if resp.status_code != 200:
            Print.log(f"Unexpected response status: {resp.status_code}", level='WARNING')
            return {'is_valid': False, 'error': resp.status_code}

        data = resp.json()
        user_info = data.get('result', {})

        # Validation method for account
        if user_info.get('action') != 'account_reactivation':
            Print.log(f"No Freelancer account found for {email}", level='WARNING')
            return {'is_valid': False, 'error': 'no_account'}

        user_id = user_info.get('user_id')
        if not user_id:
            Print.log("User ID not found in recovery response", level='WARNING')
            return {'is_valid': False, 'error': 'no_user_id'}

        if debug:
            Print.log('UID found, fetching user details')

        # Fetch user details via api
        user_url = (
            "https://www.freelancer.com/api/users/0.1/users?"  
            "avatar=true&cover_image=true&display_info=true&country_details=true&jobs=true"
            "&portfolio_details=true&preferred_details=true&profile_description=true"
            "&qualification_details=true&recommendations=true&responsiveness=true"
            "&status=true&users[]={user_id}&operating_areas=true&equipment_group_details=true"
            "&document_submissions=true&rising_star=true&staff_details=true"
            "&webapp=1&compact=true&new_errors=true&new_pools=true"
        ).format(user_id = user_id)

        user_resp = requests.get(user_url)

        if user_resp.status_code != 200:
            Print.log(f"Failed to fetch user details: {user_resp.status_code}", level='WARNING')
            return {'is_valid': False, 'error': user_resp.status_code}

        user_data = user_resp.json().get('result', {}).get('users', {}).get(str(user_id), {})

        if not user_data:
            Print.log(f"No user data found for user ID: {user_id}", level='WARNING')
            return {'is_valid': False, 'error': 'no_user_data'}

        # Convert registration date
        reg_ts = user_data.get('registration_date', 0)
        created = (
            datetime.datetime.utcfromtimestamp(reg_ts).strftime('%Y-%m-%d %H:%M:%S')
            if reg_ts else 'Unknown'
        )

        # Badges
        status = user_data.get('status', {})
        badges = []
        if user_data.get('display_name') == 'Closed User':
            badges.append('Closed Account')
        else:
            badges.append('Active Account')
        for key, name in [
            ('email_verified', 'Linked Email'),
            ('phone_verified', 'Linked Phone'),
            ('identity_verified', 'KYC Verified'),
            ('linkedin_connected', 'LinkedIn Verified'),
            ('facebook_connected', 'Facebook Verified'),
            ('freelancer_verified_user', 'Freelancer Verified'),
            ('payment_verified', 'Payment Verified')
        ]:
            if status.get(key):
                badges.append(name)

        # Table values
        rep = user_data.get('reputation', {})
        table_vals = [[
            rep.get('earnings_score', 0),
            rep.get('job_history', {}).get('count_other', 0),
            status.get('profile_complete', False)
        ]]

        # Base output format used by the NoSINT parser
        output = {
            'avatar': f"https:{user_data.get('avatar_cdn','')}" if user_data.get('avatar_cdn') else None,
            'created': created,
            'last_seen': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'display': {
                'user_id': user_data.get('id'),
                'username': user_data.get('username'),
                'display_name': user_data.get('display_name'),
                'tagline': user_data.get('tagline'),
                'chosen_role': user_data.get('chosen_role'),
                'location': user_data.get('location', {}).get('country', {}).get('name', '')
            },
            'recovery': {'email': email},
            'badges': badges,
            'table': {'headers': ['Earnings Score','Job Count','Profile Complete'], 'values': table_vals},
            'meta': {'name': 'Freelancer', 'user_link': f"https://www.freelancer.com/u/{user_data.get('username')}"},
        }

        return {'is_valid': True, 'results': output}

    except Exception as e:
        Print.log(f"Error during Freelancer recovery for {email}: {e}", level='ERROR')
        return {'is_valid': False, 'error': str(e)}