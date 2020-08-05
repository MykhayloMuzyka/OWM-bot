import wikipedia as wiki

wiki.set_lang('uk')
result = wiki.summary('Львів')
print(result)