import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import pickle

# 1 — Carregar CSV
df = pd.read_csv("dataset\dataset_cabeca_baixa.csv")   # coloque o nome do seu arquivo

# 2 — Separar features (X) e labels (y)
X = df.drop(columns=["label"])
y = df["label"]

# 3 — Transformar rótulos em números (cruzados = 1 / nao_cruzados = 0)
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# 4 — Dividir treino e teste
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)

# 5 — Treinar modelo (Random Forest)
modelo = RandomForestClassifier(n_estimators=300, random_state=42)
modelo.fit(X_train, y_train)

# 6 — Avaliar performance
acc = modelo.score(X_test, y_test)
print(f"Acuracia: {acc * 100:.2f}%")

# 7 — Salvar o modelo treinado
with open("modelo_cabeca_baixa.pkl", "wb") as f:
    pickle.dump(modelo, f)

# 8 — Salvar o label encoder (para decodificar 0/1)
with open("label_cabeca_baixa_encoder.pkl", "wb") as f:
    pickle.dump(le, f)

print("Modelo treinado e salvo com sucesso!")
