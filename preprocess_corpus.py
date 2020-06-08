#%%
import re
import os
#%%
default_re=re.compile(r'<text .*?>(.*?)</text>',re.S)
def split_text(file_name,output_name=None,p=default_re,encode='utf-8',postpocess=None,save=True):
    """split file

    Arguments:
        file_name {str} -- source file name
        output_name {str} -- output dir

    Keyword Arguments:
        p {re.compiler} -- regex (default: {default_re})
        encode {str} -- file encoder (default: {'utf-8'})
        postpocess {function} -- postpocess function (default: {None})
        save {boolean} -- save or not,if save please input `output_name`,else this function will yield the corpus (default: {true})
    """
    
    if output_name != None and not os.path.exists(output_name):
        os.mkdir(output_name)
    with open(file_name,'r',encoding=encode) as f:
        all_str = f.read()
        all_match = p.findall(all_str)
        # all_match = [m.group('review') for m in all_match]
    num=0
    for match in all_match:
        if postpocess:
            match=postpocess(match)
        if len(match) <= 0:
            continue
        if save is True:
            with open(output_name+"/"+str(num)+'.txt','w',encoding='utf-8') as f:
                f.write(match)
                print(num)
        else:
            yield match
        num += 1

def getChinese(source):
    pattern = re.compile("[\u4e00-\u9fa5]")
    return "".join(pattern.findall(source))

def get_corpus():
    """get courpus

    Yields:
        [tuple] -- (type,sentence),type:0--simplified,type:1--traditional
    """
    for x in split_text("corpus/xinhua_j.txt",postpocess=getChinese,save=False):
        yield 0,x
    for x in split_text("corpus/msn_f.txt",postpocess=getChinese,save=False):
        yield 1,x
