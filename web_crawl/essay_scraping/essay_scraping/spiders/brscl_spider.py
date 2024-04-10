import re
from datetime import datetime, timezone, timedelta

from bs4 import BeautifulSoup
from requests import get
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


def clean_html(html):
    text = BeautifulSoup(html, "html.parser").get_text()
    return (
        text.replace("&nbsp;", " ")
        .replace(" ", " ")
        .replace("\n", " ")
        .replace("\r", " ")
    )


def get_essay_urls():
    urls = [
        "https://vestibular.brasilescola.uol.com.br/mais-temas/36/12",
        "https://vestibular.brasilescola.uol.com.br/mais-temas/24/12",
        "https://vestibular.brasilescola.uol.com.br/mais-temas/12/12",
        "https://vestibular.brasilescola.uol.com.br/mais-temas/0/12",
    ]

    response_array = []

    for url in urls:
        response = get(url)
        response_array.extend(response.json())

    def complete_url(url_part):
        return f"https://vestibular.brasilescola.uol.com.br/banco-de-redacoes/tema-{url_part}.htm"

    for response in response_array:
        response["created_at"] = datetime.fromisoformat(response["created_at"])
        response["url"] = complete_url(response["url"])

    nov_2020 = datetime(2020, 11, 1).replace(tzinfo=timezone(offset=timedelta()))

    response_array = [
        response for response in response_array if response["created_at"] > nov_2020
    ]
    response_array.sort(key=lambda x: x["created_at"], reverse=True)

    start_urls = [response["url"] for response in response_array]

    return start_urls, response_array


def extrair_dados_paragrafos(paragrafos_redacao):
    comentarios_por_p = []

    for i, p in enumerate(paragrafos_redacao):
        p_limpo = clean_html(p)
        if "(" in p_limpo:
            comment_pattern = r"\(.*?\)"
            comentarios_p = re.findall(comment_pattern, p_limpo)
            comentarios_p = [comentario.strip("()") for comentario in comentarios_p]
            comentarios_por_p.append(comentarios_p)
            p_limpo = re.sub(comment_pattern, "", p_limpo).strip()
        paragrafos_redacao[i] = p_limpo

    for i, comentarios in enumerate(comentarios_por_p):
        comentarios_por_p[i] = f"Parágrafo {i + 1} - " + " ".join(comentarios)

    texto_redacao = " ".join([clean_html(p) for p in paragrafos_redacao])
    return texto_redacao, comentarios_por_p


class BrsclSpider(CrawlSpider):
    name = "brsclcrawler"
    allowed_domains = ["brasilescola.uol.com.br"]
    start_urls = []

    get_essay_urls_responses = []

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.start_urls, self.get_essay_urls_responses = get_essay_urls()

    rules = (Rule(LinkExtractor(allow="tema"), callback="parse_prompt"),)

    def parse_redacoes(self, response, pagina_tema_origem):
        titulo_redacao = response.css("h1.titulo-conteudo::text").get()
        titulo_redacao = titulo_redacao.split(" - ")[0]

        paragrafos_redacao = response.css("div.area-redacao-corrigida > p").extract()
        texto_redacao, comentarios_por_p = extrair_dados_paragrafos(paragrafos_redacao)

        notas_redacao = response.css(
            "table#redacoes_corrigidas > tr.row-colored > td.simple-td::text"
        ).extract()
        notas_redacao = notas_redacao[:5]
        notas_redacao = [nota.strip() for nota in notas_redacao]
        notas_redacao = [int(nota) for nota in notas_redacao]

        comments_selector = "body > div.area-site > div.main-content > div.left-side > article > div:nth-child(2) > div > p::text"
        comments = clean_html(response.css(comments_selector).get())

        comments += " " + " ".join(comentarios_por_p)

        yield {
            "tema": {
                "title": pagina_tema_origem["titulo"],
                "description": pagina_tema_origem["texto_limpo"],
                "url": pagina_tema_origem["url"],
                "date": pagina_tema_origem["created_at"],
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
        texto_completo = response.css("div.texto-conteudo > div > p").extract_first()
        texto_limpo = clean_html(texto_completo)

        pagina_tema_origem = next(
            r for r in self.get_essay_urls_responses if r["url"] == response.url
        )

        ahref_selector = response.css("table#redacoes_corrigidas > * > * > a")
        hrefs_redacoes = ahref_selector.xpath("@href").extract()

        pagina_tema_origem["texto_limpo"] = texto_limpo

        for href_redacao in hrefs_redacoes:
            yield Request(
                href_redacao,
                callback=self.parse_redacoes,
                cb_kwargs={"pagina_tema_origem": pagina_tema_origem},
            )
