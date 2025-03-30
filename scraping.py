import os
import requests
from bs4 import BeautifulSoup
from zipfile import ZipFile

url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

pdf_links = []
for link in soup.find_all("a", href=True): # Busca todos os links da página
    href = link["href"]
    if href.endswith(".pdf"): # Verifica se o link termina com ".pdf"
        if not href.startswith("http"):
            href = url.rsplit("/", 1)[0] + "/" + href # Adiciona o prefixo da URL

        pdf_links.append(href)
        
os.makedirs("pdfs", exist_ok=True)

for i, url_pdf in enumerate(pdf_links[:2]):
    pdf_resp = requests.get(url_pdf)
    pdf_path = os.path.join("pdfs", f"Anexo_{i+1}.pdf")
    with open(pdf_path, "wb") as f:
        f.write(pdf_resp.content)
    print(f"Arquivo {pdf_path} salvo com sucesso.")
    

zip_fileNome = "Anexando.zip"
with ZipFile(zip_fileNome, "w") as zip:
    for file in os.listdir("pdfs"):
        zip.write(os.path.join("pdfs", file), arcname=file)
        
print(f"Arquivos compactados {zip_fileNome} salvos com sucesso.")