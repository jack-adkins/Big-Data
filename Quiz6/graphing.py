import matplotlib.pyplot as plt

def load_data(file_path):
    elapsed_time = []
    unique_users = []
    with open(file_path, 'r') as file:
        next(file)
        for line in file:
            time, users = line.strip().split(', ')
            elapsed_time.append(int(time))
            unique_users.append(int(users))
    return elapsed_time, unique_users

def plot_unique_users(file_path):
    elapsed_time, unique_users = load_data(file_path)
    
    plt.figure(figsize=(10, 6))
    plt.plot(elapsed_time, unique_users, marker='o', linestyle='-', markersize=5)
    plt.title("Estimated Unique Users Over Time")
    plt.xlabel("Total Elapsed Time (s)")
    plt.ylabel("Estimated Unique Users")
    plt.grid(True)
    plt.show()

plot_unique_users("output_log.txt")
