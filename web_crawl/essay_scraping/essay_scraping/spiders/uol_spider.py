from datetime import datetime

from time import sleep

from bs4 import BeautifulSoup
from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.response import open_in_browser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


def clean_html(html):
    text = BeautifulSoup(html, "html.parser").get_text()
    return (
        text.replace("&nbsp;", " ")
        .replace(" ", " ")
        .replace("\n", " ")
        .replace("\r", " ")
    )


def press_load_more_button_get_links():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://educacao.uol.com.br/bancoderedacoes/")

    button_selector = "body > div.container > section > div > section > button"
    load_more_button = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, button_selector))
    )
    driver.execute_script("arguments[0].scrollIntoView();", load_more_button)
    load_more_button.click()
    sleep(1)
    links = driver.find_elements(By.CSS_SELECTOR, "div.thumbnails-wrapper > a")
    links = [link.get_attribute("href") for link in links]
    driver.close()
    return links


def extrair_dados_paragrafos(paragrafos_redacao):
    errors = []
    paragrafos_limpos = []

    for p in paragrafos_redacao:
        soup = BeautifulSoup(p, "html.parser")

        for b_tag in soup.find_all("b"):
            correct_span = b_tag.find_next_sibling("span", class_="certo")
            if correct_span:
                errors.append(str((b_tag.get_text(), correct_span.get_text())))
                correct_span.replace_with("")
            b_tag.replace_with(b_tag.text)

        paragrafos_limpos.append(soup.get_text())

    texto_redacao = " ".join(paragrafos_limpos)

    return texto_redacao, errors


class UolSpider(CrawlSpider):
    name = "uolcrawler"
    allowed_domains = ["educacao.uol.com.br"]
    links_iniciais = [
        "https://educacao.uol.com.br/bancoderedacoes/propostas/qualificacao-e-o-futuro-do-emprego.htm",
        "https://educacao.uol.com.br/bancoderedacoes/propostas/supremo-tribunal-federal-e-opiniao-publica.htm",
        "https://educacao.uol.com.br/bancoderedacoes/propostas/ciencia-tecnologia-e-superacao-dos-limites-humanos.htm",
        "https://educacao.uol.com.br/bancoderedacoes/propostas/um-reu-deve-ou-nao-ser-preso-apos-a-condenacao-em-2-instancia.htm",
        "https://educacao.uol.com.br/bancoderedacoes/propostas/agrotoxicos-ou-defensivos-agricolas-dois-nomes-e-uma-polemica.htm",
        "https://educacao.uol.com.br/bancoderedacoes/propostas/preservacao-da-amazonia-desafio-brasileiro-ou-internacional.htm",
        "https://educacao.uol.com.br/bancoderedacoes/propostas/criptomoeda-tecnologia-e-revolucao-economica.htm",
        "https://educacao.uol.com.br/bancoderedacoes/propostas/a-ciencia-na-era-da-pos-verdade.htm",
        "https://educacao.uol.com.br/bancoderedacoes/propostas/universidade-em-crise-quem-paga-a-conta.htm",
        "https://educacao.uol.com.br/bancoderedacoes/propostas/a-fe-e-decisiva-para-uma-vida-melhor.htm",
        "https://educacao.uol.com.br/bancoderedacoes/propostas/os-ursos-polares-da-russia-e-um-dilema-ecologico.htm",
        "https://educacao.uol.com.br/bancoderedacoes/propostas/cantar-ou-nao-cantar-o-hino-nacional-eis-a-questao.htm",
        "https://educacao.uol.com.br/bancoderedacoes/propostas/posse-de-armas-mais-seguranca-ou-mais-perigo.htm",
        "https://educacao.uol.com.br/bancoderedacoes/propostas/o-brasil-e-os-imigrantes-no-mundo-contemporaneo.htm",
        "https://educacao.uol.com.br/bancoderedacoes/propostas/epidemia-alimentar-sobrepeso-e-obesidade.htm",
        "https://educacao.uol.com.br/bancoderedacoes/propostas/a-onda-conservadora-e-o-brasil-nos-proximos-anos.htm",
    ]

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        links = []
        if len(self.links_iniciais) < 16:
            links = press_load_more_button_get_links()
        else:
            return

        if len(links) < 16:
            raise Exception("Erro na obtenção dos links pelo Driver Chrome (Selenium).")

        self.links_iniciais = links

    def start_requests(self):
        for url in self.links_iniciais:
            yield Request(url, self.parse_prompt)

    def parse_redacoes(self, response, pagina_tema_origem):
        titulo_redacao = (
            response.css("div.container-composition > h2::text").get().strip()
        )

        paragrafos_redacao = response.css(
            "div.container-composition > div.text-composition > p"
        ).extract()
        texto_redacao, errors = extrair_dados_paragrafos(paragrafos_redacao)

        notas_redacao = response.css("div.rt-line-option > span.points::text").extract()
        notas_redacao = notas_redacao[:5]
        notas_redacao = [nota.strip() for nota in notas_redacao]
        notas_redacao = [int(nota) for nota in notas_redacao]

        comentario_geral = response.css(
            "div.image-content-pad > div.text > p"
        ).extract()
        comentario_competencias = response.css(
            "div.image-content-pad > div.text > ul > li"
        ).extract()
        comentario_geral.extend(["Parágrafo " + c for c in comentario_competencias])
        comments = " ".join([clean_html(p.strip()) for p in comentario_geral])
        if errors is not None and len(errors) > 0:
            comments += "Erros gramaticais: " + " ".join(errors)

        yield {
            "tema": {
                "title": pagina_tema_origem["title"],
                "description": pagina_tema_origem["description"],
                "url": pagina_tema_origem["url"],
                "date": pagina_tema_origem["date"],
            },
            "essay": {
                "title": titulo_redacao,
                "text": texto_redacao,
                "final_score": sum(notas_redacao),
                "comments": comments,
                "url": response.url,
                "criterions": {
                    "criteria_score_1": notas_redacao[0],
                    "criteria_score_2": notas_redacao[1],
                    "criteria_score_3": notas_redacao[2],
                    "criteria_score_4": notas_redacao[3],
                    "criteria_score_5": notas_redacao[4],
                },
            },
        }

    def parse_prompt(self, response):
        paragrafo_principal = response.css(
            "div.image-content-pad > div.text > p"
        ).extract_first()
        paragrafos_descricao_tema = response.css(
            "ul.article-wording-item > li > div.item-descricao"
        ).extract()[:-1]
        paragrafos_descricao_tema.insert(0, paragrafo_principal)
        descricao_tema = " ".join([clean_html(p) for p in paragrafos_descricao_tema])
        anchors_redacoes_selector = response.css("div.rt-line-option > a")
        hrefs_redacoes = anchors_redacoes_selector.xpath("@href").extract()

        titulo_redacao = response.css("i.custom-title::text").get().strip()
        data_publicacao = (
            response.css("p.p-author.time").xpath("@ia-date-publish").get()
        )
        data_publicacao = datetime.strptime(data_publicacao, "%Y-%m-%dT%H:%M:%S%z")

        pagina_tema_origem = {
            "title": titulo_redacao,
            "description": descricao_tema,
            "url": response.url,
            "date": data_publicacao,
        }

        for href_redacao in hrefs_redacoes:
            yield Request(
                href_redacao,
                callback=self.parse_redacoes,
                cb_kwargs={"pagina_tema_origem": pagina_tema_origem},
            )
