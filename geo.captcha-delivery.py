# IMPORTANT
# 1. Make sure to have "anticaptchaofficial" package version minimum 1.0.46
# pip install 'anticaptchaofficial>=1.0.46'
#
# 2. Proxy usage is required. Each datadome cookie is associated with a proxy and user-agent.
# Use only self-installed proxy. Shared/purchased proxies WILL FAIL.
# Instruction how to install: https://anti-captcha.com/apidoc/articles/how-to-install-squid
# Again and again people people insist they have best purchased proxies. NO YOU DO NOT!
# Absolutely recommended to read this FAQ about proxies: https://anti-captcha.com/faq/510_questions_about_solving_recaptcha_with_proxy__applies_to_funcaptcha__geetest__hcaptcha_
#
# 3. Solution might not work at first attempt. Do at least 10 attempts.
#

from anticaptchaofficial.antibotcookietask  import *

# STOP! IMPORTANT! Read paragraph 2 above!
proxy_host = "localhost"
proxy_port = 3128
proxy_login = "mylogin"
proxy_pass = "mypassword"

proxies = {
    'https': f"http://{proxy_login}:{proxy_pass}@{proxy_host}:{proxy_port}",
    'http': f"http://{proxy_login}:{proxy_pass}@{proxy_host}:{proxy_port}"
}

solver = antibotcookieTask()
solver.set_verbose(1)
solver.set_key("48ccbbc3efc16cceed4e8c6b2c561576")
solver.set_website_url("https://tickets.rolandgarros.com/se-connecter")
solver.set_proxy_address(proxy_host)
solver.set_proxy_port(proxy_port)
solver.set_proxy_login(proxy_login)
solver.set_proxy_password(proxy_pass)


result = solver.solve_and_return_solution()
if result == 0:
    print("could not solve task")
    exit()

print(result)

cookies, localStorage, fingerprint = result["cookies"], result["localStorage"], result["fingerprint"]

if len(cookies) == 0:
    print("empty cookies, try again")
    exit()

cookie_string = '; '.join([f'{key}={value}' for key, value in cookies.items()])
user_agent = fingerprint['self.navigator.userAgent']
print(f"use these cookies for requests: {cookie_string}")
print(f"use this user-agent for requests: {user_agent}")

s = requests.Session()
proxies = {
  "http": f"http://{proxy_login}:{proxy_pass}@{proxy_host}:{proxy_port}",
  "https": f"http://{proxy_login}:{proxy_pass}@{proxy_host}:{proxy_port}"
}
s.proxies = proxies

content = s.get("https://tickets.rolandgarros.com/se-connecter", headers={
    "Cookie": cookie_string,
    "User-Agent": user_agent
}).text
print(content)