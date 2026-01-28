

from playwright.sync_api import sync_playwright

def salvar_cookies():
    print("--- INICIANDO PROCESSO DE LOGIN ---")
    
    with sync_playwright() as p:
        # headless=False faz o navegador aparecer na tela
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        print("1. Abrindo página de login do TikTok...")
        page.goto("https://www.tiktok.com/login/phone-or-email/email")
        
        print("\n" + "="*50)
        print("AGUARDANDO VOCÊ LOGAR...")
        print("DICA: Se o Google bloquear, use o QR CODE ou EMAIL/SENHA.")
        print("Quando terminar de logar e ver a página inicial do TikTok, volte aqui.")
        print("="*50 + "\n")
        
        input(">>> APERTE ENTER AQUI NO TERMINAL QUANDO TIVER LOGADO <<<")
        
        cookies = context.cookies()
        
        cookie_string = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
        
        with open("cookies.txt", "w", encoding="utf-8") as f:
            f.write(cookie_string)
            
        print("\n✅ SUCESSO! Arquivo 'cookies.txt' gerado.")
        browser.close()

if __name__ == "__main__":
    salvar_cookies()