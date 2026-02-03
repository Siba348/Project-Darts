from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)

def fliplr(arr):
    return np.fliplr(arr)

def combvec(*args):
    return np.array(np.meshgrid(*args, indexing='ij')).T.reshape(-1, len(args))

def calculate_output(V):
    selected_rows = np.array([])

    # Erstellung der verschiedenen Kombinationen beim Dart
    # Dafür Erstellung Matritzen welche Kombinationen enthalten, da mit einem Doppel oder 50 das Spiel beendet werden muss stellt die
    # 3te Reihe immer ein Doppel oder Bull dar. Wenn ein Triple und Single benötigt wird zuerst auf das Triple gezieht
    # In gewissen Konstellationen kann der Wurf auf das Bullseye sinnvoll sein da im Falle einer Knappen Verfehlung 25 Punkte immer noch hoeher sind als das höchste Doppel (20)
    #Triple erst ab 21 (Triple 7) da alle Zahlen kleiner als 21 auch über die Single gespielt werden kann
    #Daraus final ergeben sich folgende Kombinationen
    #S1 enhält alle Triple Single Doppel Kombinationen
    #S2 enhält alle Double Double Double Kombinationen
    #S3 enhält alle Double Single Double Kombinationen
    #S4 enhält alle Triple Single Double Kombinationen
    #S5 enhält alle Triple Triple Double Kombinationen
    #S6 enhält alle Bullseye Single Double Kombinationen
    #S7 enhält alle Bullsye Triple Double
    #S8 enhält alle Single Double Kombinationen
    #S9 enhält alle Double Double Kombinationen
    #S10 enhält alle ein Dart Finishes (Double Kombinationen + 50)

    # Schritt 1: Erstellt die Punktzahlen für die möglichen Würfe
    U = np.concatenate((np.arange(1, 21), np.array([25])))  # Mögliche Single-Werte inklusive 25 (SBull)
    D1 = 2 * np.concatenate((np.arange(1, 21), np.array([25])))  # Mögliche Double-Werte
    T = 3 * np.arange(7, 21)  # Mögliche Triple-Werte (erst ab 7 sinnvoll)

    # Schritt 2: Erstellt alle Kombinationen [Double, Single, Triple]
    S = np.fliplr(combvec(D1, U, T))  # Reihenfolge: T, S, D (wegen fliplr)

    # Schritt 3: Berechnet die Summe der drei Würfe und hängt sie als vierte Spalte an
    T = S[:, 1] + S[:, 0] + S[:, 2]  # Summiert die ersten drei Spalten
    S = np.hstack((S, T[:, np.newaxis]))  # Hängt die Summe an

    # Schritt 4: Filtert nur Kombinationen, die exakt V ergeben
    Z = S[:, 3] == V  # Erstellt Maske für gültige Kombinationen
    S = np.hstack((S, Z[:, np.newaxis]))  # Hängt Maske als fünfte Spalte an
    S1 = S[S[:, 4] == 1, :]  # Bezieht nur gültige Kombinationen

    # Schritt 5: Erstellt eine Kopie für die Dart-Schreibweise
    S1_mapped = S1.astype(object)

    # Schritt 6: Wandelt Zahlen in Dart-Notation um
    for i in range(S1.shape[0]):
        for j in range(3):  # Geht jede der drei Spalten durch
            val = int(S1[i, j])  # Holt den numerischen Wert
            if j == 0:  # Erster Wurf gilt als Triple
                S1_mapped[i, j] = f"T{val // 3}"
            elif j == 1:  # Zweiter Wurf gilt als Single oder SBull
                if val == 25:
                    S1_mapped[i, j] = "SBull"
                else:
                    S1_mapped[i, j] = f"S{val}"
            else:  # Dritter Wurf gilt als Double oder Bull
                if val == 50:
                    S1_mapped[i, j] = "Bull"
                else:
                    S1_mapped[i, j] = f"D{val // 2}"

    # Schritt 7: Hängt die Dart-Notation als weitere Spalten rechts an die numerischen Werte an
    S1 = np.hstack((S1, S1_mapped))

    # Erstellt die Werte für die Würfe:
    U = 2 * np.concatenate((np.arange(11, 21), np.array([25])))  # Nur gültige Double-Werte ab 11, inkl. 25
    D1 = 2 * np.concatenate((np.arange(1, 21), np.array([25])))  # Alle möglichen Double-Werte
    T = U  # Für diese Kombination sind alle Würfe Doubles

    # Erstellt alle Kombinationen: [D, D, D]
    S = fliplr(combvec(D1, U, T))
    T = S[:, 1] + S[:, 0] + S[:, 2]  # Berechnet die Summe
    S = np.hstack((S, T[:, np.newaxis]))  # Hängt die Summe als vierte Spalte an
    Z = S[:, 3] == V
    S = np.hstack((S, Z[:, np.newaxis]))  # Hängt die Maske (True/False) an
    S2 = S[S[:, 4] == 1, :]  # Nimmt nur die Kombinationen mit passender Summe

    # Darstellung in Dart-Notation
    U = 2 * np.concatenate((np.arange(11, 21), np.array([25])))
    S2_mapped = S2.astype(object)
    for i in range(S2.shape[0]):
        for j in range(3):
            val = int(S2[i, j])
            if j == 0:  # Double
                S2_mapped[i, j] = "Bull" if val == 50 else f"D{val // 2}"
            elif j == 1:  # Double
                S2_mapped[i, j] = "Bull" if val == 50 else f"D{val // 2}"
            else:  # Double
                S2_mapped[i, j] = "Bull" if val == 50 else f"D{val // 2}"
    S2 = np.hstack((S2, S2_mapped))  # S2 spiegelt alle 2 2 2 Kombinationen wieder

    # S3 (2 1 2)
    T = 2 * np.concatenate((np.arange(11, 21), np.array([25])))
    D1 = 2 * np.concatenate((np.arange(1, 21), np.array([25])))
    U = np.concatenate((np.arange(1, 21), np.array([25])))
    S = fliplr(combvec(D1, U, T))
    T = S[:, 1] + S[:, 0] + S[:, 2]
    S = np.hstack((S, T[:, np.newaxis]))
    Z = S[:, 3] == V
    S = np.hstack((S, Z[:, np.newaxis]))
    S3 = S[S[:, 4] == 1, :]
    S3_mapped = S3.astype(object)
    for i in range(S3.shape[0]):
        for j in range(3):
            val = int(S3[i, j])
            if j == 0:  # Double
                S3_mapped[i, j] = "Bull" if val == 50 else f"D{val // 2}"
            elif j == 1:  # Single
                S3_mapped[i, j] = "SBull" if val == 25 else f"S{val}"
            else:  # Double
                S3_mapped[i, j] = "Bull" if val == 50 else f"D{val // 2}"
    S3 = np.hstack((S3, S3_mapped))

    # S4 (3 3 2)
    U = 3 * np.arange(7, 21)
    D1 = 2 * np.concatenate((np.arange(1, 21), np.array([25])))
    T = 3 * np.arange(7, 21)
    S = fliplr(combvec(D1, U, T))
    T = S[:, 1] + S[:, 0] + S[:, 2]
    S = np.hstack((S, T[:, np.newaxis]))
    Z = S[:, 3] == V
    S = np.hstack((S, Z[:, np.newaxis]))
    S4 = S[S[:, 4] == 1, :]
    S4_mapped = S4.astype(object)
    for i in range(S4.shape[0]):
        for j in range(3):
            val = int(S4[i, j])
            if j == 0:
                S4_mapped[i, j] = f"T{val // 3}"
            elif j == 1:
                S4_mapped[i, j] = f"T{val // 3}"
            else:
                S4_mapped[i, j] = "Bull" if val == 50 else f"D{val // 2}"
    S4 = np.hstack((S4, S4_mapped))

    # S5 (3 2 2)
    U = 2 * np.concatenate((np.arange(11, 21), np.array([25])))
    D1 = 2 * np.concatenate((np.arange(1, 21), np.array([25])))
    T = 3 * np.arange(7, 21)
    S = fliplr(combvec(D1, U, T))
    T = S[:, 1] + S[:, 0] + S[:, 2]
    S = np.hstack((S, T[:, np.newaxis]))
    Z = S[:, 3] == V
    S = np.hstack((S, Z[:, np.newaxis]))
    S5 = S[S[:, 4] == 1, :]
    S5_mapped = S5.astype(object)
    for i in range(S5.shape[0]):
        for j in range(3):
            val = int(S5[i, j])
            if j == 0:
                S5_mapped[i, j] = f"T{val // 3}"
            elif j == 1:
                S5_mapped[i, j] = "Bull" if val == 50 else f"D{val // 2}"
            else:
                S5_mapped[i, j] = "Bull" if val == 50 else f"D{val // 2}"
    S5 = np.hstack((S5, S5_mapped))

    # S6 (Bull 1 2)
    U = np.concatenate((np.arange(1, 21), np.array([25])))
    B = 50. * np.ones(1)
    D1 = 2 * np.concatenate((np.arange(1, 21), np.array([25])))
    S = fliplr(combvec(D1, U, B))
    T = S[:, 1] + S[:, 0] + S[:, 2]
    S = np.hstack((S, T[:, np.newaxis]))
    Z = S[:, 3] == V
    S = np.hstack((S, Z[:, np.newaxis]))
    S6 = S[S[:, 4] == 1, :]
    S6_mapped = S6.astype(object)
    for i in range(S6.shape[0]):
        for j in range(3):
            val = int(S6[i, j])
            if j == 0:
                S6_mapped[i, j] = "Bull"
            elif j == 1:
                S6_mapped[i, j] = "SBull" if val == 25 else f"S{val}"
            else:
                S6_mapped[i, j] = "Bull" if val == 50 else f"D{val // 2}"
    S6 = np.hstack((S6, S6_mapped))

    # S31 (SBull 1 2)
    U = np.arange(1, 21)
    B = 25. * np.ones(1)
    D1 = 2 * np.concatenate((np.arange(1, 21), np.array([25])))
    S = fliplr(combvec(D1, U, B))
    T = S[:, 1] + S[:, 0] + S[:, 2]
    S = np.hstack((S, T[:, np.newaxis]))
    Z = S[:, 3] == V
    S = np.hstack((S, Z[:, np.newaxis]))
    S31 = S[S[:, 4] == 1, :]
    S31_mapped = S31.astype(object)
    for i in range(S31.shape[0]):
        for j in range(3):
            val = int(S31[i, j])
            if j == 0:
                S31_mapped[i, j] = "SBull"
            elif j == 1:
                S31_mapped[i, j] = "SBull" if val == 25 else f"S{val}"
            else:
                S31_mapped[i, j] = "Bull" if val == 50 else f"D{val // 2}"
    S31 = np.hstack((S31, S31_mapped))

    # S7 (Bull 3 2)
    U = 3 * np.arange(7, 21)
    B = 50. * np.ones(1)
    D1 = 2 * np.concatenate((np.arange(1, 21), np.array([25])))
    S = fliplr(combvec(D1, U, B))
    T = S[:, 1] + S[:, 0] + S[:, 2]
    S = np.hstack((S, T[:, np.newaxis]))
    Z = S[:, 3] == V
    S = np.hstack((S, Z[:, np.newaxis]))
    S7 = S[S[:, 4] == 1, :]
    S7_mapped = S7.astype(object)
    for i in range(S7.shape[0]):
        for j in range(3):
            val = int(S7[i, j])
            if j == 0:
                S7_mapped[i, j] = "Bull"
            elif j == 1:
                S7_mapped[i, j] = f"T{val // 3}"
            else:
                S7_mapped[i, j] = "Bull" if val == 50 else f"D{val // 2}"
    S7 = np.hstack((S7, S7_mapped))

    # S8 (NA 3 2) -> Tripple Double Kombinationen
    U = 3 * np.arange(7, 21)
    B = 0. * np.ones(1)
    D1 = 2 * np.concatenate((np.arange(1, 21), np.array([25])))
    S = fliplr(combvec(D1, U, B))
    T = S[:, 1] + S[:, 0] + S[:, 2]
    S = np.hstack((S, T[:, np.newaxis]))
    Z = S[:, 3] == V
    S = np.hstack((S, Z[:, np.newaxis]))
    S8 = S[S[:, 4] == 1, :]
    S8_mapped = S8.astype(object)
    for i in range(S8.shape[0]):
        for j in range(3):
            val = int(S8[i, j])
            if j == 0:
                S8_mapped[i, j] = "NA"
            elif j == 1:
                S8_mapped[i, j] = f"T{val // 3}"
            else:
                S8_mapped[i, j] = "Bull" if val == 50 else f"D{val // 2}"
    S8 = np.hstack((S8, S8_mapped))

    # S9 (NA 2 2)
    U = 2 * np.concatenate((np.arange(11, 21), np.array([25])))
    B = 0. * np.ones(1)
    D1 = 2 * np.concatenate((np.arange(1, 21), np.array([25])))
    S = fliplr(combvec(D1, U, B))
    T = S[:, 1] + S[:, 0] + S[:, 2]
    S = np.hstack((S, T[:, np.newaxis]))
    Z = S[:, 3] == V
    S = np.hstack((S, Z[:, np.newaxis]))
    S9 = S[S[:, 4] == 1, :]
    S9_mapped = S9.astype(object)
    for i in range(S9.shape[0]):
        for j in range(3):
            val = int(S9[i, j])
            if j == 0:
                S9_mapped[i, j] = "NA"
            elif j == 1:
                S9_mapped[i, j] = "Bull" if val == 50 else f"D{val // 2}"
            else:
                S9_mapped[i, j] = "Bull" if val == 50 else f"D{val // 2}"
    S9 = np.hstack((S9, S9_mapped))

    # S10 (NA 1 2)
    U = np.concatenate((np.arange(1, 21), np.array([25])))
    B = 0. * np.ones(1)
    D1 = 2 * np.concatenate((np.arange(1, 21), np.array([25])))
    S = fliplr(combvec(D1, U, B))
    T = S[:, 1] + S[:, 0] + S[:, 2]
    S = np.hstack((S, T[:, np.newaxis]))
    Z = S[:, 3] == V
    S = np.hstack((S, Z[:, np.newaxis]))
    S10 = S[S[:, 4] == 1, :]
    S10_mapped = S10.astype(object)
    for i in range(S10.shape[0]):
        for j in range(3):
            val = int(S10[i, j])
            if j == 0:
                S10_mapped[i, j] = "NA"
            elif j == 1:
                S10_mapped[i, j] = "SBull" if val == 25 else f"S{val}"
            else:
                S10_mapped[i, j] = "Bull" if val == 50 else f"D{val // 2}"
    S10 = np.hstack((S10, S10_mapped))

    # S11 (NA NA 2)
    U = 0. * np.ones(1)
    B = U
    D1 = 2 * np.concatenate((np.arange(1, 21), np.array([25])))
    S = fliplr(combvec(D1, U, B))
    T = S[:, 1] + S[:, 0] + S[:, 2]
    S = np.hstack((S, T[:, np.newaxis]))
    Z = S[:, 3] == V
    S = np.hstack((S, Z[:, np.newaxis]))
    S11 = S[S[:, 4] == 1, :]
    S11_mapped = S11.astype(object)
    for i in range(S11.shape[0]):
        for j in range(3):
            val = int(S11[i, j])
            if j == 0:
                S11_mapped[i, j] = "NA"
            elif j == 1:
                S11_mapped[i, j] = "NA"
            else:
                S11_mapped[i, j] = "Bull" if val == 50 else f"D{val // 2}"
    S11 = np.hstack((S11, S11_mapped))

    # definieren und zuordnen welche finishing wege wo gebraicht werden
    output_value = None
    if V < 41 and V % 2 == 0 and V > 1 :
        output_value = S11
    elif V == 3:
        output_value = S10
        
    elif V < 41 and V % 2 == 1 and V > 1:
        output_value = S10[(S10[:, 2] % 4 == 0) & (S10[:, 1] != 25)]
    
    elif 41 <= V <= 49:
        output_value = S10[(S10[:, 1] != 25)]
    elif V == 50:
        output_value = np.vstack((S11, S10))
    elif 51 <= V <= 60:
        output_value = S10
    elif 61 <= V <= 80 and V % 2 == 0:
        output_value = np.vstack((S10, S9, S8, S6))
    elif 81 <= V < 86 and V % 2 == 0:
        output_value = np.vstack((S10, S9, S8))
    elif 61 <= V < 80 and V % 2 == 1:
        output_value = np.vstack((S10, S9, S8, S6))
    elif 81 <= V < 86 and V % 2 == 1:
        output_value = np.vstack((S10, S9, S8, S6))
    elif 86 <= V < 90 and V % 2 == 0:
        output_value = np.vstack((S8))
    elif 86 <= V <= 90 and V % 2 == 1:
        output_value = np.vstack((S10, S9, S8, S6))
    elif 90 <= V <= 97 and V % 2 == 1:
        output_value = np.vstack((S10, S9, S8, S6))
    elif 90 <= V <= 97 and V % 2 == 0:
        output_value = np.vstack((S10, S9, S8, S6))
    elif V == 98 or V == 100:
        output_value = np.vstack((S8))
    elif V == 99:
        output_value = np.vstack((S1))
    elif V == 101:
        output_value = np.vstack((S8, S1, S6))
    elif 100 < V < 105 or V == 120:
        output_value = np.vstack((S10, S9, S8, S1))
    elif 104 < V < 120 and V != 119:
        output_value = np.vstack((S10, S9, S8, S6, S1))
    elif V == 99:
        output_value = np.vstack((S10, S9, S8, S1))
    elif V == 119:
        output_value = np.vstack((S10, S9, S8, S1, S2, S3, S1, S7, S5, S4))
    elif 120 < V <= 4000:
        output_value = np.vstack((S10, S9, S8, S1, S2, S3, S1, S7, S5, S4, S6))

    # wird im 2ten Schritt besser gefiltert
    if output_value is None:
        return np.array([])  # oder gib eine passende Fehlermeldung zurück

    output_value = output_value[:, :10]
    
    V_minus_50_times_3 = (V - 50) * 3
    exclude_50 = (((V - 20) < 101 and (V - 20) != 99) or
                  ((V - 19) < 101 and (V - 19) != 99) or
                  ((V - 18) < 101 and (V - 18) != 99) or
                  ((V - 17) < 101 and (V - 17) != 99))

    if (61 <= V <= 75):
        selected_rows = output_value[
            ((output_value[:, 0] == 0) & (output_value[:, 1] > 48)) |
            ((output_value[:, 0] == 0) & (output_value[:, 1] == V_minus_50_times_3)) |
            ((output_value[:, 0] == 0) & (output_value[:, 2] == 40)) |
            ((output_value[:, 0] == 0) & (output_value[:, 2] == 32)) |
            ((output_value[:, 0] == 0) & (output_value[:, 2] == 16)) |
            ((output_value[:, 0] == 0) & (output_value[:, 1] == 25)) |
            ((output_value[:, 0] == 0) & (output_value[:, 2] == 24)) |
            ((output_value[:, 0] == 0) & (output_value[:, 2] == 36)) |
            ((output_value[:, 0] == 0) & (output_value[:, 2] == 20)) |
            ((output_value[:, 0] == 0) & (output_value[:, 2] == output_value[:, 1]))
        ]
    elif (76 <= V <= 80):
        selected_rows = output_value[
            ((output_value[:, 0] == 0) & (output_value[:, 1] > 48) & (output_value[:, 1] != 50)) |
            ((output_value[:, 0] == 0) & (output_value[:, 1] == V_minus_50_times_3)) |
            ((output_value[:, 0] == 0) & (output_value[:, 2] == 40)) |
            ((output_value[:, 0] == 0) & (output_value[:, 2] == 32)) |
            ((output_value[:, 0] == 0) & (output_value[:, 2] == 16)) |
            ((output_value[:, 0] == 0) & (output_value[:, 1] == 25)) |
            ((output_value[:, 0] == 0) & (output_value[:, 2] == 24)) |
            ((output_value[:, 0] == 0) & (output_value[:, 2] == 36)) |
            ((output_value[:, 0] == 0) & (output_value[:, 2] == 20)) |
            ((output_value[:, 0] == 0) & (output_value[:, 2] == 28)) |
            ((output_value[:, 0] == 0) & (output_value[:, 2] == output_value[:, 1]))
        ]
    elif (90 <= V <= 95):
        selected_rows = output_value[
            (output_value[:, 0] == 0) | (
                (output_value[:, 0] == 50) &
                ((output_value[:, 2] == 40) | (output_value[:, 2] == 32) | (output_value[:, 2] == 16))
            & (output_value[:, 1] != 25) )
        ]
    elif (96 <= V <= 97):
        selected_rows = output_value[(output_value[:, 0] == 0)]
    elif (V == 99):
        selected_rows = output_value[
            (((V - output_value[:, 0] / 3) <= 80) & ((output_value[:, 2] == 32) | (output_value[:, 2] == 40)))
        ]
    elif (V == 98 or V == 100):
        selected_rows = output_value[(output_value[:, 0] == 0)]
    elif (81 <= V <= 85):
        selected_rows = output_value[
            ((output_value[:, 0] == 0) & (output_value[:, 1] > 48) & (output_value[:, 1] != 50)) |
            ((output_value[:, 0] == 0) & (output_value[:, 1] == V_minus_50_times_3)) |
            ((output_value[:, 0] == 0) & (output_value[:, 2] == 40)) |
            ((output_value[:, 0] == 0) & (output_value[:, 2] == 32)) |
            ((output_value[:, 0] == 0) & (output_value[:, 2] == 16)) |
            ((output_value[:, 0] == 0) & (output_value[:, 1] == 25)) |
            ((output_value[:, 0] == 0) & (output_value[:, 2] == 24)) |
            ((output_value[:, 0] == 0) & (output_value[:, 2] == 36)) |
            (output_value[:, 1] == 50) |
            ((output_value[:, 0] == 25) & ((output_value[:, 2] == 40) | (output_value[:, 2] == 24))) |
            ((output_value[:, 0] == 50) & ((output_value[:, 2] == 24) | (output_value[:, 2] == 16) | (output_value[:, 2] == 32)))
        ]
    elif (1 <= V <= 40):
        selected_rows = output_value
    elif (41 <= V <= 60):
        selected_rows = output_value[
            ((output_value[:, 1] != 25) & (output_value[:, 2] == 40)) |
            ((output_value[:, 1] != 25) & (output_value[:, 2] == 32)) |
            ((output_value[:, 1] != 25) & (output_value[:, 2] == 24)) |
            (output_value[:, 1] == 0) |
            ((output_value[:, 2] / 2) == (output_value[:, 1]))
        ]
    elif ((86 <= V <= 90) and V % 2 == 0) or (V == 100):
        selected_rows = output_value[
            ((output_value[:, 0] == 0) & (output_value[:, 1] >= 48) & (output_value[:, 1] != 50)) |
            ((output_value[:, 0] == 0) & (output_value[:, 1] == V_minus_50_times_3)) |
            ((output_value[:, 0] == 0) & (output_value[:, 2] == 40)) |
            ((output_value[:, 0] == 0) & (output_value[:, 2] == 32)) |
            ((output_value[:, 0] == 0) & (output_value[:, 2] == 16)) |
            ((output_value[:, 0] == 0) & (output_value[:, 1] == 25)) |
            ((output_value[:, 0] == 0) & (output_value[:, 2] == 24)) |
            ((output_value[:, 0] == 0) & (output_value[:, 2] == 36)) |
            (output_value[:, 1] == 50) |
            ((output_value[:, 0] == output_value[:, 2]) & (output_value[:, 2] % 4 == 0)) |
            ((output_value[:, 0] == 32) & (output_value[:, 2] == 40)) |
            ((output_value[:, 0] == 36) & (output_value[:, 2] == 40)) |
            ((output_value[:, 0] == 32) & (output_value[:, 2] == 40)) |
            ((output_value[:, 1] == (output_value[:, 2] / 2)) & (output_value[:, 0] % 4 == 0))
        ]
    elif ((86 <= V <= 90) and V % 2 == 1):
        selected_rows = output_value[
            ((output_value[:, 0] == 0) & (output_value[:, 1] >= 48) & (output_value[:, 1] != 50)) |
            ((output_value[:, 0] == 0) & (output_value[:, 1] == V_minus_50_times_3)) |
            ((output_value[:, 0] == 0) & (output_value[:, 2] == 40)) |
            ((output_value[:, 0] == 0) & (output_value[:, 2] == 32)) |
            ((output_value[:, 0] == 0) & (output_value[:, 2] == 16)) |
            ((output_value[:, 0] == 0) & (output_value[:, 1] == 25)) |
            ((output_value[:, 0] == 0) & (output_value[:, 2] == 24)) |
            ((output_value[:, 0] == 0) & (output_value[:, 2] == 36)) |
            ((output_value[:, 0] == output_value[:, 2]) & (output_value[:, 2] % 4 == 0) & (output_value[:, 1] != 25)) |
            ((output_value[:, 0] == 32) & (output_value[:, 2] == 40) & (output_value[:, 1] != 25)) |
            ((output_value[:, 0] == 36) & (output_value[:, 2] == 40) & (output_value[:, 1] != 25)) |
            ((output_value[:, 0] == 32) & (output_value[:, 2] == 40) & (output_value[:, 1] != 25)) |
            ((output_value[:, 1] == (output_value[:, 2] / 2)) & (output_value[:, 0] % 4 == 0) & (output_value[:, 1] != 25))
        ]
    elif V in [101, 102, 103, 104]:
        selected_rows = output_value[
            (
                (output_value[:, 0] == 0) |
                ((output_value[:, 0] == 50) & ((output_value[:, 2] == 32) | (output_value[:, 2] == 40))) |
                (((output_value[:, 0] != 50) & (output_value[:, 2] == 32)) | ((output_value[:, 0] != 50) & (output_value[:, 2] == 40))) |
                ((output_value[:, 2] == output_value[:, 0]) & (output_value[:, 2] != 50))
            ) & (output_value[:, 1] != 25)
        ]
    elif (105 <= V <= 118) or V == 120:
        selected_rows = output_value[
            (output_value[:, 0] != 50) &
            (~np.isin(V - (output_value[:, 0] / 3), [109, 108, 106, 103, 102, 99])) &
            (output_value[:, 1] != 25) &
            ((output_value[:, 2] == 32) | (output_value[:, 2] == 40) | (output_value[:, 2] == 36)  | (output_value[:, 2] / 2 == output_value[:, 1]) | (output_value[:, 2] / 2 == output_value[:, 1])) |
            (((output_value[:, 0] == 50) & np.isin(V - 25, [80])) & ((output_value[:, 2] == 32) | (output_value[:, 2] == 40) | (output_value[:, 2] / 2 == output_value[:, 1]))) |
            (output_value[:, 0] == 0)
        ]
    elif 119 <= V <= 123:
        selected_rows = output_value[
            ((output_value[:, 0] != 50) & (output_value[:, 2] != 50) & (output_value[:, 1] != 25) &
             (~np.isin(V - (output_value[:, 0] / 3), [109, 108, 106, 103, 102, 99])) &
             ((V - output_value[:, 0] - (output_value[:, 1] / 3) == 50))) |
            ((output_value[:, 0] == 50) & ((V - 25 < 99) | (V - 25 == 100)) &
             (V - output_value[:, 0] - (output_value[:, 1] / 3) <= 60))|(V - output_value[:, 0] - (output_value[:, 1] / 2) <= 60) & np.isin(output_value[:, 1], [40, 32, 24, 36])]
    elif V == 124:
        selected_rows = output_value[
            ((output_value[:, 0] != 50) & (output_value[:, 2] != 50) &
             np.isin(V - (output_value[:, 0] / 3), [110, 107, 104, 101, 100, 98]) &
             (output_value[:, 1] != 50) & (V - output_value[:, 0] - (output_value[:, 1] / 3) <= 60)) |
            ((output_value[:, 0] == 50) & (((V - 25) < 99) | (V - 25 == 100)) &
             (V - output_value[:, 0] - (output_value[:, 1] / 3) <= 60))|(V - output_value[:, 0] - (output_value[:, 1] / 2) <= 60) & np.isin(output_value[:, 1], [40, 32, 24, 36])
        ]
    elif V == 125:
        selected_rows = output_value[
        (
            # Case 1: no Bull in any dart, and remaining value matches given list
            ((output_value[:, 0] != 50) & (output_value[:, 1] != 50) & (output_value[:, 2] != 50) &
             np.isin(V - (output_value[:, 0] / 3), [110, 107, 104, 101, 100, 98]) &
             (V - output_value[:, 0] - (output_value[:, 1] / 3) <= 60))
            |
            # Case 2: first dart is Bull, and remaining total is valid
            ((output_value[:, 0] == 50) &
             (((V - 25) < 99) | (V - 25 == 100)) &
             (V - output_value[:, 0] - (output_value[:, 1] / 3) <= 60))
            |
            # Case 3: second dart is a double (finishing condition)
            ((V - output_value[:, 0] - (output_value[:, 1] / 2) <= 60) &
             np.isin(output_value[:, 1], [40, 32, 24, 36]))
            |
            # Case 4: first dart is Bull (50) and second dart is 25 (outer bull)
            ((output_value[:, 0] == 50) & (output_value[:, 1] == 25))
        )
    ]


    elif 126 <= V <= 130:
        selected_rows = output_value[
        (
            # ---- First part: no bullseyes ----
            (output_value[:, 0] != 50)
            & (output_value[:, 2] != 50)
            & (
                np.isin(V - (output_value[:, 0] / 3), [110, 107, 104, 101, 100, 98])
                | (
                    np.isin(V - (output_value[:, 0] / 2), [110, 107, 104, 101, 100, 98])
                    & np.isin(output_value[:, 0], [40, 32, 24, 36])
                )
                | (
                    np.isin(V - (output_value[:, 0] / 1), [110, 107, 104, 101, 100, 98])
                    & np.isin(output_value[:, 0], [25])
                )
            )
        )
        |
        (
             (output_value[:, 0] == 50)
            & np.isin(V - 25, [110, 107, 104, 101, 100])   # <--- dein gewünschter Zusatz
            & (
                (
                    (V - (output_value[:, 1] / 3) <= 110)
                    & np.isin(output_value[:, 1], [60, 57, 54, 51, 48, 45, 42])
                )
                | (
                    (V - (output_value[:, 1] / 1) <= 110)
                    & (output_value[:, 1] == 25)
                )
                | (
                    (V - (output_value[:, 1] / 2) <= 110)
                    & np.isin(output_value[:, 1], [50, 40, 38, 36, 32, 28])
                )
            )
        )
    ]


    elif V in [131, 132, 133]:
        selected_rows = output_value[
            (output_value[:, 0] != 50) & (output_value[:, 1] != 50) & (
                (
                    (V -output_value[:, 0]- (output_value[:, 1] / 3) <= 60)
                    & np.isin(output_value[:, 1], [60, 57, 54, 51, 48, 45, 42])
                )
                | (
                    (V -output_value[:, 0] -(output_value[:, 1] / 1) <= 60)
                    & (output_value[:, 1] == 25)
                )
                | (
                    (V -output_value[:, 0] -(output_value[:, 1] / 2) <= 60)
                    & np.isin(output_value[:, 1], [50, 40, 38, 36, 32, 28])
                )
            ) |
            (((output_value[:, 0] == 50) & (output_value[:, 1] == 50))) |
            ((output_value[:, 2] == output_value[:, 1]) & (output_value[:, 2] != 50) & (output_value[:, 1] != 50))
        ]
    elif V in [134, 135]:
        selected_rows = output_value[
            (output_value[:, 0] != 50) & (output_value[:, 1] != 50) & (
                (
                    (V -output_value[:, 0]- (output_value[:, 1] / 3) <= 60)
                    & np.isin(output_value[:, 1], [60, 57, 54, 51, 48, 45, 42])
                )
                | (
                    (V -output_value[:, 0] -(output_value[:, 1] / 1) <= 60)
                    & (output_value[:, 1] == 25)
                )
                | (
                    (V -output_value[:, 0] -(output_value[:, 1] / 2) <= 60)
                    & np.isin(output_value[:, 1], [50, 40, 38, 36, 32, 28])
                )
            )|(output_value[:, 0] == 50) &  np.isin(V - 25, [110, 107, 104, 101, 100])
        ]
    elif V in [136, 137, 138]:
        selected_rows = output_value[
            (output_value[:, 0] != 50) & (output_value[:, 1] != 50) & (
                (
                    (V -output_value[:, 0]- (output_value[:, 1] / 3) <= 60)
                    & np.isin(output_value[:, 1], [60, 57, 54, 51, 48, 45, 42])
                )
                | (
                    (V -output_value[:, 0] -(output_value[:, 1] / 1) <= 60)
                    & (output_value[:, 1] == 25)
                )
                | (
                    (V -output_value[:, 0] -(output_value[:, 1] / 2) <= 60)
                    & np.isin(output_value[:, 1], [50, 40, 38, 36, 32, 28])
                )
            )
        ]
    elif V ==139:
        selected_rows = output_value[
            (output_value[:, 0] != 50)  & (
                (
                    (V -output_value[:, 0]- (output_value[:, 1] / 3) <= 70)
                    & np.isin(output_value[:, 1], [60, 57, 54, 51, 48, 45, 42])
                )
                | (
                    (V -output_value[:, 0] -(output_value[:, 1] / 1) <= 70)
                    & (output_value[:, 1] == 25)
                )
                | (
                    (V -output_value[:, 0] -(output_value[:, 1] / 2) <= 70)
                    & np.isin(output_value[:, 1], [50, 40, 38, 36, 32, 28])
                )
            )
        ] 
    elif V==140:
        selected_rows = output_value[
            (output_value[:, 0] != 50)  & (
                (
                    (V -output_value[:, 0]- (output_value[:, 1] / 3) <= 70)
                    & np.isin(output_value[:, 1], [60, 57, 54, 51, 48, 45, 42])
                )
                | (
                    (V -output_value[:, 0] -(output_value[:, 1] / 1) <= 70)
                    & (output_value[:, 1] == 25)
                )
                | (
                    (V -output_value[:, 0] -(output_value[:, 1] / 2) <= 70)
                    & np.isin(output_value[:, 1], [50, 40, 38, 36, 32, 28])
                )
            )
        ] 
    elif V==141:
        selected_rows = output_value
    elif V in [141, 142, 143, 144, 145, 146]:
        selected_rows = output_value[
            (((output_value[:, 1] == 50) & (((V - output_value[:, 0] - 25) <= 60) | ((V - output_value[:, 0] - 25) == 65))) |
             ((output_value[:, 0] != 50) & (output_value[:, 1] != 50) & ((V - output_value[:, 0] - (output_value[:, 1] / 3)) <= 70)))
        ]
    
    elif 153 <= V <= 170:
        selected_rows = output_value
    elif V==147:
        selected_rows=output_value
    elif V==148:
        selected_rows=output_value
    elif V==149:
        selected_rows=output_value
    elif V==150:
        selected_rows=output_value
    elif V==151:
        selected_rows=output_value
    elif V==152:
        selected_rows=output_value
    elif V==153:
        selected_rows=output_value
    elif V==154:
        selected_rows=output_value

    if selected_rows is not None and selected_rows.ndim == 2 and selected_rows.shape[1] >= 8:
        return selected_rows[:, 5:8]
    else:
        return np.array([])
    if output_value is None:
        return np.array([])
    
def suggested_ways(V):
    all_ways = calculate_output(V)
    
    # Falls es kein Ergebnis gibt oder zu wenige Zeilen existieren
    

    # Für V = 51: Nimm die zweite Zeile und nur die Spalten mit der Dart-Notation (5 bis 7)
    if (
    V <= 60
    or V in [67, 71, 73, 79, 86, 87, 88, 89, 93, 96, 115, 116, 117, 118, 119, 120, 142, 153, 156, 160]
    or V in range(97, 100)
    or (V in range(160, 170) and V != 161)
):
        return all_ways
    
    elif V  == 61:
        return np.vstack((all_ways[0, :], all_ways[2, :], all_ways[3, :]))
    # Für alle anderen Werte leer
    elif V  == 62:
        return np.vstack((all_ways[6, :], all_ways[8, :], all_ways[9, :]))
    elif V  == 63:
        return np.vstack((all_ways[2, :], all_ways[3, :], all_ways[0, :]))
    elif V  == 64:
        return np.vstack((all_ways[5, :], all_ways[6, :], all_ways[7, :]))
    elif V  == 65:
        return np.vstack((all_ways[0, :], all_ways[4, :], all_ways[2, :]))
    elif V  == 66:
        return np.vstack((all_ways[4, :], all_ways[5, :], all_ways[7, :]))
    elif V  == 68:
        return np.vstack((all_ways[5, :], all_ways[6, :], all_ways[8, :]))
    elif V  == 69:
        return np.vstack((all_ways[3, :], all_ways[1, :], all_ways[0, :]))
    elif V  == 70:
        return np.vstack((all_ways[4, :], all_ways[5, :], all_ways[6, :]))
    elif V  == 72:
        return np.vstack((all_ways[5, :], all_ways[7, :], all_ways[1, :]))
    elif V  == 74:
        return np.vstack((all_ways[3, :], all_ways[4, :], all_ways[5, :]))
    elif V  == 75:
        return np.vstack((all_ways[0, :], all_ways[1, :], all_ways[2, :]))
    elif V  == 76:
        return np.vstack((all_ways[6, :], all_ways[4, :], all_ways[0, :]))
    elif V  == 77:
        return np.vstack((all_ways[1, :], all_ways[2, :], all_ways[0, :]))
    elif V  == 78:
        return np.vstack((all_ways[3, :], all_ways[4, :], all_ways[0, :]))
    elif V  == 80:
        return np.vstack((all_ways[3, :], all_ways[1, :], all_ways[0, :]))
    elif V  == 81:
        return np.vstack((all_ways[2, :], all_ways[1, :], all_ways[4, :]))
    elif V  == 82:
        return np.vstack((all_ways[0, :], all_ways[1, :], all_ways[2, :]))
    elif V  == 83:
        return np.vstack((all_ways[0, :], all_ways[1, :], all_ways[4, :]))
    elif V  == 84:
        return np.vstack((all_ways[3, :], all_ways[1, :], all_ways[0, :]))
    elif V  == 85:
        return np.vstack((all_ways[2, :], all_ways[5, :], all_ways[0, :]))
    elif V  == 90:
        return np.vstack((all_ways[2, :], all_ways[3, :], all_ways[1, :]))
    elif V  == 91:
        return np.vstack((all_ways[0, :], all_ways[1, :], all_ways[3, :]))
    elif V  == 92:
        return np.vstack((all_ways[1, :], all_ways[2, :], all_ways[4, :]))
    elif V  == 94:
        return np.vstack((all_ways[1, :], all_ways[3, :], all_ways[2, :]))
    elif V  == 95:
        return np.vstack((all_ways[1, :], all_ways[2, :], all_ways[0, :]))
    elif V  == 101:
        return np.vstack((all_ways[13, :], all_ways[0, :], all_ways[10, :]))
    elif V  == 102:
        return np.vstack((all_ways[5, :], all_ways[10, :], all_ways[8, :]))
    elif V  == 103:
        return np.vstack((all_ways[6, :], all_ways[8, :], all_ways[9, :]))
    elif V  == 104:
        return np.vstack((all_ways[2, :], all_ways[5, :], all_ways[8, :]))
    elif V  == 105:
        return np.vstack((all_ways[0, :], all_ways[12, :], all_ways[15, :]))
    elif V  == 106:
        return np.vstack((all_ways[11, :], all_ways[9, :], all_ways[8, :]))
    elif V  == 107:
        return np.vstack((all_ways[0, :], all_ways[9, :], all_ways[6, :]))
    elif V  == 108:
        return np.vstack((all_ways[4, :], all_ways[8, :], all_ways[11, :]))
    elif V  == 109:
        return np.vstack((all_ways[5, :], all_ways[6, :], all_ways[8, :]))
    elif V  == 110:
        return np.vstack((all_ways[0, :], all_ways[4, :], all_ways[1, :]))
    elif V  == 111:
        return np.vstack((all_ways[1, :], all_ways[4, :], all_ways[5, :]))
    elif V  == 112:
        return np.vstack((all_ways[0, :], all_ways[1, :], all_ways[5, :]))
    elif V  == 113:
        return np.vstack((all_ways[3, :], all_ways[1, :], all_ways[0, :]))
    elif V  == 114:
        return np.vstack((all_ways[1, :], all_ways[3, :], all_ways[4, :]))
    elif V ==121:
        return np.vstack((all_ways[5, :], all_ways[4, :], all_ways[0,:]))
    elif V ==122:
        return np.vstack((all_ways[5, :], all_ways[2, :], all_ways[0, :]))
    elif V ==123:
        return np.vstack((all_ways[4, :], all_ways[3, :], all_ways[2, :]))
    elif V ==124:
        return np.vstack((all_ways[16, :], all_ways[18, :], all_ways[2, :]))
    elif V ==125:
        return np.vstack((all_ways[0, :], all_ways[4, :], all_ways[14, :]))
    elif V ==126:
        return np.vstack((all_ways[19, :], all_ways[1, :], all_ways[12, :]))
    elif V ==127:
        return np.vstack((all_ways[13, :], all_ways[1, :], all_ways[9, :]))
    elif   V ==128:
        return np.vstack((all_ways[10, :], all_ways[11, :], all_ways[4, :]))
    elif   V ==129:
        return np.vstack((all_ways[9, :], all_ways[11, :], all_ways[0, :]))
    elif   V ==130:
        return np.vstack((all_ways[6, :], all_ways[8, :], all_ways[13, :]))
    elif   V ==131:
        return np.vstack((all_ways[0, :], all_ways[13, :], all_ways[14, :]))
    elif   V ==132:
        return np.vstack((all_ways[0, :], all_ways[6, :], all_ways[18, :]))
    elif   V ==133:
        return np.vstack((all_ways[10, :], all_ways[1, :], all_ways[2, :]))
    elif   V ==134:
        return np.vstack((all_ways[11, :], all_ways[0, :], all_ways[8, :]))
    elif   V ==135:
        return np.vstack((all_ways[2, :], all_ways[7, :], all_ways[11, :]))
    elif   V ==136:
        return np.vstack((all_ways[0, :], all_ways[7, :], all_ways[5, :]))
    elif   V ==137:
        return np.vstack((all_ways[0, :], all_ways[1, :], all_ways[3, :]))
    elif   V ==138:
        return np.vstack((all_ways[0, :], all_ways[1, :], all_ways[3, :]))
    elif   V ==139:
        return np.vstack((all_ways[15, :], all_ways[3, :], all_ways[9, :]))
    elif   V ==140:
        return np.vstack((all_ways[15, :], all_ways[7, :], all_ways[2, :]))
    elif   V ==141:
        return np.vstack((all_ways[8, :], all_ways[17, :], all_ways[5, :]))
    elif   V ==142:
        return np.vstack((all_ways[9, :], all_ways[5, :], all_ways[0, :]))
    elif   V ==143:
        return np.vstack((all_ways[0, :], all_ways[5, :], all_ways[3, :]))
    elif   V ==144:
        return np.vstack((all_ways[0, :], all_ways[7, :], all_ways[4, :]))
    elif V==145:
        return np.vstack((all_ways[1, :], all_ways[2, :], all_ways[3, :]))
    elif V==146:
        return np.vstack((all_ways[0, :], all_ways[2, :], all_ways[3, :]))
    elif V==147:
        return np.vstack((all_ways[5, :], all_ways[8, :], all_ways[7, :]))
    elif V==148:
        return np.vstack((all_ways[7, :], all_ways[13, :], all_ways[9, :]))
    elif V==150:
        return np.vstack((all_ways[5, :], all_ways[6, :], all_ways[7, :]))   
    elif V==151:
        return np.vstack((all_ways[6, :], all_ways[4, :], all_ways[1, :]))
    elif V==152:
        return np.vstack((all_ways[10, :], all_ways[7, :], all_ways[3, :]))   
    elif V==154:
        return np.vstack((all_ways[2, :], all_ways[3, :], all_ways[5, :]))   
    elif V==155:
        return np.vstack((all_ways[7, :], all_ways[4, :], all_ways[3, :]))   
    elif V==157:
        return np.vstack((all_ways[0, :], all_ways[2, :]))   
    elif V==158:
        return np.vstack((all_ways[2, :], all_ways[5, :]))   
    elif V==161:
        return np.vstack((all_ways[2, :], all_ways[3, :]))   

        
        
    
    
    
    
    # Für alle anderen Werte leer
    # Für alle anderen Werte leer
    # Für alle anderen Werte leer
    return np.array([])


def na_double_double_finishes(V):
    """Return NA-double-double finishes for scores 62–80."""
    if V < 62 or V > 80:
        return np.array([])

    all_ways = calculate_output(V)
    if not isinstance(all_ways, np.ndarray) or all_ways.ndim != 2 or all_ways.shape[1] < 3:
        return np.array([])

    mask = []
    for row in all_ways:
        try:
            first, second, third = row[:3]
        except Exception:
            mask.append(False)
            continue

        mask.append(str(first) == "NA" and str(second).startswith("D") and str(third).startswith("D"))

    mask = np.array(mask, dtype=bool)
    return all_ways[mask] if mask.any() else np.array([])


def print_solution(V):
    if V in [159, 162, 163, 165, 166, 168, 169] or V > 170 or V == 1:
        return "No possible outshot"
    else:
        return "Good Luck"
@app.route('/', methods=['GET', 'POST'])
def index():
    output_value = None
    print_solution_message = None

    if request.method == 'POST':
        V = float(request.form['input_value'])
        output_value = calculate_output(V)
        print_solution_message = print_solution(V)
        
        


    return render_template('index.html', output_value=output_value, print_solution_message=print_solution_message)

if __name__ == '__main__':
    app.run(debug=True)












