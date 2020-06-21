# import re
# import spacy
# import keras
# import numpy as np

# from spacy.tokenizer import Tokenizer 
# from spacy.util import compile_prefix_regex, compile_infix_regex, compile_suffix_regex
# from spacy.attrs import ORTH, NORM

# special_case = {
#     "couldn't" : [{ORTH: "could"}, {ORTH: "n't", NORM: "not"}],
#     "don't" : [{ORTH: "do"}, {ORTH: "n't", NORM: "not"}],
#     "wasn't" : [{ORTH: "was"}, {ORTH: "n't", NORM: "not"}],
#     "isn't" : [{ORTH: "is"}, {ORTH: "n't", NORM: "not"}],
#     "it's" : [{ORTH: "it"}, {ORTH: "'s", NORM: "is"}],
#     "wouldn't": [{ORTH: "would"}, {ORTH: "n't", NORM: "not"}],
# }

# class Parser:
#     def __init__(self, sent_segmenter=True, custom_tokenize=True):
#         self.pre_model = spacy.load("en_core_web_sm")
        
#         if sent_segmenter:
#             self.boundary = re.compile('^[0-9]$')
#             self.pre_model.add_pipe(self.custom_seg, before='parser')
        
#         if custom_tokenize:
#             self.pre_model.tokenizer = self.custom_tokenizer(self.pre_model)
            
#             for k,v in special_case.items():
#                 self.pre_model.tokenizer.add_special_case(k, v)
            
#         print(f"Pipe names : {self.pre_model.pipe_names}")
    
#     def custom_tokenizer(self, nlp_model):
#         infix_re = re.compile(r'''[.\,\?\:\;\...\‘\’\`\“\”\"\'~]''')
#         prefix_re = compile_prefix_regex(self.pre_model.Defaults.prefixes)
#         suffix_re = compile_suffix_regex(self.pre_model.Defaults.suffixes)
        
#         return Tokenizer(self.pre_model.vocab, prefix_search=prefix_re.search,
#                                                suffix_search=suffix_re.search,
#                                                infix_finditer=infix_re.finditer,
#                                                token_match=None)

#     def custom_seg(self, doc):
#         prev = doc[0].text
#         length = len(doc)
#         for index, token in enumerate(doc):
#             if (token.text == '.' and self.boundary.match(prev) and index!=(length - 1)):
#                 doc[index+1].sent_start = False
#             prev = token.text
#         return doc
    
#     def sent_to_doc(self, sent):
#         self.doc = self.pre_model(sent)
    
#     def token_normalizer(self, token):
#         if(token == "n't"):
#             new_token = "not"
#         else:
#             new_token = token
#         return new_token
    
#     def remove_punct(self):
#         if 'custom_seg' in self.pre_model.pipe_names:
#             rlist = []
#             for sent in (self.doc).sents:
#                 temp_ = []
#                 for token in sent:
#                     if token.pos_ == 'PUNCT':
#                         continue
#                     new_token = self.token_normalizer(token.text)
#                     temp_.append(new_token)
#                 rlist.append(temp_)
#             return rlist

# if __name__ == "__main__":
#     pass