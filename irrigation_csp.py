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

# Backtracking Algorithm
def backtracking_search(csp):
    return recursive_backtracking({}, csp)

def recursive_backtracking(assignment, csp):
    if is_complete_assignment(assignment, csp):
        return assignment
    
    var = select_unassigned_variable(assignment, csp)
    
    for value in order_domain_values(var, assignment, csp):
        if is_consistent(var, value, assignment, csp):
            assignment[var] = value
            
            inferences = {}
            if csp.get('inference') == 'forward_checking':
                inferences = forward_checking(csp, var, value, assignment)
                if inferences is None:
                    del assignment[var]
                    continue
                assignment.update(inferences)
            
            result = recursive_backtracking(assignment, csp)
            if result is not None:
                return result
            
            del assignment[var]
            if inferences:
                for inf_var in list(inferences.keys()):
                    if inf_var in assignment:
                        del assignment[inf_var]
    
    return None

def is_complete_assignment(assignment, csp):
    return len(assignment) == len(csp['variables'])

def is_consistent(var, value, assignment, csp):
    if check_capacity_constraint(var, value, assignment, csp):
        return False
    if check_priority_constraint(var, value, assignment, csp):
        return False
    if check_additional_constraints(var, value, assignment, csp):
        return False
    return True

def select_unassigned_variable(assignment, csp):
    for var in csp['variables']:
        if var not in assignment:
            return var
    return None

def order_domain_values(var, assignment, csp):
    return list(csp['domain'][var])

def _day_to_index(day_str):
    if isinstance(day_str, (int, np.integer)):
        return int(day_str)
    if isinstance(day_str, str) and day_str.startswith('Hari_'):
        try:
            return int(day_str.split('_')[1])
        except Exception:
            return None
    return None

def check_capacity_constraint(var, value, assignment, csp):
    target_day = value
    total_hours = 0
    for assigned_var, assigned_day in assignment.items():
        if assigned_day == target_day:
            total_hours += csp['kebutuhan'][assigned_var]
    total_hours += csp['kebutuhan'][var]
    return total_hours > csp.get('kapasitas_per_hari', 20)

def check_priority_constraint(var, value, assignment, csp):
    prioritas = csp['prioritas'][var]
    day_idx = _day_to_index(value)
    if prioritas >= 4 and day_idx is not None and day_idx > 3:
        return True
    return False

def check_additional_constraints(var, value, assignment, csp):
    if 'provinsi' in csp:
        provinsi_var = csp['provinsi'][var]
        for assigned_var, assigned_day in assignment.items():
            if assigned_day == value and csp['provinsi'][assigned_var] == provinsi_var:
                return True
    return False

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
