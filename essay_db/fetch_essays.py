import sys
import os
import pandas as pd
from uol_redacoes_xml import load as load_uol_essays
from uol_redacoes_xml.reader.essays import Essay as UolEssay, Prompt as UolPrompt
from sqlalchemy import select, exists, and_

from util import get_r_file_path

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from db_config.sqlaenv import Session
from essay_db.essay_orm import Essay, Prompt


@DeprecationWarning
def old_uol_essays(essays):
    essays_old = load_uol_essays()
    store_essays(essays_old)


def fetch_essays():
    fontes = ["uol", "brscl"]
    path_template = "../web_crawl/essay_scraping/essay_scraping/spiders_output/{0}.json"

    field_types = {
        "tema_date": "datetime64[ns]",
        "essay_final_score": int,
        "essay_criterions_criteria_score_1": int,
        "essay_criterions_criteria_score_2": int,
        "essay_criterions_criteria_score_3": int,
        "essay_criterions_criteria_score_4": int,
        "essay_criterions_criteria_score_5": int,
    }

    df_parts = []

    for fonte in fontes:
        path = get_r_file_path(path_template.format(fonte))
        df_parts.append(
            pd.read_json(
                path,
                dtype=field_types,
            )
        )

    essays = pd.concat(df_parts)

    def df_row_to_orm(row):
        tema = row["tema"]
        essay = row["essay"]

        prompt = UolPrompt(
            tema["title"],
            tema["description"],
            "",
            tema["url"],
            tema["date"],
        )

        criterions = essay["criterions"]

        criteria_scores = {
            "Competência 1": criterions["criteria_score_1"],
            "Competência 2": criterions["criteria_score_2"],
            "Competência 3": criterions["criteria_score_3"],
            "Competência 4": criterions["criteria_score_4"],
            "Competência 5": criterions["criteria_score_5"],
        }

        essay = UolEssay(
            essay["title"],
            essay["text"],
            essay["final_score"],
            criteria_scores,
            prompt,
            essay["url"],
            "",
            "",
            essay["comments"],
        )

        return essay

    essays = essays.apply(df_row_to_orm, axis=1)

    return essays


def store_essays(essays):
    essays_orm = []

    with Session() as session:
        for essay in essays:
            prompt = Prompt(
                title=essay.prompt.title,
                description=essay.prompt.description,
                info=essay.prompt.info,
                url=essay.prompt.url,
                date=essay.prompt.date,
            )

            prompt_query = select(
                exists().where(and_(Prompt.title == essay.prompt.title))
            )
            prompt_exists = session.scalar(prompt_query)

            if prompt_exists:
                prompt = session.query(Prompt).filter_by(title=prompt.title).scalar()
            else:
                session.add(prompt)
                session.commit()

            essay_obj = Essay(
                title=essay.title,
                text=essay.text,
                final_score=essay.final_score,
                criteria_score_1=essay.criteria_scores["Competência 1"],
                criteria_score_2=essay.criteria_scores["Competência 2"],
                criteria_score_3=essay.criteria_scores["Competência 3"],
                criteria_score_4=essay.criteria_scores["Competência 4"],
                criteria_score_5=essay.criteria_scores["Competência 5"],
                prompt=prompt,
                url=essay.url,
                comments=essay.comments,
            )

            essays_orm.append(essay_obj)

        session.add_all(essays_orm)
        session.commit()


if __name__ == "__main__":
    essays = fetch_essays()
    store_essays(essays)
    print("Finalizado")
