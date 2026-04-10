"""End-to-end tests for MagicKey using Playwright with virtual WebAuthn authenticator."""
import asyncio, threading, time, uvicorn
from playwright.async_api import async_playwright

PORT = 8123
url = f'http://localhost:{PORT}'

def _start_server():
    import os,sys
    sys.path.insert(0,os.path.dirname(__file__))
    from magickey_app import app
    uvicorn.run(app, host='localhost', port=PORT, log_level='warning')

async def _add_virtual_authenticator(page):
    cdp = await page.context.new_cdp_session(page)
    await cdp.send('WebAuthn.enable')
    await cdp.send('WebAuthn.addVirtualAuthenticator', {
        'options': {
            'protocol': 'ctap2',
            'transport': 'internal',
            'hasUserVerification': True,
            'isUserVerified': True,
            'hasResidentKey': True,
            'automaticPresenceSimulation': True,
        }
    })
    return cdp

async def _register(page, email, passkey=True):
    await page.goto(f'{url}/login')
    await page.wait_for_selector('#email-input')
    await page.fill('#email-input', email)
    await page.click('button[type="submit"]')
    await page.wait_for_selector('a[href*="verify_magiclink"]')
    link = await page.query_selector('a[href*="verify_magiclink"]')
    await link.click()
    await page.wait_for_url('**/setup_passkey**')
    if passkey: await page.click('text=Register Passkey')
    else :      await page.click('#skip-link')
    await page.wait_for_url('**/')

async def test_magic_link_and_passkey_reg(browser):
    page = await browser.new_page()
    await _add_virtual_authenticator(page)
    await _register(page, email:='alice@test.com')
    assert email in await page.content()
    await page.close()
    print('✅ test_magic_link_and_passkey_reg')

async def test_passkey_login(browser):
    page = await browser.new_page()
    await _add_virtual_authenticator(page)

    await _register(page, email:='bob@test.com')
    assert email in await page.content()

    await page.click('text=Log out')
    await page.wait_for_url('**/login**')
    await page.click('text=Sign in with Passkey')
    await page.wait_for_url('**/')
    assert 'bob@test.com' in await page.content()
    await page.close()
    print('✅ test_passkey_login')

async def test_skip_passkey_reg(browser):
    page = await browser.new_page()
    await _register(page, email:='carol@test.com', passkey=False)
    assert email in await page.content()
    await page.close()
    print('✅ test_skip_passkey_reg')


async def run_tests():
    srv = threading.Thread(target=_start_server, daemon=True)
    srv.start()
    time.sleep(2)

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        await test_magic_link_and_passkey_reg(browser)
        await test_passkey_login(browser)
        await test_skip_passkey_reg(browser)
        await browser.close()
    print('🎉 All tests passed!')

if __name__ == '__main__':
    asyncio.run(run_tests())
