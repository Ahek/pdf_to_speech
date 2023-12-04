from tika_pdf_reader import get_pagetext, text_to_chunks
from pypdf import PdfReader
from gtts import gTTS
import os
#needs to be run in gtts_env

pdf_path = r"C:\Users\arent\Documents\anime\Shield hero\Full volumes\The_Rising_of_the_Shield_Hero_Volume_12.pdf"

reader = PdfReader(pdf_path)

all_chunks = []

def create_directory(path, name):
    if not os.path.isdir(fr'{path}\{name}'):
        os.makedirs(fr'{path}\{name}')
        
saving_directory = r"C:\Users\arent\Documents\OtherStuff\scraping"
map_name = "ShieldHeroV12C200"
create_directory(saving_directory, map_name)
    
for page_nr in range(200, 210):
    pdf_text = get_pagetext(pdf_path, page_nr, reader)
    my_chunks = text_to_chunks(pdf_text)
    all_chunks.extend(my_chunks)

with open(fr'{saving_directory}\full_file.mp3', 'wb') as f:
    for chunknr, chunk in enumerate(all_chunks):
        tts = gTTS(chunk, lang = 'en')
        tts.write_to_fp(f)
f.close()   

# for chunknr, chunk in enumerate(all_chunks):
#     tts = gTTS(chunk, lang = 'en')
#     tts.save(fr'{saving_directory}\{map_name}\{chunknr}.mp3')