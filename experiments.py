from linear_map import load_img, linear_map
from error_analysis import get_statistics
import matrix as mtx
import numpy as np
import interp
import cv2
import os
import pandas as pd



def save_results(results, filename):

    dir_name = os.path.splitext(filename)[0]
    output_path = os.path.join("experiments_linear", dir_name)

    os.makedirs(output_path, exist_ok=True)

    for k, methods in results.items():
        for interp_method, img_data in methods.items():
            
            file_name = f"{k}_{interp_method}.png"
            full_file_path = os.path.join(output_path, file_name)
            
            success = cv2.imwrite(full_file_path, img_data)
            
            if success:
                print(f"Salvo: {full_file_path}")
            else:
                print(f"Erro ao salvar: {full_file_path}")


def run_linear_experiment(filename: str, A:np.ndarray, n: int, interp_methods: np.ndarray):

    v = load_img(f'assets/{filename}')
    v_fl = mtx.to_fl_matrix(v)

    results = {
        method: {
            'fl': v_fl.copy(), 
            'no_fl': v.copy()
        } for method in interp_methods
    }
    
    # 7 = # metrics
    stats_serie = {k: np.zeros((n,7)) for k in interp_methods}

    for i in range(n):

        print(f"\nIteration : {i+1}")

        for interp_method, machines in results.items():
            for machine in machines.keys():
                
                print(f"{interp_method} -- {machine}")

                func = getattr(interp, interp_method)
                _, new_img = linear_map(A, results[interp_method][machine], fl=(machine == 'fl'), interpolation=func)

                results[interp_method][machine] = new_img

            stats_serie[interp_method][i] = list(get_statistics(results[interp_method]['fl'], results[interp_method]['no_fl']).values())
    

    return results, stats_serie

# Reflection 
A = np.array([
    [1, 0],
    [0, -1]
])
n = 2 # sequence length

img = "tinycat.jpg"

results, statistics = run_linear_experiment(img, A, n, ["bilerp"])

save_results(results, img)
print(statistics["bilerp"])
# todo > criar um dataframe pra cada método de interpolaçao


