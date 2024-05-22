from profanityfilter import ProfanityFilter


pf = ProfanityFilter()
content = "what the is that?"
print(content)
print(pf.censor(content))
print(pf.is_clean(content))
