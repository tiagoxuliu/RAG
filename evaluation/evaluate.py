import time
import json
from app.chain import answer_question

TESTSET = [
    {
        "question": "Que tipos de dados existem em MongoDB?",
        "expected_keywords": ["Inteiro", "String", "Data", "Array"],
    },
    {
        "question": "O que faz o operador $lookup?",
        "expected_keywords": ["join", "coleç"],
    },
]

def evaluate():
    resultados = []
    for caso in TESTSET:
        inicio = time.time()
        resposta = answer_question(caso["question"])
        duracao = time.time() - inicio

        answer_text = resposta["answer"].lower()
        acertos = [kw for kw in caso["expected_keywords"] if kw.lower() in answer_text]

        resultados.append({
            "question": caso["question"],
            "answer": resposta["answer"],
            "keywords_encontradas": acertos,
            "keywords_esperadas": caso["expected_keywords"],
            "score": len(acertos) / len(caso["expected_keywords"]),
            "tempo_segundos": round(duracao, 2),
        })

    with open("evaluation/resultados.json", "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)

    score_medio = sum(r["score"] for r in resultados) / len(resultados)
    print(f"Score médio: {score_medio:.2f}")
    return resultados

if __name__ == "__main__":
    evaluate()