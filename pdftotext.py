from pypdf import PdfReader
import re

path = r"C:\Users\..."

def get_pagetext(path, pagenr, reader):
    '''
    Parameters
    ----------
    path : str
        The path to the pdf
    pagenr : int
        The number of the page. Make sure the page is not higher than the amount of pages the pdf has
    reader : pypdf.PdfReader
        An instance of pypdf's PdfReader
        
    Raises
    ------
    ValueError
        Page number was not in the range of possible outputs, namely the integers from 1 - number of pages

    Returns
    -------
    txt_without_link : str
        The text found on the page of that pdf. The mp4directs links removed from the string

    '''
    if pagenr not in range(1, len(reader.pages)+1):
        raise ValueError(f"pagenr was given value of {pagenr}, but the number has to be in between 1 and the number of pages({len(reader.pages)})")
    page_index = pagenr - 1
    page = reader.pages[page_index]
    txt_with_link = page.extract_text()
    txt_without_link = txt_with_link.replace('\nhttps://mp4directs.com', '')
    return txt_without_link

reader = PdfReader(path)
txt = get_pagetext(path, 10, reader)

def split_by_conjunction(text, conjunction):
    if text.split(conjunction, maxsplit = 1)[0] not in [' ', '', '\n']:
        return text.split(conjunction, maxsplit = 1)
    else:
        return [text]
    
def paste_oneword(chunks):
    paste_oneword_chunks = ['']
    for chunk in chunks:
        if ' ' not in chunk:
            paste_oneword_chunks[-1] = paste_oneword_chunks[-1] + ' ' + chunk
        else:
            paste_oneword_chunks.append(chunk)
    if paste_oneword_chunks[0] == '':
        paste_oneword_chunks = paste_oneword_chunks[1:]
    return paste_oneword_chunks
            

def text_to_chunks(text, sep = '[.,]',):
    '''
    Parameters
    ----------
    text : str
        Text to put into chunks
    sep : str
        The seperations in between the sentences, put in regex

    Returns
    -------
    improved_chunks : list[str]
        List with the contents of the text put into chunks
    '''
    chunks = re.split(sep, text)
    improved_chunks = []
    for chunk in chunks:
        chunk = chunk.replace('\n', ' ')
        if chunk.startswith(' '):
            chunk = chunk.replace(' ', '', 1)
        
        if len(chunk) > 0:
            no_newline = chunk#.replace('\n', ' ')
            conjunctions = [' as long as ', ' as soon as ', ' even though ', ' although ', ' as if ', ' because ', ' though ', ' while ', ' so ', ' if ', ' unless ', ' until ', ' and ', ' but ', ' since ', ' yet ', ' nor ', ' for ', ' or ', ' as ']
            for conjunction in conjunctions:
                if conjunction in no_newline:
                    improved_chunks.extend(split_by_conjunction(no_newline, conjunction))
                    break
    improved_chunks = paste_oneword(improved_chunks)
    return improved_chunks

def max_chunk_length(sep, text, limit):
    chunks = re.split(sep, text)
    chunk_lengths = [[len(x),x] for x in chunks]
    over_100_limit = [[length, chunk] for length, chunk in chunk_lengths if length > limit]
    over_limit_perc = len([[length, chunk] for length, chunk in chunk_lengths if length > limit]) / len(chunks) * 100
    print(f'max length: {max(chunk_lengths)}')
    print(f'min length: {min(chunk_lengths)}')
    print(f'over the 100 character limit: {len(over_100_limit)}/{len(chunks)}')
    print(f'over the limit perc: {over_limit_perc} %')
    return [chunk for length, chunk in over_100_limit]
    
def split_large_chunks(large_chunks):
    #1. Change the new lines (\n) into spaces
    #2. Split long sentences up in two by searching for conjuctions
    pass
    
limit = 50

chunks = text_to_chunks(txt, '[.,]')

# over_limit = max_chunk_length('[.,]', txt, 50)

# splitted_chunks = split_large_chunks(over_limit)
