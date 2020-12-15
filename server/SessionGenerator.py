import json

import asyncio
from pyppeteer import launch


class SessionGenerator:
    def __init__(self, email:str, password:str):
        # URLS
        self.loginURL = 'https://messenger.com/login/'
        self.passwordURL = 'https://www.messenger.com/login/password/'
        self.loggedInURL = 'https://www.messenger.com/t/'
        self.checkpointURL1 = 'https://www.messenger.com/login/checkpoint_interstitial/'
        self.checkpointURL2 = 'https://www.facebook.com/checkpoint/'

        # Extra Datas
        self.waitUntilLoad = { 'waitUntil': 'load'}
        
        self.email = email
        self.password = password
    

    def getSession(self):
        # Start Async Loop
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.main())
    

    def generateCookies(self, cookiesList):
        cookies = dict()
        for cookie in cookiesList:
            cookies[cookie['name']]=cookie['value']
        return cookies
    

    def getCodeFor2FA(self):
        return input('Enter Code for 2FA Authentiation: ')
    

    async def ss(self):
        # Take a Screenshot and Save as example.png
        await self.page.screenshot({'path': 'example.png'})
    

    async def getText(self, q):
        try:
            #await self.page.waitForNavigation(self.waitUntilLoad)
            await self.page.waitForSelector(q)
        except:
            pass
        element = await self.page.J(q)
        text = await self.page.evaluate('(element) => element.textContent', element)
        return text
    

    async def pressCPButton(self, t:int=1):
        for i in range(t):
            await self.page.waitForSelector('#checkpointSubmitButton', {'timeout': 500})
            await self.page.click('#checkpointSubmitButton')
            await self.ss()

    async def login(self):
        # Clicks Remember Checkbox for Longer Period Session
        await self.page.waitForSelector('#u_0_0')
        await self.page.click('#u_0_0')

        # Type Email and Password and hit Enter
        await self.page.type('#email', self.email)
        await self.page.type('#pass', self.password)
        await self.page.keyboard.press('Enter')

        # Wait for the full page to load
        await self.page.waitForNavigation(self.waitUntilLoad)

        #disable JS
        await self.page.setJavaScriptEnabled(False)
    
    async def rememberBrowser(self):
        await self.page.click('input[value=dont_save]')
        await self.ss()
        await self.page.keyboard.press('Enter')
        await self.ss()
    
    async def reviewRecentLogin(self):
        await self.pressCPButton(2)
        await self.rememberBrowser()

    async def on2FA(self):
        while self.page.url.startswith(self.checkpointURL1):
            print('Found Checkpoint!')
            await self.ss()

            # Click on Continue Button
            await self.page.click('#XMessengerDotComLoginViewPlaceholder > div > div._3-mr > div > a')
            await self.ss()

            pos = await self.getText('strong')

            while pos=='Two-factor authentication required':
                # Enter Code for 2FA
                code = self.getCodeFor2FA()

                # Hit with code for 2FA
                await self.page.type('#approvals_code', code)
                await self.page.keyboard.press('Enter')

                pos = await self.getText('strong')
                print(pos)
            
            await self.ss()

            # Handle Remember Browser Section
            await self.rememberBrowser()
            pos = await self.getText('strong')
            print(pos)

            # Handle Recent Login
            await self.reviewRecentLogin()

            await self.page.waitForNavigation(self.waitUntilLoad)
            await self.ss()

        return

    async def main(self):
        # Launch Browser Headless
        browser = await launch()

        # Open Tab
        self.page = await browser.newPage()

        # Load Login Page
        await self.page.goto(self.loginURL, self.waitUntilLoad)
        await self.page.screenshot({'path': 'example.png'})

        if self.page.url.startswith(self.loggedInURL):
            print('Logged In Successfully!')
            return
        else:
            await self.login()

        # Check if email / pass is correct
        if self.page.url==self.passwordURL:
            print('Login Failed. Please check username and password!')
            return
        
        # Check for 2FA
        if self.page.url.startswith(self.loggedInURL):
            print('Logged In Successfully!')
        else:
            print('2FA Enabled')
            await self.on2FA()

        #Take Screenshot for Login Confirmation
        await self.page.screenshot({'path': 'example.png'})

        cookiesList = await self.page.cookies()
        return self.generateCookies(cookiesList)

