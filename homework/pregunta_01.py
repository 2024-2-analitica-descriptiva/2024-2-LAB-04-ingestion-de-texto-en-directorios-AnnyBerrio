# pylint: disable=import-outside-toplevel
# pylint: disable=line-too-long
# flake8: noqa
"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""
import os
import pandas as pd
import zipfile


def pregunta_01():
    """
    La información requerida para este laboratio esta almacenada en el
    archivo "files/input.zip" ubicado en la carpeta raíz.
    Descomprima este archivo.

    Como resultado se creara la carpeta "input" en la raiz del
    repositorio, la cual contiene la siguiente estructura de archivos:


    ```
    train/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    test/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    ```

    A partir de esta informacion escriba el código que permita generar
    dos archivos llamados "train_dataset.csv" y "test_dataset.csv". Estos
    archivos deben estar ubicados en la carpeta "output" ubicada en la raiz
    del repositorio.

    Estos archivos deben tener la siguiente estructura:

    * phrase: Texto de la frase. hay una frase por cada archivo de texto.
    * sentiment: Sentimiento de la frase. Puede ser "positive", "negative"
      o "neutral". Este corresponde al nombre del directorio donde se
      encuentra ubicado el archivo.

    Cada archivo tendria una estructura similar a la siguiente:

    ```
    |    | phrase                                                                                                                                                                 | target   |
    |---:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------|
    |  0 | Cardona slowed her vehicle , turned around and returned to the intersection , where she called 911                                                                     | neutral  |
    |  1 | Market data and analytics are derived from primary and secondary research                                                                                              | neutral  |
    |  2 | Exel is headquartered in Mantyharju in Finland                                                                                                                         | neutral  |
    |  3 | Both operating profit and net sales for the three-month period increased , respectively from EUR16 .0 m and EUR139m , as compared to the corresponding quarter in 2006 | positive |
    |  4 | Tampere Science Parks is a Finnish company that owns , leases and builds office properties and it specialises in facilities for technology-oriented businesses         | neutral  |
    ```


    """
    zip_file = "files/input.zip"
    input_dir = "input"

    if not os.path.exists(zip_file):
        print(f"El archivo {zip_file} no existe.")
        return

    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        zip_ref.extractall(input_dir)
        print(
            f"El archivo {zip_file} ha sido descomprimido correctamente en {input_dir}"
        )

    output_dir = os.path.join("files", "output")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    test_df = pd.DataFrame(columns=["phrase", "target"])
    train_df = pd.DataFrame(columns=["phrase", "target"])

    test_dir = os.path.join("input", "input", "test")
    train_dir = os.path.join("input", "input", "train")

    sentiment_dirs = ["positive", "negative", "neutral"]

    for sentiment in sentiment_dirs:
        sentiment_path = os.path.join(test_dir, sentiment)

        if not os.path.exists(sentiment_path):
            print(f"El directorio {sentiment_path} no existe.")
            continue

        for filename in os.listdir(sentiment_path):
            file_path = os.path.join(sentiment_path, filename)

            if os.path.isfile(file_path):
                with open(file_path, "r", encoding="utf-8") as file:
                    phrase = file.read().strip()

                test_df = test_df._append(
                    {"phrase": phrase, "target": sentiment}, ignore_index=True
                )

    for sentiment in sentiment_dirs:
        sentiment_path = os.path.join(train_dir, sentiment)

        if not os.path.exists(sentiment_path):
            print(f"El directorio {sentiment_path} no existe.")
            continue

        for filename in os.listdir(sentiment_path):
            file_path = os.path.join(sentiment_path, filename)

            if os.path.isfile(file_path):
                with open(file_path, "r", encoding="utf-8") as file:
                    phrase = file.read().strip()

                train_df = train_df._append(
                    {"phrase": phrase, "target": sentiment}, ignore_index=True
                )

    test_df = test_df.sample(frac=1, random_state=42).reset_index(drop=True)
    train_df = train_df.sample(frac=1, random_state=42).reset_index(drop=True)

    test_df.to_csv(os.path.join("files/output", "test_dataset.csv"), index=False)
    train_df.to_csv(os.path.join("files/output", "train_dataset.csv"), index=False)
