# Evaluate translations via a local SBERT embedder

## Approach: Using Embedder Encodings

Using a *multi-lingual* sentence embedder such as 'paraphrase-multilingual-MiniLM-L12-v2', and assuming we are comparing pairs of sentences, one sentence from each service:

- encode each translated sentence into an embedding vector
- also encode the original text
- find which translated sentence has the closest vector to the vector of the original text translation

Benefit: no 'known good' translation is required.

To compare encoded vectors, the math is:

    the dot product of 2 normalised vectors = cosine Angle
    cosine distance = 1 - v.w
    
- *a smaller distance, means closer (the 2 sentences are more similar)*

Some sentence embedders have libraries that supply the cosine distance function.

For this Python script, we use the model via the package sentence-transformers. That package provides the function `util.cos_sim()`.

## Results

- despite not relying on the 'known good' translation (which is used by the eval-via-embedder tool), the quality of results was 98% correct compared to the eval-via-embedder tool.

## Dependencies

- Python 3.11
- pyenv - if on Windows use [pyenv-win](https://github.com/pyenv-win/pyenv-win)

## Install

Switch to Python 3.11.6:

```
pyenv install 3.11.6
pyenv local 3.11.6
```

Setup a virtual environment:

```
python3 -m venv env

env\Scripts\activate
```

Install SBERT and cornsnake via this pip command:

```
pip install -U sentence-transformers==2.2.2 cornsnake==0.0.26
```

## Usage

```
python main.py <path to CSV file> [threshold (number between 0 and 1)]
```

Where the CSV file follows this format:

```
# English, translation_a, translation_b, known_good
How do I get to the beach?,cómo puedo llegar a la playa,Cómo llego a la playa,¿Cómo llego a la playa?
```

For an example, see the [test data](../../test-resources/english-to-spanish.csv).

## Example

To test:

```
./test.sh
```

OUTPUT:

```
Loading embedder model...
'How do I get to the beach?' -> 'Cómo llego a la playa' [B is best] [known good = '¿Cómo llego a la playa?']
```

## Further improvements

Increase accuracy:

- take several embeddings per class and use their average for that class
- try different embeddings, can get better results
- try different distance measures from your library
- consider tuning the embedding (for example, for the domain vocabulary of a particular industry or problem space)

# References

[SBERT: How to Use Sentence Embeddings to Solve Real-World Problems](https://anirbansen2709.medium.com/sbert-how-to-use-sentence-embeddings-to-solve-real-world-problems-f950aa300c72)
