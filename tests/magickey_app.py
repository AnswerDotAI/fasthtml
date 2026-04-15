from fasthtml.common import *
from fasthtml.magickey import MagicKey

app, rt = fast_app()

passkey_store = {}
class Auth(MagicKey):
    def get_auth(self, email, session): return '/'
    def get_user_id(self, email): return email
    def has_passkey(self, email): return any(v['email'] == email for v in passkey_store.values())
    def get_passkey(self, credential_id): return passkey_store.get(credential_id)
    def save_passkey(self, credential_id, email, public_key, sign_count):
        passkey_store[credential_id] = dict(email=email, public_key=public_key, sign_count=sign_count)
    def update_passkey(self, credential_id, sign_count): passkey_store[credential_id]['sign_count'] = sign_count

def _dev_send_email(email, url): return P(f'Magic link for {email}: ', A(url, href=url))
mk = Auth(app, send_email=_dev_send_email)

@rt('/')
def home(auth): return Titled('Home', P(f'Hello {auth}!'), A('Log out', href='/logout'))

@rt('/login')
def login():
    return Titled('Sign In',
        Button('Sign in with Passkey', hx_post='/request_passkey_auth', target_id='scripts'),
        Hr(),
        Form(method='post', action='/send_magic_link')(
            Input(name='email', type='email', placeholder='you@example.com', id='email-input'),
            Button('Send Magic Link', type='submit')),
        Div(id='scripts'))

@rt('/setup_passkey')
def setup_passkey():
    return Titled('Set Up Passkey',
        P('Set up a passkey for faster logins next time?'),
        Button('Register Passkey', hx_post='/request_passkey_reg', target_id='scripts'),
        Form(Button('Skip', type='submit', id='skip-btn'), action='/skip_passkey_reg', method='post'),
        Div(id='scripts'))
