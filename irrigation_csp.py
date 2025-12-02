# irrigation_csp.py
# ================= BAGIAN 1 - ANGGOTA 1 =================
# Data & CSP Structure
import pandas as pd
import numpy as np


# np.random.seed(42)

# # df = pd.DataFrame({
# #     'kabupaten': [f'Kabupaten_{i}' for i in range(1, 51)],
# #     'provinsi': np.random.choice(['Provinsi A', 'Provinsi B', 'Provinsi C'], 50),
# #     'kebutuhan_jam': np.random.randint(5, 20, 50),
# #     'prioritas': np.random.randint(1, 5, 50)
# # })

# df.to_csv('dataset_irigasi_50_petak.csv', index=False)
# print("Dataset telah disimpan ke 'dataset_irigasi_50_petak.csv'")

# csp_data = df[['kabupaten', 'kebutuhan_jam', 'prioritas']]
# csp_data.to_csv('data_csp_irigasi.csv', index=False)
# print("Data CSP telah disimpan ke 'data_csp_irigasi.csv'")


# ==============================
# Fungsi Load Dataset CSP
# ==============================

def load_dataset(path_main, path_csp):
    """
    Membaca dataset irigasi dan menyiapkan struktur awal CSP.
    """

    data_main = pd.read_csv(path_main)
    data_csp = pd.read_csv(path_csp)

    # Variabel CSP: nama kabupaten (petak sawah)
    variables = list(data_csp['kabupaten'])

    # Domain: pilihan hari irigasi (bisa disesuaikan)
    domain = {}
    for v in variables:
        domain[v] = ['Hari_1', 'Hari_2', 'Hari_3', 'Hari_4', 'Hari_5', 'Hari_6', 'Hari_7']

    # Info kebutuhan dan prioritas
    kebutuhan = dict(zip(data_csp['kabupaten'], data_csp['kebutuhan_jam']))
    prioritas = dict(zip(data_csp['kabupaten'], data_csp['prioritas']))

    # Provinsi tiap kabupaten (untuk constraint wilayah)
    provinsi = dict(zip(data_main['kabupaten'], data_main['provinsi']))

    return {
        'variables': variables,
        'domain': domain,
        'kebutuhan': kebutuhan,
        'prioritas': prioritas,
        'provinsi': provinsi
    }


# Fungsi Membuat Model CSP

def create_csp_model(csp):
    """
    Membuat struktur model CSP berisi variabel, domain,
    dan daftar constraint dasar yang diperlukan.
    """

    variables = csp['variables']
    domain = csp['domain']
    provinsi = csp['provinsi']

    constraints = []

    # Constraint: setiap petak hanya boleh mendapat satu jadwal
    def single_assign(var, value):
        return True

    # Constraint: petak pada provinsi yang sama tidak boleh disiram di hari yang sama
    def provinsi_constraint(v1, v2, d1, d2):
        if provinsi[v1] == provinsi[v2]:
            return d1 != d2
        return True

    # Single assignment
    for v in variables:
        constraints.append(('single_assign', v, single_assign))

    # Constraint antar petak (berdasarkan provinsi)
    for i in range(len(variables)):
        for j in range(i + 1, len(variables)):
            v1 = variables[i]
            v2 = variables[j]
            constraints.append(('provinsi_constraint', v1, v2, provinsi_constraint))

    return {
        'variables': variables,
        'domain': domain,
        'constraints': constraints
    }


#  Contoh Penggunaan

# if __name__ == '__main__':
#     dataset = load_dataset(
#         'dataset_irigasi_50_petak.csv',
#         'data_csp_irigasi.csv'
#     )

#     model = create_csp_model(dataset)

#     print("Total variabel:", len(model['variables']))
#     print("Contoh domain:", model['domain'][model['variables'][0]])
#     print("Jumlah constraints:", len(model['constraints']))

# ================= BAGIAN 2 - ANGGOTA 2 =================  
# Backtracking Basic
def backtracking_search():
    """Implementasi backtracking dasar"""
    pass

# ================= BAGIAN 3 - ANGGOTA 3 =================
# Heuristics
def mrv_heuristic():
    """Minimum Remaining Values"""
    pass

def degree_heuristic():
    """Degree Heuristic"""
    pass

# ================= BAGIAN 4 - ANGGOTA 4 =================
# Constraint Propagation  
def forward_checking():
    """Forward Checking"""
    pass

def ac3():
    """AC-3 Algorithm"""
    pass

# ================= BAGIAN 5 - ANGGOTA 5 =================
# Testing & Visualization
def run_experiments():
    """Uji berbagai skenario"""
    pass

def visualize_results():
    """Visualisasi jadwal"""
    pass
