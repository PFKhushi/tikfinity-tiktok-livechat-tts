import asyncio, json, websockets, pygame, time, re
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play

from gtts import gTTS
import gtts.tokenizer.symbols 
from gtts.tokenizer import symbols, pre_processors
from palavras_proibidas import mapa_abrev_palav, extreme_bad


def expandir_abreviacoes(texto: str, abrev_palav: dict):

    for abrev, palavra in abrev_palav.items():
        padrao = r'(?i)\b' + re.escape(abrev) + r'\b'
        texto = re.sub(padrao, palavra, texto)
    
    return texto

def pegar_termino_mais_proximo(texto: str):
    
    for i in range(10):
        a = texto[240+i]
        b = texto[240-i]
        terminos = [' ', '.', ',', '!', '?', ':', ';']
        if a in terminos:
            return a
        
        if b in terminos:
            return b
        
def extreme_bad_check(texto: str):
    
    for palavra in extreme_bad:
        padrao = r'(?i)\b' + re.escape(palavra) + r'\b'
        if re.search(padrao, texto):
            print(f"Bloqueado por conter: {palavra}")
            return False
            
    return True
    
    
def talk(fala:str = 'algo deu errado ao ler a mensagem', linguagem:str = 'pt', sotaque:str = 'com.br'):
    
    if extreme_bad_check(fala) is not True:
        return
    
    # Confirma se iniciado ou inicia o mixer do pygame
    if not pygame.mixer.get_init():
        pygame.mixer.init()
        
    # Criamos um ponteiro com nada
    mp3_filepointer = BytesIO()
    
    # Tokenizamos o texto
    fala = expandir_abreviacoes(fala, mapa_abrev_palav)
    
    # Limitamos o tamanho da string
    if len(fala)>240:
        termino = pegar_termino_mais_proximo(fala)
        fala = fala[:termino]
    
    # Fazemos o request para a API retornar o audio
    tts = gTTS(text=fala, lang='pt', tld='pt')
    
    # Escrevemos esse audio no ponteiro
    tts.write_to_fp(mp3_filepointer)
    
    # Apontamos para o inicio do pontetiro com o audio
    mp3_filepointer.seek(0)

    # pygame carrega o audio a partir do ponteiro
    pygame.mixer.music.load(mp3_filepointer)
    
    # pygame toca o audio
    pygame.mixer.music.play()

    print(f'Tocando: {fala}...')

    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
